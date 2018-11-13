import unittest
from Board.ChessBoard import ChessBoard
from Pieces.Knight import Knight
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


class TestKnight(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()

    def test_GetValidMoves_BishopInMiddle_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put a new knight in middle
        knight = Knight(TeamEnum.White, BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(knight)

        expectedValidMoves = []

        # Top right
        expectedValidMoves.append(BoardPoints(5, 4))
        expectedValidMoves.append(BoardPoints(4, 5))

        # Top left
        expectedValidMoves.append(BoardPoints(1, 4))
        expectedValidMoves.append(BoardPoints(2, 5))

        # Bottom left
        expectedValidMoves.append(BoardPoints(1, 2))
        expectedValidMoves.append(BoardPoints(2, 1))

        # Bottom right
        expectedValidMoves.append(BoardPoints(4, 1))
        expectedValidMoves.append(BoardPoints(5, 2))

        expectedValidMoves.sort()

        validMoves = knight.GetValidMoves(self.chessBoard, False)
        validMoves.sort()
        self.assertEqual(validMoves, expectedValidMoves)
