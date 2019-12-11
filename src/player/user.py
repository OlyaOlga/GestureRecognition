from multiprocessing import Process, Array
import ctypes
from typing import Tuple

import numpy as np
import cv2

from src.camera import CameraStreamer
from src.gesture import CvGestureDetector, GestureDetectorBase, Gesture
from .player import Player
from .image_hub import ImageHub


class User(Player):

    def __init__(self, device: int):
        super().__init__()

        self._win_name = f'User {id(self)}'

        self.stream = CameraStreamer(device)
        self.gesture_detector: GestureDetectorBase = CvGestureDetector()

        self.frame_shared_memory = Array(ctypes.c_uint8, self.stream.pixels, lock=True)

        self.stream.start()

        self.current_gesture = None

    def __del__(self):
        print('Stream stopped')
        self.stream.stop()

    def _shared_frame_to_ndarray(self):
        frame = np.ctypeslib.as_array(self.frame_shared_memory.get_obj()).reshape(self.stream.shape)
        return frame

    def get_gesture(self) -> Tuple[Gesture, np.ndarray]:
        frame = self.stream.frame
        shared_frame = self._shared_frame_to_ndarray()
        np.copyto(shared_frame, frame)
        self.current_gesture, cfd = self.gesture_detector.recognize(frame)
        return self.current_gesture, cfd

    def set_result_of_previous_game(self, is_win: bool) -> None:
        pass

    # def stop_player(self):
    #     self.stream.stop()

    # def hide_player(self):
    #     super().hide_player()
    #     self.stream.stop()

    def _show_async(self):
        graph_buffer = None

        while True:

            gesture, cfd = self.get_gesture()
            gesture_image = self._image_hub[gesture]

            canvas = self._shared_frame_to_ndarray().copy()

            h, w, _ = canvas.shape
            gh, gw, _ = gesture_image.shape

            if graph_buffer is None:
                graph_buffer = np.zeros([w-gw, 3])

            status_bar = np.zeros([gh, w, 3], np.uint8)
            canvas = np.concatenate([canvas, status_bar], axis=0)

            canvas[h:, 0:gw, :] = gesture_image

            graph_buffer = np.roll(graph_buffer, -1, axis=0)
            graph_buffer[-1, :] = cfd

            chart_colors = [
                (0, 0, 255),
                (0, 255, 0),
                (255, 0, 0)
            ]
            for idx in range(graph_buffer.shape[0]-1):
                col_prev = idx
                col_next = col_prev + 1
                for c in range(3):
                    value_prev = h-int(graph_buffer[col_prev, c]*gh)+gh
                    value_next = h-int(graph_buffer[col_next, c]*gh)+gh
                    cv2.line(canvas, (col_prev+gw, value_prev), (col_next+gw, value_next),
                             chart_colors[c], thickness=1)
                # canvas[]

            cv2.imshow(self._win_name, canvas)
            cv2.waitKey(1)

