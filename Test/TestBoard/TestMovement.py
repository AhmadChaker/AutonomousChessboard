import unittest
from Board.Movement import Movement
from Pieces.NoPiece import NoPiece
from Pieces.Pawn import Pawn
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


class TestMovement(unittest.TestCase):

    def test_Equal_AreEqual(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4,3))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3,3))
        isEnPassantMove = False
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(), isEnPassantMove)

        move2PawnA = Pawn(TeamEnum.White, BoardPoints(4,3))
        move2PawnB = Pawn(TeamEnum.Black, BoardPoints(3,3))
        move2IsEnPassantMove = False
        move2 = Movement(move2PawnA.GetTeam(), move2PawnA.GetPieceEnum(), move2PawnB.GetPieceEnum(), move2PawnA.GetCoordinates(), move2PawnB.GetCoordinates(), move2IsEnPassantMove)

        self.assertEqual(move2, move1)

    def test_Equal_NotEqual(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4, 3))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3, 3))
        isEnPassantMove = False
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         isEnPassantMove)

        move2PawnA = Pawn(TeamEnum.White, BoardPoints(4, 3))
        move2PawnB = Pawn(TeamEnum.Black, BoardPoints(5, 3))
        move2IsEnPassantMove = False
        move2 = Movement(move2PawnA.GetTeam(), move2PawnA.GetPieceEnum(), move2PawnB.GetPieceEnum(), move2PawnA.GetCoordinates(), move2PawnB.GetCoordinates(),
                         move2IsEnPassantMove)

        self.assertNotEqual(move2, move1)

    def test_IsCaptureMove_IsEnPassantMoveTrue_True(self):
        move1Pawn = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1Empty = NoPiece(BoardPoints(3, 5))
        isEnPassantMove = True
        move1 = Movement(move1Pawn.GetTeam(), move1Pawn.GetPieceEnum(), move1Empty.GetPieceEnum(), move1Pawn.GetCoordinates(), move1Empty.GetCoordinates(),
                         isEnPassantMove)

        self.assertTrue(move1.IsCaptureMove())

    def test_IsCaptureMove_IsEnPassantMoveFalse_False(self):
        move1Pawn = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1Empty = NoPiece(BoardPoints(4, 5))
        isEnPassantMove = False
        move1 = Movement(move1Pawn.GetTeam(), move1Pawn.GetPieceEnum(), move1Empty.GetPieceEnum(), move1Pawn.GetCoordinates(), move1Empty.GetCoordinates(),
                         isEnPassantMove)

        self.assertFalse(move1.IsCaptureMove())

    def test_IsCaptureMove_MovingIntoOtherTeamPiece_True(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3, 5))
        isEnPassantMove = False
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         isEnPassantMove)

        self.assertTrue(move1.IsCaptureMove())

    def test_GetXMovement(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3, 5))
        isEnPassantMove = False
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         isEnPassantMove)

        expectedXMovement = 1
        self.assertEqual(move1.GetXMovement(), expectedXMovement)

    def test_GetYMovement(self):
        move1PawnA = Pawn(TeamEnum.White, BoardPoints(4, 4))
        move1PawnB = Pawn(TeamEnum.Black, BoardPoints(3, 7))
        isEnPassantMove = False
        move1 = Movement(move1PawnA.GetTeam(), move1PawnA.GetPieceEnum(), move1PawnB.GetPieceEnum(), move1PawnA.GetCoordinates(), move1PawnB.GetCoordinates(),
                         isEnPassantMove)

        expectedYMovement = 3
        self.assertEqual(move1.GetYMovement(), expectedYMovement)
