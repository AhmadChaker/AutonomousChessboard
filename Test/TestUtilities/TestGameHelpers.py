import unittest
from Utilities.GameHelpers import GameHelpers
from Miscellaneous.Constants import GameType, PlayerEnum


class TestGameHelpers(unittest.TestCase):

    # region IsValidPlayerEnum Tests

    def test_IsValidPlayerEnum_TestAllCases(self):
        self.assertTrue(GameHelpers.IsValidPlayerEnum(PlayerEnum.AI))
        self.assertTrue(GameHelpers.IsValidPlayerEnum(PlayerEnum.Human))

        self.assertFalse(GameHelpers.IsValidPlayerEnum(PlayerEnum.Unknown))

    # endregion

    # region IsValidGameType Tests

    def test_IsValidGameType_TestAllCases(self):
        self.assertTrue(GameHelpers.IsValidGameType(GameType.AIvsAI))
        self.assertTrue(GameHelpers.IsValidGameType(GameType.AIvsHuman))
        self.assertTrue(GameHelpers.IsValidGameType(GameType.HumanvsHuman))

        self.assertFalse(GameHelpers.IsValidGameType(GameType.Unknown))

    # endregion