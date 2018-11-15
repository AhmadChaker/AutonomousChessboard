import unittest
import Pieces.IBasePiece
import Pieces.Constants
import Board.Constants
import Utilities.CoordinateConverters
import Miscellaneous.BoardPoints
import Board.Constants
import logging
from Utilities.BoardHelpers import BoardHelpers
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Board.Constants import TeamEnum
from Board.History import History
from Board.ChessBoard import ChessBoard
from Pieces.Constants import PieceEnums
from Pieces.King import King
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

    # end region

    # region