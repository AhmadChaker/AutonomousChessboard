import unittest
from Board.ChessBoard import ChessBoard
from Pieces.King import King
from Pieces.Rook import Rook
from Pieces.NoPiece import NoPiece
from Board.Constants import TeamEnum
from Board.History import History
from Miscellaneous.BoardPoints import BoardPoints
from Utilities.MoveHelpers import MoveHelpers


class TestKing(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()
        MoveHelpers.Update(History())

    def tearDown(self):
        MoveHelpers.Update(None)

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

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

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

    def test_CanCastle_CanNeverCastleSetTrue_ReturnsFalse(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4,0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.SetCanCastleInTheFuture(False)

        canCastle = king.CanCastle(self.chessBoard, False)

        self.assertFalse(canCastle)

    def test_CanCastle_KingHasMoved_ReturnsFalse(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4,0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # Use ForceMove instead of Move so that short circuiting does not occur
        king.ForceMove(BoardPoints(3, 0))
        king.ForceMove(BoardPoints(4, 0))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanCastleInTheFuture())

    def test_CanCastle_NoRooks_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # Remove rooks
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(7, 0)))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanCastleInTheFuture())

    def test_CanCastle_NoRookCanCastleAndCannotCastleInFuture_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        leftRook = self.chessBoard.GetPieceAtCoordinate((BoardPoints(0, 0)))
        leftRook.Move(self.chessBoard, BoardPoints(1, 0))
        leftRook.Move(self.chessBoard, BoardPoints(0, 0))

        rightRook = self.chessBoard.GetPieceAtCoordinate((BoardPoints(7, 0)))
        rightRook.Move(self.chessBoard, BoardPoints(6, 0))
        rightRook.Move(self.chessBoard, BoardPoints(7, 0))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanCastleInTheFuture())

    def test_CanCastle_BothRooksCanCastle_ReturnsTrue(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertTrue(canCastle)
        self.assertTrue(king.CanCastleInTheFuture())

    def test_CanCastle_OnlyLeftRookCanCastle_ReturnsTrue(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))

        # comment out below so that only left rook can castle
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertTrue(canCastle)
        self.assertTrue(king.CanCastleInTheFuture())

    # endregion

    # region GetCastleMoves tests

    def test_GetCastleMoves_CantCastle_ReturnsEmpty(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Don't remove any pieces between king and rooks
        castleMoves = king.GetCastleMoves(self.chessBoard, False)
        self.assertEqual(castleMoves, [])

    def test_GetCastleMoves_LeftAndRightCastlePossible_ReturnsMoves(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove pieces between king and rooks
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        castleMoves = king.GetCastleMoves(self.chessBoard, False)
        castleMoves.sort()

        expectedMoves = [BoardPoints(2, 0), BoardPoints(6, 0)]
        expectedMoves.sort()

        self.assertEqual(castleMoves, expectedMoves)

    def test_GetCastleMoves_OnlyRightCastlePossible_ReturnsMoves(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove pieces between king and rooks
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        castleMoves = king.GetCastleMoves(self.chessBoard, False)
        castleMoves.sort()

        expectedMoves = [BoardPoints(6, 0)]
        expectedMoves.sort()

        self.assertEqual(castleMoves, expectedMoves)
    # endregion
