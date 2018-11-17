import logging
import Utilities.CoordinateConverters
import Board.Constants
from Pieces.IBasePiece import IBasePiece
from Pieces.NoPiece import NoPiece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints


logger = logging.getLogger(__name__)


class ChessBoard:

    def __init__(self):
        logger.debug("Entered constructor")

        # Initialise chess board 2D structure
        self.__board = [None] * Board.Constants.MAXIMUM_X_SQUARES
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            # for each y line
            self.__board[xIndex] = [None] * Board.Constants.MAXIMUM_Y_SQUARES

        # Set board to initial positions
        self.ResetToDefault()

    def UpdatePieceOnBoard(self, piece: IBasePiece):
        pieceCoords = piece.GetCoordinates()

        if not Utilities.CoordinateConverters.IsPointInRange(pieceCoords):
            logger.error("Not in range, pieceCoords: " + pieceCoords.ToString())

        self.__board[pieceCoords.GetX()][pieceCoords.GetY()] = piece

    def GetPieceAtCoordinate(self, pieceCoords:BoardPoints):
        if not Utilities.CoordinateConverters.IsPointInRange(pieceCoords):
            logger.error("Not in range, pieceCoords: " + pieceCoords.ToString())
            return None

        return self.__board[pieceCoords.GetX()][pieceCoords.GetY()]

    def ResetToDefault(self):

        logger.debug("Entered ResetBoard")
        # Set empty pieces first

        yIndexNoPieces = [2, 3, 4, 5]

        for yIndex in yIndexNoPieces:
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                self.UpdatePieceOnBoard(NoPiece(BoardPoints(xIndex, yIndex)))

        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            self.UpdatePieceOnBoard(Pawn(TeamEnum.White, BoardPoints(xIndex, Board.Constants.WHITE_PAWNS_Y_ARRAY_COORDINATE)))

        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            self.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(xIndex, Board.Constants.BLACK_PAWNS_Y_ARRAY_COORDINATE)))

        # White major pieces
        self.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(0, 0)))
        self.UpdatePieceOnBoard(Rook(TeamEnum.White, BoardPoints(7, 0)))

        self.UpdatePieceOnBoard(Knight(TeamEnum.White, BoardPoints(1, 0)))
        self.UpdatePieceOnBoard(Knight(TeamEnum.White, BoardPoints(6, 0)))

        self.UpdatePieceOnBoard(Bishop(TeamEnum.White, BoardPoints(2, 0)))
        self.UpdatePieceOnBoard(Bishop(TeamEnum.White, BoardPoints(5, 0)))

        self.UpdatePieceOnBoard(Queen(TeamEnum.White, BoardPoints(3, 0)))
        self.UpdatePieceOnBoard(King(TeamEnum.White, BoardPoints(4, 0)))

        # Black Major pieces
        self.UpdatePieceOnBoard(Rook(TeamEnum.Black, BoardPoints(0, 7)))
        self.UpdatePieceOnBoard(Rook(TeamEnum.Black, BoardPoints(7, 7)))

        self.UpdatePieceOnBoard(Knight(TeamEnum.Black, BoardPoints(1, 7)))
        self.UpdatePieceOnBoard(Knight(TeamEnum.Black, BoardPoints(6, 7)))

        self.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(2, 7)))
        self.UpdatePieceOnBoard(Bishop(TeamEnum.Black, BoardPoints(5, 7)))

        self.UpdatePieceOnBoard(Queen(TeamEnum.Black, BoardPoints(3, 7)))
        self.UpdatePieceOnBoard(King(TeamEnum.Black, BoardPoints(4, 7)))

        logger.debug("End ResetBoard")

    def RemoveAllPieces(self):
        for yCoord in reversed(range(Board.Constants.MAXIMUM_Y_SQUARES)):
            # cycle over y coordinates
            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                self.UpdatePieceOnBoard(NoPiece(BoardPoints(xCoord, yCoord)))

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
                lineToPrint += self.GetPieceAtCoordinate(BoardPoints(xCoord, yCoord)).GetPieceStr() + "\t"
            lineToPrint += "  " + boardReferenceNumericalDigits
            logger.error(lineToPrint)

        # Bottom reference coordinates
        logger.error("")
        logger.error(boardReferenceAlphabeticalDigits)
