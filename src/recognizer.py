import os
import logging
import face_recognition


class FaceRecognizer():
    """Face recognition module for package theft detection system"""

    def __init__(self):
        self._load_known_face()

    def _load_known_face(self):
        """Loads known faces from the filesystem"""
        faces_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'faces')
        faces = [os.path.join(faces_dir, f) for f in os.listdir(faces_dir) if f.endswith('.jpeg')]
        known_images = [face_recognition.load_image_file(i) for i in faces]
        self.known_faces = []
        for image in known_images:
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                logging.debug('Adding known face')
                self.known_faces.append(encoding[0])

    def known_face_detected(self, frame):
        """Retuns bool if a known face is detected"""
        faces_detected = face_recognition.face_encodings(frame)
        if len(faces_detected) > 0:
            unknown = face_recognition.face_encodings(frame)[0]
            results = face_recognition.compare_faces(self.known_faces, unknown)
            if True in results:
                logging.info('Known face detected')
                return True
            logging.info('Unknown face detected')
            return False
