class Result:

    def __init__(self, isSuccessful, statusCode):
        self.__isSuccessful = isSuccessful
        self.__statusCode = statusCode

    def GetStatusCode(self):
        return self.__statusCode

    def IsSuccessful(self):
        return self.__isSuccessful
