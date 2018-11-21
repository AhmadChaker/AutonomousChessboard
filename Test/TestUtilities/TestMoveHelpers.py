import unittest
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Board.Constants import TeamEnum
from Board.History import History
from Board.Movement import Movement
from Board.ChessBoard import ChessBoard
from Pieces.Constants import PieceEnums
from Pieces.King import King
from Pieces.Queen import Queen
from Pieces.Rook import Rook
from Pieces.Bishop import Bishop
from Pieces.Pawn import Pawn
from Pieces.NoPiece import NoPiece
from Test.Helpers.Helper import Helper


class TestMoveHelpers(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()
        self.history = History()
        MoveHelpers.Update(self.history)

    def tearDown(self):
        MoveHelpers.Update(None)

    # region GetPieceCentricMovesForTeam tests

    # Tests here don't take into account moves where after the move is made, the king (of moving team) is in check
    def test_GetPieceCentricMovesForTeam_GetsValidMoves(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        # Make sure its really only getting the piece centric moves and not taking into accout the king being in check
        # after the move!
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.Black, BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        actualMoves = MoveHelpers.GetPieceCentricMovesForTeam(self.chessBoard, TeamEnum.Black)
        uniqueActualMoves = Helper.GetUniqueElements(actualMoves)
        uniqueActualMoves.sort()

        expectedMoves = []

        # Rook moves
        expectedMoves.append(BoardPoints(6, 0))
        expectedMoves.append(BoardPoints(4, 0))
        expectedMoves.append(BoardPoints(3, 0))
        expectedMoves.append(BoardPoints(2, 0))
        expectedMoves.append(BoardPoints(1, 0))
        expectedMoves.append(BoardPoints(5, 1))
        expectedMoves.append(BoardPoints(5, 2))

        # Pawn moves
        expectedMoves.append(BoardPoints(5, 2))

        # King moves
        expectedMoves.append(BoardPoints(6, 0))
        expectedMoves.append(BoardPoints(6, 1))
        expectedMoves.append(BoardPoints(7, 1))

        uniqueExpectedMoves = Helper.GetUniqueElements(expectedMoves)
        uniqueExpectedMoves.sort()
        self.assertEqual(uniqueActualMoves, uniqueExpectedMoves)

    # endregion

    # region GetValidMovesForTeam tests

    # Tests here take into account the king of the team being in check as part of the move

    def test_GetValidMovesForTeam_GetsValidMoves(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        # Make sure its really only getting the piece centric moves and not taking into accout the king being in check
        # after the move!
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.Black, BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        actualMoves = MoveHelpers.GetValidMovesForTeam(self.chessBoard, TeamEnum.Black)
        uniqueActualMoves = Helper.GetUniqueElements(actualMoves)
        uniqueActualMoves.sort()

        expectedMoves = []

        # Rook moves
        expectedMoves.append(BoardPoints(6, 0))
        expectedMoves.append(BoardPoints(4, 0))
        expectedMoves.append(BoardPoints(3, 0))
        expectedMoves.append(BoardPoints(2, 0))
        expectedMoves.append(BoardPoints(1, 0))

        # can't move up due to being pinned down
        #expectedMoves.append(BoardPoints(5, 1))
        #expectedMoves.append(BoardPoints(5, 2))

        # Pawn moves
        expectedMoves.append(BoardPoints(5, 2))

        # King moves
        expectedMoves.append(BoardPoints(6, 0))
        expectedMoves.append(BoardPoints(6, 1))
        expectedMoves.append(BoardPoints(7, 1))

        uniqueExpectedMoves = Helper.GetUniqueElements(expectedMoves)
        uniqueExpectedMoves.sort()
        self.assertEqual(uniqueActualMoves, uniqueExpectedMoves)

    # endregion

    # region FilterPieceMovesThatPutPlayerInCheck Tests

    def test_FilterPieceMovesThatPutPlayerInCheck_FiltersMoves(self):

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        # Make sure its really only getting the piece centric moves and not taking into accout the king being in check
        # after the move!
        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        potentialRookMoves = []

        # Sidewards rook moves, no change to king being in check
        potentialRookMoves.append(BoardPoints(6, 0))
        potentialRookMoves.append(BoardPoints(4, 0))
        potentialRookMoves.append(BoardPoints(3, 0))
        potentialRookMoves.append(BoardPoints(2, 0))
        potentialRookMoves.append(BoardPoints(1, 0))

        # These moves result in king being in check
        potentialRookMoves.append(BoardPoints(5, 1))
        potentialRookMoves.append(BoardPoints(5, 2))

        actualFilteredMoves = MoveHelpers.FilterPieceMovesThatPutPlayerInCheck(self.chessBoard, rookUnderExamination, potentialRookMoves)
        actualFilteredMoves.sort()

        expectedFilteredRookMoves = []
        expectedFilteredRookMoves.append(BoardPoints(6, 0))
        expectedFilteredRookMoves.append(BoardPoints(4, 0))
        expectedFilteredRookMoves.append(BoardPoints(3, 0))
        expectedFilteredRookMoves.append(BoardPoints(2, 0))
        expectedFilteredRookMoves.append(BoardPoints(1, 0))
        expectedFilteredRookMoves.sort()

        self.assertEqual(actualFilteredMoves, expectedFilteredRookMoves)

    def test_FilterPieceMovesThatPutPlayerInCheck_NoMovesToFilter(self):

        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        # Make sure its really only getting the piece centric moves and not taking into accout the king being in check
        # after the move!
        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)

        # Move the king one space up so that rook movements up won't result in check
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 1)))

        potentialRookMoves = []

        # Sidewards rook moves, no change to king being in check
        potentialRookMoves.append(BoardPoints(6, 0))
        potentialRookMoves.append(BoardPoints(4, 0))
        potentialRookMoves.append(BoardPoints(3, 0))
        potentialRookMoves.append(BoardPoints(2, 0))
        potentialRookMoves.append(BoardPoints(1, 0))

        # Upwards moves
        potentialRookMoves.append(BoardPoints(5, 1))
        potentialRookMoves.append(BoardPoints(5, 2))

        actualFilteredMoves = MoveHelpers.FilterPieceMovesThatPutPlayerInCheck(self.chessBoard, rookUnderExamination, potentialRookMoves)
        actualFilteredMoves.sort()

        expectedFilteredRookMoves = []
        expectedFilteredRookMoves.append(BoardPoints(6, 0))
        expectedFilteredRookMoves.append(BoardPoints(4, 0))
        expectedFilteredRookMoves.append(BoardPoints(3, 0))
        expectedFilteredRookMoves.append(BoardPoints(2, 0))
        expectedFilteredRookMoves.append(BoardPoints(1, 0))
        expectedFilteredRookMoves.append(BoardPoints(5, 1))
        expectedFilteredRookMoves.append(BoardPoints(5, 2))
        expectedFilteredRookMoves.sort()

        self.assertEqual(actualFilteredMoves, expectedFilteredRookMoves)

    # endregion

    # region GetValidMoves tests

    def test_GetValidMoves_MoveIterationsLessThanZero_ReturnsEmptyList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = -1
        enforceKingUnderAttack = False
        directionVector = Points(-1,0)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = []
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_PieceBeingMovedHasNoTeam_ReturnsEmptyList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        # Change team of rook to no team
        rookUnderExamination = Rook(TeamEnum.NoTeam, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = 1
        enforceKingUnderAttack = False
        directionVector = Points(-1,0)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = []
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_PieceBeingMovedIsNoPiece_ReturnsEmptyList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0,0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        rookUnderExamination = NoPiece(BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = 1
        enforceKingUnderAttack = False
        directionVector = Points(-1,0)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = []
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_DirectionVectorResultsInPieceBeingOutOfRange_ReturnsValidList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 1)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(0, 2)))

        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(1, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = 10
        enforceKingUnderAttack = False
        directionVector = Points(-1,0)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = [BoardPoints(0,0)]
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_PieceOfSameTeamIsInPath_ReturnsValidList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(1, 0)))

        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = 10
        enforceKingUnderAttack = False
        directionVector = Points(-1,0)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        actualValidMoves.sort()
        expectedValidMoves = [BoardPoints(3,0), BoardPoints(4,0)]
        expectedValidMoves.sort()
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_NonPawn_AttackStopsAfterHittingOppositeTeamPiece_ReturnsValidList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(3, 0)))

        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = 10
        enforceKingUnderAttack = False
        directionVector = Points(-1,0)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        actualValidMoves.sort()
        expectedValidMoves = [BoardPoints(3,0), BoardPoints(4,0)]
        expectedValidMoves.sort()
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_NonPawn_EnforceKingInCheckSetToFalse_KingInCheck_ReturnsValidList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(3, 0)))

        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = 10
        enforceKingUnderAttack = False
        directionVector = Points(0,1)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = [BoardPoints(5,1), BoardPoints(5,2)]
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_NonPawn_EnforceKingInCheckSetToTrue_KingInCheck_ReturnsValidList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(3, 0)))

        rookUnderExamination = Rook(TeamEnum.Black, BoardPoints(5, 0))
        self.chessBoard.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(5, 3)))
        self.chessBoard.UpdatePieceOnBoard(rookUnderExamination)
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 0)))

        moveIterations = 10
        enforceKingUnderAttack = True
        directionVector = Points(0,1)

        actualValidMoves = MoveHelpers.GetValidMoves(rookUnderExamination, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = []
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_Pawn_DiagonalMove_OpposingTeamAtToLocation_AddsMoveToList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 1)))

        whitePawn = Pawn(TeamEnum.White, BoardPoints(3,3))
        blackPawn = Pawn(TeamEnum.Black, BoardPoints(2,4))
        self.chessBoard.UpdatePieceOnBoard(whitePawn)
        self.chessBoard.UpdatePieceOnBoard(blackPawn)

        moveIterations = 1
        enforceKingUnderAttack = False
        directionVector = Points(1,-1)

        actualValidMoves = MoveHelpers.GetValidMoves(blackPawn, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = [BoardPoints(3,3)]
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_Pawn_DiagonalMove_NoTeamAtToLocation_NoEnPassant_NoAdditionToList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 1)))

        whitePawn = NoPiece(BoardPoints(3,3))
        blackPawn = Pawn(TeamEnum.Black, BoardPoints(2,4))
        self.chessBoard.UpdatePieceOnBoard(whitePawn)
        self.chessBoard.UpdatePieceOnBoard(blackPawn)

        moveIterations = 1
        enforceKingUnderAttack = False
        directionVector = Points(1,-1)

        actualValidMoves = MoveHelpers.GetValidMoves(blackPawn, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = []
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_Pawn_DiagonalMove_NoTeamAtToLocation_IsEnPassantMove_ReturnsValidList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 1)))

        whitePawnCoords = BoardPoints(3,3)
        whitePawn = Pawn(TeamEnum.White, whitePawnCoords)
        blackPawn = Pawn(TeamEnum.Black, BoardPoints(2,3))
        self.chessBoard.UpdatePieceOnBoard(whitePawn)
        self.chessBoard.UpdatePieceOnBoard(blackPawn)

        moveIterations = 1
        enforceKingUnderAttack = False
        directionVector = Points(1,-1)

        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(3,1), BoardPoints(3,3), None)
        self.history.AppendMovement(lastMove)

        actualValidMoves = MoveHelpers.GetValidMoves(blackPawn, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = [BoardPoints(3,2)]
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_Pawn_StraightMove_NoTeamAtToLocation_ReturnsValidList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 1)))

        whitePawnCoords = BoardPoints(3,3)
        whitePawn = Pawn(TeamEnum.White, whitePawnCoords)
        blackPawn = Pawn(TeamEnum.Black, BoardPoints(2,3))
        self.chessBoard.UpdatePieceOnBoard(whitePawn)
        self.chessBoard.UpdatePieceOnBoard(blackPawn)

        moveIterations = 1
        enforceKingUnderAttack = False
        directionVector = Points(0,-1)

        actualValidMoves = MoveHelpers.GetValidMoves(blackPawn, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = [BoardPoints(2,2)]
        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_Pawn_StraightMove_TeamAtToLocation_NoAdditionToList(self):
        self.chessBoard.RemoveAllPieces()
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(0, 0)))
        self.chessBoard.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(7, 1)))

        whitePawnCoords = BoardPoints(2,2)
        whitePawn = Pawn(TeamEnum.White, whitePawnCoords)
        blackPawn = Pawn(TeamEnum.Black, BoardPoints(2,3))
        self.chessBoard.UpdatePieceOnBoard(whitePawn)
        self.chessBoard.UpdatePieceOnBoard(blackPawn)

        moveIterations = 1
        enforceKingUnderAttack = False
        directionVector = Points(0,-1)

        actualValidMoves = MoveHelpers.GetValidMoves(blackPawn, self.chessBoard, directionVector, moveIterations, enforceKingUnderAttack)
        expectedValidMoves = []
        self.assertEqual(actualValidMoves, expectedValidMoves)

    # endregion

    # region IsCastleMove Tests

    def test_IsCastleMove_NotKing_ReturnsFalse(self):
        queen = Queen(TeamEnum.White, BoardPoints(4,0))
        fromCoords = queen.GetCoordinates()
        toCoords = BoardPoints(2,0)
        isCastleMove = MoveHelpers.IsCastleMove(queen.GetPieceEnum(), fromCoords, toCoords)
        self.assertFalse(isCastleMove)

    def test_IsCastleMove_KingMovesOneSpot_ReturnsFalse(self):
        king = King(TeamEnum.White, BoardPoints(4,0))
        fromCoords = king.GetCoordinates()
        toCoords = BoardPoints(3,0)
        isCastleMove = MoveHelpers.IsCastleMove(king.GetPieceEnum(), fromCoords, toCoords)
        self.assertFalse(isCastleMove)

    def test_IsCastleMove_KingMovesTwoSpots_ReturnsTrue(self):
        king = King(TeamEnum.White, BoardPoints(4,0))
        fromCoords = king.GetCoordinates()
        toCoords = BoardPoints(2,0)
        isCastleMove = MoveHelpers.IsCastleMove(king.GetPieceEnum(), fromCoords, toCoords)
        self.assertTrue(isCastleMove)

    # endregion

    # region IsEnPassantMove tests

    def test_IsEnPassantMove_LastMoveIsNone_ReturnsFalse(self):
        lastMove = None
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = MoveHelpers.IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassantMove_PieceMovingIsNotPawn_ReturnsFalse(self):
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), None)
        pieceMovingEnum = PieceEnums.Queen
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = MoveHelpers.IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassantMove_LastMoveNotPawn_ReturnsFalse(self):
        # Standard two square move
        isLastMoveAnEnPassant = False
        lastMove = Movement(TeamEnum.White, PieceEnums.Queen, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), isLastMoveAnEnPassant)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = MoveHelpers.IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassantMove_LastMoveIsPawnButNotTwoMoves_ReturnsFalse(self):
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,2), None)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        newCoords = BoardPoints(1,2)

        isEnPassant = MoveHelpers.IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassantMove_ConditionsValidButNotEnPassantMove_ReturnsFalse(self):
        # Standard two square move
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), None)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        # Standard move down
        newCoords = BoardPoints(0,2)

        isEnPassant = MoveHelpers.IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertFalse(isEnPassant)

    def test_IsEnPassantMove_IsBlackEnPassantMove_ReturnsTrue(self):
        # Standard two square move
        lastMove = Movement(TeamEnum.White, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,1), BoardPoints(1,3), None)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,3)
        # Killing move across to an empty square
        newCoords = BoardPoints(1,2)

        isEnPassant = MoveHelpers.IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertTrue(isEnPassant)

    def test_IsEnPassantMove_IsWhiteEnPassantMove_ReturnsTrue(self):
        lastMove = Movement(TeamEnum.Black, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(1,6), BoardPoints(1,4), None)
        pieceMovingEnum = PieceEnums.Pawn
        oldPieceCoords = BoardPoints(0,4)
        # Killing move across to an empty square
        newCoords = BoardPoints(1,5)

        isEnPassant = MoveHelpers.IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newCoords, lastMove)
        self.assertTrue(isEnPassant)

    # endregion
