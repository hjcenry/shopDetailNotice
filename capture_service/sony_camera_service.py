import os

import capture_factory
from redis_dao import RedisDao
from model.price_model import PriceMode


class SonyCameraService(object):
    item_keys = ['sony_cam_lens_55_18', 'sony_lens_85_18']
    config = None
    redis_dao = None

    item_min_price_key_pre = 'min_price_'
    min_price_key_pre = item_min_price_key_pre + "sony_total"
    platform_price_key_pre = "platform_price_"

    def __init__(self, config):
        self.config = config
        self.redis_dao = RedisDao()

    def run(self):
        # 遍历所有电商平台的key
        for platform in self.config.get_config_dict().keys():
            platform_keys = self.config.get_config_dict()[platform]
            platform_name = self.config.get_config_dict()[platform]['name']
            # 总价值最低价model
            sony_min_price_mode = PriceMode.load_from_str(self.redis_dao.get_value(self.min_price_key_pre))
            sony_price = 0
            calc_all = True
            for item_key in self.item_keys:
                # 遍历需要抓取的商品key
                # 平台-商品价格model
                platform_item_price_mode = PriceMode.load_from_str(
                    self.redis_dao.get_value(self.platform_price_key_pre + platform + item_key))
                # 当前商品最低价model
                item_min_price_mode = PriceMode.load_from_str(
                    self.redis_dao.get_value(self.item_min_price_key_pre + item_key))
                if item_key in platform_keys:
                    # 电商平台包含此商品
                    current_price = 0
                    item_name = ""
                    for key in platform_keys[item_key].split(','):
                        # 统计价格
                        if key == '':
                            continue
                        shop_detail_capture = capture_factory.get_shop_detail_capture(platform, key)
                        # 抓取
                        result_json = shop_detail_capture.capture()
                        item_name = ("" if item_name == "" else ",") + shop_detail_capture.get_item_name(result_json,
                                                                                                         key)
                        current_price = current_price + shop_detail_capture.get_item_price(result_json)
                    print(platform_name, "的", item_key, "价格：", current_price)
                    if item_min_price_mode.price == 0 or item_min_price_mode.price > current_price:
                        # 超过当前商品记录中的最低价
                        item_min_price_mode.platform = platform_name + "," + item_name
                        pre_platform = item_min_price_mode.platform
                        pre_price = item_min_price_mode.price
                        item_min_price_mode.price = current_price
                        # 存储redis
                        self.redis_dao.set_value(self.item_min_price_key_pre + item_key,
                                                 item_min_price_mode.convert_to_str())
                        # 消息通知
                        msg = "%s的商品%s出现当前最低价%d，低于之前%s的最低价%d" % (
                            platform_name, item_name, current_price, pre_platform, pre_price)
                        self.msg_notice(msg)
                    if platform_item_price_mode.price == 0 or platform_item_price_mode.price != current_price:
                        # 当前平台价格变动通知
                        msg = "%s的商品%s价格变动！，现在是%s，之前是%s" % (
                            platform_name, item_name, current_price, platform_item_price_mode.price)
                        self.msg_notice(msg)
                        # 存储redis
                        platform_item_price_mode.platform = platform_name
                        platform_item_price_mode.price = current_price
                        self.redis_dao.set_value(self.platform_price_key_pre + platform + item_key,
                                                 platform_item_price_mode.convert_to_str())

                    sony_price = sony_price + current_price
                else:
                    print(platform_name, "没有商品", item_key)
                    # 平台没有对应商品，不计总价对比
                    calc_all = False

            if calc_all and (sony_min_price_mode.price == 0 or sony_min_price_mode.price > sony_price):
                # 超过记录中的最低价
                pre_platform = sony_min_price_mode.platform
                pre_price = sony_min_price_mode.price
                sony_min_price_mode.platform = platform_name
                sony_min_price_mode.price = sony_price
                # 存储redis
                self.redis_dao.set_value(self.min_price_key_pre, sony_min_price_mode.convert_to_str())
                # 消息通知
                msg = "想买的所有商品总价在%s出现最低价%d，低于之前%s的最低价%d" % (platform_name, sony_price, pre_platform, pre_price)
                self.msg_notice(msg)

    @classmethod
    def msg_notice(cls, content):
        print('notice msg!!!!:' + content)
        invoke_shell = "cd /home/pi/Soft/python/sender;python3 /home/pi/Soft/python/sender/sender.py -st 4 -t %s" % content
        result = os.system(invoke_shell)
        return result is 0
