import logging
import Utilities.Points
import Game


logger = logging.getLogger(__name__)

# Chess board coordinates
ALPHABETICAL_ORDINATE = "ABCDEFGH"
NUMERICAL_ORDINATE = "12345678"


def ConvertArrayToChessCoordinates(arrayCoordinate: Utilities.Points.Points) -> str:
    xCoord = arrayCoordinate.GetX()
    yCoord = arrayCoordinate.GetY()

    if 0 <= xCoord < Game.MaxXSquares and 0 <= yCoord < Game.MaxYSquares:
        return ALPHABETICAL_ORDINATE[xCoord] + NUMERICAL_ORDINATE[xCoord]
    return ""


def ConvertChessToArrayCoordinates(chessCoordinate: str) -> Utilities.Points.Points:
    strChessCoords = str(chessCoordinate)
    if len(strChessCoords) != 2:
        logger.error("Invalid chess coordinates, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    firstOrdinate = strChessCoords[0]
    secondOrdinate = strChessCoords[1]
    if not firstOrdinate.isalpha():
        logger.error("First ordinate is not alphabetical, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    indexAlpha = ALPHABETICAL_ORDINATE.find(firstOrdinate)
    if indexAlpha == -1:
        logger.error("First ordinate is not in approved alphabetical list, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    if not secondOrdinate.isnumeric():
        logger.error("Second ordinate is not numerical, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    indexNumeric = NUMERICAL_ORDINATE.find(secondOrdinate)
    if indexNumeric == -1:
        logger.error("Second ordinate is not in approved numerical list, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    return Utilities.Points.Points(indexAlpha, indexNumeric)

