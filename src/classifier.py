import os
import logging
import numpy as np
import tensorflow as tf
import cv2


class Classifier():
    """Identifies if there is or isn't a package on the porch"""

    def __init__(self):
        self._set_defaults()
        self._load_model()
        self._load_labels()

    def _set_defaults(self):
        parent_dir = os.path.dirname(os.path.realpath(__file__))
        self.model_file = os.path.join(parent_dir, 'models/model.tflite')
        self.label_file = os.path.join(parent_dir, 'models/dict.txt')
        self.input_mean = 127.5
        self.input_stdev = 127.5
        self.num_threads = None

    def _load_model(self):
        """Load the model into memory"""
        self.model = tf.lite.Interpreter(
            model_path=self.model_file
            )
        self.model.allocate_tensors()
        self.input_details = self.model.get_input_details()
        self.output_details = self.model.get_output_details()
        self.is_floating_model = self.input_details[0]['dtype'] == np.float32
        self._set_default_height_width()

    def _load_labels(self):
        """Load labels from the filesystem"""
        with open(self.label_file, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

    def _set_default_height_width(self):
        """Sets the default expected height and width"""
        self.default_height = self.input_details[0]['shape'][1]
        self.default_width = self.input_details[0]['shape'][2]

    def _normalize_input(self, frame):
        """Normalizies the input frame"""
        frame = cv2.resize(frame, (self.default_width, self.default_height))
        return frame

    def _build_input_data(self, frame):
        """Build the input data array"""
        return np.expand_dims(frame, axis=0)

    def classify_frame(self, frame):
        """Classifies a frame"""
        logging.debug('Classifying image')
        input_data = self._build_input_data(self._normalize_input(frame))
        self.model.set_tensor(self.input_details[0]['index'], input_data)
        self.model.invoke()
        # dont judge this code plz
        results = np.squeeze(self.model.get_tensor(self.output_details[0]['index']))
        top_k = results.argsort()
        top_confidence = 0.0
        top_label = ''
        for i in top_k:
            confidence = float(results[i] / 255.0)
            label = self.labels[i]
            if confidence > top_confidence:
                top_confidence = confidence
                top_label = label
        logging.debug('Classification complete')
        return round(top_confidence, 3), top_label

    def is_package_present(self, frame, min_confidence=0.5):
        """Determines if the package is currently present"""
        confidence, label = self.classify_frame(frame)
        logging.debug(str(confidence) + ' - ' + label)
        return label == 'package' and confidence > min_confidence
