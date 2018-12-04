import unittest
from Board.ChessBoard import ChessBoard
from Pieces.King import King
from Pieces.NoPiece import NoPiece
from Board.Constants import TeamEnum
from Board.History import History
from Miscellaneous.BoardPoints import BoardPoints
from Utilities.MoveHelpers import MoveHelpers


class TestKing(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()

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

    # region CanCastleBaseChecks tests

    def test_CanCastleBaseChecks_CanCastleInFutureIsFalse_ReturnsFalse(self):

        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4,0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.SetCanCastleInTheFuture(False)

        canCastle = king.CanCastleBaseChecks(self.chessBoard)

        self.assertFalse(canCastle)
        # Verify queen side and king side castling are also forbidden
        self.assertFalse(king.CanCastleInTheFuture())
        self.assertFalse(king.CanKingSideCastleInTheFuture())
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    def test_CanCastleBaseChecks_KingHasMoved_ReturnsFalse(self):

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

        canCastle = king.CanCastleBaseChecks(self.chessBoard)
        self.assertFalse(canCastle)
        # Verify queen side and king side castling are also forbidden
        self.assertFalse(king.CanCastleInTheFuture())
        self.assertFalse(king.CanKingSideCastleInTheFuture())
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    def test_CanCastleBaseChecks_NoRooks_ReturnsFalse(self):
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

        canCastle = king.CanCastleBaseChecks(self.chessBoard)
        self.assertFalse(canCastle)
        # Verify queen side and king side castling are also forbidden
        self.assertFalse(king.CanCastleInTheFuture())
        self.assertFalse(king.CanKingSideCastleInTheFuture())
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    # endregion

    # region CanCastle

    def test_CanCastle_CantQueenSideCastleAndCantKingSideCastle_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanCastle_CanQueenSideCastleCantKingSideCastle_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    def test_CanCastle_CantQueenSideCastleCanKingSideCastle_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    # endregion

    # region CanKingSideCastle tests

    def test_CanKingSideCastle_CanKingSideCastleInFutureIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.SetCanKingSideCastleInTheFuture(False)

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanKingSideCastleInTheFuture())

    def test_CanKingSideCastle_CanCastleBaseChecksIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # Enforce no rooks so that base check fails
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(7,0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(0,0)))

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanKingSideCastleInTheFuture())

    def test_CanKingSideCastle_NoKingSideRook_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # remove rook on the right
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(7,0)))

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanKingSideCastleInTheFuture())

    def test_CanKingSideCastle_RookHasCannotCastleFlagSet_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # get king side rook
        rook = self.chessBoard.GetPieceAtCoordinate(BoardPoints(7,0))
        rook.SetCanCastleInTheFuture(False)

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanKingSideCastleInTheFuture())

    def test_CanKingSideCastle_RookCannotCastle_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # Stop castling on king side
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanKingSideCastle_ValidConditions_ReturnsTrue(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    # endregion

    # region CanQueenSideCastle tests

    def test_CanQueenSideCastle_CanQueenSideCastleInFutureIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.SetCanQueenSideCastleInTheFuture(False)

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    def test_CanQueenSideCastle_CanCastleBaseChecksIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # Enforce no rooks so that base check fails
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(7,0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(0,0)))

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    def test_CanQueenSideCastle_NoQueenSideRook_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # remove rook on the left
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(0,0)))

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    def test_CanQueenSideCastle_RookHasCannotCastleFlagSet_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        # get king side rook
        rook = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,0))
        rook.SetCanCastleInTheFuture(False)

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    def test_CanQueenSideCastle_RookCannotCastle_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Stop castling on queen side
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanQueenSideCastle_ValidConditions_ReturnsTrue(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    # endregion

    # region SetCanCastleInTheFuture tests

    def test_SetCanCastleInTheFuture_FlagSetTrue_BothQueenAndKingSideFlagsSetToTrue(self):
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))
        king.SetCanCastleInTheFuture(True)

        self.assertTrue(king.CanKingSideCastleInTheFuture())
        self.assertTrue(king.CanQueenSideCastleInTheFuture())

    def test_SetCanCastleInTheFuture_FlagSetFalse_BothQueenAndKingSideFlagsSetToFalse(self):
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))
        king.SetCanCastleInTheFuture(False)

        self.assertFalse(king.CanKingSideCastleInTheFuture())
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    # endregion

    # region CanCastleInTheFuture tests

    def test_CanCastleInTheFuture_QueenSideFlagTrueKingSideFalse_ReturnsTrue(self):
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))
        king.SetCanKingSideCastleInTheFuture(False)
        king.SetCanQueenSideCastleInTheFuture(True)

        self.assertTrue(king.CanCastleInTheFuture())

        # additional verification of setters
        self.assertFalse(king.CanKingSideCastleInTheFuture())
        self.assertTrue(king.CanQueenSideCastleInTheFuture())

    def test_CanCastleInTheFuture_KingSideFlagTrueQueenSideFalse_ReturnsTrue(self):
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))
        king.SetCanKingSideCastleInTheFuture(True)
        king.SetCanQueenSideCastleInTheFuture(False)

        self.assertTrue(king.CanCastleInTheFuture())

        # additional verification of setters
        self.assertTrue(king.CanKingSideCastleInTheFuture())
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

    def test_CanCastleInTheFuture_KingSideFlagFalseQueenSideFalse_ReturnsTrue(self):
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))
        king.SetCanKingSideCastleInTheFuture(False)
        king.SetCanQueenSideCastleInTheFuture(False)

        self.assertFalse(king.CanCastleInTheFuture())

        # additional verification of setters
        self.assertFalse(king.CanKingSideCastleInTheFuture())
        self.assertFalse(king.CanQueenSideCastleInTheFuture())

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
