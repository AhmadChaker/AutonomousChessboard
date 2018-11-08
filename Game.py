import logging
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
from Miscellaneous.BoardPoints import BoardPoints
from Board.Movement import Movement
from Board.History import History
from Miscellaneous.Result import Result
from Miscellaneous.Messages import Status, CanMoveEnum, MoveEnum, CanMoveMessageDictionary, MoveMessageDictionary


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
                self.__board[xIndex][yIndex] = EmptyPiece(BoardPoints(xIndex, yIndex))

        yIndexWhitePawns = 1
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            self.__board[xIndex][yIndexWhitePawns] = Pawn(TeamEnum.White, BoardPoints(xIndex, yIndexWhitePawns))

        yIndexBlackPawns = 6
        for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
            self.__board[xIndex][yIndexBlackPawns] = Pawn(TeamEnum.Black, BoardPoints(xIndex, yIndexBlackPawns))

        # White major pieces
        self.__board[0][0] = Rook(TeamEnum.White, BoardPoints(0, 0))
        self.__board[7][0] = Rook(TeamEnum.White, BoardPoints(7, 0))

        self.__board[1][0] = Knight(TeamEnum.White, BoardPoints(1, 0))
        self.__board[6][0] = Knight(TeamEnum.White, BoardPoints(6, 0))

        self.__board[2][0] = Bishop(TeamEnum.White, BoardPoints(2, 0))
        self.__board[5][0] = Bishop(TeamEnum.White, BoardPoints(5, 0))

        self.__board[3][0] = Queen(TeamEnum.White, BoardPoints(3, 0))
        self.__board[4][0] = King(TeamEnum.White, BoardPoints(4, 0))

        # Black Major pieces
        self.__board[0][7] = Rook(TeamEnum.Black, BoardPoints(0, 7))
        self.__board[7][7] = Rook(TeamEnum.Black, BoardPoints(7, 7))

        self.__board[1][7] = Knight(TeamEnum.Black, BoardPoints(1, 7))
        self.__board[6][7] = Knight(TeamEnum.Black, BoardPoints(6, 7))

        self.__board[2][7] = Bishop(TeamEnum.Black, BoardPoints(2, 7))
        self.__board[5][7] = Bishop(TeamEnum.Black, BoardPoints(5, 7))

        self.__board[3][7] = Queen(TeamEnum.Black, BoardPoints(3, 7))
        self.__board[4][7] = King(TeamEnum.Black, BoardPoints(4, 7))

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
        self.PrintPieceProperties()

    def PrintHistory(self):
        logger.error("Printing history")

        for historicalMove in self.GetHistory().GetHistoricalMoves():
            strToPrint = PieceEnums(historicalMove.GetPieceEnumFrom()).name + " at [" + \
                         historicalMove.GetFromCoord().ToString() + "] moved to [" + \
                         historicalMove.GetToCoord().ToString() + "], IsCaptureMove: " + \
                         str(historicalMove.IsCaptureMove())
            logger.error(strToPrint)

    def CanMove(self, fromBoardCoords: str, toBoardCoords: str):

        logger.debug("Entered, FromBoardCoords: " + fromBoardCoords + ", ToBoardCoords: " + toBoardCoords)

        fromCoords = Utilities.CoordinateConverters.ConvertChessToArrayCoordinates(fromBoardCoords)
        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoords):
            logger.error("Exiting CanMove prematurely, not in range, FromCoord: " + fromCoords.ToString())
            return Result(Status.Report, CanMoveMessageDictionary[CanMoveEnum.FromCoordOutOfRange])

        toCoords = Utilities.CoordinateConverters.ConvertChessToArrayCoordinates(toBoardCoords)
        if not Utilities.CoordinateConverters.ValidatePointIsInRange(toCoords):
            logger.error("Exiting CanMove prematurely, not in range, ToCoord: " + toCoords.ToString())
            return Result(Status.Report, CanMoveMessageDictionary[CanMoveEnum.ToCoordOutOfRange])

        pieceBeingMoved = self.__board[fromCoords.GetX()][fromCoords.GetY()]

        # Check persons turn!
        if pieceBeingMoved.GetTeam() == TeamEnum.NoTeam:
            logger.error("Can't move empty piece, Go again")
            return Result(Status.Report, CanMoveMessageDictionary[CanMoveEnum.SlotHasNoTeam])

        if pieceBeingMoved.GetTeam() != self.__playersTurn:
            logger.error("Not this players turn, not moving!")
            return Result(Status.Report, CanMoveMessageDictionary[CanMoveEnum.WrongTeam])

        isValidPieceMove = pieceBeingMoved.CanMove(self.__board, toCoords, self.GetHistory().GetLastMove())
        if not isValidPieceMove:
            logger.error("Not a valid piece move, returning false")
            return Result(Status.Report, CanMoveMessageDictionary[CanMoveEnum.InvalidPieceCentricMove])

        logger.debug("Exiting method with success")
        return Result(Status.NoReport, CanMoveMessageDictionary[CanMoveEnum.Success])

    def PerformPawnPromotionCheck(self):
        # Use the fact that a pawn promotion only occurs for one pawn at a time and on the top or bottom squares
        yIndexPawnPromotions = [0, Board.Constants.MAXIMUM_Y_SQUARES - 1]
        for yIndex in yIndexPawnPromotions:
            for xIndex in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = self.__board[xIndex][yIndex]
                if piece.GetPieceEnum() == PieceEnums.Pawn:
                    self.__board[xIndex][yIndex] = Queen(piece.GetTeam(), BoardPoints(xIndex, yIndex))

    def PerformMoveProcessing(self, pieceBeingMoved, fromCoord: BoardPoints, toCoord: BoardPoints):

        logger.debug("Entered method")

        # Very basic validation just in case
        if not Utilities.CoordinateConverters.ValidatePointIsInRange(fromCoord) or not Utilities.CoordinateConverters.ValidatePointIsInRange(toCoord):
            logger.error("Points are not in range, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())
            return

        # Check for en-passant before history check
        isEnPassant = BoardHelpers.IsEnPassant(pieceBeingMoved.GetPieceEnum(), fromCoord, toCoord, self.GetHistory().GetLastMove())
        if isEnPassant:
            # Piece at new x coordinate and old y coordinate should now be empty as its captured
            self.__board[toCoord.GetX()][fromCoord.GetY()] = EmptyPiece(Points(toCoord.GetX(), fromCoord.GetY()))

        # Update history
        self.GetHistory().AppendMovement(Movement(self.__board[fromCoord.GetX()][fromCoord.GetY()],
                                         self.__board[toCoord.GetX()][toCoord.GetY()],
                                         fromCoord, toCoord, isEnPassant))

        # Update board
        self.__board[toCoord.GetX()][toCoord.GetY()] = pieceBeingMoved
        self.__board[fromCoord.GetX()][fromCoord.GetY()] = EmptyPiece(fromCoord)

        isCastleMove = BoardHelpers.IsCastleMove(pieceBeingMoved, fromCoord, toCoord)

        if isCastleMove:
            # It's a castle move so we need to move the corresponding rook as well.
            commonYCoord = fromCoord.GetY()
            isCastleToTheLeft = True if fromCoord.GetX() - toCoord.GetX() > 0 else False
            oldRookXCoord = 0 if isCastleToTheLeft > 0 else Board.Constants.MAXIMUM_X_SQUARES-1
            newRookXCoord = toCoord.GetX()+1 if isCastleToTheLeft else toCoord.GetX() - 1

            oldRookCoords = Points(oldRookXCoord, commonYCoord)
            newRookCoords = Points(newRookXCoord, commonYCoord)

            # Update history
            self.GetHistory().AppendMovement(Movement(self.__board[oldRookCoords.GetX()][oldRookCoords.GetY()],
                                                      self.__board[newRookCoords.GetX()][newRookCoords.GetY()],
                                                      oldRookCoords,
                                                      newRookCoords))

            rook = self.__board[oldRookCoords.GetX()][oldRookCoords.GetY()]
            rook.ForceMove(newRookCoords)
            self.__board[newRookCoords.GetX()][newRookCoords.GetY()] = rook
            self.__board[oldRookCoords.GetX()][oldRookCoords.GetY()] = EmptyPiece(oldRookCoords)

        # Check if pawn is being promoted
        self.PerformPawnPromotionCheck()

    def Move(self, fromBoardCoords: str, toBoardCoords: str):

        logger.debug("Entered, fromBoardCoords: " + fromBoardCoords + ", toBoardCoords: " + toBoardCoords)

        fromCoords = Utilities.CoordinateConverters.ConvertChessToArrayCoordinates(fromBoardCoords)
        toCoords = Utilities.CoordinateConverters.ConvertChessToArrayCoordinates(toBoardCoords)

        canMoveResult = self.CanMove(fromBoardCoords, toBoardCoords)
        if canMoveResult.GetStatus() == Status.Report:
            logger.error("Can't move piece to requested coordinated, FromCoord: " + fromCoords.ToString() +
                         ", ToCoord: " + toCoords.ToString())
            return Result(Status.Report, MoveMessageDictionary[MoveEnum.GeneralFailure])

        pieceBeingMoved = self.__board[fromCoords.GetX()][fromCoords.GetY()]

        # Move piece! Now update the board
        hasMoved = pieceBeingMoved.Move(self.__board, toCoords, self.GetHistory().GetLastMove())

        if hasMoved:
            self.PerformMoveProcessing(pieceBeingMoved, fromCoords, toCoords)
            self.PrintBoard()
            self.PrintHistory()

            # Perform post moving processing
            opposingTeam = BoardHelpers.GetOpposingTeam(self.__playersTurn)
            isCheckMated = BoardHelpers.IsInCheckMate(self.GetBoard(), opposingTeam)
            if isCheckMated:
                logger.error("Checkmate!")
                return Result(Status.Report, MoveMessageDictionary[MoveEnum.CheckMate])

            # Check draw conditions
            isDraw = BoardHelpers.IsDraw(self.GetBoard(), self.GetHistory().GetHistoricalMoves(), self.__playersTurn)
            if isDraw:
                logger.error("Draw declared")
                return Result(Status.Report, MoveMessageDictionary[MoveEnum.Draw])

            # Change players turn
            logger.error(TeamEnum(self.__playersTurn).name + " just finished their turn")
            self.__playersTurn = BoardHelpers.GetOpposingTeam(self.__playersTurn)
            logger.error("Now " + TeamEnum(self.__playersTurn).name + "'s turn")

            isInCheck = BoardHelpers.IsInCheck(self.GetBoard(), self.__playersTurn)
            if isInCheck:
                logger.error("Check")
                return Result(Status.Report, MoveMessageDictionary[MoveEnum.Check])

        return Result(Status.NoReport, MoveMessageDictionary[MoveEnum.Success])

    def PrintAllValidMoves(self):
        logger.info("Printing all valid white moves")

        BoardHelpers.GetValidMovesForTeam(self.GetBoard(), Board.Constants.TeamEnum.White)
        BoardHelpers.GetValidMovesForTeam(self.GetBoard(), Board.Constants.TeamEnum.Black)

    def PrintPieceProperties(self):
        for yCoord in reversed(range(Board.Constants.MAXIMUM_Y_SQUARES)):
            # cycle over y coordinates
            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = self.__board[xCoord][yCoord]
                if piece.GetPieceEnum() == PieceEnums.Empty:
                    continue
                logger.info("Start printing properties for: " + piece.GetPieceStr())
                logger.info("Board coordinates: " + BoardPoints(xCoord, yCoord).ToString())
                logger.info("Self reported coordinates: " + piece.GetCoordinates().ToString())
                logger.info("History: ")
                for historicalMove in piece.GetHistory():
                    logger.info(historicalMove.ToString())
                logger.info("End printing properties for: " + piece.GetPieceStr())
