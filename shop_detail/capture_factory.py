from shop_detail.gome_detail_capture import GomeDetailCapture
from shop_detail.jd_detail_capture import JDDetailCapture
from shop_detail.sd_detail_capture import SundanDetailCapture
from shop_detail.sn_detail_capture import SuningDetailCapture


def get_shop_detail_capture(capture: str, item_id):
    """
    根据电商获取不同抓取类
    :param capture: 电商平台名字
    :param item_id: 商品id
    :return:
    """
    if capture == 'jd':
        return JDDetailCapture(item_id)
    elif capture == 'sn':
        return SuningDetailCapture(item_id)
    elif capture == 'gome':
        return GomeDetailCapture(item_id)
    elif capture == 'sundan':
        return SundanDetailCapture(item_id)
    else:
        print("no capture")
        return None
