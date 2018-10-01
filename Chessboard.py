from Pieces.EmptyPiece import EmptyPiece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Constants import TeamEnum
from Utilities.Points import Points
import logging


logger = logging.getLogger(__name__)


class Chessboard:

    MaxXSquares = 8
    MaxYSquares = 8

    def __init__(self):
        logger.debug("Entered constructor")

        # Initialise chess board 2D structure
        self.__board = [None] * Chessboard.MaxXSquares
        for xIndex in range(Chessboard.MaxXSquares):
            # for each y line
            self.__board[xIndex] = [None] * Chessboard.MaxYSquares

        # Set board to initial positions
        self.ResetBoard()

    def ResetBoard(self):

        # Set empty pieces first

        yIndexEmptyPieces = [2, 3, 4, 5]

        for yIndex in yIndexEmptyPieces:
            for xIndex in range(Chessboard.MaxXSquares):
                self.__board[xIndex][yIndex] = EmptyPiece(TeamEnum.NoTeam, Points(xIndex, yIndex))

        yIndexWhitePawns = 1
        for xIndex in range(Chessboard.MaxXSquares):
            self.__board[xIndex][yIndexWhitePawns] = Pawn(TeamEnum.White, Points(xIndex, yIndexWhitePawns))

        yIndexBlackPawns = 6
        for xIndex in range(Chessboard.MaxXSquares):
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

    def GetBoard(self):
        return self.__board

    def PrintBoard(self):
        for yCoord in reversed(range(Chessboard.MaxYSquares)):
            # cycle over y coordinates
            lineToPrint = ""
            for xCoord in range(Chessboard.MaxXSquares):
                lineToPrint += self.__board[xCoord][yCoord].GetPieceStr() + "\t"
            logger.error(lineToPrint)