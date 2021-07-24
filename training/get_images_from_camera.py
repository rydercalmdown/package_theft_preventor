"""Script for gathering training images from camera"""
import time
import os
from rtsparty import Stream
import cv2


print('Establishing stream')
stream_url = 'rtsp://username:password@host/endpoint'
stream = Stream(stream_url, live=True)


def get_file_name():
    """Returns the appropriate file name for the image"""
    prefix = 'normal_daytime_door_closed'
    # prefix = 'package_1_daytime_door_closed'
    prefix = 'testing'
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', prefix)
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
    try:
        while True:
            saved = save_image_to_file()
            if saved:
                print(saved)
                time.sleep(5)
            else:
                print('Error, waiting 5 seconds')
                time.sleep(5)
    except KeyboardInterrupt:
        print('Stopping')
