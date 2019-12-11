import time

import numpy as np
import cv2

from src.gesture import CvGestureDetector
from src.camera import UsbCamReader, CameraStreamer
from src.player import DummyCpuPlayer, User
from src.game import Game

print('Hello, world!')


# with UsbCamReader(0) as cam:
#     while cv2.waitKey(1) != 27:
#         cv2.imshow('frame', cam.grab_frame())

# with CameraStreamer(0) as stream:
#     while cv2.waitKey(1) != 27:
#         # frame = np.array(stream.frame_shared_memory).reshape(stream.shape).astype(np.uint8)
#         # frame = np.ctypeslib.as_array(stream.frame_shared_memory.get_obj()).reshape(stream.shape)
#         frame = stream._shared_frame_to_ndarray()
#         cv2.imshow('frame', frame)
#         print(stream._fps.value)
#         pass

# player = User(0)
# player.show_player()
#
# while True:
#     pass

g = Game(User(0), DummyCpuPlayer(), 10)
for i in range(3):
    g.start_game()
    pass

g.end_game()

