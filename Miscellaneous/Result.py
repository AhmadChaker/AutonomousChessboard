class Result:

    def __init__(self, status, message):
        self.__status = status
        self.__message = message

    def GetStatus(self):
        return self.__status

    def GetMessage(self):
        return self.__message
