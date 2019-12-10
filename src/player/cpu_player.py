import abc
from typing import Union
from multiprocessing import Process, Value
import ctypes
import time

import numpy as np
import cv2

from src.gesture import Gesture
from .player import Player
from .image_hub import ImageHub


class CpuPlayer(Player, metaclass=abc.ABCMeta):

    def __init__(self):
        self._thread_show: Union[Process, None] = None
        self._image_hub = ImageHub()
        self._win_name = f'CpuPlayer {id(self)}'

    def __del__(self):
        if self._thread_show is not None:
            self._thread_show.terminate()
        cv2.destroyWindow(self._win_name)

    def set_result_of_previous_game(self, is_win: bool) -> None:
        pass

    def show_player(self):
        self._thread_show = Process(target=self._show_async)
        self._thread_show.start()

    def _show_async(self):
        while True:
            image = self._image_hub[self.get_gesture()]
            cv2.imshow(self._win_name, image)
            cv2.waitKey(1)

