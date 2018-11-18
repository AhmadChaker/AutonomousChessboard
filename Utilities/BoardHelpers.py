import Pieces.IBasePiece
import Pieces.Constants
import Board.Constants
import Board.Constants
import logging
from Miscellaneous.BoardPoints import BoardPoints
from Board.Constants import TeamEnum
from Board.History import History
from Pieces.Constants import PieceEnums
from Utilities.MoveHelpers import MoveHelpers


logger = logging.getLogger(__name__)


class BoardHelpers:

    @classmethod
    def UpdateVariables(cls, history: History):
        cls.History = history

    # Due to three part nature of the TeamEnum, this functions gets black team when white is fed, otherwise white
    @staticmethod
    def GetOpposingTeam(team: TeamEnum):
        if team == TeamEnum.NoTeam:
            return TeamEnum.NoTeam
        return TeamEnum.Black if team == TeamEnum.White else TeamEnum.White

    @staticmethod
    def GetPieceByPieceType(board, pieceType, team: Board.Constants.TeamEnum):
        pieces = []
        for yCoord in range(Board.Constants.MAXIMUM_Y_SQUARES):
            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board.GetPieceAtCoordinate(BoardPoints(xCoord,yCoord))
                if piece.GetTeam() == team and piece.GetPieceEnum() == pieceType:
                    pieces.append(piece)
        return pieces

    # For the team passed in, check if that King is in check
    @staticmethod
    def IsInCheck(board, teamA: Board.Constants.TeamEnum):
        teamAKingArray = BoardHelpers.GetPieceByPieceType(board, Pieces.Constants.PieceEnums.King, teamA)
        if len(teamAKingArray) == 0:
            # Should never happen really
            logger.error("Can't find a King for this team! Something horrible has happened")
            return True

        teamAKing = teamAKingArray[0]
        teamB = BoardHelpers.GetOpposingTeam(teamA)
        teamBMoves = MoveHelpers.GetPieceCentricMovesForTeam(board, teamB)
        for teamBMove in teamBMoves:
            if teamBMove == teamAKing.GetCoordinates():
                return True
        return False

    @staticmethod
    def GetTeamPieceCounts(board, currentTeam:Board.Constants.TeamEnum):
        count = 0
        for yIndex in range(Board.Constants.MAXIMUM_Y_SQUARES):
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board.GetPieceAtCoordinate(BoardPoints(xIndex, yIndex))
                if piece.GetTeam() == currentTeam:
                    count = count + 1
        return count

    @staticmethod
    def IsInCheckMate(board, team: TeamEnum):
        logger.debug("Entered")
        # Check if King is in check and that there are NO valid moves
        validMoves = MoveHelpers.GetValidMovesForTeam(board, team)
        isInCheck = BoardHelpers.IsInCheck(board, team)
        if len(validMoves) == 0 and isInCheck:
            return True
        return False

    # Checkmate will not be possible for certain piece configurations, they are:
    # a) King vs King
    # b) King and Bishop vs King
    # c) King and Knight vs King
    # d) King and Bishop versus King and Bishop with Bishops on same color.
    @staticmethod
    def IsDrawByInsufficientPieces(board, currentTeam):

        logger.debug("Entered")
        opposingTeam = BoardHelpers.GetOpposingTeam(currentTeam)

        pieceCountCurrentTeam = BoardHelpers.GetTeamPieceCounts(board, currentTeam)
        pieceCountOtherTeam = BoardHelpers.GetTeamPieceCounts(board, opposingTeam)

        # Short circuit
        if pieceCountCurrentTeam > 2 or pieceCountOtherTeam > 2:
            return False

        # King vs King
        if pieceCountCurrentTeam == 1 and pieceCountOtherTeam == 1:
            return True

        # Remaining cases:  2-2, 2-1, 1-2

        knightsCurrentTeam = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Knight, currentTeam)
        bishopsCurrentTeam = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Bishop, currentTeam)
        knightsOtherTeam = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Knight, opposingTeam)
        bishopsOtherTeam = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Bishop, opposingTeam)

        # 1) King and Bishop vs King is a draw
        # 2) King and Knight vs King is a draw
        if pieceCountCurrentTeam == 1:
            # current team only has king, the other team has knight or a bishop
            if len(knightsOtherTeam) == 1 or len(bishopsOtherTeam) == 1:
                return True

        if pieceCountOtherTeam == 1:
            if len(knightsCurrentTeam) == 1 or len(bishopsCurrentTeam) == 1:
                return True

        # King and Bishop versus King and Bishop with Bishops on same color
        if len(bishopsCurrentTeam) == 1 and len(bishopsOtherTeam) == 1:
            currentTeamBishopCoords = bishopsCurrentTeam[0].GetCoordinates()
            otherTeamBishopCoords = bishopsOtherTeam[0].GetCoordinates()

            # Check that both are on same square squares
            if (currentTeamBishopCoords.GetX() % 2) == (currentTeamBishopCoords.GetY() % 2) and \
                    (otherTeamBishopCoords.GetX() % 2) == (otherTeamBishopCoords.GetY() % 2):
                return True
            elif (currentTeamBishopCoords.GetX() % 2) != (currentTeamBishopCoords.GetY() % 2) and \
                    (otherTeamBishopCoords.GetX() % 2) != (otherTeamBishopCoords.GetY() % 2):
                return True

        return False

    # If in the previous 75 moves by EACH side, no pawn has moved and no capture has been made
    @staticmethod
    def IsDrawBySeventyFiveMovesEachRule(history):
        if len(history) >= Board.Constants.DRAW_CONDITION_TOTAL_MOVES:
            # Get last x moves
            pertinentMoves = history[-Board.Constants.DRAW_CONDITION_TOTAL_MOVES:]

            hasPawnMoved = False
            hasCaptureBeenMade = False

            for move in pertinentMoves:
                if move.IsCaptureMove():
                    hasCaptureBeenMade = True
                    break

                if move.GetPieceEnumFrom() == Pieces.Constants.PieceEnums.Pawn:
                    hasPawnMoved = True
                    break

            if not hasPawnMoved and not hasCaptureBeenMade:
                logger.error("No capture or pawn move in last n moves, draw declared, returning True")
                return True
        return False

    @staticmethod
    def IsDraw(board, history, currentTeam: TeamEnum):
        logger.debug("Entered")

        opposingTeam = BoardHelpers.GetOpposingTeam(currentTeam)

        # Player whose turn it will now be has no legal moves but is not in check
        validMovesOpposingTeam = MoveHelpers.GetValidMovesForTeam(board, opposingTeam)
        isInCheck = BoardHelpers.IsInCheck(board, opposingTeam)

        if len(validMovesOpposingTeam) == 0 and not isInCheck:
            logger.error("Player whose turn it is has no legal move and is not in check, returning True")
            return True

        if BoardHelpers.IsDrawBySeventyFiveMovesEachRule(history):
            logger.error("Draw by 75 moves rule, returning True")
            return True

        if BoardHelpers.IsDrawByInsufficientPieces(board, currentTeam):
            logger.error("Draw by insufficient pieces is declared, returning True")
            return True

        logger.debug("No Draw, returning False")
        return False
