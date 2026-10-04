#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝 PC 商品详情采集器（纯协议版，无任何浏览器自动化）
======================================================
数据来源：
  1) 主体数据：item.taobao.com/item.htm 的 SSR HTML 内嵌 JSON
     （window.__ICE_APP_CONTEXT__ 脚本里的 var b = {...}）
  2) 详情图文：mtop.taobao.detail.getdesc v7.0（--desc 时开启，需 md5 sign + 令牌预热）

用法示例：
  python taobao_item_detail.py "https://item.taobao.com/item.htm?id=1056191431122&skuId=6100482645581"
  python taobao_item_detail.py --id 1056191431122 --sku 6100482645581 --desc -o detail.json

说明：
  - cookie 默认读 /home/kongchenshuo/下载/taobao_search/cookie.txt（登录后的 cookie 串）
  - 不需要 bx-ua/bx-umidtoken/bx_et，主体数据走服务端渲染，desc 接口也不校验 bx
  - _m_h5_tk 令牌过期会先失败一次并下发新令牌，自动预热重试
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import requests

APP_KEY = "12574478"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36")
DEFAULT_COOKIE_FILE = "cookie.txt"
ITEM_HOST = "item.taobao.com"
DESC_URL = "https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdesc/7.0/"

MISSING_COOKIE_HINT = (
    "缺少登录 cookie。请先登录淘宝，然后把 Cookie 串写到 %s\n"
    "（可用浏览器登录后复制，或用原仓库 DrissionPage 流程刷新）。"
)


def load_cookie(cookie_file: str | None = None, cookie_str: str | None = None) -> str:
    if cookie_str:
        return cookie_str.strip()
    path = cookie_file or DEFAULT_COOKIE_FILE
    if not Path(path).exists():
        raise SystemExit(MISSING_COOKIE_HINT % path)
    return Path(path).read_text(encoding="utf-8").strip()


def build_session(cookie: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "user-agent": UA,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "zh-CN,zh;q=0.9",
    })
    for kv in cookie.split(";"):
        kv = kv.strip()
        if not kv:
            continue
        k, _, v = kv.partition("=")
        s.cookies.set(k, v, domain=".taobao.com")
    return s


def parse_url(url: str) -> tuple[str, str]:
    """从商品链接解析 (item_id, sku_id)，支持 item.taobao.com/item.htm"""
    if "item.htm" not in url:
        raise ValueError(f"不是 item.htm 链接: {url[:80]}")
    q = {}
    if "?" in url:
        for kv in url.split("?", 1)[1].split("&"):
            k, _, v = kv.partition("=")
            q[k] = v
    item_id = q.get("id", "")
    if not item_id or not item_id.isdigit():
        raise ValueError(f"链接缺少有效 id 参数: {url[:80]}")
    return item_id, q.get("skuId", "")


