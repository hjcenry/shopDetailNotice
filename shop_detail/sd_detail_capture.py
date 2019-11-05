import json
import requests
import time
import math
from lxml import etree

from shop_detail.i_shop_detail import IShopDetail


class SundanDetailCapture(IShopDetail):
    item_id = None
    item_url = None

    def __init__(self, item_id):
        self.item_id = int(item_id)
        self.item_url = 'https://www.sundan.com/product-%d.html' % self.item_id

    def capture(self):
        """
        抓取顺电商品接口
        :return:
        """
        url = "https://www.sundan.com/product-ajax_product_price-%d.html" % self.item_id
        headers = {
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-origin",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            'Accept': "text/javascript, text/html, application/xml, text/xml, */*",
            'Referer': self.item_url,
            'X-Requested-With': "XMLHttpRequest",
            'Connection': "keep-alive",
            'Cache-Control': "no-cache",
            'Host': "www.sundan.com",
            'Cookie': "s=2deb57fa9da53750f2d6239bc376c060; vary=ae2c3ec2d7539bd20d4cb3cca92a2f2050e866b103cbdd38b4491e75b4df2c72",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers)
        result_json = json.loads(response.text)
        return result_json

    @classmethod
    def get_item_name(cls, item_json, item_id):
        url = "https://www.sundan.com/product-%d.html" % int(item_id)
        headers = {
            'Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            'Sec-Fetch-Mode': "navigate",
            'Sec-Fetch-User': "?1",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Sec-Fetch-Site': "none",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Host': "www.sundan.com",
            'Cookie': "s=2deb57fa9da53750f2d6239bc376c060; vary=ae2c3ec2d7539bd20d4cb3cca92a2f2050e866b103cbdd38b4491e75b4df2c72",
            'cache-control': "no-cache"
        }
        response = requests.request("GET", url, headers=headers)
        html = etree.HTML(response.text)
        name_result = html.xpath('//div[@class="product-titles"]/h2/text()')
        for ret in name_result:
            if ret.replace('\n', '').strip() != '':
                return ret.strip()
        return None

    @classmethod
    def get_item_price(cls, item_json):
        return 0 if item_json['price'] == '' else float(item_json['price'])

    @classmethod
    def is_item_sold_out(cls, item_json):
        print("sundan not supported")
        return False


if __name__ == '__main__':
    item_id = 3034
    sd = SundanDetailCapture(item_id)
    result = sd.capture()
    print(sd.get_item_name(result, item_id))
    print(sd.get_item_price(result))
    print(sd.is_item_sold_out(result))
