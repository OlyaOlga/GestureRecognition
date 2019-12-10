import numpy as np

from .gesture_detector_base import GestureDetectorBase
from .gesture import Gesture


class CvGestureDetector(GestureDetectorBase):

    def recognize(self, frame: np.ndarray) -> Gesture:
        gesture_id = int(np.random.uniform(0, 2))
        return Gesture(gesture_id)
