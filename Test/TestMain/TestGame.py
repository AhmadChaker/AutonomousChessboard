import unittest
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Messages import MoveEnum
from Board.Constants import TeamEnum
from Board.History import History
from Board.Movement import Movement
from Board.ChessBoard import ChessBoard
from Pieces.Constants import PieceEnums
from Pieces.King import King
from Pieces.Rook import Rook
from Pieces.Queen import Queen
from Pieces.Pawn import Pawn
from Pieces.NoPiece import NoPiece
from Main.Game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.Game = Game()
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
        self.Game.AppendToHistory((Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.Pawn,
                                            BoardPoints(2,2), BoardPoints(3,3), None)))
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
        self.assertEqual(0, len(self.chessBoard.GetHistoricalMoves()))
        self.assertEqual(TeamEnum.White, self.Game.GetPlayersTurn())
        self.assertFalse(self.Game.GetHasGameEnded())
        self.assertFalse(self.Game.GetIsInCheckmate())
        self.assertFalse(self.Game.GetIsDraw())
        self.assertFalse(self.Game.GetIsInCheck())

# endregion

# region PerformMoveProcessing tests

    def test_PerformMoveProcessing_RegularPieceMove(self):
        self.Game.GetBoard().RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case
        coordinatesPreMove = BoardPoints(0,0)
        rook = Rook(TeamEnum.White, coordinatesPreMove)
        self.Game.GetBoard().UpdatePieceOnBoard(rook)

        # now move rook but not board
        coordinatesPostMove = BoardPoints(0, 2)
        rook.SetCoordinates(coordinatesPostMove)

        self.Game.PerformMoveProcessing(rook, coordinatesPreMove, coordinatesPostMove)

        # expectations
        expectedMove = Movement(rook.GetTeam(), rook.GetPieceEnum(), PieceEnums.NoPiece,
                                coordinatesPreMove, coordinatesPostMove, None)
        expectedPieceAtPreMoveCoordinate = PieceEnums.NoPiece
        expectedPieceAtPostMoveCoordinate = PieceEnums.Rook

        # assertions
        self.assertEqual(1, len(self.chessBoard.GetHistoricalMoves()))
        self.assertEqual(expectedMove, self.chessBoard.GetLastHistoricalMove())
        self.assertEqual(expectedPieceAtPreMoveCoordinate,self.Game.GetBoard().GetPieceAtCoordinate(coordinatesPreMove).GetPieceEnum())
        self.assertEqual(expectedPieceAtPostMoveCoordinate, self.Game.GetBoard().GetPieceAtCoordinate(coordinatesPostMove).GetPieceEnum())

    def test_PerformMoveProcessing_IsEnPassantMove(self):
        self.Game.GetBoard().RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case

        # set up for en-passant
        byPassCoordinates = BoardPoints(2,3)
        self.Game.GetBoard().UpdatePieceOnBoard(Pawn(TeamEnum.White, byPassCoordinates))
        previousMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(2,1), byPassCoordinates, None)
        self.Game.AppendToHistory(previousMove)

        coordinatesPreMove = BoardPoints(1,3)
        pawn = Pawn(TeamEnum.Black, coordinatesPreMove)
        self.Game.GetBoard().UpdatePieceOnBoard(pawn)

        coordinatesPostMove = BoardPoints(2, 2)
        pawn.SetCoordinates(coordinatesPostMove)

        self.Game.PerformMoveProcessing(pawn, coordinatesPreMove, coordinatesPostMove)

        # expectations
        expectedPieceAtPreMoveCoordinate = PieceEnums.NoPiece
        expectedPieceAtPostMoveCoordinate = PieceEnums.Pawn
        expectedPieceAtByPassCoordinate = PieceEnums.NoPiece

        # assertions
        self.assertEqual(2, len(self.chessBoard.GetHistoricalMoves()))
        self.assertEqual(expectedPieceAtPreMoveCoordinate,self.Game.GetBoard().GetPieceAtCoordinate(coordinatesPreMove).GetPieceEnum())
        self.assertEqual(expectedPieceAtPostMoveCoordinate, self.Game.GetBoard().GetPieceAtCoordinate(coordinatesPostMove).GetPieceEnum())
        self.assertEqual(expectedPieceAtByPassCoordinate, self.Game.GetBoard().GetPieceAtCoordinate(byPassCoordinates).GetPieceEnum())

    def test_PerformMoveProcessing_IsCastleMove_LeftCastle(self):
        self.Game.GetBoard().RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case

        preMoveKingCoords = BoardPoints(4,0)
        preMoveRookCoords = BoardPoints(0,0)
        king = King(TeamEnum.White, preMoveKingCoords)
        rook = Rook(TeamEnum.White, preMoveRookCoords)
        self.Game.GetBoard().UpdatePieceOnBoard(king)
        self.Game.GetBoard().UpdatePieceOnBoard(rook)

        postMoveKingCoords = BoardPoints(2,0)
        postMoveRookCoords = BoardPoints(3,0)
        hasMoved = king.Move(self.Game.GetBoard(), postMoveKingCoords)

        self.Game.PerformMoveProcessing(king, preMoveKingCoords, postMoveKingCoords)

        # Assertions
        firstMove = Movement(TeamEnum.White, PieceEnums.King, PieceEnums.NoPiece, preMoveKingCoords, postMoveKingCoords, None)
        secondMove = Movement(TeamEnum.White, PieceEnums.Rook, PieceEnums.NoPiece, preMoveRookCoords, postMoveRookCoords, None)
        expectedHistory = History()
        expectedHistory.AppendMovement(firstMove)
        expectedHistory.AppendMovement(secondMove)

        self.assertTrue(hasMoved)
        self.assertEqual(expectedHistory, self.chessBoard.GetHistory())
        self.assertEqual(PieceEnums.NoPiece, self.Game.GetBoard().GetPieceAtCoordinate(preMoveKingCoords).GetPieceEnum())
        self.assertEqual(PieceEnums.NoPiece, self.Game.GetBoard().GetPieceAtCoordinate(preMoveRookCoords).GetPieceEnum())
        actualRook = self.Game.GetBoard().GetPieceAtCoordinate(postMoveRookCoords)
        self.assertEqual(PieceEnums.Rook, actualRook.GetPieceEnum())
        self.assertEqual(BoardPoints(3, 0), actualRook.GetCoordinates())
        self.assertEqual(PieceEnums.King, self.Game.GetBoard().GetPieceAtCoordinate(postMoveKingCoords).GetPieceEnum())

    def test_PerformMoveProcessing_IsCastleMove_RightCastle(self):
        self.Game.GetBoard().RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case

        preMoveKingCoords = BoardPoints(4,0)
        preMoveRookCoords = BoardPoints(7,0)
        king = King(TeamEnum.White, preMoveKingCoords)
        rook = Rook(TeamEnum.White, preMoveRookCoords)
        self.Game.GetBoard().UpdatePieceOnBoard(king)
        self.Game.GetBoard().UpdatePieceOnBoard(rook)

        postMoveKingCoords = BoardPoints(6,0)
        postMoveRookCoords = BoardPoints(5,0)
        hasMoved = king.Move(self.Game.GetBoard(), postMoveKingCoords)

        self.Game.PerformMoveProcessing(king, preMoveKingCoords, postMoveKingCoords)

        # Assertions
        firstMove = Movement(TeamEnum.White, PieceEnums.King, PieceEnums.NoPiece, preMoveKingCoords, postMoveKingCoords, None)
        secondMove = Movement(TeamEnum.White, PieceEnums.Rook, PieceEnums.NoPiece, preMoveRookCoords, postMoveRookCoords, None)
        expectedHistory = History()
        expectedHistory.AppendMovement(firstMove)
        expectedHistory.AppendMovement(secondMove)

        self.assertTrue(hasMoved)
        self.assertEqual(expectedHistory, self.chessBoard.GetHistory())
        self.assertEqual(PieceEnums.NoPiece, self.Game.GetBoard().GetPieceAtCoordinate(preMoveKingCoords).GetPieceEnum())
        self.assertEqual(PieceEnums.NoPiece, self.Game.GetBoard().GetPieceAtCoordinate(preMoveRookCoords).GetPieceEnum())
        actualRook = self.Game.GetBoard().GetPieceAtCoordinate(postMoveRookCoords)
        self.assertEqual(PieceEnums.Rook, actualRook.GetPieceEnum())
        self.assertEqual(BoardPoints(5, 0), actualRook.GetCoordinates())
        self.assertEqual(PieceEnums.King, self.Game.GetBoard().GetPieceAtCoordinate(postMoveKingCoords).GetPieceEnum())

    def test_PerformPawnPromotionCheck_PawnPromoted(self):
        self.Game.GetBoard().RemoveAllPieces()

        pawn = Pawn(TeamEnum.White, BoardPoints(0,7))
        self.Game.PerformMoveProcessing(pawn, BoardPoints(0, 6), BoardPoints(0, 7))

        self.assertEqual(PieceEnums.Queen, self.Game.GetPieceAtCoordinate(BoardPoints(0,7)).GetPieceEnum())

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
        self.assertEqual(TeamEnum.Black, self.Game.GetPlayersTurn())
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
