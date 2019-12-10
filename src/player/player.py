import abc

from src.gesture import Gesture


class Player(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_result_of_previous_game(self, is_win: bool) -> None:
        pass

    @abc.abstractmethod
    def get_gesture(self) -> Gesture:
        pass

    @abc.abstractmethod
    def show_player(self):
        pass
