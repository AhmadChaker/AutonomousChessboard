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
from Pieces.Bishop import Bishop
from Pieces.Pawn import Pawn
from Main.Game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        chessBoard = ChessBoard()
        history = History()
        self.Game = Game(history, chessBoard)
        MoveHelpers.Update(history)

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

    def test_PerformPawnPromotionCheck_PawnMoving_YCoordIsZero(self):
        pass

# endregion
