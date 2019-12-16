import abc
from typing import Union
from multiprocessing import Process, Value
import ctypes
import time

import numpy as np
import cv2
from src.global_locl import Lock

from src.gesture import Gesture
from .player import Player


class CpuPlayer(Player, metaclass=abc.ABCMeta):

    def __init__(self):
        self._win_name = f'Cpu {id(self)}'
        super().__init__()

    def __del__(self):
        super().__del__()

    def set_result_of_previous_game(self, is_win: bool) -> None:
        pass

    def show_async(self):
        # while True:
        #     with Lock.LOCK:
        gesture, cfd = self.get_gesture()
        image = self._image_hub[gesture]
        cv2.imshow(self._win_name, image)
        cv2.waitKey(1)

