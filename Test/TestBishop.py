import unittest
import Board.Constants
from Pieces.EmptyPiece import EmptyPiece
from Pieces.Bishop import Bishop
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


class TestBishop(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.__board = [None] * Board.Constants.MAXIMUM_X_SQUARES
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            # for each y line
            self.__board[xIndex] = [None] * Board.Constants.MAXIMUM_Y_SQUARES

        for yIndex in range(Board.Constants.MAXIMUM_Y_SQUARES):
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                self.__board[xIndex][yIndex] = EmptyPiece(BoardPoints(xIndex, yIndex))

    def test_GetValidMoves_BishopInMiddle_ReturnsValidMoves(self):

        bishop = Bishop(TeamEnum.White, BoardPoints(3, 3))
        self.__board[3][3] = bishop

        expectedValidMoves = []

        # Top right
        expectedValidMoves.append(BoardPoints(4, 4))
        expectedValidMoves.append(BoardPoints(5, 5))
        expectedValidMoves.append(BoardPoints(6, 6))
        expectedValidMoves.append(BoardPoints(7, 7))

        # Top left
        expectedValidMoves.append(BoardPoints(2, 4))
        expectedValidMoves.append(BoardPoints(1, 5))
        expectedValidMoves.append(BoardPoints(0, 6))

        # Bottom left
        expectedValidMoves.append(BoardPoints(2, 2))
        expectedValidMoves.append(BoardPoints(1, 1))
        expectedValidMoves.append(BoardPoints(0, 0))

        # Bottom right
        expectedValidMoves.append(BoardPoints(4, 2))
        expectedValidMoves.append(BoardPoints(5, 1))
        expectedValidMoves.append(BoardPoints(6, 0))

        expectedValidMoves.sort()

        validMoves = bishop.GetValidMoves(self.__board, False)
        validMoves.sort()
        self.assertEqual(validMoves, expectedValidMoves)
