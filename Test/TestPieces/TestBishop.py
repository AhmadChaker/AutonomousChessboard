import unittest
from Board.ChessBoard import ChessBoard
from Pieces.Bishop import Bishop
from Miscellaneous.Constants import TeamEnum
from Board.History import History
from Miscellaneous.BoardPoints import BoardPoints


class TestBishop(unittest.TestCase):

    def setUp(self):
        history = History()
        self.chessBoard = ChessBoard(history)

    def test_GetValidMoves_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put a new bishop in middle
        bishop = Bishop(TeamEnum.White, BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(bishop)

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

        validMoves = bishop.GetValidMoves(self.chessBoard, False)
        validMoves.sort()
        self.assertEqual(validMoves, expectedValidMoves)
