import unittest
import Pieces.IBasePiece
import Pieces.Constants
import Board.Constants
import Utilities.CoordinateConverters
import Miscellaneous.BoardPoints
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Board.Constants import TeamEnum
from Board.History import History
from Board.Movement import Movement
from Board.ChessBoard import ChessBoard
from Pieces.Constants import PieceEnums
from Pieces.King import King
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
from Pieces.Pawn import Pawn



class TestBoardHelpers(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()
        BoardHelpers.UpdateVariables(History())

    def tearDown(self):
        BoardHelpers.UpdateVariables(None)

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
        isEnPassant = False
        history.AppendMovement(Movement(TeamEnum.White,
                                        PieceEnums.Pawn,
                                        PieceEnums.Queen,
                                        BoardPoints(1,1),
                                        BoardPoints(2,2),
                                        isEnPassant))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertFalse(isDraw)

    def test_IsDrawBySeventyFiveMovesEachRule_MoreThanXMoves_CaptureMade_ReturnsFalse(self):
        history = History()
        isEnPassant = False
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            history.AppendMovement(Movement(TeamEnum.White,
                                            PieceEnums.Knight,
                                            PieceEnums.Queen,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            isEnPassant))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertFalse(isDraw)

    def test_IsDrawBySeventyFiveMovesEachRule_MoreThanXMoves_PawnMoves_ReturnsFalse(self):
        history = History()
        isEnPassant = False
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            history.AppendMovement(Movement(TeamEnum.White,
                                            PieceEnums.Pawn,
                                            PieceEnums.NoPiece,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            isEnPassant))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertFalse(isDraw)

    def test_IsDrawBySeventyFiveMovesEachRule_MoreThanXMoves_NoCaptureOrPawnMoves_ReturnsTrue(self):
        history = History()
        isEnPassant = False
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            history.AppendMovement(Movement(TeamEnum.White,
                                            PieceEnums.Knight,
                                            PieceEnums.NoPiece,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            isEnPassant))
        isDraw = BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history.GetHistoricalMoves())
        self.assertTrue(isDraw)

    # endregion

    # region IsDraw Tests

    def test_IsDraw_OpposingTeamNoMovesAndNotInCheck_ReturnsTrue(self):
        history = History()
        currentTeam = TeamEnum.White

        # White team haas no legal moves and is not in check
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.White, BoardPoints(0, 5)))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(0, 6)))

        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(Bishop(TeamEnum.White, BoardPoints(1, 2)))
        isDraw = BoardHelpers.IsDraw(self.chessBoard, history.GetHistoricalMoves(), currentTeam)
        self.assertTrue(isDraw)

    def test_IsDraw_IsDrawBy75MovesEach_ReturnsTrue(self):
        history = History()
        isEnPassant = False
        for i in range(Board.Constants.DRAW_CONDITION_TOTAL_MOVES):
            history.AppendMovement(Movement(TeamEnum.White,
                                            PieceEnums.Knight,
                                            PieceEnums.NoPiece,
                                            BoardPoints(1,1),
                                            BoardPoints(2,2),
                                            isEnPassant))
        currentTeam = TeamEnum.White

        isDraw = BoardHelpers.IsDraw(self.chessBoard, history.GetHistoricalMoves(), currentTeam)
        self.assertTrue(isDraw)

    def test_IsDraw_IsDrawByInsufficientPieces_ReturnsTrue(self):
        history = History()
        currentTeam = TeamEnum.White

        # Only Kings on the board
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(2, 0)))

        isDraw = BoardHelpers.IsDraw(self.chessBoard, history.GetHistoricalMoves(), currentTeam)
        self.assertTrue(isDraw)

    def test_IsDraw_NoDraw_ReturnsFalse(self):
        history = History()
        currentTeam = TeamEnum.White

        isDraw = BoardHelpers.IsDraw(self.chessBoard, history.GetHistoricalMoves(), currentTeam)
        self.assertFalse(isDraw)

    # endregion

    # region IsCastleMove Tests

    def test_IsCastleMove_NotKing_ReturnsFalse(self):
        queen = Queen(TeamEnum.White, BoardPoints(4,0))
        fromCoords = queen.GetCoordinates()
        toCoords = BoardPoints(2,0)
        isCastleMove = BoardHelpers.IsCastleMove(queen.GetPieceEnum(), fromCoords, toCoords)
        self.assertFalse(isCastleMove)

    def test_IsCastleMove_KingMovesOneSpot_ReturnsFalse(self):
        king = King(TeamEnum.White, BoardPoints(4,0))
        fromCoords = king.GetCoordinates()
        toCoords = BoardPoints(3,0)
        isCastleMove = BoardHelpers.IsCastleMove(king.GetPieceEnum(), fromCoords, toCoords)
        self.assertFalse(isCastleMove)

    def test_IsCastleMove_KingMovesTwoSpots_ReturnsTrue(self):
        king = King(TeamEnum.White, BoardPoints(4,0))
        fromCoords = king.GetCoordinates()
        toCoords = BoardPoints(2,0)
        isCastleMove = BoardHelpers.IsCastleMove(king.GetPieceEnum(), fromCoords, toCoords)
        self.assertTrue(isCastleMove)

    # endregion

    # region IsEnPassant tests

    def test_IsEnPassant_LastMoveIsNone_ReturnsFalse(self):
        lastMove = None
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = BoardHelpers.IsEnPassant(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassant_PieceMovingIsNotPawn_ReturnsFalse(self):
        # Standard two square move
        isLastMoveAnEnPassant = False
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), isLastMoveAnEnPassant)
        pieceMovingEnum = PieceEnums.Queen
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = BoardHelpers.IsEnPassant(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassant_LastMoveNotPawn_ReturnsFalse(self):
        # Standard two square move
        isLastMoveAnEnPassant = False
        lastMove = Movement(TeamEnum.White, PieceEnums.Queen, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), isLastMoveAnEnPassant)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = BoardHelpers.IsEnPassant(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassant_LastMoveIsPawnButNotTwoMoves_ReturnsFalse(self):
        # Standard two square move
        isLastMoveAnEnPassant = False
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,2), isLastMoveAnEnPassant)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = BoardHelpers.IsEnPassant(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassant_ConditionsValidButNotEnPassantMove_ReturnsFalse(self):
        # Standard two square move
        isLastMoveAnEnPassant = False
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), isLastMoveAnEnPassant)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        # Standard move down
        newCoords = BoardPoints(0,2)

        isEnPassant = BoardHelpers.IsEnPassant(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassant_IsBlackEnPassantMove_ReturnsTrue(self):
        # Standard two square move
        isLastMoveAnEnPassant = False
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), isLastMoveAnEnPassant)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        # Killing move across to an empty square
        newCoords = BoardPoints(1,2)

        isEnPassant = BoardHelpers.IsEnPassant(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertTrue(isEnPassant)

    def test_IsEnPassant_IsWhiteEnPassantMove_ReturnsTrue(self):
        # Standard two square move
        isLastMoveAnEnPassant = False
        lastMove = Movement(TeamEnum.Black, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,6), BoardPoints(1,4), isLastMoveAnEnPassant)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,4)
        # Killing move across to an empty square
        newCoords = BoardPoints(1,5)

        isEnPassant = BoardHelpers.IsEnPassant(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertTrue(isEnPassant)

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