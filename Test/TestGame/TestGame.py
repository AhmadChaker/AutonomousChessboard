import unittest
from Utilities.BoardHelpers import BoardHelpers
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Messages import MoveEnum
from Miscellaneous.Constants import TeamEnum, PieceEnums
from Board.History import History
from Board.Movement import Movement
from Board.ChessBoard import ChessBoard
from Pieces.King import King
from Pieces.Rook import Rook
from Pieces.Queen import Queen
from Pieces.NoPiece import NoPiece
from Game.Game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        history = History()
        chessBoard = ChessBoard(history)
        self.Game = Game(chessBoard)
        self.chessBoard = self.Game.GetBoard()

    def tearDown(self):
        self.Game = None

    # region CanMove tests

    def test_CanMove_HasGameEndedSetToTrue_ReturnsFalse(self):
        fromCoord = "C2"
        toCoord = "C4"

        self.Game.SetHasGameEnded(True)
        canMoveResult = self.Game.CanMove(fromCoord, toCoord)
        self.assertFalse(canMoveResult.IsSuccessful())
        self.assertEqual(MoveEnum.GameEnded, canMoveResult.GetStatusCode())

    def test_CanMove_FromCoordIsInvalid_ReturnsFalse(self):
        fromCoord = "00"
        toCoord = "C4"

        canMoveResult = self.Game.CanMove(fromCoord, toCoord)
        self.assertFalse(canMoveResult.IsSuccessful())
        self.assertEqual(MoveEnum.CoordOutOfRange, canMoveResult.GetStatusCode())

    def test_CanMove_ToCoordIsInvalid_ReturnsFalse(self):
        fromCoord = "C2"
        toCoord = "Z1"

        canMoveResult = self.Game.CanMove(fromCoord, toCoord)
        self.assertFalse(canMoveResult.IsSuccessful())
        self.assertEqual(MoveEnum.CoordOutOfRange, canMoveResult.GetStatusCode())

    def test_CanMove_PieceBeingMovedIsNoPiece_ReturnsFalse(self):
        fromCoord = "C4"
        toCoord = "C5"

        canMoveResult = self.Game.CanMove(fromCoord, toCoord)
        self.assertFalse(canMoveResult.IsSuccessful())
        self.assertEqual(MoveEnum.SlotHasNoTeam, canMoveResult.GetStatusCode())

    def test_CanMove_NotThisPlayersTurn_ReturnsFalse(self):
        fromCoord = "C7"
        toCoord = "C6"

        canMoveResult = self.Game.CanMove(fromCoord, toCoord)
        self.assertFalse(canMoveResult.IsSuccessful())
        self.assertEqual(MoveEnum.WrongTeam, canMoveResult.GetStatusCode())

    def test_CanMove_PieceCantMoveToThisLocation_ReturnsFalse(self):
        fromCoord = "C2"
        toCoord = "C5"

        canMoveResult = self.Game.CanMove(fromCoord, toCoord)
        self.assertFalse(canMoveResult.IsSuccessful())
        self.assertEqual(MoveEnum.InvalidPieceCentricMove, canMoveResult.GetStatusCode())

    def test_CanMove_ValidMove_ReturnsTrue(self):
        fromCoord = "C2"
        toCoord = "C4"

        canMoveResult = self.Game.CanMove(fromCoord, toCoord)
        self.assertTrue(canMoveResult.IsSuccessful())
        self.assertEqual(MoveEnum.Success, canMoveResult.GetStatusCode())

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
        self.Game.AppendToHistory((Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.Pawn,
                                            BoardPoints(2,2), BoardPoints(3,3), None)))
        self.Game.GetBoard().RemoveAllPieces()
        self.Game.GetBoard().SetTeamsTurn(TeamEnum.Black)
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
        self.assertEqual(0, len(self.chessBoard.GetHistoricalMoves()))
        self.assertEqual(TeamEnum.White, self.Game.GetTeamsTurn())
        self.assertFalse(self.Game.GetHasGameEnded())
        self.assertFalse(self.Game.GetIsInCheckmate())
        self.assertFalse(self.Game.GetIsDraw())
        self.assertFalse(self.Game.GetIsInCheck())

    # endregion

    # region Move tests

    def test_Move_GameHasEnded_ReturnsGameEndedEnum(self):
        self.Game.SetHasGameEnded(True)

        C2CoordToArrayCoord = BoardPoints(2,1)
        moveResult = self.Game.Move("C2", "C4")
        self.assertFalse(moveResult.IsSuccessful())
        self.assertEqual(MoveEnum.GameEnded, moveResult.GetStatusCode())

        # verify no movement
        self.assertEqual(PieceEnums.Pawn, self.Game.GetPieceAtCoordinate(C2CoordToArrayCoord).GetPieceEnum())

    def test_Move_CantMove_ReturnsCantMoveEnum(self):

        # Pawn impossible move
        C2CoordToArrayCoord = BoardPoints(2,1)
        moveResult = self.Game.Move("C2", "C5")
        self.assertEqual(False, moveResult.IsSuccessful())
        self.assertEqual(MoveEnum.InvalidPieceCentricMove, moveResult.GetStatusCode())

        # verify no movement
        self.assertEqual(PieceEnums.Pawn, self.Game.GetPieceAtCoordinate(C2CoordToArrayCoord).GetPieceEnum())

    def test_Move_ValidMove_NormalMoveVariablesSet(self):

        moveResult = self.Game.Move("C2", "C4")

        # Verify pawn coordinates moved
        self.assertEqual(True, moveResult.IsSuccessful())
        self.assertEqual(MoveEnum.Success, moveResult.GetStatusCode())

        # basic validation of post move information
        movedPawn = self.Game.GetBoard().GetPieceAtCoordinate(BoardPoints(2,3))
        self.assertEqual(BoardPoints(2,3), movedPawn.GetCoordinates())
        self.assertEqual(PieceEnums.Pawn, movedPawn.GetPieceEnum())
        self.assertEqual(PieceEnums.NoPiece, self.Game.GetBoard().GetPieceAtCoordinate(BoardPoints(2, 1)).GetPieceEnum())
        self.assertEqual(TeamEnum.Black, self.Game.GetTeamsTurn())
        self.assertFalse(self.Game.GetIsInCheckmate())
        self.assertFalse(self.Game.GetIsDraw())
        self.assertFalse(self.Game.GetIsInCheck())
        self.assertFalse(self.Game.GetHasGameEnded())

    def test_Move_ValidMove_IsCheckmateTrue(self):

        self.Game.GetBoard().UpdatePieceOnBoard(NoPiece(BoardPoints(2, 7)))
        self.Game.GetBoard().UpdatePieceOnBoard(NoPiece(BoardPoints(3, 7)))
        self.Game.GetBoard().UpdatePieceOnBoard(NoPiece(BoardPoints(3, 6)))
        self.Game.GetBoard().UpdatePieceOnBoard(Queen(TeamEnum.White, BoardPoints(3, 3)))
        self.Game.GetBoard().UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(3, 2)))

        moveResult = self.Game.Move("D4", "D8")

        self.assertEqual(True, moveResult.IsSuccessful())
        self.assertEqual(MoveEnum.Success, moveResult.GetStatusCode())

        self.assertFalse(self.Game.GetIsDraw())
        self.assertFalse(self.Game.GetIsInCheck())

        self.assertTrue(self.Game.GetIsInCheckmate())
        self.assertTrue(self.Game.GetHasGameEnded())

    def test_Move_ValidMove_IsCheckTrue(self):

        # comment out bishop removal:  self.Game.GetBoard().UpdatePieceOnBoard(NoPiece(BoardPoints(2, 7)))
        self.Game.GetBoard().UpdatePieceOnBoard(NoPiece(BoardPoints(3, 7)))
        self.Game.GetBoard().UpdatePieceOnBoard(NoPiece(BoardPoints(3, 6)))
        self.Game.GetBoard().UpdatePieceOnBoard(Queen(TeamEnum.White, BoardPoints(3, 3)))
        self.Game.GetBoard().UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(3, 2)))

        moveResult = self.Game.Move("D4", "D7")

        self.assertEqual(True, moveResult.IsSuccessful())
        self.assertEqual(MoveEnum.Success, moveResult.GetStatusCode())

        self.assertFalse(self.Game.GetIsInCheckmate())
        self.assertFalse(self.Game.GetIsDraw())

        self.assertTrue(self.Game.GetIsInCheck())
        self.assertFalse(self.Game.GetHasGameEnded())

    def test_Move_ValidMove_IsDrawTrue(self):

        self.Game.GetBoard().RemoveAllPieces()

        self.Game.GetBoard().UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.Game.GetBoard().UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 7)))

        moveResult = self.Game.Move("A1", "A2")

        self.assertEqual(True, moveResult.IsSuccessful())
        self.assertEqual(MoveEnum.Success, moveResult.GetStatusCode())

        self.assertFalse(self.Game.GetIsInCheckmate())
        self.assertFalse(self.Game.GetIsInCheck())

        self.assertTrue(self.Game.GetIsDraw())
        self.assertTrue(self.Game.GetHasGameEnded())

    # endregion

    # region GetFenRepresentation Tests

    def test_GetFenRepresentation_TwoStepPawnMove_EnPassantFlagSet(self):

        self.Game.Move("c2", "c4")
        actualFenRep = self.Game.GetFenRepresentation()
        expectedFenRep = "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq c3 0 0"

        self.assertEqual(expectedFenRep, actualFenRep)

    def test_GetFenRepresentation_NoCastling_NoEnPassant(self):

        self.Game.Move("d2", "d4")
        self.Game.Move("d7", "d5")

        # move kings a position
        self.Game.Move("e1", "d2")
        self.Game.Move("e8", "d7")

        # move kings back
        self.Game.Move("d2", "e1")
        self.Game.Move("d7", "e8")
        actualFenRep = self.Game.GetFenRepresentation()
        expectedFenRep = "rnbqkbnr/pp1ppppp/8/2p5/2P5/8/PP1PPPPP/RNBQKBNR w - - 0 3"
        self.assertEqual(expectedFenRep, actualFenRep)

    # endregion

    # region Miscellaneous tests

    def test_SimulateEntireGame_FoolsMate(self):

        self.Game.Move("F2", "F3")
        self.Game.Move("E7", "E5")
        self.Game.Move("G2", "G4")

        # check that we are not in checkmate
        self.assertFalse(self.Game.GetIsInCheckmate())

        self.Game.Move("D8", "H4")

        self.assertTrue(self.Game.GetIsInCheckmate)

    # endregion
