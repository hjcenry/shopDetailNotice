import json
import requests
import time
import math
from lxml import etree

from shop_detail.i_shop_detail import IShopDetail


class SuningDetailCapture(IShopDetail):
    item_id = None
    item_url = None

    def __init__(self, item_id):
        self.item_id = item_id
        self.item_url = 'https://product.suning.com/0000000000/%d.html?safp=d488778a.13701.productWrap.11&safc=prd.3.ssdsn_name02-1_jz' % self.item_id

    def capture(self):
        """
        抓取苏宁商品接口
        :return:
        """
        url = "https://pas.suning.com/nspcsale_0_000000010437707469_0000000%d_0000000000_10_010_0100101_20089_1000000_9017_10106_Z001___R1207002_0.565_0___000051813___.html" % self.item_id
        querystring = {
            'callback': 'pcData',
            '_': math.floor(time.time() * 1000)
        }
        headers = {
            'Referer': self.item_url,
            'Sec-Fetch-Mode': 'no-cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        result_sub = response.text.replace('pcData', '')[1:-2]
        result_json = json.loads(result_sub)
        item_json = result_json['data']['price']['saleInfo'][0]
        return item_json

    @classmethod
    def get_item_name(cls, item_json, item_id):
        url = "https://product.suning.com/0000000000/%d.html" % item_id
        querystring = {
            "safp": "d488778a.13701.productWrap.10",
            "safc": "prd.3.ssdsn_pic02-1_jz"
        }
        headers = {
            'Sec-Fetch-Mode': "no-cors",
            'Referer': "https://product.suning.com/0000000000/%d.html?safp=d488778a.13701.productWrap.11^&safc=prd.3.ssdsn_name02-1_jz" % item_id,
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': "product.suning.com",
            'Cookie': "tradeLdc=NJYH",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        html = etree.HTML(response.text)
        name_result = html.xpath('//h1[@id="itemDisplayName"]/text()')
        for ret in name_result:
            if ret.strip() != '':
                return ret.strip()
        return None

    @classmethod
    def get_item_price(cls, item_json):
        return 0 if item_json['promotionPrice'] == '' else item_json['promotionPrice']

    @classmethod
    def is_item_sold_out(cls, item_json):
        return item_json['promotionPrice'] == ''


if __name__ == '__main__':
    item_id = 10437707469
    sn = SuningDetailCapture(item_id)
    result = sn.capture()
    print(sn.get_item_name(result, item_id))
    print(sn.get_item_price(result))
    print(sn.is_item_sold_out(result))
