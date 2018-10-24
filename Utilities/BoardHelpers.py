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

    # Due to three part nature of the TeamEnum, this functions gets black team when white is fed, otherwise white
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
    # Direction vector is the direction with which to move.
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

    # Gets all valid moves for the team, this takes into account moves which result in the player being in check
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

    @staticmethod
    def GetPieces(board, currentTeam:Board.Constants.TeamEnum):
        piecesCurrentTeam = []
        piecesOtherTeam = []

        otherTeam = BoardHelpers.GetOpposingTeam(currentTeam)
        for yIndex in range(Board.Constants.MAXIMUM_Y_SQUARES):
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board[xIndex][yIndex]
                if piece.GetTeam() == currentTeam:
                    piecesCurrentTeam.append(piece)
                if piece.GetTeam() == otherTeam:
                    piecesOtherTeam.append(piece)
        return piecesCurrentTeam, piecesOtherTeam

    @staticmethod
    def IsInCheckMate(board, team: TeamEnum):

        logger.debug("Entered")
        # Check if King is in check and that there are NO valid moves
        validMoves = BoardHelpers.GetValidMovesForTeam(board, team)
        if len(validMoves) == 0:
            return False

        isKingInCheck = BoardHelpers.IsKingInCheck(board, team)
        return isKingInCheck

    # Checkmate will not be possible for certain piece configurations, they are:
    # a) King vs King
    # b) King and Bishop vs King
    # c) King and Knight vs King
    # d) King and Bishop versus King and Bishop with Bishops on same color.
    @staticmethod
    def IsDrawByInsufficientPieces(board, currentTeam):

        logger.debug("Entered")
        teamAPieces, teamBPieces = BoardHelpers.GetPieces(board, currentTeam)

        numberOfPiecesTeamA = len(teamAPieces)
        numberOfPiecesTeamB = len(teamBPieces)

        if numberOfPiecesTeamA > 2 and numberOfPiecesTeamB > 2:
            return False

        # King vs King
        if numberOfPiecesTeamA == 1 and numberOfPiecesTeamB == 1:
            return True

        # King and Bishop vs King and King and Knight vs King
        if numberOfPiecesTeamA == 1 and numberOfPiecesTeamB == 2:
            for piece in teamBPieces:
                if piece.GetPieceEnum() == Pieces.Constants.PieceEnums.Bishop or piece.GetPieceEnum() == Pieces.Constants.PieceEnums.Knight:
                    return True

        if numberOfPiecesTeamB == 1 and numberOfPiecesTeamA == 2:
            for piece in teamAPieces:
                if piece.GetPieceEnum() == Pieces.Constants.PieceEnums.Bishop or piece.GetPieceEnum() == Pieces.Constants.PieceEnums.Knight:
                    return True

        # King and Bishop versus King and Bishop with Bishops on same color
        if numberOfPiecesTeamA == 2 and numberOfPiecesTeamB == 2:
            teamABishop = None
            teamBBishop = None
            for pieceForTeamA in teamAPieces:
                if pieceForTeamA.GetPieceEnum() == Pieces.Constants.PieceEnums.Bishop:
                    teamABishop = pieceForTeamA
            for pieceForTeamB in teamBPieces:
                if pieceForTeamB.GetPieceEnum() == Pieces.Constants.PieceEnums.Bishop:
                    teamBBishop = pieceForTeamB

            if teamABishop is not None and teamBBishop is not None:
                # Two bishops remaining, test to see if they are on the same color
                teamABishopCoords = teamABishop.GetCoordinates()
                teamBBishopCoords = teamBBishop.GetCoordinates()

                # Check that both are on light squares
                if (teamABishopCoords.GetX() % 2) == (teamABishopCoords.GetY() % 2) and \
                        (teamBBishopCoords.GetX() % 2) == (teamBBishopCoords.GetY() % 2):
                    return True
                elif (teamABishopCoords.GetX() % 2) != (teamABishopCoords.GetY() % 2) and \
                        (teamBBishopCoords.GetX() % 2) != (teamBBishopCoords.GetY() % 2):
                    return True

        return False

    @staticmethod
    def IsDraw(board, history, currentTeam: TeamEnum):
        logger.debug("Entered")

        opposingTeam = BoardHelpers.GetOpposingTeam(currentTeam)
        # If player whose turn it will now be has no legal move but is not in check
        validMovesOpposingTeam = BoardHelpers.GetValidMovesForTeam(board, opposingTeam)
        if len(validMovesOpposingTeam) == 0 and not BoardHelpers.IsKingInCheck(board, opposingTeam):
            logger.error("Player whose turn it is has no legal move and is now in check, returning False")
            return False

        # Fifty move rule: If previous 50 moves by EACH side, no pawn has moved and no capture has been made
        if len(history) > Board.Constants.DRAW_CONDITION_TOTAL_MOVES:

            # Get last x moves
            pertinentMoves = history[-Board.Constants.DRAW_CONDITION_TOTAL_MOVES:]

            hasPawnMoved = False
            hasCaptureBeenMade = False

            for move in pertinentMoves:
                if move.IsCaptureMove():
                    hasCaptureBeenMade = True
                    break

                if move.GetPieceFrom() == Pieces.Constants.PieceEnums.Pawn:
                    hasPawnMoved = True
                    break

            if not hasPawnMoved and not hasCaptureBeenMade:
                logger.error("No capture or pawn move in last n moves, draw declared, returning True")
                return True

        if BoardHelpers.IsDrawByInsufficientPieces(board, currentTeam):
            logger.error("Draw by insufficient pieces is declared, returning True")
            return True

        logger.debug("No Draw, returning False")
        return False
