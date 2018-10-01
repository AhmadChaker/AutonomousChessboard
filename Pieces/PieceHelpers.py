import logging
import Pieces.IBasePiece
import Pieces.Constants
import Chessboard
from Utilities.Points import Points


logger = logging.getLogger(__name__)


class PieceHelpers:

    def __init__(self, board):
        self.__board = board

    @classmethod
    # Direction vector is the direction which which to move.
    # moveIterations variable corresponds to iterations of the direction vector.
    def GetValidMoves(cls, piece: Pieces.IBasePiece, directionVector: Points, moveIterations: int):

        pieceToMoveTeam = piece.GetTeam()
        pieceToMovePieceEnum = piece.GetPieceEnum()
        pieceToMoveCoords = piece.GetCoordinates()

        validMoves = []

        # Validate parameters
        if moveIterations <= 0 or \
                directionVector == Points.POINTS_UNDEFINED or \
                pieceToMoveCoords == Points.POINTS_UNDEFINED:
            logger.error("Problems with input variables, radius of movement: " + str(moveIterations) +
                         ", Piece Coords: " + str(pieceToMoveCoords.GetX()) + "," + str(pieceToMoveCoords.GetY()) +
                         ", Vector Coords:" + str(directionVector.GetX()) + "," + str(directionVector.GetY()))
            return validMoves

        if pieceToMoveTeam == Pieces.Constants.TeamEnum.NoTeam or \
                pieceToMovePieceEnum == Pieces.Constants.PieceEnums.Empty:
            return validMoves

        # killing pieces logic

        xPotentialCoord = pieceToMoveCoords.GetX()
        yPotentialCoord = pieceToMoveCoords.GetY()

        for step in range(moveIterations):
            xPotentialCoord += directionVector.GetX()
            yPotentialCoord += directionVector.GetY()
            if xPotentialCoord < 0 or \
                    xPotentialCoord > (Chessboard.MaxXSquares - 1) or \
                    yPotentialCoord < 0 or \
                    yPotentialCoord > (Chessboard.MaxYSquares - 1):
                break

            pieceAtCalculatedPosition = cls.__board[xPotentialCoord][yPotentialCoord]
            if pieceAtCalculatedPosition.GetTeam() == pieceToMoveTeam:
                # Can't move to this position as it's occupied by the same team
                break

            # Differentiate pawns as they have the following properties
            # 1) Can only kill diagonally of the opposite team (NOT vertically)
            # 2) They can only move forward in empty spaces of 1 (and 2 at the beginning)
            if pieceToMovePieceEnum == Pieces.Constants.PieceEnums.Pawn:
                hasNoTeamAtCalculatedPosition = (pieceAtCalculatedPosition.GetTeam() == Pieces.Constants.TeamEnum.NoTeam)
                if abs(xPotentialCoord) == abs(yPotentialCoord):
                    # Diagonal move, need to check that the opposite team is at this position (due to earlier if statement
                    # this is equivalent to checking the above boolean
                    if not hasNoTeamAtCalculatedPosition:
                        validMoves.append(Points(xPotentialCoord, yPotentialCoord))
                else:
                    # Straight move, check if no team occupies the space
                    if hasNoTeamAtCalculatedPosition:
                        validMoves.append(Points(xPotentialCoord, yPotentialCoord))
            else:
                validMoves.append(Points(xPotentialCoord, yPotentialCoord))

        return validMoves