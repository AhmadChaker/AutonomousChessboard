import unittest
import Board.Constants
from Pieces.EmptyPiece import EmptyPiece
from Pieces.Pawn import Pawn
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints
from Utilities.BoardHelpers import BoardHelpers
from Board.History import History


class TestPawn(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.__board = [None] * Board.Constants.MAXIMUM_X_SQUARES
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            # for each y line
            self.__board[xIndex] = [None] * Board.Constants.MAXIMUM_Y_SQUARES

        for yIndex in range(Board.Constants.MAXIMUM_Y_SQUARES):
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                self.__board[xIndex][yIndex] = EmptyPiece(BoardPoints(xIndex, yIndex))

        BoardHelpers.UpdateVariables(History())

    def tearDown(self):
        # get rid of persisted variables
        BoardHelpers.History = None

    # Due to unidirectional nature of Pawns, test white and then black Pawns for each case

    #  TODO: Test all of the IBasePiece methods here (the ones that require implementations of abstract methods
    def test_GetValidMoves_WhitePawn_NoHistory_ReturnsTwoMoves(self):
        whitePawn = Pawn(TeamEnum.White, BoardPoints(3, 3))
        self.__board[3][3] = whitePawn

        actualValidMoves = whitePawn.GetValidMoves(self.__board, False)

        expectedValidMoves = []
        expectedValidMoves.append(BoardPoints(3,4))
        expectedValidMoves.append(BoardPoints(3,5))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_WhitePawn_HasHistory_ReturnsOneMove(self):
        whitePawn = Pawn(TeamEnum.White, BoardPoints(3, 3))
        self.__board[3][3] = whitePawn

        # add some nonsense history
        whitePawn.GetHistory().append(BoardPoints(2,3))
        whitePawn.GetHistory().append(BoardPoints(1,3))

        actualValidMoves = whitePawn.GetValidMoves(self.__board, False)

        expectedValidMoves = []
        expectedValidMoves.append(BoardPoints(3, 4))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_WhitePawn_HasHistory_AttackingLeft_ReturnsTwoMoves(self):

        whitePawn = Pawn(TeamEnum.White, BoardPoints(3, 3))
        self.__board[3][3] = whitePawn

        # add some nonsense history to the Pawn!
        whitePawn.GetHistory().append(BoardPoints(2,3))
        whitePawn.GetHistory().append(BoardPoints(1,3))

        blackPiece = Pawn(TeamEnum.Black, BoardPoints(2,4))
        self.__board[2][4] = blackPiece

        actualValidMoves = whitePawn.GetValidMoves(self.__board, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(3, 4))
        # Attack move
        expectedValidMoves.append(BoardPoints(2,4))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_WhitePawn_HasHistory_AttackingRight_ReturnsTwoMoves(self):

        whitePawn = Pawn(TeamEnum.White, BoardPoints(3, 3))
        self.__board[3][3] = whitePawn

        # add some nonsense history to the Pawn!
        whitePawn.GetHistory().append(BoardPoints(2, 3))
        whitePawn.GetHistory().append(BoardPoints(1, 3))

        blackPiece = Pawn(TeamEnum.Black, BoardPoints(4, 4))
        self.__board[4][4] = blackPiece

        actualValidMoves = whitePawn.GetValidMoves(self.__board, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(3, 4))
        # Attack move
        expectedValidMoves.append(BoardPoints(4, 4))

        self.assertEqual(actualValidMoves, expectedValidMoves)