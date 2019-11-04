from config import Config
import shop_detail.capture_factory as ShopDetailFactory

config = Config('config.ini')

if __name__ == '__main__':
    item_keys = ['sony_cam_lens_55_18', 'sony_lens_85_18']
    for item_key in item_keys:
        for platform in config.get_config_dict().keys():
            platform_keys = config.get_config_dict()[platform]
            if item_key in platform_keys:
                price = 0
                for key in platform_keys[item_key].split(','):
                    if key == '':
                        continue
                    shop_detail_capture = ShopDetailFactory.get_shop_detail_capture(platform, key)
                    # 抓取
                    result_json = shop_detail_capture.capture()
                    price = price + shop_detail_capture.get_item_price(result_json)
                print(platform, "的", item_key, "价格：", price)
            else:
                print(platform, "没有商品", item_key)
