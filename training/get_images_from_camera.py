"""Script for gathering training images from camera"""
import time
import pathlib
import os
from rtsparty import Stream
import cv2


print('Establishing stream')
stream = Stream(os.environ['RTSP_URL'], live=True)


def get_data_dir():
    """Returns the data directory"""
    return os.path.dirname(os.path.realpath(__file__)), 'data'


def create_dirs():
    """Creates directories if not exists"""
    pathlib.Path(os.path.join(get_data_dir(), 'package')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.join(get_data_dir(), 'no_package')).mkdir(parents=True, exist_ok=True)


def get_file_name():
    """Returns the appropriate file name for the image"""
    prefix = 'no_package'
    if bool(os.environ.get('PACKAGE_PRESENT', False)):
        prefix = 'package'
    data_dir = os.path.join(get_data_dir(), 'data', prefix)
    file_name = prefix + '__' + str(int(time.time())) + '.jpg'
    return os.path.join(data_dir, file_name)


def save_image_to_file():
    """saves the image to the local filesystem"""
    frame = stream.get_frame()
    file_name = get_file_name()
    if stream.is_frame_empty(frame):
        return False
    cv2.imwrite(file_name, frame)
    return file_name


if __name__ == '__main__':
    create_dirs()
    try:
        while True:
            saved = save_image_to_file()
            if saved:
                print(saved)
                time.sleep(5)
            else:
                print('Error, waiting 5 seconds')
                time.sleep(int(os.environ.get('SLEEP_SECONDS', '5')))
    except KeyboardInterrupt:
        print('Stopping')
