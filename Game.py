import Utilities.Points
import Utilities.CoordinateConverters
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Pieces.EmptyPiece import EmptyPiece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from Board.Constants import TeamEnum
from Pieces.Constants import PieceEnums
from Utilities.Points import Points
from Board.History import History
import logging


logger = logging.getLogger(__name__)


class Game:

    def __init__(self):
        logger.debug("Entered constructor")

        self.__playersTurn = TeamEnum.White
        self.__history = []

        # Initialise chess board 2D structure
        self.__board = [None] * Board.Constants.MAXIMUM_X_SQUARES
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            # for each y line
            self.__board[xIndex] = [None] * Board.Constants.MAXIMUM_Y_SQUARES

        # Set board to initial positions
        self.ResetBoard()

    def GetHistory(self):
        return self.__history

    def ResetBoard(self):

        logger.debug("Entered ResetBoard")
        # Set empty pieces first

        yIndexEmptyPieces = [2, 3, 4, 5]

        for yIndex in yIndexEmptyPieces:
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                self.__board[xIndex][yIndex] = EmptyPiece(TeamEnum.NoTeam, Points(xIndex, yIndex))

        yIndexWhitePawns = 1
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            self.__board[xIndex][yIndexWhitePawns] = Pawn(TeamEnum.White, Points(xIndex, yIndexWhitePawns))

        yIndexBlackPawns = 6
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            self.__board[xIndex][yIndexBlackPawns] = Pawn(TeamEnum.Black, Points(xIndex, yIndexBlackPawns))

        # White major pieces
        self.__board[0][0] = Rook(TeamEnum.White, Points(0, 0))
        self.__board[7][0] = Rook(TeamEnum.White, Points(7, 0))

        self.__board[1][0] = Knight(TeamEnum.White, Points(1, 0))
        self.__board[6][0] = Knight(TeamEnum.White, Points(6, 0))

        self.__board[2][0] = Bishop(TeamEnum.White, Points(2, 0))
        self.__board[5][0] = Bishop(TeamEnum.White, Points(5, 0))

        self.__board[3][0] = Queen(TeamEnum.White, Points(3, 0))
        self.__board[4][0] = King(TeamEnum.White, Points(4, 0))

        self.__board[0][7] = Rook(TeamEnum.Black, Points(0, 7))
        self.__board[7][7] = Rook(TeamEnum.Black, Points(7, 7))

        # Black Major pieces
        self.__board[1][7] = Knight(TeamEnum.Black, Points(1, 7))
        self.__board[6][7] = Knight(TeamEnum.Black, Points(6, 7))

        self.__board[2][7] = Bishop(TeamEnum.Black, Points(2, 7))
        self.__board[5][7] = Bishop(TeamEnum.Black, Points(5, 7))

        self.__board[3][7] = Queen(TeamEnum.Black, Points(3, 7))
        self.__board[4][7] = King(TeamEnum.Black, Points(4, 7))

        logger.debug("End ResetBoard")

    def GetBoard(self):
        return self.__board

    def PrintBoard(self):

        # Top reference coordinates
        boardReferenceAlphabeticalDigits = "\t\t"
        for index in range(len(Board.Constants.ALPHABETICAL_BOARD_ORDINATES)):
            boardReferenceAlphabeticalDigits += Board.Constants.ALPHABETICAL_BOARD_ORDINATES[index] + "|" + str(index) + "\t"

        logger.error(boardReferenceAlphabeticalDigits)
        logger.error("")

        for yCoord in reversed(range(Board.Constants.MAXIMUM_Y_SQUARES)):
            # cycle over y coordinates
            boardReferenceNumericalDigits = str(yCoord+1) + "|" + str(yCoord) + "\t"
            lineToPrint = boardReferenceNumericalDigits
            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                lineToPrint += self.__board[xCoord][yCoord].GetPieceStr() + "\t"
            lineToPrint += "  " + boardReferenceNumericalDigits
            logger.error(lineToPrint)

        # Bottom reference coordinates
        logger.error("")
        logger.error(boardReferenceAlphabeticalDigits)

        self.PrintAllValidMoves()

    def PrintHistory(self):
        logger.error("Printing history")

        for historicalMove in self.GetHistory():
            strToPrint = PieceEnums(historicalMove.GetPieceFrom()).name + " at [" + \
                         historicalMove.GetFromCoord().ToString() + "] moved to [" + \
                         historicalMove.GetToCoord().ToString() + "], IsCaptureMove: " + \
                         str(historicalMove.IsCaptureMove())
            logger.error(strToPrint)

    def CanMove(self, fromCoord: Points, toCoord: Points):

        logger.debug("Entered, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())

        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not \
                Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Exiting CanMove prematurely, FromCoord: " + fromCoord.ToString() +
                         ", ToCoord: " + toCoord.ToString())
            return False

        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]

        isValidPieceMove = pieceBeingMoved.CanMove(toCoord, self.__board)
        if not isValidPieceMove:
            logger.debug("Not a valid piece move, returning false")
            return False

        logger.debug("Exiting method with value True")
        return True

    def PerformPawnPromotionCheck(self):
        # Use the fact that a pawn promotion only occurs for one pawn at a time and on the top or bottom squares
        yIndexPawnPromotions = [0, Board.Constants.MAXIMUM_Y_SQUARES - 1]
        for yIndex in yIndexPawnPromotions:
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = self.__board[xIndex][yIndex]
                if piece.GetPieceEnum() == PieceEnums.Pawn:
                    self.__board[xIndex][yIndex] = Queen(piece.GetTeam(), Points(xIndex, yIndex))

    def GetPieces(self, board):
        piecesCurrentTeam = []
        piecesOtherTeam = []

        currentTeam = self.__playersTurn
        otherTeam = BoardHelpers.GetOpposingTeam(currentTeam)
        for yIndex in range(Board.Constants.MAXIMUM_Y_SQUARES):
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = board[xIndex][yIndex]
                if piece.GetTeam() == currentTeam:
                    piecesCurrentTeam.append(piece)
                if piece.GetTeam() == otherTeam:
                    piecesOtherTeam.append(piece)
        return piecesCurrentTeam, piecesOtherTeam

    def IsInCheckMate(self, team: TeamEnum):
        # Check if King is in check and that there are NO valid moves
        validMoves = BoardHelpers.GetValidMovesForTeam(self.__board, team)
        if len(validMoves) == 0:
            return False

        isKingInCheck = BoardHelpers.IsKingInCheck(self.__board, team)
        return isKingInCheck

    def IsDrawByInsufficientPieces(self, board):

        # Insufficient pieces for checkmate:
        # a) King vs King
        # b) King and Bishop vs King
        # c) King and Knight vs King
        # d) King and Bishop versus King and Bishop with Bishops on same color.
        teamAPieces, teamBPieces = self.GetPieces(board)

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
                if piece.GetPieceEnum() == PieceEnums.Bishop or piece.GetPieceEnum() == PieceEnums.Knight:
                    return True

        if numberOfPiecesTeamB == 1 and numberOfPiecesTeamA == 2:
            for piece in teamAPieces:
                if piece.GetPieceEnum() == PieceEnums.Bishop or piece.GetPieceEnum() == PieceEnums.Knight:
                    return True

        # King and Bishop versus King and Bishop with Bishops on same color
        if numberOfPiecesTeamA == 2 and numberOfPiecesTeamB == 2:
            teamABishop = None
            teamBBishop = None
            for pieceForTeamA in teamAPieces:
                if pieceForTeamA.GetPieceEnum() == PieceEnums.Bishop:
                    teamABishop = pieceForTeamA
            for pieceForTeamB in teamBPieces:
                if pieceForTeamB.GetPieceEnum() == PieceEnums.Bishop:
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

    def IsDraw(self, opposingTeam: TeamEnum):
        logger.debug("Entered")

        # If player whose turn it will now be has no legal move but is not in check
        validMovesOpposingTeam = BoardHelpers.GetValidMovesForTeam(self.__board, opposingTeam)
        if len(validMovesOpposingTeam) == 0 and not self.IsKingInCheck(self.GetBoard(), opposingTeam):
            logger.error("Player whose turn it is has no legal move and is now in check")
            return True

        # Fifty move rule: If previous 50 moves by EACH side, no pawn has moved and no capture has been made
        history = self.GetHistory()
        if len(history) > Board.Constants.DRAW_CONDITION_TOTAL_MOVES:

            # Get last x moves
            pertinentMoves = history[-Board.Constants.DRAW_CONDITION_TOTAL_MOVES:]

            hasPawnMoved = False
            hasCaptureBeenMade = False

            for move in pertinentMoves:
                if move.IsCaptureMove():
                    hasCaptureBeenMade = True
                    break

                if move.GetPieceFrom() == PieceEnums.Pawn:
                    hasPawnMoved = True
                    break

            if not hasPawnMoved and not hasCaptureBeenMade:
                logger.error("No capture or pawn move in last n moves, draw declared")
                return True

        if self.IsDrawByInsufficientPieces(self.GetBoard()):
            logger.error("Draw by insufficient pieces is declared")
            return True

        return False

    def PerformPostMoveProcessing(self, fromCoord: Points, toCoord: Points):

        logger.debug("Entered method")

        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Points are not in range, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())
            return

        # Update history, check if this was a capture and if so what piece!
        self.GetHistory().append(History(self.__board[fromCoord.GetX()][fromCoord.GetY()].GetPieceEnum(),
                                         self.__board[toCoord.GetX()][toCoord.GetY()].GetPieceEnum(),
                                         fromCoord, toCoord))

        # Update board
        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]
        self.__board[toCoord.GetX()][toCoord.GetY()] = pieceBeingMoved

        # Need provision for castling!
        self.__board[fromCoord.GetX()][fromCoord.GetY()] = EmptyPiece(TeamEnum.NoTeam, fromCoord)

        # Check if pawn is being promoted
        self.PerformPawnPromotionCheck()

        # Check if player whos turn it's about to be is checkmated
        opposingTeam = BoardHelpers.GetOpposingTeam(self.__playersTurn)
        isCheckMated = self.IsInCheckMate(opposingTeam)

        # Check draw conditions
        self.IsDraw(opposingTeam)

        # Change players turn
        logger.error(TeamEnum(self.__playersTurn).name + " just finished their turn")
        self.__playersTurn = BoardHelpers.GetOpposingTeam(self.__playersTurn)
        logger.error("Now " + TeamEnum(self.__playersTurn).name + "'s turn")

        self.PrintBoard()

        self.PrintHistory()

    def Move(self, fromCoord: Points, toCoord:Points):

        logger.debug("Entered, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())

        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not \
                Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Exiting prematurely, fromCoord or toCoord are not in range, exiting prematurely, FromCoord: "
                         + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())

        # Check persons turn!
        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]
        if pieceBeingMoved.GetTeam() != self.__playersTurn:
            logger.error("Not this players turn, not moving!")
            return False

        if not self.CanMove(fromCoord, toCoord):
            logger.error("Can't move piece to requested coordinated, FromCoord: " + fromCoord.ToString() +
                         ", ToCoord: " + toCoord.ToString())
            return False

        # Move piece! Now update the board
        hasMoved = pieceBeingMoved.Move(toCoord, self.__board)

        if hasMoved:
            self.PerformPostMoveProcessing(fromCoord, toCoord)

        logger.debug("Exiting with argument: " + str(hasMoved))
        return hasMoved

    def PrintAllValidMoves(self):
        logger.info("Printing all valid white moves")

        BoardHelpers.GetValidMovesForTeam(self.GetBoard(), Board.Constants.TeamEnum.White)
        #self.GetValidMovesForTeam(self.GetBoard(), Utilities.Constants.TeamEnum.Black)
