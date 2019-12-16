from typing import Tuple

import numpy as np

from .gesture_detector_base import GestureDetectorBase
from .gesture import Gesture


class CvGestureDetector(GestureDetectorBase):

    def recognize(self, frame: np.ndarray) -> Tuple[Gesture, np.ndarray]:
        gesture_id = int(np.random.uniform(0, 4))
        cfd = np.random.normal(0, 0.5, [4,])
        cfd = np.exp(cfd)/np.sum(np.exp(cfd))
        return Gesture(gesture_id), cfd
