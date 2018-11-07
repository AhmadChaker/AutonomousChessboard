import unittest
from Board.Movement import Movement
from Board.History import History
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Board.Constants import TeamEnum
from Miscellaneous.Points import Points


class TestHistory(unittest.TestCase):

    def test_GetLastMove_NoMoves(self):
        hist = History()
        self.assertEqual(hist.GetLastMove(), None)

    def test_GetLastMove_Success(self):

        # Initialise variables
        hist = History()
        move1Rook = Rook(TeamEnum.White, Points(5,5))
        move1Pawn = Pawn(TeamEnum.Black, Points(4,4))
        move2Rook = Rook(TeamEnum.Black, Points(2,2))
        move2Pawn = Pawn(TeamEnum.White, Points(3,3))
        moveIsEnPassant = False

        # Start methods
        move1 = Movement(move1Rook, move1Pawn, move1Rook.GetCoordinates(), move1Pawn.GetCoordinates(), moveIsEnPassant)
        move2 = Movement(move2Rook, move2Pawn, move2Rook.GetCoordinates(), move2Pawn.GetCoordinates(), moveIsEnPassant)
        hist.AppendMovement(move1)
        hist.AppendMovement(move2)

        # Test output
        self.assertEqual(hist.GetLastMove(), move2)

    def test_GetHistoricalMoves_HistoryAppendedSuccessfully(self):
        # Initialise variables
        hist = History()
        move1Rook = Rook(TeamEnum.White, Points(5,5))
        move1Pawn = Pawn(TeamEnum.Black, Points(4,4))
        move2Rook = Rook(TeamEnum.Black, Points(2,2))
        move2Pawn = Pawn(TeamEnum.White, Points(3,3))
        moveIsEnPassant = False

        # Start methods
        move1 = Movement(move1Rook, move1Pawn, move1Rook.GetCoordinates(), move1Pawn.GetCoordinates(), moveIsEnPassant)
        move2 = Movement(move2Rook, move2Pawn, move2Rook.GetCoordinates(), move2Pawn.GetCoordinates(), moveIsEnPassant)
        hist.AppendMovement(move1)
        hist.AppendMovement(move2)

        underlyingStructure = [move1, move2]
        self.assertEqual(underlyingStructure, hist.GetHistoricalMoves())
