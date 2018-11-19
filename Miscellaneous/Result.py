class Result:

    def __init__(self, isSuccessful, message):
        self.__isSuccessful = isSuccessful
        self.__message = message

    def GetMessage(self):
        return self.__message

    def IsSuccessful(self):
        return self.__isSuccessful