def extract_ice_context(html: str) -> dict:
    """在 SSR HTML 里定位 __ICE_APP_CONTEXT__ 脚本，用括号配对精确取出 var b = {...}"""
    for tag in re.findall(r"<script[^>]*>([\s\S]*?)</script>", html):
        if "__ICE_APP_CONTEXT__" not in tag:
            continue
        idx = tag.find("var b =")
        if idx < 0:
            continue
        start = tag.find("{", idx)
        if start < 0:
            continue
        depth = 0
        in_str = False
        esc = False
        end = -1
        for i in range(start, len(tag)):
            c = tag[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            continue
        try:
            return json.loads(tag[start:end + 1])
        except json.JSONDecodeError:
            continue
    raise RuntimeError("HTML 中未找到 __ICE_APP_CONTEXT__ 数据，页面可能被风控/登录拦截")


def build_vid_name_map(props: list) -> dict:
    """pid:vid -> 属性值名称"""
    m = {}
    for p in props or []:
        pid = str(p.get("pid", ""))
        for v in p.get("values", []) or []:
            m[f"{pid}:{v.get('vid')}"] = v.get("name", "")
    return m


def name_skus(skus: list, vid_map: dict, props: list) -> list:
    """把 sku 的 propPath 转成可读的属性字典"""
    prop_names = {str(p.get("pid")): p.get("name", str(p.get("pid"))) for p in props or []}
    out = []
    for sk in skus or []:
        props_dict = {}
        for seg in (sk.get("propPath") or "").split(";"):
            if ":" not in seg:
                continue
            pid, _, vid = seg.partition(":")
            props_dict[prop_names.get(pid, pid)] = vid_map.get(f"{pid}:{vid}", vid)
        out.append({"sku_id": str(sk.get("skuId")), "props": props_dict})
    return out


def sku_stock_map(sku2info: dict) -> dict:
    return {
        str(sid): {
            "price": (i.get("price") or {}).get("priceText", ""),
            "price_money": (i.get("price") or {}).get("priceMoney", ""),
            "quantity": i.get("quantity"),
            "quantity_text": i.get("quantityText", ""),
            "logistics_time": i.get("logisticsTime", ""),
        }
        for sid, i in (sku2info or {}).items()
    }


def industry_params(industry_param_vo: dict) -> dict:
    out = {}
    for lst, key in ((industry_param_vo.get("basicParamList"), "basic"),
                     (industry_param_vo.get("enhanceParamList"), "enhance")):
        if not lst:
            continue
        items = {}
        for it in lst:
            items[it.get("propertyName")] = it.get("valueName")
        out[key] = items
    return out


def fetch_item(session: requests.Session, item_id: str, sku_id: str = "") -> dict:
    url = f"https://{ITEM_HOST}/item.htm?id={item_id}"
    if sku_id:
        url += f"&skuId={sku_id}"
    resp = session.get(url, timeout=20)

    if resp.headers.get("x-sec-reason") or resp.headers.get("bxpunish"):
        raise RuntimeError(f"触发风控 x-sec-reason={resp.headers.get('x-sec-reason')}，"
                           f"cookie 可能失效或需要刷新")
    if "login.taobao.com" in resp.url:
        raise RuntimeError("被重定向到登录页，cookie 会话已失效，请刷新 cookie")
    if "__ICE_APP_CONTEXT__" not in resp.text:
        raise RuntimeError("响应中无 SSR 数据，可能被反爬拦截")

    ctx = extract_ice_context(resp.text)
    res = ctx["loaderData"]["home"]["data"]["res"]

    item = res.get("item") or {}
    seller = res.get("seller") or {}
    sku_base = res.get("skuBase") or {}
    sku_core = res.get("skuCore") or {}
    pc_trade = res.get("pcTrade") or {}
    industry = (res.get("plusViewVO") or {}).get("industryParamVO") or {}
    title_vo = (res.get("componentsVO") or {}).get("titleVO") or {}

    props = sku_base.get("props") or []
    skus = name_skus(sku_base.get("skus") or [], build_vid_name_map(props), props)
    stock = sku_stock_map(sku_core.get("sku2info") or {})

    for sk in skus:
        sk.update(stock.get(sk["sku_id"], {}))

    evaluates = {e.get("title"): e.get("score", "").strip()
                 for e in (seller.get("evaluates") or [])}

    current_price = ""
    if sku_id:
        current_price = stock.get(sku_id, {}).get("price", "")
    if not current_price:
        current_price = (pc_trade.get("pcBuyParams") or {}).get("buy_now", "")

    shop_url = seller.get("pcShopUrl", "")
    if shop_url.startswith("//"):
        shop_url = "https:" + shop_url

    return {
        "item_id": str(item.get("itemId", item_id)),
        "sku_id": sku_id,
        "title": item.get("title", ""),
        "price": current_price,
        "sold_count": item.get("vagueSellCount", ""),
        "sold_desc": title_vo.get("salesDesc", ""),
        "images": item.get("images") or [],
        "desc_url": item.get("pcADescUrl", ""),
        "seller": {
            "nick": seller.get("sellerNick", ""),
            "shop_name": seller.get("shopName", ""),
            "shop_url": shop_url,
            "shop_id": seller.get("shopId", ""),
            "seller_id": seller.get("sellerId", ""),
            "seller_type": seller.get("sellerType", ""),
            "credit_level": seller.get("creditLevel", ""),
            "evaluates": evaluates,
        },
        "params": {p.get("name"): [v.get("name") for v in p.get("values") or []]
                   for p in props},
        "params_attrs": industry_params(industry),
        "skus": skus,
        "sku_count": len(skus),
    }


def fetch_desc(session: requests.Session, item_id: str, sku_id: str = "") -> list[str]:
    """拉取详情图文（getdesc v7.0），返回图片 URL 列表。含 _m_h5_tk 令牌预热重试。"""
    data = json.dumps({
        "abbucket": "9",
        "id": item_id,
        "mi_id": "0000OL4rUJH85X4AO3UCEQL_ihkkjsw1p_k8fzPiNDCGcLQ",
        "ns": "1",
        "skuId": sku_id or "0",
        "xxc": "taobaoSearch",
        "detail_v": "3.3.0",
        "preferWireless": "true",
    }, separators=(",", ":"))

    def token():
        return next((c.value.split("_")[0]
                     for c in session.cookies if c.name == "_m_h5_tk"), "")

    def call():
        t = str(int(time.time() * 1000))
        tk = token()
        sign = hashlib.md5((tk + "&" + t + "&" + APP_KEY + "&" + data).encode()).hexdigest()
        params = {
            "jsv": "2.7.5", "appKey": APP_KEY, "t": t, "sign": sign,
            "_bx-login": "new", "dangerouslySetWindvaneParams": "[object Object]",
            "api": "mtop.taobao.detail.getdesc", "v": "7.0",
            "AntiFlood": "true", "AntiCreep": "true", "timeout": "3000",
            "ttid": "2022@tmall_litepc_9.17.0", "type": "jsonp",
            "dataType": "jsonp", "callback": "mtopjsonp11", "data": data,
        }
        resp = session.get(DESC_URL, params=params, timeout=15)
        m = re.match(r"^[^(]+\((.*)\)\s*$", resp.text.strip(), re.S)
        return json.loads(m.group(1)) if m else {}

    j = call()
    for _ in range(3):
        ret = " ".join(j.get("ret", []))
        if "SUCCESS" in ret:
            break
        if "FAIL_SYS_TOKEN_EXOIRED" in ret:
            j = call()  # 预热：失败响应已下发新 token，重算签名
            continue
        raise RuntimeError(f"getdesc 接口失败: {ret}")
    cd = j.get("data", {}).get("components", {}).get("componentData", {}) or {}
    imgs = []
    for v in cd.values():
        if isinstance(v, dict) and v.get("model", {}).get("picUrl"):
            u = v["model"]["picUrl"]
            if u.startswith("//"):
                u = "https:" + u
            elif u.startswith("http://"):
                u = "https://" + u[7:]
            imgs.append(u)
    return imgs


def main():
    ap = argparse.ArgumentParser(description="淘宝 PC 商品详情采集器（纯 requests）")
    ap.add_argument("url", nargs="?", help="item.htm 商品链接")
    ap.add_argument("--id", help="商品 id")
    ap.add_argument("--sku", default="", help="sku id")
    ap.add_argument("--cookie", default=None, help="cookie 串（缺省读 cookie 文件）")
    ap.add_argument("--cookie-file", default=DEFAULT_COOKIE_FILE, help="cookie 文件路径")
    ap.add_argument("--desc", action="store_true", help="同时抓取详情图文图片")
    ap.add_argument("-o", "--output", default="", help="输出 JSON 文件（默认打印）")
    args = ap.parse_args()

    if args.url:
        item_id, sku_id = parse_url(args.url)
        if args.sku:
            sku_id = args.sku
    elif args.id:
        item_id = args.id
        sku_id = args.sku
    else:
        ap.error("需要提供商品链接 或 --id")

    cookie = load_cookie(args.cookie_file, args.cookie)
    session = build_session(cookie)

    print(f"[抓取] 商品 {item_id} sku={sku_id or '(默认)'} ...")
    data = fetch_item(session, item_id, sku_id)
    if args.desc:
        print("[抓取] 详情图文 ...")
        data["desc_images"] = fetch_desc(session, item_id, sku_id)

    out = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"[完成] 已写入 {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    sys.exit(main())
