from copy import deepcopy
import Pieces.IBasePiece
import Pieces.Constants
import Board.Constants
import Utilities.CoordinateConverters
import Utilities.Points
import Board.Constants
import logging
from Utilities.Points import Points
from Board.Constants import TeamEnum
logger = logging.getLogger(__name__)


class BoardHelpers:

    @staticmethod
    def GetOpposingTeam(team: TeamEnum):
        return TeamEnum.Black if team == TeamEnum.White else TeamEnum.White

    # This method gets all legal moves from the piece's perspective, this does not take into account board
    # considerations such as being in check
    @staticmethod
    def GetPieceCentricMovesForTeam(board, teamToGet: Board.Constants.TeamEnum):
        moves = []
        for yCoord in range(Board.Constants.MAXIMUM_Y_SQUARES):
            # cycle over y coordinates

            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board[xCoord][yCoord]
                if piece.GetTeam() != teamToGet:
                    continue

                # Get valid moves from the perspective of the piece independent of the board
                enforceKingUnderAttackCheck = False
                pieceCentricValidMoves = piece.GetValidMoves(board, enforceKingUnderAttackCheck)
                moves.extend(pieceCentricValidMoves)
        return moves

    @staticmethod
    def GetKing(board, team: Board.Constants.TeamEnum):
        for yCoord in range(Board.Constants.MAXIMUM_Y_SQUARES):
            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board[xCoord][yCoord]
                if piece.GetTeam() == team and piece.GetPieceEnum() == Pieces.Constants.PieceEnums.King:
                    return piece
        return Pieces.EmptyPiece()

    # For the team passed in, check if that King is in check
    @staticmethod
    def IsKingInCheck(board, teamA: Board.Constants.TeamEnum):
        teamAKing = BoardHelpers.GetKing(board, teamA)
        teamB = BoardHelpers.GetOpposingTeam(teamA)
        teamBMoves = BoardHelpers.GetPieceCentricMovesForTeam(board, teamB)
        for teamBMove in teamBMoves:
            if teamBMove == teamAKing.GetCoordinates():
                return True
        return False

    @staticmethod
    # Direction vector is the direction which which to move.
    # moveIterations variable corresponds to iterations of the direction vector.
    def GetValidMoves(piece: Pieces.IBasePiece, board, enforceKingUnderAttackCheck, directionVector: Points, moveIterations: int):

        pieceToMoveTeam = piece.GetTeam()
        pieceToMovePieceEnum = piece.GetPieceEnum()
        pieceToMoveCoords = piece.GetCoordinates()

        # Validate parameters
        if moveIterations <= 0 or \
                directionVector == Utilities.Points.POINTS_UNDEFINED or \
                pieceToMoveCoords == Utilities.Points.POINTS_UNDEFINED:
            logger.error("Problems with input variables, radius of movement: " + str(moveIterations) +
                         ", Piece Coords: " + str(pieceToMoveCoords.GetX()) + "," + str(pieceToMoveCoords.GetY()) +
                         ", Vector Coords:" + str(directionVector.GetX()) + "," + str(directionVector.GetY()))
            return None

        if pieceToMoveTeam == Board.Constants.TeamEnum.NoTeam or \
                pieceToMovePieceEnum == Pieces.Constants.PieceEnums.Empty:
            return None

        # killing pieces logic

        xPotentialCoord = pieceToMoveCoords.GetX()
        yPotentialCoord = pieceToMoveCoords.GetY()

        potentialMoves = []
        for step in range(moveIterations):
            xPotentialCoord += directionVector.GetX()
            yPotentialCoord += directionVector.GetY()

            if not Utilities.CoordinateConverters.ValidatePointIsInRange(Points(xPotentialCoord, yPotentialCoord)):
                # Not in range
                break

            pieceAtCalculatedPosition = board[xPotentialCoord][yPotentialCoord]
            if pieceAtCalculatedPosition.GetTeam() == pieceToMoveTeam:
                # Can't move to this position as it's occupied by the same team
                break

            # Differentiate pawns as they have the following properties
            # 1) Can only kill diagonally of the opposite team (NOT vertically)
            # 2) They can only move forward in empty spaces of 1 (and 2 at the beginning)
            if pieceToMovePieceEnum == Pieces.Constants.PieceEnums.Pawn:
                hasNoTeamAtCalculatedPosition = (pieceAtCalculatedPosition.GetTeam() == Board.Constants.TeamEnum.NoTeam)

                if abs(directionVector.GetX()) == abs(directionVector.GetY()):
                    # Diagonal move, check that the opposite team is at this position (due to earlier if statement
                    # this is equivalent to checking the above boolean
                    if not hasNoTeamAtCalculatedPosition:
                        potentialMoves.append(Points(xPotentialCoord, yPotentialCoord))
                else:
                    # Straight move, check if no team occupies the space
                    if hasNoTeamAtCalculatedPosition:
                        potentialMoves.append(Points(xPotentialCoord, yPotentialCoord))
            else:
                potentialMoves.append(Points(xPotentialCoord, yPotentialCoord))
                if pieceAtCalculatedPosition.GetTeam() != Board.Constants.TeamEnum.NoTeam:
                    break

        if not enforceKingUnderAttackCheck:
            return potentialMoves

        # Check each potential move and see if that move puts the King in check!
        validMoves = []
        if len(potentialMoves) > 0:
            copyBoard = deepcopy(board)
            for potentialMove in potentialMoves:
                preMovePieceCoords = piece.GetCoordinates()
                pieceAtMoveCoordinateBeforeMove = copyBoard[potentialMove.GetX()][potentialMove.GetY()]

                piece.ForceMove(potentialMove)
                copyBoard[potentialMove.GetX()][potentialMove.GetY()] = piece

                # Moved, now check if King if own team is in check
                isKingInCheck = BoardHelpers.IsKingInCheck(copyBoard, piece.GetTeam())

                if not isKingInCheck:
                    validMoves.append(potentialMove)

                # Undo the previous moves
                piece.ForceMove(preMovePieceCoords)
                copyBoard[preMovePieceCoords.GetX()][preMovePieceCoords.GetY()] = piece
                copyBoard[potentialMove.GetX()][potentialMove.GetY()] = pieceAtMoveCoordinateBeforeMove

        return validMoves

    @staticmethod
    def GetValidMovesForTeam(board, teamToPrint: Board.Constants.TeamEnum):

        moves = []
        for yCoord in range(Board.Constants.MAXIMUM_Y_SQUARES):
            # cycle over y coordinates

            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board[xCoord][yCoord]
                if piece.GetTeam() != teamToPrint:
                    continue

                enforceKingUnderAttackCheck = True
                validPieceMoves = piece.GetValidMoves(board, enforceKingUnderAttackCheck)
                if len(validPieceMoves) == 0:
                    continue

                logger.info("Printing valid moves (" + str(len(validPieceMoves)) + ") " + "for: " + piece.GetPieceStr()
                            + ", at: " + piece.GetCoordinates().ToString())
                for validMove in validPieceMoves:
                    logger.info(validMove.ToString())

                moves.extend(validPieceMoves)

        return moves
