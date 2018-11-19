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

    def tearDown(self):
        self.Game = None

# region CanMove tests

    def test_CanMove_InvalidFromCoordinate_Returns(self):
        initialTeam = TeamEnum.NoTeam
        expectedTeam = TeamEnum.NoTeam
        self.assertEqual(BoardHelpers.GetOpposingTeam(initialTeam), expectedTeam)

# endregion
