from enum import Enum


# This is a bit retarded, but wanted to make things a bit explicit
class LevelEnums(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15


class Level:
    def __init__(self, number, skill, depth, thinkingTime):
        self.__number = number
        self.__skillOption = {"Skill Level" : str(skill)}
        self.__depth = depth
        self.__thinkingTime = thinkingTime

    def GetLevelNumber(self):
        return self.__number

    def GetSkill(self):
        return self.__skillOption

    def GetDepth(self):
        return self.__depth

    def GetThinkingTime(self):
        return self.__thinkingTime

# TODO Fix levels
# Levels of AI
LevelsList = [Level(LevelEnums.ONE, 10, 10, 200),
              Level(LevelEnums.TWO, 3, 5, 100),
              Level(LevelEnums.THREE, 3, 5, 100),
              Level(LevelEnums.FOUR, 3, 5, 100),
              Level(LevelEnums.FIVE, 3, 5, 100),
              Level(LevelEnums.SIX, 3, 5, 100),
              Level(LevelEnums.SEVEN, 3, 5, 100),
              Level(LevelEnums.EIGHT, 3, 5, 100),
              Level(LevelEnums.NINE, 3, 5, 100),
              Level(LevelEnums.TEN, 3, 5, 100),
              Level(LevelEnums.ELEVEN, 3, 5, 100),
              Level(LevelEnums.TWELVE, 3, 5, 100),
              Level(LevelEnums.THIRTEEN, 3, 5, 100),
              Level(LevelEnums.FOURTEEN, 3, 5, 100),
              Level(LevelEnums.FIFTEEN, 3, 5, 100)]
