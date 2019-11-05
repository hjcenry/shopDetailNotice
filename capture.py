from config import Config
from sony_camera_service import SonyCameraService

config = Config('config.ini')

if __name__ == '__main__':
    sony_cam_capture = SonyCameraService(config)
    sony_cam_capture.run()
