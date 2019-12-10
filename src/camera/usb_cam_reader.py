from typing import Union

import numpy as np
import cv2

class UsbCamReader:

    def __init__(self, device: int):
        self.device = device
        self.cam: Union[cv2.VideoCapture, None] = None

    def __enter__(self):
        self.cam = cv2.VideoCapture(self.device)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cam.release()

    def grab_frame(self) -> np.ndarray:
        if self.cam is None:
            raise RuntimeError('Camera has not been opened yet. Use context manager style')

        succ, frame = self.cam.read()

        if not succ:
            raise RuntimeError('Failed to grab the next frame')

        return frame
