import unittest
from Board.ChessBoard import ChessBoard
from Miscellaneous.Constants import PieceEnums, TeamEnum
from Pieces.King import King
from Pieces.NoPiece import NoPiece
from Board.History import History
from Miscellaneous.BoardPoints import BoardPoints


class TestKing(unittest.TestCase):

    def setUp(self):
        history = History()
        self.chessBoard = ChessBoard(history)

    # region CanPotentiallyCastleInTheFutureBaseCheck tests

    def test_CanPotentiallyCastleInTheFutureBaseCheck_KingHasMoved_ReturnsFalse(self):

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

        canCastle = king.CanPotentiallyCastleInTheFutureBaseCheck(self.chessBoard, PieceEnums.King)
        self.assertFalse(canCastle)

    def test_CanPotentiallyCastleInTheFutureBaseCheck_NoRooks_ReturnsFalse(self):
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

        canCastle = king.CanPotentiallyCastleInTheFutureBaseCheck(self.chessBoard, PieceEnums.King)
        self.assertFalse(canCastle)

    def test_CanPotentiallyCastleInTheFutureBaseCheck_QueenSideRookNotOnStartingCoord_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        QueenSideRook = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,0))
        QueenSideRook.ForceMoveNoHistory(BoardPoints(0,1))
        self.chessBoard.UpdatePieceOnBoard(QueenSideRook)
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(0, 0)))

        canCastle = king.CanPotentiallyCastleInTheFutureBaseCheck(self.chessBoard, PieceEnums.Queen)
        self.assertFalse(canCastle)

    def test_CanPotentiallyCastleInTheFutureBaseCheck_KingSideRookNotOnStartingCoord_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        KingSideRook = self.chessBoard.GetPieceAtCoordinate(BoardPoints(7,0))
        KingSideRook.ForceMoveNoHistory(BoardPoints(7,1))
        self.chessBoard.UpdatePieceOnBoard(KingSideRook)
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(7, 0)))

        canCastle = king.CanPotentiallyCastleInTheFutureBaseCheck(self.chessBoard, PieceEnums.King)
        self.assertFalse(canCastle)

    def test_CanPotentiallyCastleInTheFutureBaseCheck_AllConditionsMet_ReturnsTrue(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        # Remove major pieces around King to allow castling
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanPotentiallyCastleInTheFutureBaseCheck(self.chessBoard, PieceEnums.King)
        self.assertTrue(canCastle)

    # endregion

    # region CanPotentiallyQueenSideCastleInTheFuture Tests

    def test_CanPotentiallyQueenSideCastleInTheFuture_CanCastleQueenSideInFutureSetToFalse_ShortCircuit_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.CanCastleQueenSideInTheFuture = False
        canCastle = king.CanPotentiallyQueenSideCastleInTheFuture(self.chessBoard)
        self.assertFalse(canCastle)

    def test_CanPotentiallyQueenSideCastleInTheFuture_CanPotentiallyCastleBaseCheckIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.ForceMove(BoardPoints(3, 0))
        king.ForceMove(BoardPoints(4, 0))
        canCastle = king.CanPotentiallyQueenSideCastleInTheFuture(self.chessBoard)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanCastleQueenSideInTheFuture)

    def test_CanPotentiallyQueenSideCastleInTheFuture_AllConditionsSatisfied_ReturnsTrue(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanPotentiallyQueenSideCastleInTheFuture(self.chessBoard)
        self.assertTrue(canCastle)

    # endregion

    # region CanQueenSideCastle tests

    def test_CanQueenSideCastle_CanPotentiallyQueenSideCastleIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.CanCastleQueenSideInTheFuture = False
        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanQueenSideCastle_QueenSideRookHasMoved_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        queenSideRook = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,0))
        queenSideRook.ForceMove(BoardPoints(0, 1))
        queenSideRook.ForceMove(BoardPoints(0, 0))

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanQueenSideCastle_AllConditionsMet_ReturnsTrue(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        # self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanQueenSideCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    # endregion

    # region CanPotentiallyKingSideCastleInTheFuture Tests

    def test_CanPotentiallyKingSideCastleInTheFuture_CanCastleKingSideInFutureSetToFalse_ShortCircuit_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.CanCastleKingSideInTheFuture = False
        canCastle = king.CanPotentiallyKingSideCastleInTheFuture(self.chessBoard)
        self.assertFalse(canCastle)

    def test_CanPotentiallyKingSideCastleInTheFuture_CanPotentiallyCastleBaseCheckIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.ForceMove(BoardPoints(3, 0))
        king.ForceMove(BoardPoints(4, 0))
        canCastle = king.CanPotentiallyKingSideCastleInTheFuture(self.chessBoard)
        self.assertFalse(canCastle)
        self.assertFalse(king.CanCastleKingSideInTheFuture)

    def test_CanPotentiallyKingSideCastleInTheFuture_AllConditionsSatisfied_ReturnsTrue(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanPotentiallyKingSideCastleInTheFuture(self.chessBoard)
        self.assertTrue(canCastle)

    # endregion

    # region CanKingSideCastle tests

    def test_CanKingSideCastle_CanPotentiallyKingSideCastleIsFalse_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        king.CanCastleKingSideInTheFuture = False
        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanKingSideCastle_KingSideRookHasMoved_ReturnsFalse(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        kingSideRook = self.chessBoard.GetPieceAtCoordinate(BoardPoints(7,0))
        kingSideRook.ForceMove(BoardPoints(7, 1))
        kingSideRook.ForceMove(BoardPoints(7, 0))

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanKingSideCastle_AllConditionsMet_ReturnsTrue(self):
        # Get King
        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4, 0))

        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(1, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(2, 0)))
        #self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(3, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(NoPiece(BoardPoints(6, 0)))

        canCastle = king.CanKingSideCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    # endregion

    # region CanCastle tests

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
