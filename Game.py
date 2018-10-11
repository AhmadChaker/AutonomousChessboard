import sys
import Utilities.Points
import Utilities.CoordinateConverters
import Utilities.Constants
import Pieces.Constants
from copy import deepcopy
from Pieces.EmptyPiece import EmptyPiece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from Utilities.Constants import TeamEnum
from Pieces.Constants import PieceEnums
from Utilities.Points import Points
import logging


logger = logging.getLogger(__name__)


class Game:

    def __init__(self):
        logger.debug("Entered constructor")

        self.__playersTurn = TeamEnum.White

        # Initialise chess board 2D structure
        self.__board = [None] * Utilities.Constants.MAXIMUM_X_SQUARES
        for xIndex in range(Utilities.Constants.MAXIMUM_X_SQUARES):
            # for each y line
            self.__board[xIndex] = [None] * Utilities.Constants.MAXIMUM_Y_SQUARES

        # Set board to initial positions
        self.ResetBoard()

    def ResetBoard(self):

        logger.debug("Entered ResetBoard")
        # Set empty pieces first

        yIndexEmptyPieces = [2, 3, 4, 5]

        for yIndex in yIndexEmptyPieces:
            for xIndex in range(Utilities.Constants.MAXIMUM_X_SQUARES):
                self.__board[xIndex][yIndex] = EmptyPiece(TeamEnum.NoTeam, Points(xIndex, yIndex))

        yIndexWhitePawns = 1
        for xIndex in range(Utilities.Constants.MAXIMUM_X_SQUARES):
            self.__board[xIndex][yIndexWhitePawns] = Pawn(TeamEnum.White, Points(xIndex, yIndexWhitePawns))

        yIndexBlackPawns = 6
        for xIndex in range(Utilities.Constants.MAXIMUM_X_SQUARES):
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

    # This method gets all legal moves from the piece's perspective, this does not take into account board
    # considerations such as being in check
    @staticmethod
    def GetPieceCentricMovesForTeam(board, teamToGet: Utilities.Constants.TeamEnum):
        moves = []
        for yCoord in range(Utilities.Constants.MAXIMUM_Y_SQUARES):
            # cycle over y coordinates

            for xCoord in range(Utilities.Constants.MAXIMUM_X_SQUARES):
                piece = board[xCoord][yCoord]
                if piece.GetTeam() != teamToGet:
                    continue

                # Get valid moves from the perspective of the piece independent of the board
                pieceCentricValidMoves = piece.GetValidMoves()
                moves.extend(pieceCentricValidMoves)
        return moves

    @staticmethod
    def GetKing(board, team:Utilities.Constants.TeamEnum):
        for yCoord in range(Utilities.Constants.MAXIMUM_Y_SQUARES):
            for xCoord in range(Utilities.Constants.MAXIMUM_X_SQUARES):
                piece = board[xCoord][yCoord]
                if piece.GetTeam() == team and piece.GetPieceEnum() == Pieces.Constants.PieceEnums.King:
                    return piece
        return Pieces.EmptyPiece()

    # For the team passed in, check if that King is in check
    @staticmethod
    def IsKingInCheck(board, teamA: Utilities.Constants.TeamEnum):

        teamAKing = Game.GetKing(board, teamA)
        teamB = Utilities.Constants.TeamEnum.Black if teamA == Utilities.Constants.TeamEnum.White else \
            Utilities.Constants.TeamEnum.White
        teamBMoves = Game.GetPieceCentricMovesForTeam(board, teamB)
        for teamBMove in teamBMoves:
            if teamBMove == teamAKing.GetCoordinates():
                return True
        return False

    @staticmethod
    def GetValidMovesForTeam(board, teamToPrint: Utilities.Constants.TeamEnum):

        moves = []
        copyBoard = deepcopy(board)
        for yCoord in range(Utilities.Constants.MAXIMUM_Y_SQUARES):
            # cycle over y coordinates

            for xCoord in range(Utilities.Constants.MAXIMUM_X_SQUARES):
                piece = copyBoard[xCoord][yCoord]
                if piece.GetTeam() != teamToPrint:
                    continue

                # Get valid moves for this piece, if this move results in the King being in check, then it's not
                # actually a valid move
                validPieceCentricMoves = piece.GetValidMoves()
                if len(validPieceCentricMoves) == 0:
                    continue

                validPieceMoves = []
                # For all these moves try them out and see if we are in check afterwards!
                for pieceMove in validPieceCentricMoves:
                    preMovePieceCoords = piece.GetCoordinates()
                    pieceAtMoveCoordinateBeforeMove = copyBoard[pieceMove.GetX()][pieceMove.GetY()]

                    piece.ForceMove(pieceMove)
                    copyBoard[pieceMove.GetX()][pieceMove.GetY()] = piece

                    # Moved, now check if King is in check
                    isKingInCheck = Game.IsKingInCheck(copyBoard, piece.GetTeam())

                    # Undo the previous moves
                    piece.ForceMove(preMovePieceCoords)
                    copyBoard[preMovePieceCoords.GetX()][preMovePieceCoords.GetY()] = piece
                    copyBoard[pieceMove.GetX()][pieceMove.GetY()] = pieceAtMoveCoordinateBeforeMove

                    if isKingInCheck:
                        continue

                    validPieceMoves.append(pieceMove)

                moves.extend(validPieceMoves)

                logger.info("Printing valid moves (" + str(len(validPieceMoves)) + ") " + "for: " + piece.GetPieceStr()
                            + ", at: " + piece.GetCoordinates().ToString())
                for validMove in validPieceMoves:
                    logger.info(validMove.ToString())
        return moves

    def PrintBoard(self):

        # Top reference coordinates
        boardReferenceAlphabeticalDigits = "\t\t"
        for index in range(len(Utilities.Constants.ALPHABETICAL_BOARD_ORDINATES)):
            boardReferenceAlphabeticalDigits += Utilities.Constants.ALPHABETICAL_BOARD_ORDINATES[index] + "|" + str(index) + "\t"

        logger.error(boardReferenceAlphabeticalDigits)
        logger.error("")

        for yCoord in reversed(range(Utilities.Constants.MAXIMUM_Y_SQUARES)):
            # cycle over y coordinates
            boardReferenceNumericalDigits = str(yCoord+1) + "|" + str(yCoord) + "\t"
            lineToPrint = boardReferenceNumericalDigits
            for xCoord in range(Utilities.Constants.MAXIMUM_X_SQUARES):
                lineToPrint += self.__board[xCoord][yCoord].GetPieceStr() + "\t"
            lineToPrint += "  " + boardReferenceNumericalDigits
            logger.error(lineToPrint)

        # Bottom reference coordinates
        logger.error("")
        logger.error(boardReferenceAlphabeticalDigits)

        self.PrintAllValidMoves()

    def CanMove(self, fromCoord: Points, toCoord: Points):

        logger.debug("Entered, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())

        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not \
                Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Exiting CanMove prematurely, FromCoord: " + fromCoord.ToString() +
                         ", ToCoord: " + toCoord.ToString())
            return False

        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]

        isValidPieceMove = pieceBeingMoved.CanMove(toCoord)

        if not isValidPieceMove:
            logger.debug("Not a valid piece move, returning false")
            return False

        # Check if after this move the king is in check.
        pieceBeingMovedCopy = deepcopy(pieceBeingMoved)
        boardCopy = deepcopy(self.GetBoard())
        boardCopy[toCoord.GetX()][toCoord.GetY()] = pieceBeingMoved
        pieceBeingMovedCopy.SetCoordinates(toCoord)
        isKingInCheckAfterMove = Game.IsKingInCheck(boardCopy, self.__playersTurn)

        if isKingInCheckAfterMove:
            logger.debug("King is in check after move, returning false")
            return False

        logger.debug("Exiting method with value True")
        return True

    def __TurnChanged(self):
        logger.error(TeamEnum(self.__playersTurn).name + " just finished their turn")
        self.__playersTurn = (TeamEnum.Black if self.__playersTurn == TeamEnum.White else TeamEnum.White)
        logger.error("Now " + TeamEnum(self.__playersTurn).name + "'s turn")

    def __PerformPawnPromotionCheck(self):
        # Use the fact that a pawn promotion only occurs for one pawn at a time and on the top or bottom squares
        yIndexPawnPromotions = [0, Utilities.Constants.MAXIMUM_Y_SQUARES-1]
        for yIndex in yIndexPawnPromotions:
            for xIndex in range(Utilities.Constants.MAXIMUM_X_SQUARES):
                piece = self.__board[xIndex][yIndex]
                if piece.GetPieceEnum() == PieceEnums.Pawn:
                    self.__board[xIndex][yIndex] = Queen(piece.GetTeam(), Points(xIndex, yIndex))

    def __PerformPostMoveProcessing(self, fromCoord: Points, toCoord: Points):

        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Points are not in range, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())
            return

        # Update board
        pieceBeingMoved = self.__board[fromCoord.GetX()][fromCoord.GetY()]
        self.__board[toCoord.GetX()][toCoord.GetY()] = pieceBeingMoved

        # Need provision for castling!
        self.__board[fromCoord.GetX()][fromCoord.GetY()] = EmptyPiece(TeamEnum.NoTeam, fromCoord)

        # Check if pawn is being promoted
        self.__PerformPawnPromotionCheck()

        # Change players turn
        self.__TurnChanged()

        self.PrintBoard()

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
        hasMoved = pieceBeingMoved.Move(toCoord)

        if hasMoved:
            self.__PerformPostMoveProcessing(fromCoord, toCoord)

        logger.debug("Exiting with argument: " + str(hasMoved))
        return hasMoved

    def PrintAllValidMoves(self):
        logger.info("Printing all valid white moves")

        self.GetValidMovesForTeam(self.GetBoard(), Utilities.Constants.TeamEnum.White)
        self.GetValidMovesForTeam(self.GetBoard(), Utilities.Constants.TeamEnum.Black)
