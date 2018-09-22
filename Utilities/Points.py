class Points:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def GetX(self):
        return self.__x

    def GetY(self):
        return self.__y


POINTS_UNDEFINED = Points(-1, -1)
