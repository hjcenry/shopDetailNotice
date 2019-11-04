import json
import requests
import time
import math
from lxml import etree

from shop_detail.i_shop_detail import IShopDetail


class GomeDetailCapture(IShopDetail):
    item_id = None
    item_url = None

    def __init__(self, item_id):
        self.item_id = str(item_id)
        self.item_url = 'https://item.gome.com.cn/%s.html?intcmp=list-9000000700-1_1_1^&search_id=CATPL^@1pYSyIkQ35uE' % self.item_id

    def capture(self):
        """
        抓取国美商品接口
        :return:
        """
        now_time = math.floor(time.time() * 1000)
        url = "https://ss.gome.com.cn/item/v1/d/m/store/unite/%s/N/11010200/110102002/1/null/flag/item/allStores?callback=allStores^&_=%d" % (
            self.item_id.replace('-', '/'), now_time)
        querystring = {
            'callback': 'allStores^',
            '_': now_time
        }
        headers = {
            'Referer': self.item_url,
            'Sec-Fetch-Mode': 'no-cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        result_sub = response.text.replace('allStores', '')[1:-1]
        result_json = json.loads(result_sub)
        if 'result' not in result_json:
            return None
        item_json = result_json['result']
        return item_json

    @classmethod
    def get_item_name(cls, item_json, item_id):
        url = "https://item.gome.com.cn/%s.html" % item_id
        response = requests.request("GET", url)
        html = etree.HTML(response.text)
        name_result = html.xpath('//div[@class="hgroup"]/h1/text()')
        for ret in name_result:
            if ret.strip() != '':
                return ret.strip()
        return None

    @classmethod
    def get_item_price(cls, item_json):
        if item_json is None:
            return 0
        return float(item_json['gomePrice']['salePrice'])

    @classmethod
    def is_item_sold_out(cls, item_json):
        return item_json is None


if __name__ == '__main__':
    item_id = '9140125925-1130643932'
    gome = GomeDetailCapture(item_id)
    result = gome.capture()
    print(gome.get_item_name(result, item_id))
    print(gome.get_item_price(result))
    print(gome.is_item_sold_out(result))
