from typing import Tuple

import numpy as np

import abc

from .gesture import Gesture


class GestureDetectorBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def recognize(self, frame: np.ndarray) -> Tuple[Gesture, np.ndarray]:
        pass
