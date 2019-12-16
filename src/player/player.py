import abc
from typing import Union, Tuple
from multiprocessing import Process

import numpy as np
from src.global_locl import Lock

from src.gesture import Gesture
from .image_hub import ImageHub


class Player(metaclass=abc.ABCMeta):


    def __init__(self):
        self._thread_show: Union[Process, None] = None
        self._win_name = f'Player {id(self)}'
        self._image_hub = ImageHub()

    def __del__(self):
        self.hide_player()

    @abc.abstractmethod
    def set_result_of_previous_game(self, is_win: bool) -> None:
        pass

    @abc.abstractmethod
    def get_gesture(self) -> Tuple[Gesture, np.ndarray]:
        pass

    @abc.abstractmethod
    def show_async(self):
        pass

    # @abc.abstractmethod
    # def stop_player(self):
        # self._thread_show.terminate()

    def show_player(self):
        # self._thread_show = Process(target=self.show_async)
        # self._thread_show.start()
        pass

    def hide_player(self):
        if self._thread_show is not None:
            self._thread_show.terminate()
        self._thread_show = None
