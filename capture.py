from config import Config
from capture_service.sony_camera_service import SonyCameraService

config = Config('config.ini')

if __name__ == '__main__':
    sony_cam_capture = SonyCameraService(config)
    sony_cam_capture.run()
