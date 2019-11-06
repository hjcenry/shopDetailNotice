class IShopDetail(object):

    def capture(self):
        """
        抓取数据
        :return:
        """
        pass

    @classmethod
    def get_item_name(cls, item_json, item_id):
        """
        获取商品名字
        :param item_json:
        :param item_id:
        :return:
        """
        pass

    @classmethod
    def get_item_price(cls, item_json):
        """
        获取商品价格
        :param item_json:
        :return:
        """
        pass

    @classmethod
    def is_item_sold_out(cls, item_json):
        """
        商品是否下架
        :param item_json:
        :return:
        """
        pass

    def get_item_id(self):
        """
        获取商品id
        :return:
        """
        pass

    def get_item_url(self):
        """
        获取商品购买链接
        :return:
        """
        pass
