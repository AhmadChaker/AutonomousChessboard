import unittest
from Board.Movement import Movement
from Pieces.Pawn import Pawn
from Pieces.EmptyPiece import EmptyPiece
from Board.Constants import TeamEnum
from Miscellaneous.Points import Points


class TestMovement(unittest.TestCase):

    def test_Equal_AreEqual(self):
        move1PawnA = Pawn(TeamEnum.White, Points(4,3))
        move1PawnB = Pawn(TeamEnum.Black, Points(3,3))
        move1IsEnPassant = False
        move1 = Movement(move1PawnA, move1PawnB, move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(), move1IsEnPassant)

        move2PawnA = Pawn(TeamEnum.White, Points(4,3))
        move2PawnB = Pawn(TeamEnum.Black, Points(3,3))
        move2IsEnPassant = False
        move2 = Movement(move2PawnA, move2PawnB, move2PawnA.GetCoordinates(), move2PawnB.GetCoordinates(), move2IsEnPassant)

        self.assertEqual(move2, move1)

    def test_Equal_NotEqual(self):
        move1PawnA = Pawn(TeamEnum.White, Points(4, 3))
        move1PawnB = Pawn(TeamEnum.Black, Points(3, 3))
        move1IsEnPassant = False
        move1 = Movement(move1PawnA, move1PawnB, move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         move1IsEnPassant)

        move2PawnA = Pawn(TeamEnum.White, Points(4, 3))
        move2PawnB = Pawn(TeamEnum.Black, Points(5, 3))
        move2IsEnPassant = False
        move2 = Movement(move2PawnA, move2PawnB, move2PawnA.GetCoordinates(), move2PawnB.GetCoordinates(),
                         move2IsEnPassant)

        self.assertNotEqual(move2, move1)

    def test_IsCaptureMove_IsEnPassantTrue_True(self):
        move1Pawn = Pawn(TeamEnum.White, Points(4, 4))
        move1Empty = EmptyPiece(Points(3, 5))
        move1IsEnPassant = True
        move1 = Movement(move1Pawn, move1Empty, move1Pawn.GetCoordinates(), move1Empty.GetCoordinates(),
                         move1IsEnPassant)

        self.assertTrue(move1.IsCaptureMove())

    def test_IsCaptureMove_IsEnPassantFalse_False(self):
        move1Pawn = Pawn(TeamEnum.White, Points(4, 4))
        move1Empty = EmptyPiece(Points(4, 5))
        move1IsEnPassant = False
        move1 = Movement(move1Pawn, move1Empty, move1Pawn.GetCoordinates(), move1Empty.GetCoordinates(),
                         move1IsEnPassant)

        self.assertFalse(move1.IsCaptureMove())

    def test_IsCaptureMove_MovingIntoOtherTeamPiece_True(self):
        move1PawnA = Pawn(TeamEnum.White, Points(4, 4))
        move1PawnB = Pawn(TeamEnum.Black, Points(3, 5))
        move1IsEnPassant = False
        move1 = Movement(move1PawnA, move1PawnB, move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         move1IsEnPassant)

        self.assertTrue(move1.IsCaptureMove())
