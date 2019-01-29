import logging
from Miscellaneous.Constants import GameType, PlayerEnum


logger = logging.getLogger(__name__)


class GameHelpers:

    @staticmethod
    def IsValidPlayerEnum(player):
        if player == PlayerEnum.Human or player == PlayerEnum.AI:
            return True
        return False

    @staticmethod
    def IsValidGameType(gameType):
        if gameType == GameType.AIvsHuman or gameType == GameType.HumanvsHuman or gameType == GameType.AIvsAI:
            return True
        return False
