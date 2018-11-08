import sys
import Board.Constants
from Miscellaneous.Points import Points


# General points, this covers direction vectors as well as chess board and array coordinates
class BoardPoints(Points):

    def __init__(self, x, y):
        if 0 <= x < len(Board.Constants.ALPHABETICAL_BOARD_ORDINATES) and 0 <= y < len(Board.Constants.NUMERICAL_BOARD_ORDINATES):
            Points.__init__(self, x, y)
            self.__xBoard = Board.Constants.ALPHABETICAL_BOARD_ORDINATES[x]
            self.__yBoard = Board.Constants.NUMERICAL_BOARD_ORDINATES[y]
            return

        Points.__init__(self, -sys.maxsize, -sys.maxsize)
        self.__xBoard = self.__yBoard = -sys.maxsize

    def __eq__(self, other):
        return self.GetX() == other.GetX() and \
               self.GetY() == other.GetY() and \
               self.GetXBoard() == other.GetXBoard() and \
               self.GetYBoard() == other.GetYBoard()

    def __lt__(self, other):
        if self.GetX() == other.GetX():
            return self.GetY() < other.GetY()

        return self.GetX() < other.GetX()

    def ToString(self):
        return "Array:(" + str(self.GetX()) + "," + str(self.GetY()) + "), Board:(" + \
                    str(self.GetXBoard()) + "," + str(self.GetYBoard()) + ")"

    def GetXBoard(self):
        return self.__xBoard

    def GetYBoard(self):
        return self.__yBoard


BOARD_POINTS_UNDEFINED = BoardPoints(-sys.maxsize, -sys.maxsize)
