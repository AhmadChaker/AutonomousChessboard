import unittest
from Board.ChessBoard import ChessBoard
from Pieces.King import King
from Pieces.Rook import Rook
from Pieces.EmptyPiece import EmptyPiece
from Board.Constants import TeamEnum
from Board.History import History
from Miscellaneous.BoardPoints import BoardPoints
from Utilities.BoardHelpers import BoardHelpers


class TestKing(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()
        BoardHelpers.UpdateVariables(History())

    def tearDown(self):
        BoardHelpers.UpdateVariables(None)

    # region GetValidMoves

    def test_GetValidMovesNoCastle_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put a new king in middle
        king = King(TeamEnum.White, BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(king)

        expectedValidMoves = []

        # Top right
        expectedValidMoves.append(BoardPoints(4, 4))

        # Top
        expectedValidMoves.append(BoardPoints(3, 4))

        # Top left
        expectedValidMoves.append(BoardPoints(2, 4))

        # Left
        expectedValidMoves.append(BoardPoints(2, 3))

        # Bottom left
        expectedValidMoves.append(BoardPoints(2, 2))

        # Bottom
        expectedValidMoves.append(BoardPoints(3, 2))

        # Bottom right
        expectedValidMoves.append(BoardPoints(4, 2))

        # Right
        expectedValidMoves.append(BoardPoints(4, 3))

        expectedValidMoves.sort()

        validMoves = king.GetValidMoves(self.chessBoard, False)
        validMoves.sort()
        self.assertEqual(validMoves, expectedValidMoves)

    def test_GetValidMovesCastleAllowed_ReturnsAllValidMoves(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4,0))

        # Remove major pieces around King to allow castling

        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(6, 0)))

        expectedValidMoves = [BoardPoints(3, 0),
                              BoardPoints(2, 0),
                              BoardPoints(5, 0),
                              BoardPoints(6, 0)]
        expectedValidMoves.sort()

        validMoves = king.GetValidMoves(self.chessBoard, False)
        validMoves.sort()
        self.assertEqual(validMoves, expectedValidMoves)

    # endregion

    # region CanCastle tests

    def test_CanCastle_CanNeverCastleSetTrue_RetursnFalse(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4,0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(6, 0)))

        king.SetCanNeverCastleThisPiece(True)

        canCastle = king.CanCastle(self.chessBoard, False)

        self.assertFalse(canCastle)

    def test_CanCastle_KingHasMoved_ReturnsFalse(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4,0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(6, 0)))

        # Use ForceMove instead of Move so that short circuiting does not occur
        king.ForceMove(BoardPoints(3, 0))
        king.ForceMove(BoardPoints(4, 0))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertTrue(king.GetCanNeverCastleThisPiece())

    def test_CanCastle_NoRooks_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(6, 0)))

        # Remove rooks
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(7, 0)))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertTrue(king.GetCanNeverCastleThisPiece())

    # endregion
