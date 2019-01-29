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
LevelsList = [Level(LevelEnums.ONE, 3, 1, 50),
              Level(LevelEnums.TWO, 5, 2, 100),
              Level(LevelEnums.THREE, 6, 3, 150),
              Level(LevelEnums.FOUR, 7, 3, 200),
              Level(LevelEnums.FIVE, 9, 3, 200),
              Level(LevelEnums.SIX, 11, 4, 200),
              Level(LevelEnums.SEVEN, 12, 5, 200),
              Level(LevelEnums.EIGHT, 13, 6, 300),
              Level(LevelEnums.NINE, 14, 7, 300),
              Level(LevelEnums.TEN, 15, 8, 300),
              Level(LevelEnums.ELEVEN, 16, 8, 300),
              Level(LevelEnums.TWELVE, 17, 9, 300),
              Level(LevelEnums.THIRTEEN, 18, 10, 300),
              Level(LevelEnums.FOURTEEN, 19, 11, 400),
              Level(LevelEnums.FIFTEEN, 20, 12, 500)]
