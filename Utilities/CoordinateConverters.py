import logging
import Miscellaneous.Points
import Board.Constants

logger = logging.getLogger(__name__)


def ValidatePointIsInRange(arrayCoordinate: Miscellaneous.Points.Points) -> bool:
    xCoord = arrayCoordinate.GetX()
    yCoord = arrayCoordinate.GetY()

    if 0 <= xCoord < Board.Constants.MAXIMUM_X_SQUARES and 0 <= yCoord < Board.Constants.MAXIMUM_Y_SQUARES:
        return True
    return False


def ConvertArrayToChessCoordinates(arrayCoordinate: Miscellaneous.Points.Points) -> str:
    xCoord = arrayCoordinate.GetX()
    yCoord = arrayCoordinate.GetY()

    if 0 <= xCoord < Board.Constants.MAXIMUM_X_SQUARES and 0 <= yCoord < Board.Constants.MAXIMUM_Y_SQUARES:
        return Board.Constants.ALPHABETICAL_BOARD_ORDINATES[xCoord] + Board.Constants.NUMERICAL_BOARD_ORDINATES[xCoord]
    return ""


def ConvertChessToArrayCoordinates(chessCoordinate: str) -> Miscellaneous.Points.Points:
    strChessCoords = str(chessCoordinate)
    if len(strChessCoords) != 2:
        logger.error("Invalid chess coordinates, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.Points.POINTS_UNDEFINED

    firstOrdinate = strChessCoords[0]
    secondOrdinate = strChessCoords[1]
    if not firstOrdinate.isalpha():
        logger.error("First ordinate is not alphabetical, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.Points.POINTS_UNDEFINED

    indexAlpha = Board.Constants.ALPHABETICAL_BOARD_ORDINATES.find(firstOrdinate)
    if indexAlpha == -1:
        logger.error("First ordinate is not in approved alphabetical list, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.Points.POINTS_UNDEFINED

    if not secondOrdinate.isnumeric():
        logger.error("Second ordinate is not numerical, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.Points.POINTS_UNDEFINED

    indexNumeric = Board.Constants.NUMERICAL_BOARD_ORDINATES.find(secondOrdinate)
    if indexNumeric == -1:
        logger.error("Second ordinate is not in approved numerical list, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.Points.POINTS_UNDEFINED

    return Miscellaneous.Points.Points(indexAlpha, indexNumeric)

