from multiprocessing import Process, Value
import time
import ctypes
from typing import Tuple

import numpy as np

from src.gesture import Gesture
from .cpu_player import CpuPlayer


class DummyCpuPlayer(CpuPlayer):

    def __init__(self):
        super().__init__()
        self._current_gesture = Value(ctypes.c_int, 0, lock=True)
        self._thread_gesture_choice = Process(target=self._gesture_choice_async)
        self._thread_gesture_choice.start()

    def __del__(self):
        super().__del__()
        self._thread_gesture_choice.terminate()

    def get_gesture(self) -> Tuple[Gesture, np.ndarray]:
        gesture = Gesture(self._current_gesture.value)
        return gesture, np.array([0, 0, 1])

    # def hide_player(self):
        # super().hide_player()
        # self._thread_gesture_choice.terminate()

    def _gesture_choice_async(self):
        while True:
            time.sleep(np.random.uniform(0, 3))
            self._current_gesture.value = int(np.random.uniform(0, 4))
