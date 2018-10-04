import Utilities.Points
import Utilities.CoordinateConverters
from Pieces.EmptyPiece import EmptyPiece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from Utilities.Constants import TeamEnum
from Utilities.Points import Points
import logging


logger = logging.getLogger(__name__)


class Game:

    MaxXSquares = 8
    MaxYSquares = 8

    def __init__(self):
        logger.debug("Entered constructor")

        self.__playersTurn = TeamEnum.White

        # Initialise chess board 2D structure
        self.__board = [None] * Game.MaxXSquares
        for xIndex in range(Game.MaxXSquares):
            # for each y line
            self.__board[xIndex] = [None] * Game.MaxYSquares

        # Set board to initial positions
        self.ResetBoard()

    def ResetBoard(self):

        logger.debug("Entered ResetBoard")
        # Set empty pieces first

        yIndexEmptyPieces = [2, 3, 4, 5]

        for yIndex in yIndexEmptyPieces:
            for xIndex in range(Game.MaxXSquares):
                self.__board[xIndex][yIndex] = EmptyPiece(TeamEnum.NoTeam, Points(xIndex, yIndex))

        yIndexWhitePawns = 1
        for xIndex in range(Game.MaxXSquares):
            self.__board[xIndex][yIndexWhitePawns] = Pawn(TeamEnum.White, Points(xIndex, yIndexWhitePawns))

        yIndexBlackPawns = 6
        for xIndex in range(Game.MaxXSquares):
            self.__board[xIndex][yIndexBlackPawns] = Pawn(TeamEnum.Black, Points(xIndex, yIndexBlackPawns))

        # White major pieces
        self.__board[0][0] = Rook(TeamEnum.White, Points(0, 0))
        self.__board[7][0] = Rook(TeamEnum.White, Points(7, 0))

        self.__board[1][0] = Knight(TeamEnum.White, Points(1, 0))
        self.__board[6][0] = Knight(TeamEnum.White, Points(6, 0))

        self.__board[2][0] = Bishop(TeamEnum.White, Points(2, 0))
        self.__board[5][0] = Bishop(TeamEnum.White, Points(5, 0))

        self.__board[3][0] = King(TeamEnum.White, Points(3, 0))
        self.__board[4][0] = Queen(TeamEnum.White, Points(4, 0))

        self.__board[0][7] = Rook(TeamEnum.Black, Points(0, 7))
        self.__board[7][7] = Rook(TeamEnum.Black, Points(7, 7))

        # Black Major pieces
        self.__board[1][7] = Knight(TeamEnum.Black, Points(1, 7))
        self.__board[6][7] = Knight(TeamEnum.Black, Points(6, 7))

        self.__board[2][7] = Bishop(TeamEnum.Black, Points(2, 7))
        self.__board[5][7] = Bishop(TeamEnum.Black, Points(5, 7))

        self.__board[3][7] = King(TeamEnum.Black, Points(3, 7))
        self.__board[4][7] = Queen(TeamEnum.Black, Points(4, 7))

        logger.debug("End ResetBoard")

    def GetBoard(self):
        return self.__board

    def PrintBoard(self):

        # Top reference coordinates
        boardReferenceAlphabeticalDigits = "\t"
        for alphaOrdinate in Utilities.Constants.ALPHABETICAL_BOARD_ORDINATES:
            boardReferenceAlphabeticalDigits += alphaOrdinate + "\t"

        logger.error(boardReferenceAlphabeticalDigits)

        for yCoord in reversed(range(Game.MaxYSquares)):
            # cycle over y coordinates
            boardReferenceNumericalDigit = str(yCoord+1)
            lineToPrint = boardReferenceNumericalDigit + "\t"
            for xCoord in range(Game.MaxXSquares):
                lineToPrint += self.__board[xCoord][yCoord].GetPieceStr() + "\t"
            lineToPrint += boardReferenceNumericalDigit
            logger.error(lineToPrint)

        # Bottom reference coordinates
        logger.error(boardReferenceAlphabeticalDigits)

    def CanMove(self, fromCoord: Points, toCoord: Points):

        logger.debug("Entered, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())

        if fromCoord == Utilities.Points.POINTS_UNDEFINED or toCoord == Utilities.Points.POINTS_UNDEFINED:
            logger.error("Exiting CanMove prematurely, FromCoord: " + fromCoord.ToString() +
                         ", ToCoord: " + toCoord.ToString())
            return False

        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]

        canMove = pieceBeingMoved.CanMove(toCoord)

        logger.debug("Exiting with argument: " + str(canMove))
        return canMove

    def __UpdateBoardWithMove(self, fromCoord: Points, toCoord: Points):

        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Point not in range returning")
            return

        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]
        self.__board[toCoord.GetX()][toCoord.GetY()] = pieceBeingMoved

        # Need provision for castling!
        self.__board[fromCoord.GetX()][fromCoord.GetY()] = EmptyPiece(TeamEnum.NoTeam, fromCoord)

        self.PrintBoard()

        logger.error(TeamEnum(self.__playersTurn).name + " just finished their turn")
        self.__playersTurn = (TeamEnum.Black if self.__playersTurn == TeamEnum.White else TeamEnum.White)
        logger.error("Now " + TeamEnum(self.__playersTurn).name + "'s turn")

    def Move(self, fromCoord: Points, toCoord:Points):

        logger.debug("Entered, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())

        if fromCoord == Utilities.Points.POINTS_UNDEFINED or toCoord == Utilities.Points.POINTS_UNDEFINED:
            logger.error("Exiting CanMove prematurely, FromCoord: " + fromCoord.ToString() +
                         ", ToCoord: " + toCoord.ToString())
            return False

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
        hasMoved = pieceBeingMoved.Move(toCoord)

        if hasMoved:
            self.__UpdateBoardWithMove(fromCoord, toCoord)


        logger.debug("Exiting with argument: " + str(hasMoved))
        return hasMoved


