import Pieces.IBasePiece
import Pieces.Constants
import Board.Constants
import Utilities.CoordinateConverters
import Board.Constants
import Utilities.BoardHelpers
import logging
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Pieces.Constants import PieceEnums
from Pieces.NoPiece import NoPiece


logger = logging.getLogger(__name__)


class MoveHelpers:

    @classmethod
    def Update(cls, history):
        cls.History = history

    # This method gets all legal moves from the piece's perspective, this does not take into account board
    # considerations such as being in check
    @staticmethod
    def GetPieceCentricMovesForTeam(board, teamToGet: Board.Constants.TeamEnum, enforceKingUnderAttackCheck):
        moves = []
        for yCoord in range(Board.Constants.MAXIMUM_Y_SQUARES):
            # cycle over y coordinates

            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board.GetPieceAtCoordinate(BoardPoints(xCoord, yCoord))
                if piece.GetTeam() != teamToGet:
                    continue

                # Get valid moves from the perspective of the piece independent of the board
                pieceCentricValidMoves = piece.GetValidMoves(board, enforceKingUnderAttackCheck)
                moves.extend(pieceCentricValidMoves)
        return moves

    @staticmethod
    def FilterPieceMovesThatPutPlayerInCheck(board, pieceBeingMoved: Pieces.IBasePiece, potentialMoves):
        # Check each potential move and see if that move puts the King in check!
        validMoves = []

        for potentialMove in potentialMoves:
            preMovePieceCoords = pieceBeingMoved.GetCoordinates()
            pieceAtMoveCoordinateBeforeMove = board.GetPieceAtCoordinate(potentialMove)

            pieceBeingMoved.ForceMoveNoHistory(potentialMove)
            board.UpdatePieceOnBoard(pieceBeingMoved)
            board.UpdatePieceOnBoard(NoPiece(preMovePieceCoords))

            # Moved, now check if King on own team is in check
            isInCheck = Utilities.BoardHelpers.BoardHelpers.IsInCheck(board, pieceBeingMoved.GetTeam())

            if not isInCheck:
                validMoves.append(potentialMove)

            # Undo the previous moves
            pieceBeingMoved.ForceMoveNoHistory(preMovePieceCoords)
            board.UpdatePieceOnBoard(pieceBeingMoved)
            board.UpdatePieceOnBoard(pieceAtMoveCoordinateBeforeMove)

        return validMoves

    @classmethod
    # Direction vector is the direction with which to move.
    # moveIterations variable corresponds to iterations of the direction vector.
    def GetValidMoves(cls, piece: Pieces.IBasePiece, board, directionVector: Points, moveIterations: int,
                      enforceKingUnderAttackCheck):

        pieceToMoveTeam = piece.GetTeam()
        pieceToMovePieceEnum = piece.GetPieceEnum()
        pieceToMoveCoords = piece.GetCoordinates()

        # Validate parameters
        if moveIterations <= 0:
            logger.error("Problems with input variables, move iterations: " + str(moveIterations) +
                         ", Piece being moved coords: " + pieceToMoveCoords.ToString() +
                         ", Direction vector: " + directionVector.ToString())
            return []

        if pieceToMovePieceEnum == Pieces.Constants.PieceEnums.NoPiece or pieceToMoveTeam == Board.Constants.TeamEnum.NoTeam:
            logger.error("Trying to move empty piece or piece with no team, returning empty list")
            return []

        xPotentialCoord = pieceToMoveCoords.GetX()
        yPotentialCoord = pieceToMoveCoords.GetY()

        potentialMoves = []
        for step in range(moveIterations):
            xPotentialCoord += directionVector.GetX()
            yPotentialCoord += directionVector.GetY()
            potentialPoint = BoardPoints(xPotentialCoord, yPotentialCoord)

            if not Utilities.CoordinateConverters.IsPointInRange(potentialPoint):
                # Not in range
                break

            pieceAtCalculatedPosition = board.GetPieceAtCoordinate(BoardPoints(xPotentialCoord, yPotentialCoord))
            if pieceAtCalculatedPosition.GetTeam() == pieceToMoveTeam:
                # Can't move to this position as it's occupied by the same team
                break

            # Differentiate pawns as they have the following properties
            # 1) Can only kill diagonally of the opposite team (NOT vertically)
            # 2) They can only move forward in empty spaces of 1 (and 2 at the beginning)
            if pieceToMovePieceEnum == Pieces.Constants.PieceEnums.Pawn:
                hasTeamAtCalculatedPosition = (pieceAtCalculatedPosition.GetTeam() != Board.Constants.TeamEnum.NoTeam)

                if abs(directionVector.GetX()) == abs(directionVector.GetY()):
                    # Diagonal move, check that the opposite team is at this position (due to earlier if statement
                    # this is equivalent to checking the above boolean
                    if hasTeamAtCalculatedPosition:
                        potentialMoves.append(potentialPoint)
                    else:
                        # no team at calculated position, check for en-passant
                        if MoveHelpers.IsEnPassantMove(piece.GetPieceEnum(), piece.GetCoordinates(), potentialPoint, cls.History.GetLastMove()):
                            potentialMoves.append(potentialPoint)
                else:
                    # Straight move
                    if hasTeamAtCalculatedPosition:
                        break
                    potentialMoves.append(potentialPoint)
            else:
                potentialMoves.append(potentialPoint)
                if pieceAtCalculatedPosition.GetTeam() != Board.Constants.TeamEnum.NoTeam:
                    break

        if len(potentialMoves) == 0:
            return []

        if not enforceKingUnderAttackCheck:
            return potentialMoves

        return MoveHelpers.FilterPieceMovesThatPutPlayerInCheck(board, piece, potentialMoves)

    @staticmethod
    def IsEnPassantMove(pieceMovingEnum, oldPieceCoords, newPotentialCoords, lastMove):
        if lastMove is not None and \
                pieceMovingEnum == PieceEnums.Pawn and \
                lastMove.GetPieceEnumFrom() == PieceEnums.Pawn and \
                lastMove.GetYMovement() == Board.Constants.MAXIMUM_PAWN_FORWARD_MOVEMENT:
            # if previous to moving the y coords match and then this move causes the x coordinates to match
            # then it corresponds to an en-passant move
            if lastMove.GetToCoord().GetY() == oldPieceCoords.GetY() and \
                    lastMove.GetToCoord().GetX() == newPotentialCoords.GetX():
                return True
        return False

    @staticmethod
    def IsCastleMove(pieceEnum, frmOrd: BoardPoints, toOrd:BoardPoints):
        return pieceEnum == PieceEnums.King and \
               abs(frmOrd.GetX() - toOrd.GetX()) == Board.Constants.KING_CASTLE_SQUARE_MOVES

    @staticmethod
    def PrintValidMoves(board, teamToPrint: Board.Constants.TeamEnum):

        for yCoord in range(Board.Constants.MAXIMUM_Y_SQUARES):
            # cycle over y coordinates

            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board.GetPieceAtCoordinate(BoardPoints(xCoord,yCoord))
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
