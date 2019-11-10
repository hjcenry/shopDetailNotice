import json
import requests
import time
import math

from shop_detail.i_shop_detail import IShopDetail


class JDDetailCapture(IShopDetail):
    item_id = None
    item_url = None

    def __init__(self, item_id):
        self.item_id = int(item_id)
        self.item_url = 'https://item.jd.com/%d.html' % self.item_id

    def capture(self):
        """
        抓取京东商品价格接口
        :return:
        """
        url = "https://c.3.cn/recommend"
        querystring = {
            'callback': 'handleComboCallback',
            'methods': 'accessories',
            'p': 103003,
            'sku': self.item_id,
            'cat': '652,654,5012',
            'lid': 1,
            'uuid': 1302831477,
            'pin': 'hjcenry',
            'ck': 'pin,ipLocation,atw,aview',
            'lim': 5,
            'cuuid': 1302831477,
            'csid': '122270672.4.1302831477|7.1572785865',
            '_': math.floor(time.time() * 1000)
        }
        headers = {
            'Referer': self.item_url,
            'Sec-Fetch-Mode': 'no-cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        result_sub = response.text.replace('handleComboCallback', '')[1:-1]
        result_json = json.loads(result_sub)
        item_json = result_json['accessories']['data']
        return item_json

    @classmethod
    def get_item_name(cls, item_json, item_id):
        return item_json['wName']

    @classmethod
    def get_item_price(cls, item_json):
        return float(item_json['wMaprice'])

    @classmethod
    def is_item_sold_out(cls, item_json):
        return item_json['wMaprice'] == -1.0


if __name__ == '__main__':
    item_ids = [100001877615, 4648654]
    price = 0
    for item_id in item_ids:
        jd = JDDetailCapture(item_id)
        result = jd.capture()
        print(jd.get_item_name(result, 100001877615))
        item_price = jd.get_item_price(result)
        print(jd.get_item_price(result))
        price = price + item_price
        # print(jd.is_item_sold_out(result))

    print(price)
