from typing import Dict

import cv2
import numpy as np

from src.gesture import Gesture

class ImageHub:
    GESTURE_IMAGE_FILES = {
        Gesture.ROCK: 'data/rock.png',
        Gesture.PAPER: 'data/paper.png',
        Gesture.SCISSOR: 'data/scissors.png'
    }

    GESTURE_IMAGES: Dict[str, np.ndarray] = None

    def __init__(self):
        if ImageHub.GESTURE_IMAGES is None:
            ImageHub.GESTURE_IMAGES = {}
            for gesture, file in ImageHub.GESTURE_IMAGE_FILES.items():
                ImageHub.GESTURE_IMAGES[gesture] = cv2.imread(file)

    def __getitem__(self, item):
        return ImageHub.GESTURE_IMAGES[item].copy()