import time
import multiprocessing as mp
import ctypes

import numpy as np
import cv2

from src.player import Player
from src.gesture import Gesture, GestureBattle


class Game:

    def __init__(self, player1: Player, player2: Player, delay_choice: int):
        self.player1 = player1
        self.player2 = player2
        self.delay_choice = delay_choice

        self.gestures1 = []
        self.gestures2 = []

        self.player1gesture = None
        self.player2gesture = None

        self.ended = False

    def __del__(self):
        if not self.ended:
            self.end_game()

    def start_game(self):

        time.sleep(self.delay_choice)

        gesture1, cfd = self.player1.get_gesture()
        gesture2, cfd = self.player2.get_gesture()

        result = gesture1.compare(gesture2)

        self.gestures1.append(gesture1)
        self.gestures2.append(gesture2)

        # self.player1.hide_player()
        # self.player2.hide_player()
        start = time.time()
        while time.time() < start+self.delay_choice:
            print('show ', time.time())
            self.player1.show_async()
            self.player2.show_async()

        result1 = gesture1.compare(gesture2)
        result2 = gesture2.compare(gesture1)

        self.player1gesture = gesture1
        self.player2gesture = gesture2

        print(f'Player1: {result1.name} | Player2 {result2.name}')


        return gesture1, gesture2, result

    def _show(self, img):
        cv2.imshow('test', img)
        cv2.waitKey(1000)

    @staticmethod
    def plot_player(no: int, result: GestureBattle):
        canvas = np.zeros([230, 380, 3], np.uint8)

        cv2.putText(canvas, f'Player{no}', (0, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 3)
        if result == GestureBattle.WIN:
            cv2.putText(canvas, 'WIN', (100, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (40, 255, 40), 3)
        if result == GestureBattle.LOSS:
            cv2.putText(canvas, 'LOSE', (68, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (40, 40, 255), 3)
        if result == GestureBattle.DRAW:
            cv2.putText(canvas, 'DRAW', (60, 200), cv2.FONT_HERSHEY_COMPLEX, 3, (160, 160, 160), 3)

        return canvas

    def end_game(self):
        # self._show_thread.terminate()
        self.player1.__del__()
        self.player2.__del__()
        self.ended = True

    # def _plot_canvas(self, number):
    #     canvas = np.zeros([150, 150, 3])
    #     cv2.putText(canvas, f'{number}', (20, 20), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 5)
    #     return canvas

    # def _show_async(self):
    #     while True:
    #         canvas = self._plot_canvas(4)
    #
    #         cv2.imshow('Results', canvas)
    #         cv2.waitKey()
            # print(self._results_player1)
            # time.sleep(0.5)
            # wins = 0
            # for i in range(wins):
            #     if s
