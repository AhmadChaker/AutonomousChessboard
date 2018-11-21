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
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Main.Game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()
        self.history = History()
        self.Game = Game(self.history, self.chessBoard)
        MoveHelpers.Update(self.history)

    def tearDown(self):
        self.Game = None
        MoveHelpers.Update(None)

# region CanMove tests

    def test_CanMove_HasGameEndedSetToTrue_ReturnsFalse(self):
        fromCoord = "C2"
        toCoord = "C4"

        self.Game.SetHasGameEnded(True)
        self.assertFalse(self.Game.CanMove(fromCoord, toCoord).IsSuccessful())

    def test_CanMove_FromCoordIsInvalid_ReturnsFalse(self):
        fromCoord = "00"
        toCoord = "C4"

        self.assertFalse(self.Game.CanMove(fromCoord, toCoord).IsSuccessful())

    def test_CanMove_ToCoordIsInvalid_ReturnsFalse(self):
        fromCoord = "C2"
        toCoord = "Z1"

        self.assertFalse(self.Game.CanMove(fromCoord, toCoord).IsSuccessful())

    def test_CanMove_PieceBeingMovedIsNoPiece_ReturnsFalse(self):
        fromCoord = "C4"
        toCoord = "C5"

        self.assertFalse(self.Game.CanMove(fromCoord, toCoord).IsSuccessful())

    def test_CanMove_NotThisPlayersTurn_ReturnsFalse(self):
        fromCoord = "C7"
        toCoord = "C6"

        self.assertFalse(self.Game.CanMove(fromCoord, toCoord).IsSuccessful())

    def test_CanMove_PieceCantMoveToThisLocation_ReturnsFalse(self):
        fromCoord = "C2"
        toCoord = "C5"

        self.assertFalse(self.Game.CanMove(fromCoord, toCoord).IsSuccessful())

    def test_CanMove_ValidMove_ReturnsTrue(self):
        fromCoord = "C2"
        toCoord = "C4"

        self.assertTrue(self.Game.CanMove(fromCoord, toCoord).IsSuccessful())

# endregion

# region PerformPawnPromotionCheck tests

    def test_PerformPawnPromotionCheck_NotPawnMoving_NoChangeInPieceType(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Rook(TeamEnum.White, BoardPoints(0, 0))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        self.Game.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,0))

        expectedPieceType = PieceEnums.Rook
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())

    def test_PerformPawnPromotionCheck_PawnMoving_YIndexNotZeroOrSeven_NoChange(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Pawn(TeamEnum.White, BoardPoints(0, 4))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        self.Game.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,4))

        expectedPieceType = PieceEnums.Pawn
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())

    def test_PerformPawnPromotionCheck_PawnMoving_YIndexIsZero_PawnPromoted(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Pawn(TeamEnum.Black, BoardPoints(0, 0))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        self.Game.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,0))

        expectedPieceType = PieceEnums.Queen
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())

    def test_PerformPawnPromotionCheck_PawnMoving_YIndexIsSeven_PawnPromoted(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Pawn(TeamEnum.White, BoardPoints(0, 7))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        self.Game.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,7))

        expectedPieceType = PieceEnums.Queen
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())

# endregion

# region SetIsCheckmate tests

    def test_SetIsCheckmate_IsCheckmateTrue_GameEndedTrue(self):
        self.Game.SetIsInCheckmate(True)

        self.assertTrue(self.Game.GetIsInCheckmate())
        self.assertTrue(self.Game.GetHasGameEnded())

    def test_SetIsCheckmate_IsCheckmateFalse_GameEndedFalse(self):
        self.Game.SetIsInCheckmate(False)

        self.assertFalse(self.Game.GetIsInCheckmate())
        self.assertFalse(self.Game.GetHasGameEnded())

# endregion

# region SetIsDraw tests

    def test_SetIsDraw_IsDrawTrue_GameEndedTrue(self):
        self.Game.SetIsDraw(True)

        self.assertTrue(self.Game.GetIsDraw())
        self.assertTrue(self.Game.GetHasGameEnded())

    def test_SetIsDraw_IsDrawFalse_GameEndedFalse(self):
        self.Game.SetIsDraw(False)

        self.assertFalse(self.Game.GetIsDraw())
        self.assertFalse(self.Game.GetHasGameEnded())

# endregion

# region ResetGame tests

    def test_ResetGame_AllRelevantVariablesReset(self):

        # Set all variables that will need to be reset
        self.Game.GetHistory().AppendMovement(Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.Pawn,
                                                       BoardPoints(2,2), BoardPoints(3,3), None))
        self.Game.GetBoard().RemoveAllPieces()
        self.Game.SetPlayersTurn(TeamEnum.Black)
        self.Game.SetHasGameEnded(True)
        self.Game.SetIsInCheckmate(True)
        self.Game.SetIsDraw(True)
        self.Game.SetIsInCheck(True)

        # Reset
        self.Game.ResetGame()

        # Check chessboard has reset by just checking 16 pieces each
        actualwhitePieces = BoardHelpers.GetTeamPieceCounts(self.chessBoard, TeamEnum.White)
        actualBlackPieces = BoardHelpers.GetTeamPieceCounts(self.chessBoard, TeamEnum.Black)

        # Assertions
        self.assertEqual(16, actualwhitePieces)
        self.assertEqual(16, actualBlackPieces)
        self.assertEqual(0, len(self.Game.GetHistory().GetHistoricalMoves()))
        self.assertEqual(TeamEnum.White, self.Game.GetPlayersTurn())
        self.assertFalse(self.Game.GetHasGameEnded())
        self.assertFalse(self.Game.GetIsInCheckmate())
        self.assertFalse(self.Game.GetIsDraw())
        self.assertFalse(self.Game.GetIsInCheck())

# endregion

# region PerformMoveProcessing tests

    def test_ResetGame_AllRelevantVariablesReset(self):
        self.chessBoard.RemoveAllPieces()


# endregion
