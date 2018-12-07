import unittest
from Board.History import History
from Board.ChessBoard import ChessBoard
from Pieces.NoPiece import NoPiece
from Miscellaneous.BoardPoints import BoardPoints


class TestNoPiece(unittest.TestCase):

    def setUp(self):
        history = History()
        self.chessBoard = ChessBoard(history)

    def test_GetValidMoves_BishopInMiddle_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put an empty piece in middle
        noPiece = NoPiece(BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(noPiece)

        expectedValidMoves = []

        validMoves = noPiece.GetValidMoves(self.chessBoard, False)
        self.assertEqual(validMoves, expectedValidMoves)
