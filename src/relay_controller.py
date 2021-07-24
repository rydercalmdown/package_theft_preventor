import logging
import time
import threading
import RPi.GPIO as GPIO


class RelayController():
    """Class for controlling the relay"""

    def __init__(self):
        self._set_defaults()
        self._setup_gpio()

    def __del__(self):
        GPIO.cleanup()

    def _set_defaults(self):
        """Set defaults for the application"""
        self.silent = False
        self.sprinkler_running_timeout_seconds = 10
        self.air_solenoid_running_timeout_seconds = 2
        self.misc_running_timeout_seconds = 5
        self.sprinkler_pin_bcm = 27
        self.misc_pin_bcm = 17
        self.air_solenoid_pin_bcm = 22

    def _setup_gpio(self):
        """Set up the GPIO defaults"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sprinkler_pin_bcm, GPIO.OUT)
        GPIO.setup(self.misc_pin_bcm, GPIO.OUT)
        GPIO.setup(self.air_solenoid_pin_bcm, GPIO.OUT)
        GPIO.output(self.sprinkler_pin_bcm, 1)
        GPIO.output(self.misc_pin_bcm, 1)
        GPIO.output(self.sprinkler_pin_bcm, 1)

    def _cycle_gpios(self):
        """Cycle all active channels in the relay opn and off"""
        logging.info('Cycling Relay')
        time.sleep(1)
        channels = [
            self.sprinkler_pin_bcm,
            self.misc_pin_bcm,
            self.air_solenoid_pin_bcm,
        ]
        for c in channels:
            self._cycle_pin(c, 1)

    def _cycle_pin(self, pin, timeout):
        """Cycle a relay channel on and off"""
        GPIO.output(pin, 0)
        time.sleep(timeout)
        GPIO.output(pin, 1)

    def activate_sprinkler(self):
        """Cycles the sprinkler on and off"""
        time.sleep(1)
        logging.info('Activating Sprinkler')
        self._cycle_pin(self.sprinkler_pin_bcm, self.sprinkler_running_timeout_seconds)
        logging.info('Deactivating Sprinkler')

    def activate_misc_items(self):
        """Activates all misc 12v items, the siren, lights, etc."""
        logging.info('Activating Misc Items')
        self._cycle_pin(self.misc_pin_bcm, self.misc_running_timeout_seconds)
        logging.info('Deactivating Misc Items')

    def activate_solenoid(self):
        """Activates the air solenoid."""
        time.sleep(2)
        logging.info('Activating air solenoid')
        self._cycle_pin(self.air_solenoid_pin_bcm, self.air_solenoid_running_timeout_seconds)
        logging.info('Deactivating air solenoid')

    def activate_general_alarm(self):
        """Activates all aspects of the alarm using background threads"""
        sprinkler_thread = threading.Thread(name='sprinkler_thread', target=self.activate_sprinkler)
        sprinkler_thread.setDaemon(True)
        if not self.silent:
            solenoid_thread = threading.Thread(name='solenoid_thread', target=self.activate_solenoid)
            misc_thread = threading.Thread(name='misc_thread', target=self.activate_misc_items)
            solenoid_thread.setDaemon(True)
            misc_thread.setDaemon(True)
        sprinkler_thread.start()
        if not self.silent:
            solenoid_thread.start()
            misc_thread.start()
