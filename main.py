import numpy as np
import cv2

from src.gesture import CvGestureDetector
from src.camera import UsbCamReader, CameraStreamer
from src.player import DummyCpuPlayer

print('Hello, world!')

g = CvGestureDetector()

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

player = DummyCpuPlayer()
player.show_player()
while cv2.waitKey(1):
    pass
