import logging
import Miscellaneous.BoardPoints
import Board.Constants
from Miscellaneous.BoardPoints import BoardPoints

logger = logging.getLogger(__name__)


def ValidatePointIsInRange(arrayCoordinate: BoardPoints) -> bool:
    xCoord = arrayCoordinate.GetX()
    yCoord = arrayCoordinate.GetY()

    if 0 <= xCoord < Board.Constants.MAXIMUM_X_SQUARES and 0 <= yCoord < Board.Constants.MAXIMUM_Y_SQUARES:
        return True
    return False


def ConvertArrayToChessCoordinates(arrayCoordinate: BoardPoints) -> str:
    xCoord = arrayCoordinate.GetX()
    yCoord = arrayCoordinate.GetY()

    if 0 <= xCoord < Board.Constants.MAXIMUM_X_SQUARES and 0 <= yCoord < Board.Constants.MAXIMUM_Y_SQUARES:
        return Board.Constants.ALPHABETICAL_BOARD_ORDINATES[xCoord] + Board.Constants.NUMERICAL_BOARD_ORDINATES[xCoord]
    return ""


def ConvertChessToArrayCoordinates(chessCoordinate: str) -> BoardPoints:
    strChessCoords = str(chessCoordinate)
    if len(strChessCoords) != 2:
        logger.error("Invalid chess coordinates, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED

    firstOrdinate = strChessCoords[0]
    secondOrdinate = strChessCoords[1]
    if not firstOrdinate.isalpha():
        logger.error("First ordinate is not alphabetical, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED

    indexAlpha = Board.Constants.ALPHABETICAL_BOARD_ORDINATES.find(firstOrdinate)
    if indexAlpha == -1:
        logger.error("First ordinate is not in approved alphabetical list, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED

    if not secondOrdinate.isnumeric():
        logger.error("Second ordinate is not numerical, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED

    indexNumeric = Board.Constants.NUMERICAL_BOARD_ORDINATES.find(secondOrdinate)
    if indexNumeric == -1:
        logger.error("Second ordinate is not in approved numerical list, ChessCoordinates: " + strChessCoords)
        return Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED

    return BoardPoints(indexAlpha, indexNumeric)

