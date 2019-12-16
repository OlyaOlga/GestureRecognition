from src.camera import CameraStreamer
import cv2

with CameraStreamer(1) as cam:
    for i in range(1000):
        cv2.imshow('Frame', cam.frame)
        cv2.waitKey(1)

    for i in range(1000):
        frame = cam.frame.copy()
        cv2.imshow('Frame', frame)
        cv2.imwrite(f'./data/tmp/frame{i}.png', cv2.resize(frame, (224, 224)))
