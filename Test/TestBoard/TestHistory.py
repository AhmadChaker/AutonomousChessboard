import unittest
import Utilities.BoardHelpers
from Board.Movement import Movement
from Board.History import History
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


class TestHistory(unittest.TestCase):

    def test_GetLastMove_NoMoves(self):
        hist = History()
        self.assertEqual(hist.GetLastMove(), None)

    def test_GetLastMove_Success(self):

        # Initialise variables
        hist = History()
        move1Rook = Rook(TeamEnum.White, BoardPoints(5,5))
        move1Pawn = Pawn(TeamEnum.Black, BoardPoints(4,4))
        move2Rook = Rook(TeamEnum.Black, BoardPoints(2,2))
        move2Pawn = Pawn(TeamEnum.White, BoardPoints(3,3))

        # Start methods
        move1 = Movement(move1Rook.GetTeam(), move1Rook.GetPieceEnum(), move1Pawn.GetPieceEnum(), move1Rook.GetCoordinates(), move1Pawn.GetCoordinates(), None)
        move2 = Movement(move2Rook.GetTeam(), move2Pawn.GetPieceEnum(), move2Rook.GetPieceEnum(),  move2Rook.GetCoordinates(), move2Pawn.GetCoordinates(), None)
        hist.AppendMovement(move1)
        hist.AppendMovement(move2)

        # Test output
        self.assertEqual(hist.GetLastMove(), move2)

    def test_GetHistoricalMoves_HistoryAppendedSuccessfully(self):
        # Initialise variables
        hist = History()
        move1Rook = Rook(TeamEnum.White, BoardPoints(5,5))
        move1Pawn = Pawn(TeamEnum.Black, BoardPoints(4,4))
        move2Rook = Rook(TeamEnum.Black, BoardPoints(2,2))
        move2Pawn = Pawn(TeamEnum.White, BoardPoints(3,3))

        # Start methods
        move1 = Movement(move1Rook.GetPieceEnum(), move1Rook.GetPieceEnum(), move1Pawn.GetPieceEnum(), move1Rook.GetCoordinates(), move1Pawn.GetCoordinates(), None)
        move2 = Movement(move2Rook.GetPieceEnum(), move2Rook.GetPieceEnum(), move2Pawn.GetPieceEnum(), move2Rook.GetCoordinates(), move2Pawn.GetCoordinates(), None)
        hist.AppendMovement(move1)
        hist.AppendMovement(move2)

        underlyingStructure = [move1, move2]
        self.assertEqual(underlyingStructure, hist.GetHistoricalMoves())
