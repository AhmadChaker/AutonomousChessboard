import unittest
import Pieces.IBasePiece
import Pieces.Constants
import Board.Constants
import Utilities.CoordinateConverters
import Miscellaneous.BoardPoints
import Board.Constants
import logging
from Utilities.BoardHelpers import BoardHelpers
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Board.Constants import TeamEnum
from Board.History import History
from Pieces.Constants import PieceEnums


class TestBoardHelpers(unittest.TestCase):

    # region GetOpposingTeam Tests
    def test_GetOpposingTeam_NoTeam_ReturnsNoTeam(self):
        initialTeam = TeamEnum.NoTeam
        expectedTeam = TeamEnum.NoTeam
        self.assertEqual(BoardHelpers.GetOpposingTeam(initialTeam), expectedTeam)

    def test_GetOpposingTeam_WhiteTeam_ReturnsBlack(self):
        initialTeam = TeamEnum.White
        expectedTeam = TeamEnum.Black
        self.assertEqual(BoardHelpers.GetOpposingTeam(initialTeam), expectedTeam)

    def test_GetOpposingTeam_BlackTeam_ReturnsWhite(self):
        initialTeam = TeamEnum.Black
        expectedTeam = TeamEnum.White
        self.assertEqual(BoardHelpers.GetOpposingTeam(initialTeam), expectedTeam)
    # endregion

    # region
