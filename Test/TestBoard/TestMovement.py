import unittest
import Utilities.BoardHelpers
from Board.Movement import Movement
from Pieces.NoPiece import NoPiece
from Pieces.Pawn import Pawn
from Pieces.King import King
from Pieces.Constants import PieceEnums
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


class TestMovement(unittest.TestCase):

    def test_Equal_AreEqual(self):
        lastMove = Movement(TeamEnum.Black, PieceEnums.Queen, PieceEnums.NoPiece, BoardPoints(0,0), BoardPoints(1,0), None)

        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4,3))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3,3))
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(), lastMove)

        move2PawnA = Pawn(TeamEnum.White, BoardPoints(4,3))
        move2PawnB = Pawn(TeamEnum.Black, BoardPoints(3,3))
        move2 = Movement(move2PawnA.GetTeam(), move2PawnA.GetPieceEnum(), move2PawnB.GetPieceEnum(), move2PawnA.GetCoordinates(), move2PawnB.GetCoordinates(), lastMove)

        self.assertEqual(move2, move1)

    def test_IsCaptureMove_IsEnPassantMoveTrue_True(self):
        move1Pawn = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1Empty = NoPiece(BoardPoints(3, 5))
        lastMove = Movement(TeamEnum.Black, PieceEnums.Pawn, PieceEnums.NoPiece, BoardPoints(3,6), BoardPoints(3,4), None)
        move1 = Movement(move1Pawn.GetTeam(), move1Pawn.GetPieceEnum(), move1Empty.GetPieceEnum(), move1Pawn.GetCoordinates(), move1Empty.GetCoordinates(),
                         lastMove)

        self.assertTrue(move1.IsCaptureMove())

    def test_IsCaptureMove_IsEnPassantMoveFalse_False(self):
        move1Pawn = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1Empty = NoPiece(BoardPoints(4, 5))
        lastMove = Movement(TeamEnum.Black, PieceEnums.Queen, PieceEnums.NoPiece, BoardPoints(0, 0), BoardPoints(1, 0), None)
        move1 = Movement(move1Pawn.GetTeam(), move1Pawn.GetPieceEnum(), move1Empty.GetPieceEnum(), move1Pawn.GetCoordinates(), move1Empty.GetCoordinates(),
                         lastMove)

        self.assertFalse(move1.IsCaptureMove())
        self.assertFalse(move1.IsEnPassantMove())

    def test_IsCaptureMove_MovingIntoOtherTeamPiece_True(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3, 5))
        lastMove = Movement(TeamEnum.Black, PieceEnums.Queen, PieceEnums.NoPiece, BoardPoints(0,0), BoardPoints(1,0), None)
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         lastMove)

        self.assertTrue(move1.IsCaptureMove())

    def test_IsCastleMove_CastlingTrue_True(self):
        king = King(TeamEnum.White, BoardPoints(4, 0))
        move = Movement(TeamEnum.White, king.GetPieceEnum(), PieceEnums.NoPiece, king.GetCoordinates(), BoardPoints(6, 0), None)
        self.assertTrue(move.IsCastleMove())

    def test_IsCastleMove_CastlingFalse_False(self):
        king = King(TeamEnum.White, BoardPoints(4, 0))
        move = Movement(TeamEnum.White, king.GetPieceEnum(), PieceEnums.NoPiece, king.GetCoordinates(), BoardPoints(5, 0), None)
        self.assertFalse(move.IsCastleMove())

    def test_GetXMovement(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3, 5))
        lastMove = Movement(TeamEnum.Black, PieceEnums.Queen, PieceEnums.NoPiece, BoardPoints(0,0), BoardPoints(1,0), None)
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         lastMove)

        expectedXMovement = 1
        self.assertEqual(move1.GetXMovement(), expectedXMovement)

    def test_GetYMovement(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3, 7))
        lastMove = Movement(TeamEnum.Black, PieceEnums.Queen, PieceEnums.NoPiece, BoardPoints(0,0), BoardPoints(1,0), None)
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         lastMove)

        expectedYMovement = 3
        self.assertEqual(move1.GetYMovement(), expectedYMovement)
