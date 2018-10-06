import sys
import Utilities.Constants


class Points:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y

    def ToString(self):
        strCoords = "Array Coords: (X,Y)=(" + str(self.__x) + "," + str(self.__y) + ") "
        if 0 <= self.__x < len(Utilities.Constants.ALPHABETICAL_BOARD_ORDINATES) and \
                0 <= self.__y < len(Utilities.Constants.NUMERICAL_BOARD_ORDINATES):
            boardCoords = "Board Coords: (X,Y)=(" + Utilities.Constants.ALPHABETICAL_BOARD_ORDINATES[self.__x] \
                         + "," + Utilities.Constants.NUMERICAL_BOARD_ORDINATES[self.__y] + ")"
            strCoords += boardCoords
        return strCoords

    def GetX(self):
        return self.__x

    def GetY(self):
        return self.__y


POINTS_UNDEFINED = Points(-sys.maxsize, -sys.maxsize)
