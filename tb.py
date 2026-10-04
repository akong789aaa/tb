import requests
import json
from lxml import etree
# from test_select import search
__id=input("id:")
cookies = {
    'cna': 'htZDI+Mrz18BASQJiT1lmp2S',
    'xlly_s': '1',
    'lid': 'jnhxjg',
    'wk_cookie2': '16483a4f5b3772dfe4e8796a3c855f44',
    'wk_unb': 'WvZtD7EUevlf',
    'isg': 'BMbGrQQs0Gz0qoSJCPhJGcGLF7VIJwrheBxnibDvsunEs2bNGLda8axAi-9_GwL5',
    'skupanel-skuoptions-layout-mode': 'listMode',
    'dnk': 'jnhxjg',
    'uc1': 'cookie21',
    'uc3': 'vt3',
    'tracknick': 'jnhxjg',
    '_l_g_': 'Ug%3D%3D',
    'havana_lgc_exp': '1822019568896',
    'uc4': 'nk4',
    'unb': '968510362',
    'lgc': 'jnhxjg',
    'cookie1': 'WqTCOWiL80wN2FjchDKHDtpFSj%2B%2B8tZMQB9rd96heBA%3D',
    'login': 'true',
    'cookie17': 'WvZtD7EUevlf',
    'cookie2': '244bf724d855e0d3ca2c735bba55557b',
    '_nk_': 'jnhxjg',
    'sgcookie': 'E100M6MIhKv%2FraYB9ie8L4Sw2i4G4%2Bp5apMhxPrr%2BrnpcHsoAMccnLS6ugjm5VjgWee4AiojfoFcSG8uZhY0UUfgAYwkzCo3irG%2F8R%2Fb0R%2F94QALwVFfaOfleXhNYILkCEsq',
    'cancelledSubSites': 'empty',
    'sg': 'g22',
    't': 'da9f886ab76863448f4b7e283b1e4a03',
    'csg': 'b389f5ec',
    'sn': '',
    '_tb_token_': '7380ee3f7f77b',
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': '17d006bab23d09eca350c1febfc169da_1790923494012',
    '_m_h5_tk_enc': 'a2233c967b75bbf1df871d24685a0816',
    '_3dtid': 'vhsyV6UL+l78VprtdN7byz+yQtFm60FfiyB+op1dN2HgDHVeU56HkeYL5K8XNpTs',
    'tfstk': 'h16nsncvYoBCIlFTny-hPqrtE5evI0jf0UHKap7MqZI4AMQR43WlyNJJay9dENbd06dd4TKPELpzkY1Lnl8BVG8rvBemuM9WUrntUSe0Zl-qxvJPzd8w4npy4Y8zjd-JVLkeavlw7FtyUU7yTVuwv3oE8Q-UQlxW7UJyUaSaj3LwzLJPzGRTIM2MvXYisz7YhbHrUO2WtEyXSYkPI6dHuvLgJIZ0wIbeZTZmINXkrQLXOmuyQi1O8hv0Kqth_ivem9rSwK5fSTxUJblolG6CBAEbxWXGVIBLpuEhFwBCtwyK86CMVtQNwDNYt81Ots5sfjWPFefCVIo0wSaCB6QeNJM5QoBlVp7gnf4lFOWajEdhWkL_i3nujlqigbOefHSzjlcSNB-6jEEgjjxDThtF4',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="151", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    # 'Cookie': 'cna=htZDI+Mrz18BASQJiT1lmp2S; xlly_s=1; lid=jnhxjg; wk_cookie2=16483a4f5b3772dfe4e8796a3c855f44; wk_unb=WvZtD7EUevlf; isg=BMbGrQQs0Gz0qoSJCPhJGcGLF7VIJwrheBxnibDvsunEs2bNGLda8axAi-9_GwL5; skupanel-skuoptions-layout-mode=listMode; dnk=jnhxjg; uc1=cookie21; uc3=vt3; tracknick=jnhxjg; _l_g_=Ug%3D%3D; havana_lgc_exp=1822019568896; uc4=nk4; unb=968510362; lgc=jnhxjg; cookie1=WqTCOWiL80wN2FjchDKHDtpFSj%2B%2B8tZMQB9rd96heBA%3D; login=true; cookie17=WvZtD7EUevlf; cookie2=244bf724d855e0d3ca2c735bba55557b; _nk_=jnhxjg; sgcookie=E100M6MIhKv%2FraYB9ie8L4Sw2i4G4%2Bp5apMhxPrr%2BrnpcHsoAMccnLS6ugjm5VjgWee4AiojfoFcSG8uZhY0UUfgAYwkzCo3irG%2F8R%2Fb0R%2F94QALwVFfaOfleXhNYILkCEsq; cancelledSubSites=empty; sg=g22; t=da9f886ab76863448f4b7e283b1e4a03; csg=b389f5ec; sn=; _tb_token_=7380ee3f7f77b; mtop_partitioned_detect=1; _m_h5_tk=17d006bab23d09eca350c1febfc169da_1790923494012; _m_h5_tk_enc=a2233c967b75bbf1df871d24685a0816; _3dtid=vhsyV6UL+l78VprtdN7byz+yQtFm60FfiyB+op1dN2HgDHVeU56HkeYL5K8XNpTs; tfstk=h16nsncvYoBCIlFTny-hPqrtE5evI0jf0UHKap7MqZI4AMQR43WlyNJJay9dENbd06dd4TKPELpzkY1Lnl8BVG8rvBemuM9WUrntUSe0Zl-qxvJPzd8w4npy4Y8zjd-JVLkeavlw7FtyUU7yTVuwv3oE8Q-UQlxW7UJyUaSaj3LwzLJPzGRTIM2MvXYisz7YhbHrUO2WtEyXSYkPI6dHuvLgJIZ0wIbeZTZmINXkrQLXOmuyQi1O8hv0Kqth_ivem9rSwK5fSTxUJblolG6CBAEbxWXGVIBLpuEhFwBCtwyK86CMVtQNwDNYt81Ots5sfjWPFefCVIo0wSaCB6QeNJM5QoBlVp7gnf4lFOWajEdhWkL_i3nujlqigbOefHSzjlcSNB-6jEEgjjxDThtF4',
}

params = {
    'id': __id,
}
result={}
resp = requests.get('https://detail.tmall.com/item.htm', params=params, cookies=cookies, headers=headers)
print(resp.text)
tree=etree.HTML(resp.text)
price=tree.xpath('//*[@id="tbpcDetail_SkuPanelBody"]/div[2]/div[1]/span[2]/text()')[0]
result['id']=__id
title=tree.xpath('//*[@id="tbpcDetail_SkuPanelBody"]/div[1]/div/div/div[1]/span/text()')[0]
result['title']=title
# result['type']=search(title)
result["price"]=price
skus=tree.xpath('//*[@id="skuOptionsArea"]/div/div/div[2]/div/div/div')
result['sku_count']=len(skus)
result['sku']=[]
for sku in skus:
    result['sku'].append(sku.xpath('./span/text()')[0])
json_str = json.dumps(result, ensure_ascii=False, indent=2)
with open(f'{__id}.json',mode='w',encoding='utf-8')as f:
    f.write(json_str)
print(json_str)