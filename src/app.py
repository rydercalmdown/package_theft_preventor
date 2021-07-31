import time
import os
from classifier import Classifier
from rtsparty import Stream
from recognizer import FaceRecognizer
import logging
import requests
import sys


class PackageSentry():
    """Parent class for Package Sentry System"""

    def __init__(self):
        self._set_logging()
        self._set_defaults()

    def _set_defaults(self):
        """Set all defaults"""
        logging.info('Starting stream')
        self.server_mode = False  # Enable seerber mode; (separate the relay and processing components)
        self.alarm_endpoint = os.environ.get('ALARM_ENDPOINT', 'http://10.0.0.1:5000/alarm/')
        self.stream = Stream(os.environ.get('STREAM_URL'), live=True)
        self.recognizer = FaceRecognizer()
        logging.info('Starting classifier')
        self.classifier = Classifier()
        logging.info('Loading relay controller')
        if not self.server_mode:
            from relay_controller import RelayController
            self.relay_controller = RelayController()
        self.package_last_seen = None
        self.min_confidence = 0.5
        self.theft_tolerance_seconds = 0.1
        self.system_armed = False
        self.alarm_is_active = False
        self.package_detection_debounce_count = 0
        self.package_detection_debounce_threshold = 30
        self.known_person_timeout_seconds = 30
        self.known_persons_counter = 0
        self.known_person_last_seen = time.time()
        self.known_person_present = False

    def _set_logging(self):
        """Set the log level for the system"""
        level = logging.INFO
        logging.basicConfig(stream=sys.stdout, level=level)

    def arm_system(self):
        """Arm the system after a package has been left on the step"""
        logging.info('Arming System')
        self.system_armed = True

    def disarm_system(self):
        """Arm the system after a package has been left on the step"""
        logging.info('Disarming System')
        self.system_armed = False

    def activate_alarm(self):
        """A theft has occurred, activate the alarm"""
        if self.alarm_is_active:
            return
        logging.info('Activating Alarm')
        self.alarm_is_active = True
        if not self.server_mode:
            self.relay_controller.activate_general_alarm()
        else:
            requests.get(self.alarm_endpoint)

    def _package_detected(self):
        """A package has been identified in the frame"""
        logging.debug('Package detected')
        if self.package_detection_debounce_count > self.package_detection_debounce_threshold:
            if not self.system_armed:
                self.arm_system()
        else:
            self.package_detection_debounce_count = self.package_detection_debounce_count + 1
        self.package_last_seen = time.time()

    def _package_not_detected(self):
        """The package is missing from the frame"""
        self.package_detection_debounce_count = 0
        if not self.system_armed:
            logging.debug('System not armed, ignoring')
            return
        if self.known_person_present:
            logging.debug('Known person removed package')
            self.disarm_system()
            return
        # This code gives the system a tolerance for frames that may be inaccurately
        # reporting the package as missing because of errors in the model or stream
        current_time = time.time()
        if current_time > self.package_last_seen + self.theft_tolerance_seconds:
            self.activate_alarm()

    def _check_for_known_persons(self, frame):
        """Checks frame for known persons and responds accordingly"""
        # Only check once every n frrames
        check_every_n_frames = 60
        self.known_persons_counter = self.known_persons_counter + 1
        if self.known_persons_counter < check_every_n_frames:
            return
        self.known_persons_counter = 0
        logging.debug('Checking frame for faces')
        if self.recognizer.known_face_detected(frame):
            logging.info('Known person present')
            self.known_person_last_seen = time.time()
            self.known_person_present = True
        current_time = time.time()
        if current_time > self.known_person_timeout_seconds + self.known_person_last_seen:
            self.known_person_present = False

    def _check_frame(self):
        """Check the frame for packages"""
        frame = self.stream.get_frame()
        if not self.stream.is_frame_empty(frame):
            self._check_for_known_persons(frame)
            if self.classifier.is_package_present(frame, self.min_confidence):
                self._package_detected()
            else:
                self._package_not_detected()

    def watch(self):
        """Watch for thieves and act accordingly"""
        logging.info('System watching')
        while True:
            self._check_frame()


def main():
    """Run app"""
    try:
        ps = PackageSentry()
        ps.watch()
    except KeyboardInterrupt:
        print('Exiting')


if __name__ == '__main__':
    main()
