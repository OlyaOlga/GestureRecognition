from multiprocessing import Process, Array, Value
import ctypes
import functools
from typing import Union
import time

import numpy as np
import cv2

from .usb_cam_reader import UsbCamReader


class CameraStreamer:

    def __init__(self, device: int):
        self.device = device

        with UsbCamReader(self.device) as cam:
            width = int(cam.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cam.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.shape = (height, width, 3)

        self.pixels = functools.reduce(lambda x, a: x*a, self.shape)
        self.frame_shared_memory = Array(ctypes.c_uint8, self.pixels, lock=True)
        self._fps = Value(ctypes.c_float, 0, lock=True)
        self._process: Union[Process, None] = None

    @property
    def frame(self) -> np.ndarray:
        return self._shared_frame_to_ndarray().copy()

    @property
    def fps(self) -> float:
        return self._fps.value

    def start(self):
        self._process = Process(target=self._grab_frames_async)
        self._process.start()

    def stop(self):
        if self._process:
            self._process.terminate()
            self._process = None

    def __enter__(self):
        if self._process is not None:
            raise RuntimeError('Stream started! Use newly created object with context manager')

        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _shared_frame_to_ndarray(self):
        frame = np.ctypeslib.as_array(self.frame_shared_memory.get_obj()).reshape(self.shape)
        return frame

    def _grab_frames_async(self):
        with UsbCamReader(self.device) as cam:
            while True:
                start = time.time()
                frame = cam.grab_frame()
                np.copyto(self._shared_frame_to_ndarray(), frame)
                self._fps.value = 1/(time.time()-start)
