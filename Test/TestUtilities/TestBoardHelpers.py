import unittest
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Miscellaneous.BoardPoints import BoardPoints
from Board.Constants import TeamEnum
from Board.History import History
from Board.Movement import Movement
from Board.ChessBoard import ChessBoard
from Pieces.Constants import PieceEnums
from Pieces.King import King
from Pieces.Bishop import Bishop
from Pieces.Pawn import Pawn


class TestBoardHelpers(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        history = History()
        self.chessBoard = ChessBoard(history)

    # region GetOpposingTeam Tests

    def test_GetOpposingTeam_NoTeam_ReturnsNoTeam(self):
        initialTeam = TeamEnum.NoTeam
        expectedTeam = TeamEnum.NoTeam
        self.assertEqual(BoardHelpers.GetOpposingTeam(initialTeam), expectedTeam)

    def test_GetOpposingTeam_WhiteTeam_ReturnsBlack(self):
        initialTeam = TeamEnum.White
        expectedTeam = TeamEnum.Black
        self.assertEqual(BoardHelpers.GetOpposingTeam(initialTeam), expectedTeam)

    def test_GetOpposingTeam_BlackTeam_ReturnsWhite(self):
        initialTeam = TeamEnum.Black
        expectedTeam = TeamEnum.White
        self.assertEqual(BoardHelpers.GetOpposingTeam(initialTeam), expectedTeam)

    # endregion

    # region IsDrawByInsufficientPieces Tests

    def test_IsDrawByInsufficientPieces_BothTeamsHaveManyPieces_ReturnsFalse(self):
        initialTeam = TeamEnum.White
        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertFalse(isDraw)

    def test_IsDrawByInsufficientPieces_OnlyKingsRemaining_ReturnsTrue(self):
        initialTeam = TeamEnum.White

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(3,3)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(5,5)))

        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertTrue(isDraw)

    def test_IsDrawByInsufficientPieces_WhiteKingAndBishopVsBlackKing_ReturnsTrue(self):
        initialTeam = TeamEnum.White

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(3, 3)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(5, 5)))

        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertTrue(isDraw)

    def test_IsDrawByInsufficientPieces_BlackKingAndBishopVsWhiteKing_ReturnsTrue(self):
        initialTeam = TeamEnum.Black

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(3, 3)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(5, 5)))

        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertTrue(isDraw)

    def test_IsDrawByInsufficientPieces_KingAndBishopVsKingAndBishop_BishopsOnSameColour_ReturnsTrue(self):
        initialTeam = TeamEnum.Black

        self.chessBoard.RemoveAllPieces()
        # Bishops on same color
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(3, 3)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(5, 5)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.White, BoardPoints(2, 0)))

        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertTrue(isDraw)

    def test_IsDrawByInsufficientPieces_KingAndBishopVsKingAndBishop_BishopsDifferentColour_ReturnsTrue(self):
        initialTeam = TeamEnum.Black

        self.chessBoard.RemoveAllPieces()
        # Bishops on same color
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(3, 3)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(5, 5)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.White, BoardPoints(1, 0)))

        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertFalse(isDraw)

    def test_IsDrawByInsufficientPieces_WhiteKingVsBlackKingAndPawn_ReturnsFalse(self):
        initialTeam = TeamEnum.Black

        self.chessBoard.RemoveAllPieces()
        # Bishops on same color
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(3, 3)))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(5, 5)))

        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertFalse(isDraw)

    def test_IsDrawByInsufficientPieces_BlackKingVsWhiteKingAndPawn_ReturnsFalse(self):
        initialTeam = TeamEnum.Black

        self.chessBoard.RemoveAllPieces()
        # Bishops on same color
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(3, 3)))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(5, 5)))

        isDraw = BoardHelpers.IsDrawByInsufficientPieces(self.chessBoard, initialTeam)
        self.assertFalse(isDraw)

    # endregion

    # region IsDrawBySeventyFiveMovesEachRule Tests

    def test_IsDrawBySeventyFiveMovesEachRule_LessThan75MovesEach_ReturnsFalse(self):
        history = History()
        history.AppendMovement(Movement(TeamEnum.White,
                                        PieceEnums.Pawn,
                                        PieceEnums.Queen,
                                        BoardPoints(1,1),
                                        BoardPoints(2,2),
                                        None))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertFalse(isDraw)

    def test_IsDrawBySeventyFiveMovesEachRule_MoreThanXMoves_CaptureMade_ReturnsFalse(self):
        history = History()
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            history.AppendMovement(Movement(TeamEnum.White,
                                            PieceEnums.Knight,
                                            PieceEnums.Queen,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            None))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertFalse(isDraw)

    def test_IsDrawBySeventyFiveMovesEachRule_MoreThanXMoves_PawnMoves_ReturnsFalse(self):
        history = History()
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            history.AppendMovement(Movement(TeamEnum.White,
                                            PieceEnums.Pawn,
                                            PieceEnums.NoPiece,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            None))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertFalse(isDraw)

    def test_IsDrawBySeventyFiveMovesEachRule_MoreThanXMoves_NoCaptureOrPawnMoves_ReturnsTrue(self):
        history = History()
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            history.AppendMovement(Movement(TeamEnum.White,
                                            PieceEnums.Knight,
                                            PieceEnums.NoPiece,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            None))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertTrue(isDraw)

    # endregion

    # region IsDraw Tests

    def test_IsDraw_OpposingTeamNoMovesAndNotInCheck_ReturnsTrue(self):
        opposingTeam = TeamEnum.Black

        # White team haas no legal moves and is not in check
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.White, BoardPoints(0, 5)))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(0, 6)))

        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.White, BoardPoints(1, 2)))
        isDraw = BoardHelpers.IsDraw(self.chessBoard, opposingTeam)
        self.assertTrue(isDraw)

    def test_IsDraw_IsDrawBy75MovesEach_ReturnsTrue(self):
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            self.chessBoard.AppendToHistory(Movement(TeamEnum.White,
                                            PieceEnums.Knight,
                                            PieceEnums.NoPiece,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            None))
        currentTeam = TeamEnum.White

        isDraw = BoardHelpers.IsDraw(self.chessBoard, currentTeam)
        self.assertTrue(isDraw)

    def test_IsDraw_IsDrawByInsufficientPieces_ReturnsTrue(self):
        currentTeam = TeamEnum.White

        # Only Kings on the board
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(2, 0)))

        isDraw = BoardHelpers.IsDraw(self.chessBoard, currentTeam)
        self.assertTrue(isDraw)

    def test_IsDraw_NoDraw_ReturnsFalse(self):
        currentTeam = TeamEnum.White

        isDraw = BoardHelpers.IsDraw(self.chessBoard, currentTeam)
        self.assertFalse(isDraw)

    # endregion

    # region GetPiecesByPieceType tests

    def test_GetPiecesByPieceType_NoPiecesOfType_ReturnsEmpty(self):
        self.chessBoard.RemoveAllPieces()
        actualPieces = BoardHelpers.GetPieceByPieceType(self.chessBoard, PieceEnums.Pawn, TeamEnum.White)
        expectedPieces = []
        self.assertEqual(actualPieces, expectedPieces)

    def test_GetPiecesByPieceType_TwoWhitePieces_ReturnsTheTwo(self):
        actualPieces = BoardHelpers.GetPieceByPieceType(self.chessBoard, PieceEnums.Bishop, TeamEnum.White)
        expectedPieces = [self.chessBoard.GetPieceAtCoordinate(BoardPoints(2, 0)),
                          self.chessBoard.GetPieceAtCoordinate(BoardPoints(5, 0))]
        self.assertEqual(len(actualPieces), len(expectedPieces))
        for i in range(len(actualPieces)):
            self.assertEqual(actualPieces[i].GetPieceEnum(), expectedPieces[i].GetPieceEnum())
            self.assertEqual(actualPieces[i].GetTeam(), expectedPieces[i].GetTeam())

    def test_GetPiecesByPieceType_TwoBlackPieces_ReturnsTheTwo(self):
        actualPieces = BoardHelpers.GetPieceByPieceType(self.chessBoard, PieceEnums.Rook, TeamEnum.Black)
        expectedPieces = [self.chessBoard.GetPieceAtCoordinate(BoardPoints(0, 7)),
                          self.chessBoard.GetPieceAtCoordinate(BoardPoints(7, 7))]
        self.assertEqual(len(actualPieces), len(expectedPieces))
        for i in range(len(actualPieces)):
            self.assertEqual(actualPieces[i].GetPieceEnum(), expectedPieces[i].GetPieceEnum())
            self.assertEqual(actualPieces[i].GetTeam(), expectedPieces[i].GetTeam())

    # endregion

    # region GetTeamPieceCounts Tests

    def test_GetTeamPieceCounts_AllPiecesThere(self):
        actualPieceCount = BoardHelpers.GetTeamPieceCounts(self.chessBoard, TeamEnum.White)
        expectedPieceCount = 16
        self.assertEqual(actualPieceCount, expectedPieceCount)

    def test_GetTeamPieceCounts_OnlyOneBlackPiece_ReturnsOne(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(0,0)))
        actualBlackPieceCount = BoardHelpers.GetTeamPieceCounts(self.chessBoard, TeamEnum.Black)
        expectedBlackPieceCount = 1
        self.assertEqual(actualBlackPieceCount, expectedBlackPieceCount)

        actualWhitePieceCount = BoardHelpers.GetTeamPieceCounts(self.chessBoard, TeamEnum.White)
        expectedWhitePieceCount = 0
        self.assertEqual(actualWhitePieceCount, expectedWhitePieceCount)

    # endregion

    # region IsInCheck tests

    def test_IsInCheck_NotInCheck_ReturnsFalse(self):
        isInCheck = BoardHelpers.IsInCheck(self.chessBoard, TeamEnum.Black)
        self.assertFalse(isInCheck)

    def test_IsInCheck_InCheck_ReturnsTrue(self):
        # Black King in check against White Bishop
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(2, 2)))
        isInCheck = BoardHelpers.IsInCheck(self.chessBoard, TeamEnum.White)
        self.assertTrue(isInCheck)

    # endregion

    # region IsInCheckmate tests

    def test_IsInCheckMate_NoValidMovesButNotInCheck_ReturnsFalse(self):

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(2, 3)))
        isInCheckMate = BoardHelpers.IsInCheckMate(self.chessBoard, TeamEnum.White)
        self.assertFalse(isInCheckMate)

    def test_IsInCheckMate_InCheckButHasValidMoves_ReturnsFalse(self):

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(2, 2)))
        isInCheckMate = BoardHelpers.IsInCheckMate(self.chessBoard, TeamEnum.White)
        self.assertFalse(isInCheckMate)

    def test_IsInCheckMate_InCheckAndHasNoValidMoves_ReturnsTrue(self):

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(2, 2)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(1, 2)))
        isInCheckMate = BoardHelpers.IsInCheckMate(self.chessBoard, TeamEnum.White)
        self.assertTrue(isInCheckMate)

    # endregion
