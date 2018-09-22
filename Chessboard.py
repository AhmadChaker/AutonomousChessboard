from Pieces.EmptyPiece import EmptyPiece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from Pieces.Constants import TeamEnum
import logging
logger = logging.getLogger(__name__)

MaxXSquares = 8
MaxYSquares = 8


class ChessBoard:
    def __init__(self):
        logger.debug("Entered constructor")

        # Initialise chess board 2D structure
        self.__board = [None] * MaxXSquares
        for xIndex in range(MaxXSquares):
            # for each y line
            self.__board[xIndex] = [EmptyPiece(TeamEnum.Empty)]*MaxYSquares

        # Set board to initial positions
        self.ResetBoard()

    def ResetBoard(self):
        self.__board[0][0] = Rook(TeamEnum.White)
        self.__board[7][0] = Rook(TeamEnum.White)

        self.__board[1][0] = Knight(TeamEnum.White)
        self.__board[6][0] = Knight(TeamEnum.White)

        self.__board[2][0] = Bishop(TeamEnum.White)
        self.__board[5][0] = Bishop(TeamEnum.White)

        self.__board[3][0] = King(TeamEnum.White)
        self.__board[4][0] = Queen(TeamEnum.White)

        yIndexWhitePawns = 1
        for xIndex in range(MaxXSquares):
            self.__board[xIndex][yIndexWhitePawns] = Pawn(TeamEnum.White)

        yIndexBlackPawns = 6
        for xIndex in range(MaxXSquares):
            self.__board[xIndex][yIndexBlackPawns] = Pawn(TeamEnum.Black)

        self.__board[0][7] = Rook(TeamEnum.Black)
        self.__board[7][7] = Rook(TeamEnum.Black)

        self.__board[1][7] = Knight(TeamEnum.Black)
        self.__board[6][7] = Knight(TeamEnum.Black)

        self.__board[2][7] = Bishop(TeamEnum.Black)
        self.__board[5][7] = Bishop(TeamEnum.Black)

        self.__board[3][7] = King(TeamEnum.Black)
        self.__board[4][7] = Queen(TeamEnum.Black)

    def GetBoard(self):
        return self.__board

    def PrintBoard(self):
        for yCoord in reversed(range(MaxYSquares)):
            # cycle over y coordinates
            lineToPrint = ""
            for xCoord in range(MaxXSquares):
                lineToPrint += self.__board[xCoord][yCoord].GetPieceStr() + "\t"
            logger.error(lineToPrint)
