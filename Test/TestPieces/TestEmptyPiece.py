import unittest
from Board.ChessBoard import ChessBoard
from Pieces.EmptyPiece import EmptyPiece
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


class TestEmptyPiece(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()

    def test_GetValidMoves_BishopInMiddle_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put an empty piece in middle
        emptpyPiece = EmptyPiece(BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(emptpyPiece)

        expectedValidMoves = []

        validMoves = emptpyPiece.GetValidMoves(self.chessBoard, False)
        self.assertEqual(validMoves, expectedValidMoves)
