from config import Config
from sony_a7m3_service import SonyA7M3Service

config = Config('config.ini')

if __name__ == '__main__':
    sony_cam_capture = SonyA7M3Service(config)
    sony_cam_capture.run()
