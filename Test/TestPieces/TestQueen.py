import unittest
from Board.ChessBoard import ChessBoard
from Pieces.Queen import Queen
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


class TestQueen(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()

    def test_GetValidMoves_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put a new queen in middle
        queen = Queen(TeamEnum.White, BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(queen)

        expectedValidMoves = []

        # Top right
        expectedValidMoves.append(BoardPoints(4, 4))
        expectedValidMoves.append(BoardPoints(5, 5))
        expectedValidMoves.append(BoardPoints(6, 6))
        expectedValidMoves.append(BoardPoints(7, 7))

        # Top
        expectedValidMoves.append(BoardPoints(3, 4))
        expectedValidMoves.append(BoardPoints(3, 5))
        expectedValidMoves.append(BoardPoints(3, 6))
        expectedValidMoves.append(BoardPoints(3, 7))

        # Top left
        expectedValidMoves.append(BoardPoints(2, 4))
        expectedValidMoves.append(BoardPoints(1, 5))
        expectedValidMoves.append(BoardPoints(0, 6))

        # Left
        expectedValidMoves.append(BoardPoints(2, 3))
        expectedValidMoves.append(BoardPoints(1, 3))
        expectedValidMoves.append(BoardPoints(0, 3))

        # Bottom left
        expectedValidMoves.append(BoardPoints(2, 2))
        expectedValidMoves.append(BoardPoints(1, 1))
        expectedValidMoves.append(BoardPoints(0, 0))

        # Bottom
        expectedValidMoves.append(BoardPoints(3, 2))
        expectedValidMoves.append(BoardPoints(3, 1))
        expectedValidMoves.append(BoardPoints(3, 0))

        # Bottom right
        expectedValidMoves.append(BoardPoints(4, 2))
        expectedValidMoves.append(BoardPoints(5, 1))
        expectedValidMoves.append(BoardPoints(6, 0))

        # Right
        expectedValidMoves.append(BoardPoints(4, 3))
        expectedValidMoves.append(BoardPoints(5, 3))
        expectedValidMoves.append(BoardPoints(6, 3))
        expectedValidMoves.append(BoardPoints(7, 3))

        expectedValidMoves.sort()

        validMoves = queen.GetValidMoves(self.chessBoard, False)
        validMoves.sort()
        self.assertEqual(validMoves, expectedValidMoves)
