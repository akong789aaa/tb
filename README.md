# 淘宝商品详情采集器

纯协议版淘宝/天猫商品信息采集工具，无浏览器自动化依赖。

## 特性

- **纯 HTTP 协议**：使用 `requests` 发送请求，不依赖 Playwright/Selenium/Puppeteer
- **SSR 数据解析**：从淘宝页面服务端渲染的 HTML 中提取 `__ICE_APP_CONTEXT__` 数据
- **详情图文支持**：可选抓取商品详情页图片（mtop API + md5 签名）
- **令牌自动续期**：`_m_h5_tk` 过期时自动预热重试
- **完整商品信息**：标题、价格、销量、SKU、卖家信息、属性参数等

## 安装依赖

```bash
pip install requests lxml
```

## 使用方法

### 主采集器（taobao_item_detail.py）

**基础用法**：

```bash
# 通过商品链接抓取
python taobao_item_detail.py "https://item.taobao.com/item.htm?id=1056191431122&skuId=6100482645581"

# 通过 ID 抓取
python taobao_item_detail.py --id 1056191431122 --sku 6100482645581

# 同时抓取详情图文
python taobao_item_detail.py --id 1056191431122 --desc

# 输出到文件
python taobao_item_detail.py --id 1056191431122 --desc -o detail.json
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| `url` | 商品链接（item.htm 格式） |
| `--id` | 商品 ID |
| `--sku` | SKU ID（可选） |
| `--desc` | 抓取详情图文 |
| `--cookie` | Cookie 字符串 |
| `--cookie-file` | Cookie 文件路径（默认 `cookie.txt`） |
| `-o, --output` | 输出 JSON 文件 |

### 天猫采集器（tb.py）

简单的天猫商品抓取脚本，使用 XPath 解析：

```bash
python tb.py
# 交互式输入商品 ID
```

## Cookie 配置

**方式一：使用 cookie.txt 文件**

在项目根目录创建 `cookie.txt`，粘贴淘宝登录后的 Cookie 字符串。

**方式二：命令行传入**

```bash
python taobao_item_detail.py --cookie "your_cookie_string" --id 123456
```

**获取 Cookie**：

1. 浏览器登录淘宝
2. 打开开发者工具（F12）→ Network
3. 刷新页面，找到 `item.htm` 请求
4. 复制 Request Headers 中的 Cookie

## 输出数据结构

```json
{
  "item_id": "1056191431122",
  "sku_id": "6100482645581",
  "title": "商品标题",
  "price": "99.00",
  "sold_count": "10万+",
  "sold_desc": "月销10万+",
  "images": ["https://..."],
  "desc_url": "https://...",
  "seller": {
    "nick": "店铺昵称",
    "shop_name": "店铺名称",
    "shop_url": "https://...",
    "shop_id": "123456",
    "seller_id": "789",
    "seller_type": "B",
    "credit_level": "20",
    "evaluates": {
      "描述相符": "4.9",
      "服务态度": "4.9"
    }
  },
  "params": {
    "颜色": ["黑色", "白色"],
    "尺码": ["S", "M", "L"]
  },
  "params_attrs": {
    "basic": {...},
    "enhance": {...}
  },
  "skus": [
    {
      "sku_id": "6100482645581",
      "props": {
        "颜色": "黑色",
        "尺码": "M"
      },
      "price": "99.00",
      "quantity": 100,
      "quantity_text": "有货"
    }
  ],
  "sku_count": 6,
  "desc_images": ["https://..."]
}
```

## 技术实现

### 数据来源

1. **主体数据**：从 `item.taobao.com/item.htm` 页面 SSR HTML 中提取
   - 使用括号配对算法精确定位 `var b = {...}` JSON 对象
   - 不依赖浏览器环境，直接解析 HTML

2. **详情图文**：通过 `mtop.taobao.detail.getdesc` API 获取
   - 需要 md5 签名：`md5(token + "&" + timestamp + "&" + appKey + "&" + data)`
   - 自动处理 `FAIL_SYS_TOKEN_EXOIRED` 错误并重试

### 签名机制

```python
# _m_h5_tk 令牌
token = cookie中的 _m_h5_tk 前半部分

# 计算签名
sign = md5(f"{token}&{timestamp}&{APP_KEY}&{json_data}")
```

## 常见问题

**Q: 提示"触发风控"或"被重定向到登录页"？**

A: Cookie 已失效，需要重新登录淘宝并更新 `cookie.txt`。

**Q: 响应中无 SSR 数据？**

A: 可能触发反爬，尝试：
- 更换 IP
- 刷新 Cookie
- 降低请求频率

**Q: getdesc 接口失败？**

A: 令牌过期，脚本会自动重试 3 次。如仍失败，检查 Cookie 完整性。

## 项目结构

```
taobao/
├── taobao_item_detail.py   # 主采集器（推荐）
├── tb.py                   # 天猫简易采集器
├── test_select.py          # 测试脚本
├── cookie.txt              # Cookie 配置（需自行创建）
├── *.json                  # 样本数据
└── README.md
```

## 注意事项

- **登录 Cookie 必需**：所有接口均需登录态
- **请求频率控制**：建议间隔 1-3 秒，避免触发风控
- **数据仅供学习**：请遵守淘宝服务条款，不要用于商业用途
- **Cookie 安全**：不要将 Cookie 提交到公开仓库

## 开发原则

根据项目 `AGENTS.md` 规则：

1. **禁止浏览器自动化**：成品代码不使用 Playwright/Selenium/Puppeteer
2. **Python + HTTP 请求**：使用 `requests`/`httpx`/`aiohttp`
3. **JS 辅助**：复杂加密逻辑可通过 `execjs` 或 Node.js 子进程处理
4. **V8 兼容**：JS 代码可在 V8 环境运行

## 许可

本项目仅供学习交流使用。
