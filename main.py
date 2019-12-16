import time

import numpy as np
import cv2

from src.gesture import GestureBattle, Gesture
from src.player import DummyCpuPlayer, User, ImageHub
from src.game import Game
import gc
import psutil
import matplotlib.pyplot as plt

print('Hello, world!')

class CpuStats:
    def __init__(self):
        self.c = 1000
        self.cpu_h = [0]*self.c

    def stats(self):
        cpu = psutil.cpu_percent()
        self.cpu_h.append(cpu)
        self.cpu_h = self.cpu_h[1:self.c]
        plt.plot(range(999), self.cpu_h)
        plt.show()


g = Game(User(0), DummyCpuPlayer(), 8)
for i in range(10):
    g.start_game()

    print(g.player1gesture.value)

    hub = ImageHub()
    gesture1 = hub[g.player1gesture]
    gesture2 = hub[g.player2gesture]

    results = np.concatenate([gesture2, gesture1], axis=1)
    canvas = np.zeros([230, 380, 3], np.uint8)

    result = g.player1gesture.compare(g.player2gesture)

    cv2.putText(canvas, f'Player1', (0, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 3)
    if result == GestureBattle.WIN:
        cv2.putText(canvas, 'WIN', (100, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (40, 255, 40), 3)
    if result == GestureBattle.LOSS:
        cv2.putText(canvas, 'LOSE', (68, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (40, 40, 255), 3)
    if result == GestureBattle.DRAW:
        cv2.putText(canvas, 'DRAW', (60, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (160, 160, 160), 3)

    results = np.concatenate([results, canvas], axis=0)

    cv2.imshow('win', results)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

g.end_game()

