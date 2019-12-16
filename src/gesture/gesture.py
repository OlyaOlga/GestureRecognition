from enum import IntEnum


class GestureBattle(IntEnum):
    WIN = 0,
    LOSS = 1,
    DRAW = 2


class Gesture(IntEnum):
    ROCK = 0,
    PAPER = 1,
    SCISSOR = 2
    NOTHING = 3,

    def compare(self, other):
        if self == other:
            return GestureBattle.DRAW

        if self == Gesture.NOTHING or other == Gesture.NOTHING:
            return GestureBattle.DRAW

        if self == Gesture.SCISSOR and other == Gesture.ROCK:
            return GestureBattle.LOSS

        if self == Gesture.SCISSOR and other == Gesture.PAPER:
            return GestureBattle.WIN

        if self == Gesture.PAPER and other == Gesture.SCISSOR:
            return GestureBattle.LOSS

        if self == Gesture.PAPER and other == Gesture.ROCK:
            return GestureBattle.WIN

        if self == Gesture.ROCK and other == Gesture.PAPER:
            return GestureBattle.LOSS

        if self == Gesture.ROCK and other == Gesture.SCISSOR:
            return GestureBattle.WIN



