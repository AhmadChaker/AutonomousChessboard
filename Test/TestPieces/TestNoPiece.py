import unittest
from Board.ChessBoard import ChessBoard
from Pieces.NoPiece import NoPiece
from Miscellaneous.BoardPoints import BoardPoints


class TestNoPiece(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()

    def test_GetValidMoves_BishopInMiddle_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put an empty piece in middle
        noPiece = NoPiece(BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(noPiece)

        expectedValidMoves = []

        validMoves = noPiece.GetValidMoves(self.chessBoard, False)
        self.assertEqual(validMoves, expectedValidMoves)
