class Helper:

    @staticmethod
    def GetUniqueElements(inputList):
        uniqueElements = []
        for inputElement in inputList:
            if inputElement not in uniqueElements:
                uniqueElements.append(inputElement)
        return uniqueElements
