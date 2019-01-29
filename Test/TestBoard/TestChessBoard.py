import unittest
from Board.ChessBoard import ChessBoard
from Miscellaneous.Constants import PieceEnums, TeamEnum
from Pieces.Bishop import Bishop
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Pieces.King import King
from Board.History import History
from Board.Movement import Movement
from Miscellaneous.BoardPoints import BoardPoints


class TestChessBoard(unittest.TestCase):

    # NOTE: Unit tests for GetFenRepresentation are done in TestGame.py

    def setUp(self):
        history = History()
        self.chessBoard = ChessBoard(history)

    # region PerformPawnPromotionCheck tests

    def test_PerformPawnPromotionCheck_NotPawnMoving_NoChangeInPieceType(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Bishop(TeamEnum.White, BoardPoints(0, 0))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        isPawnPromotion = self.chessBoard.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,0))

        expectedPieceType = PieceEnums.Bishop
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())
        self.assertFalse(isPawnPromotion)

    def test_PerformPawnPromotionCheck_PawnMoving_YIndexNotZeroOrSeven_NoChange(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Pawn(TeamEnum.White, BoardPoints(0, 4))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        isPawnPromotion = self.chessBoard.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,4))

        expectedPieceType = PieceEnums.Pawn
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())
        self.assertFalse(isPawnPromotion)

    def test_PerformPawnPromotionCheck_PawnMoving_YIndexIsZero_PawnPromoted(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Pawn(TeamEnum.Black, BoardPoints(0, 0))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        isPawnPromotion = self.chessBoard.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,0))

        expectedPieceType = PieceEnums.Queen
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())
        self.assertTrue(isPawnPromotion)

    def test_PerformPawnPromotionCheck_PawnMoving_YIndexIsSeven_PawnPromoted(self):
        self.chessBoard.RemoveAllPieces()
        pieceOfInterest = Pawn(TeamEnum.White, BoardPoints(0, 7))
        self.chessBoard.UpdatePieceOnBoard(pieceOfInterest)

        isPawnPromotion = self.chessBoard.PerformPawnPromotionCheck(pieceOfInterest)
        pieceAtCoord = self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,7))

        expectedPieceType = PieceEnums.Queen
        self.assertEqual(expectedPieceType, pieceAtCoord.GetPieceEnum())
        self.assertTrue(isPawnPromotion)

    # endregion

    # region PerformMoveProcessing tests

    def test_PerformMoveProcessing_RegularPieceMove(self):
        self.chessBoard.RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case
        coordinatesPreMove = BoardPoints(0,0)
        rook = Rook(TeamEnum.White, coordinatesPreMove)
        self.chessBoard.UpdatePieceOnBoard(rook)

        # now move rook but not board
        coordinatesPostMove = BoardPoints(0, 2)
        rook.SetCoordinates(coordinatesPostMove)

        self.chessBoard.PerformMoveProcessing(rook, coordinatesPreMove, coordinatesPostMove)

        # expectations
        expectedMove = Movement(rook.GetTeam(), rook.GetPieceEnum(), PieceEnums.NoPiece,
                                coordinatesPreMove, coordinatesPostMove, None)
        expectedPieceAtPreMoveCoordinate = PieceEnums.NoPiece
        expectedPieceAtPostMoveCoordinate = PieceEnums.Rook

        # assertions
        self.assertEqual(1, len(self.chessBoard.GetHistoricalMoves()))
        self.assertEqual(expectedMove, self.chessBoard.GetLastHistoricalMove())
        self.assertEqual(expectedPieceAtPreMoveCoordinate,self.chessBoard.GetPieceAtCoordinate(coordinatesPreMove).GetPieceEnum())
        self.assertEqual(expectedPieceAtPostMoveCoordinate, self.chessBoard.GetPieceAtCoordinate(coordinatesPostMove).GetPieceEnum())

    def test_PerformMoveProcessing_IsEnPassantMove(self):
        self.chessBoard.RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case

        # set up for en-passant
        byPassCoordinates = BoardPoints(2,3)
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.White, byPassCoordinates))
        previousMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(2,1), byPassCoordinates, None)
        self.chessBoard.AppendToHistory(previousMove)

        coordinatesPreMove = BoardPoints(1,3)
        pawn = Pawn(TeamEnum.Black, coordinatesPreMove)
        self.chessBoard.UpdatePieceOnBoard(pawn)

        coordinatesPostMove = BoardPoints(2, 2)
        pawn.SetCoordinates(coordinatesPostMove)

        self.chessBoard.PerformMoveProcessing(pawn, coordinatesPreMove, coordinatesPostMove)

        # expectations
        expectedPieceAtPreMoveCoordinate = PieceEnums.NoPiece
        expectedPieceAtPostMoveCoordinate = PieceEnums.Pawn
        expectedPieceAtByPassCoordinate = PieceEnums.NoPiece

        # assertions
        self.assertEqual(2, len(self.chessBoard.GetHistoricalMoves()))
        self.assertEqual(expectedPieceAtPreMoveCoordinate,self.chessBoard.GetPieceAtCoordinate(coordinatesPreMove).GetPieceEnum())
        self.assertEqual(expectedPieceAtPostMoveCoordinate, self.chessBoard.GetPieceAtCoordinate(coordinatesPostMove).GetPieceEnum())
        self.assertEqual(expectedPieceAtByPassCoordinate, self.chessBoard.GetPieceAtCoordinate(byPassCoordinates).GetPieceEnum())

    def test_PerformMoveProcessing_IsCastleMove_LeftCastle(self):
        self.chessBoard.RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case

        preMoveKingCoords = BoardPoints(4,0)
        preMoveRookCoords = BoardPoints(0,0)
        king = King(TeamEnum.White, preMoveKingCoords)
        rook = Rook(TeamEnum.White, preMoveRookCoords)
        self.chessBoard.UpdatePieceOnBoard(king)
        self.chessBoard.UpdatePieceOnBoard(rook)

        postMoveKingCoords = BoardPoints(2,0)
        postMoveRookCoords = BoardPoints(3,0)
        hasMoved = king.Move(self.chessBoard, postMoveKingCoords)

        self.chessBoard.PerformMoveProcessing(king, preMoveKingCoords, postMoveKingCoords)

        # Assertions
        firstMove = Movement(TeamEnum.White, PieceEnums.King, PieceEnums.NoPiece, preMoveKingCoords, postMoveKingCoords, None)
        secondMove = Movement(TeamEnum.White, PieceEnums.Rook, PieceEnums.NoPiece, preMoveRookCoords, postMoveRookCoords, None)
        expectedHistory = History()
        expectedHistory.AppendMovement(firstMove)
        expectedHistory.AppendMovement(secondMove)

        self.assertTrue(hasMoved)
        self.assertEqual(expectedHistory, self.chessBoard.GetHistory())
        self.assertEqual(PieceEnums.NoPiece, self.chessBoard.GetPieceAtCoordinate(preMoveKingCoords).GetPieceEnum())
        self.assertEqual(PieceEnums.NoPiece, self.chessBoard.GetPieceAtCoordinate(preMoveRookCoords).GetPieceEnum())
        actualRook = self.chessBoard.GetPieceAtCoordinate(postMoveRookCoords)
        self.assertEqual(PieceEnums.Rook, actualRook.GetPieceEnum())
        self.assertEqual(BoardPoints(3, 0), actualRook.GetCoordinates())
        self.assertEqual(PieceEnums.King, self.chessBoard.GetPieceAtCoordinate(postMoveKingCoords).GetPieceEnum())

    def test_PerformMoveProcessing_IsCastleMove_RightCastle(self):
        self.chessBoard.RemoveAllPieces()
        # Note piece has already updated itself, the board however has not been updated to reflect its coordinates!
        # we mirror this case

        preMoveKingCoords = BoardPoints(4,0)
        preMoveRookCoords = BoardPoints(7,0)
        king = King(TeamEnum.White, preMoveKingCoords)
        rook = Rook(TeamEnum.White, preMoveRookCoords)
        self.chessBoard.UpdatePieceOnBoard(king)
        self.chessBoard.UpdatePieceOnBoard(rook)

        postMoveKingCoords = BoardPoints(6,0)
        postMoveRookCoords = BoardPoints(5,0)
        hasMoved = king.Move(self.chessBoard, postMoveKingCoords)

        self.chessBoard.PerformMoveProcessing(king, preMoveKingCoords, postMoveKingCoords)

        # Assertions
        firstMove = Movement(TeamEnum.White, PieceEnums.King, PieceEnums.NoPiece, preMoveKingCoords, postMoveKingCoords, None)
        secondMove = Movement(TeamEnum.White, PieceEnums.Rook, PieceEnums.NoPiece, preMoveRookCoords, postMoveRookCoords, None)
        expectedHistory = History()
        expectedHistory.AppendMovement(firstMove)
        expectedHistory.AppendMovement(secondMove)

        self.assertTrue(hasMoved)
        self.assertEqual(expectedHistory, self.chessBoard.GetHistory())
        self.assertEqual(PieceEnums.NoPiece, self.chessBoard.GetPieceAtCoordinate(preMoveKingCoords).GetPieceEnum())
        self.assertEqual(PieceEnums.NoPiece, self.chessBoard.GetPieceAtCoordinate(preMoveRookCoords).GetPieceEnum())
        actualRook = self.chessBoard.GetPieceAtCoordinate(postMoveRookCoords)
        self.assertEqual(PieceEnums.Rook, actualRook.GetPieceEnum())
        self.assertEqual(BoardPoints(5, 0), actualRook.GetCoordinates())
        self.assertEqual(PieceEnums.King, self.chessBoard.GetPieceAtCoordinate(postMoveKingCoords).GetPieceEnum())

    def test_PerformPawnPromotionCheck_PawnPromoted(self):
        self.chessBoard.RemoveAllPieces()

        pawn = Pawn(TeamEnum.White, BoardPoints(0,7))
        self.chessBoard.PerformMoveProcessing(pawn, BoardPoints(0, 6), BoardPoints(0, 7))

        self.assertEqual(PieceEnums.Queen, self.chessBoard.GetPieceAtCoordinate(BoardPoints(0,7)).GetPieceEnum())

    # endregion

    # region ResetToDefault

    def test_ResetToDefault_RelevantValuesReset(self):
        # perform a standard move and then reset
        self.chessBoard.RemoveAllPieces()

        coordinatesPreMove = BoardPoints(0,0)
        rook = Rook(TeamEnum.White, coordinatesPreMove)
        self.chessBoard.UpdatePieceOnBoard(rook)

        # now move rook but not board
        coordinatesPostMove = BoardPoints(0, 2)
        rook.SetCoordinates(coordinatesPostMove)

        self.chessBoard.PerformMoveProcessing(rook, coordinatesPreMove, coordinatesPostMove)

        # verify before reset that values are set (just double checking)

        self.assertEqual(TeamEnum.Black, self.chessBoard.GetTeamsTurn())
        self.assertEqual(1, len(self.chessBoard.GetHistoricalMoves()))

        self.chessBoard.ResetToDefault()

        self.assertEqual(TeamEnum.White, self.chessBoard.GetTeamsTurn())
        self.assertEqual(0, len(self.chessBoard.GetHistoricalMoves()))

    # endregion
