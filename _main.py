import numpy as np

from src.camera import CameraStreamer
from src.gesture import AiDetector, Gesture, GestureBattle
from src.player import ImageHub
import cv2
import time

class _User :

    def __init__(self):
        self.graph_buffer = None
        self._image_hub = ImageHub()

    def show(self, gesture, cfd, frame):
        gesture_image = self._image_hub[gesture]

        canvas = frame.copy()

        h, w, _ = canvas.shape
        gh, gw, _ = gesture_image.shape

        if self.graph_buffer is None:
            self.graph_buffer = np.zeros([w-gw, 3])

        status_bar = np.zeros([gh, w, 3], np.uint8)
        canvas = np.concatenate([canvas, status_bar], axis=0)

        canvas[h:, 0:gw, :] = gesture_image

        self.graph_buffer = np.roll(self.graph_buffer, -2, axis=0)
        self.graph_buffer[-1, :] = cfd
        self.graph_buffer[-2, :] = cfd

        chart_colors = [
            (0, 0, 255),
            (0, 255, 0),
            (255, 0, 0),
            (160, 160, 160)
        ]
        for idx in range(self.graph_buffer.shape[0]-1):
            col_prev = idx
            col_next = col_prev + 1
            for c in range(3):
                value_prev = h-int(self.graph_buffer[col_prev, c]*gh)+gh
                value_next = h-int(self.graph_buffer[col_next, c]*gh)+gh
                cv2.line(canvas, (col_prev+gw, value_prev), (col_next+gw, value_next),
                         chart_colors[c], thickness=1)
            # canvas[]
        return canvas


ai_gesture = AiDetector()
user = _User()
hub = ImageHub()
with CameraStreamer(0) as cam:
    for i in range(10):
        start = time.time()
        gesture_time = start+1
        cpu_gesture = Gesture(int(np.random.uniform(0, 3)))
        while time.time() < start + 5:
            frame = cam.frame
            user_gesture, ucfd = ai_gesture.recognize(frame)
            if time.time() > gesture_time:
                gesture_time = time.time()+1
                cpu_gesture = Gesture(int(np.random.uniform(0, 3)))

            canvas = user.show(user_gesture, ucfd, frame)

            cv2.imshow('User', canvas)
            cv2.imshow('CPU', hub[cpu_gesture])
            cv2.waitKey(1)

            print(user_gesture, cpu_gesture)


        results = np.concatenate([hub[user_gesture], hub[cpu_gesture]], axis=1)
        canvas = np.zeros([230, 380, 3], np.uint8)

        result = user_gesture.compare(cpu_gesture)

        cv2.putText(canvas, f'Player1', (0, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 3)
        if result == GestureBattle.WIN:
            cv2.putText(canvas, 'WIN', (100, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (40, 255, 40), 3)
        if result == GestureBattle.LOSS:
            cv2.putText(canvas, 'LOSE', (68, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (40, 40, 255), 3)
        if result == GestureBattle.DRAW:
            cv2.putText(canvas, 'DRAW', (60, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (160, 160, 160), 3)

        results = np.concatenate([results, canvas], axis=0)
        cv2.destroyAllWindows()
        cv2.imshow('Result', results)
        if cv2.waitKey() == 27:
            exit(0)

