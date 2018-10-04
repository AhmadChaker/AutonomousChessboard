import logging
import Utilities.Points
import Game


logger = logging.getLogger(__name__)

# Chess board coordinates
ALPHABETICAL_ORDINATES = "ABCDEFGH"
NUMERICAL_ORDINATES = "12345678"


def ConvertArrayToChessCoordinates(arrayCoordinate: Utilities.Points.Points) -> str:
    xCoord = arrayCoordinate.GetX()
    yCoord = arrayCoordinate.GetY()

    if 0 <= xCoord < Game.MaxXSquares and 0 <= yCoord < Game.MaxYSquares:
        return ALPHABETICAL_ORDINATES[xCoord] + NUMERICAL_ORDINATES[xCoord]
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

    indexAlpha = ALPHABETICAL_ORDINATES.find(firstOrdinate)
    if indexAlpha == -1:
        logger.error("First ordinate is not in approved alphabetical list, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    if not secondOrdinate.isnumeric():
        logger.error("Second ordinate is not numerical, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    indexNumeric = NUMERICAL_ORDINATES.find(secondOrdinate)
    if indexNumeric == -1:
        logger.error("Second ordinate is not in approved numerical list, ChessCoordinates: " + strChessCoords)
        return Utilities.Points.POINTS_UNDEFINED

    return Utilities.Points.Points(indexAlpha, indexNumeric)

