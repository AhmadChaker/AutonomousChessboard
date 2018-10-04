class Points:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y

    def ToString(self):
        return "Array Coords: (X,Y)=(" + str(self.__x) + "," + str(self.__y) + ")"

    def GetX(self):
        return self.__x

    def GetY(self):
        return self.__y


POINTS_UNDEFINED = Points(-1, -1)
