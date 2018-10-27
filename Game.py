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
from Board.Movement import Movement
from Board.History import History
import logging


logger = logging.getLogger(__name__)


class Game:

    def __init__(self):
        logger.debug("Entered constructor")

        self.__playersTurn = TeamEnum.White
        self.__history = History()

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

        for historicalMove in self.GetHistory().GetHistoricalMoves():
            strToPrint = PieceEnums(historicalMove.GetPieceEnumFrom()).name + " at [" + \
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

    def PerformPostMoveProcessing(self, fromCoord: Points, toCoord: Points):

        logger.debug("Entered method")

        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Points are not in range, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())
            return

        # Update history, check if this was a capture and if so what piece!
        self.GetHistory().AppendMovement(Movement(self.__board[fromCoord.GetX()][fromCoord.GetY()],
                                         self.__board[toCoord.GetX()][toCoord.GetY()],
                                         fromCoord, toCoord))

        # Update board
        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]
        self.__board[toCoord.GetX()][toCoord.GetY()] = pieceBeingMoved
        self.__board[fromCoord.GetX()][fromCoord.GetY()] = EmptyPiece(TeamEnum.NoTeam, fromCoord)

        # Need provision for castling!

        # Check if pawn is being promoted
        self.PerformPawnPromotionCheck()

        # Check if player whose turn it's about to be is checkmated
        opposingTeam = BoardHelpers.GetOpposingTeam(self.__playersTurn)
        isCheckMated = BoardHelpers.IsInCheckMate(self.GetBoard(), opposingTeam)

        # Check draw conditions
        isDraw = BoardHelpers.IsDraw(self.GetBoard(), self.GetHistory().GetHistoricalMoves(), self.__playersTurn)

        # Change players turn
        logger.error(TeamEnum(self.__playersTurn).name + " just finished their turn")
        self.__playersTurn = BoardHelpers.GetOpposingTeam(self.__playersTurn)
        logger.error("Now " + TeamEnum(self.__playersTurn).name + "'s turn")

        self.PrintBoard()

        self.PrintHistory()

    def Move(self, fromCoord: Points, toCoord: Points):

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
