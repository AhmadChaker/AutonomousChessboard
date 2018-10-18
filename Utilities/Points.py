import sys
import Board.Constants


class Points:

    def __init__(self, x, y):
        self.__xArray = x
        self.__yArray = y
        self.__xBoard = Board.Constants.ALPHABETICAL_BOARD_ORDINATES[self.__xArray] \
            if 0 <= self.__xArray < len(Board.Constants.ALPHABETICAL_BOARD_ORDINATES) else -1
        self.__yBoard = Board.Constants.NUMERICAL_BOARD_ORDINATES[self.__yArray] \
            if 0 <= self.__yArray < len(Board.Constants.NUMERICAL_BOARD_ORDINATES) else -1

    def __eq__(self, other):
        return self.__xArray == other.__xArray and self.__yArray == other.__yArray

    def ToString(self):
        return "Array:(" + str(self.__xArray) + "," + str(self.__yArray) + "), Board:(" + \
                    str(self.__xBoard) + "," + str(self.__yBoard) + ")"

    def GetX(self):
        return self.__xArray

    def GetY(self):
        return self.__yArray


POINTS_UNDEFINED = Points(-sys.maxsize, -sys.maxsize)
