import sys
import Board.Constants


class Points:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y

    def ToString(self):
        strCoords = "Array:(" + str(self.__x) + "," + str(self.__y) + "), "
        if 0 <= self.__x < len(Board.Constants.ALPHABETICAL_BOARD_ORDINATES) and \
                0 <= self.__y < len(Board.Constants.NUMERICAL_BOARD_ORDINATES):
            boardCoords = "Board:(" + Board.Constants.ALPHABETICAL_BOARD_ORDINATES[self.__x] \
                          + "," + Board.Constants.NUMERICAL_BOARD_ORDINATES[self.__y] + ")"
            strCoords += boardCoords
        return strCoords

    def GetX(self):
        return self.__x

    def GetY(self):
        return self.__y


POINTS_UNDEFINED = Points(-sys.maxsize, -sys.maxsize)
