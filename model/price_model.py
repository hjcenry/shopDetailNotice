import json


class PriceMode(object):
    # 电商平台
    platform = ""
    # 价格
    price = 0

    @staticmethod
    def load_from_str(model_str: str):
        model = PriceMode()
        if model_str is None:
            model.platform = ""
            model.price = 0
        else:
            model_json = json.loads(model_str)
            model.platform = model_json['platform']
            model.price = model_json['price']
        return model

    def convert_to_str(self):
        model_str = json.dumps(self.__dict__)
        return model_str
