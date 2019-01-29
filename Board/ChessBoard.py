import logging
import Utilities.CoordinateConverters
import Miscellaneous.Constants
from Pieces.IBasePiece import IBasePiece
from Pieces.NoPiece import NoPiece
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from Miscellaneous.Constants import TeamEnum, PieceEnums
from Board.Movement import Movement
from Miscellaneous.BoardPoints import BoardPoints
from Utilities.BoardHelpers import BoardHelpers


logger = logging.getLogger(__name__)


class ChessBoard:

    def __init__(self, history):
        logger.debug("Entered constructor")

        self.__history = history
        self.__teamsTurn = TeamEnum.White

        # Initialise chess board 2D structure
        self.__board = [None] * Miscellaneous.Constants.MAXIMUM_X_SQUARES
        for xIndex in range(Miscellaneous.Constants.MAXIMUM_X_SQUARES):
            # for each y line
            self.__board[xIndex] = [None] * Miscellaneous.Constants.MAXIMUM_Y_SQUARES

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

    def PerformMoveProcessing(self, pieceBeingMoved, fromCoord: BoardPoints, toCoord: BoardPoints):

        logger.debug("Entered method")

        move = Movement(pieceBeingMoved.GetTeam(),
                        pieceBeingMoved.GetPieceEnum(),
                        self.GetPieceAtCoordinate(toCoord).GetPieceEnum(),
                        fromCoord,
                        toCoord,
                        self.GetLastHistoricalMove())

        # Update history
        self.AppendToHistory(move)

        # Update board
        self.UpdatePieceOnBoard(pieceBeingMoved)
        self.UpdatePieceOnBoard(NoPiece(fromCoord))

        # change team
        logger.error(TeamEnum(self.GetTeamsTurn()).name + " just finished their turn")
        opposingTeam = TeamEnum.Black if self.GetTeamsTurn() == TeamEnum.White else TeamEnum.White
        self.SetTeamsTurn(opposingTeam)
        logger.error("Now " + TeamEnum(self.GetTeamsTurn()).name + "'s turn")

        # do piece specific post move checks
        if pieceBeingMoved.GetPieceEnum() == PieceEnums.Pawn:
            self.PerformPawnPromotionCheck(pieceBeingMoved)
            if move.IsEnPassantMove():
                # Piece at new x coordinate and old y coordinate should now be empty as its captured
                self.UpdatePieceOnBoard(NoPiece(BoardPoints(toCoord.GetX(), fromCoord.GetY())))
            return

        if move.IsCastleMove():
            # It's a castle move so we need to move the corresponding rook as well.
            commonYCoord = fromCoord.GetY()
            isCastleToTheLeft = True if fromCoord.GetX() - toCoord.GetX() > 0 else False
            oldRookXCoord = 0 if isCastleToTheLeft > 0 else Miscellaneous.Constants.MAXIMUM_X_SQUARES - 1
            newRookXCoord = toCoord.GetX()+1 if isCastleToTheLeft else toCoord.GetX() - 1

            oldRookCoords = BoardPoints(oldRookXCoord, commonYCoord)
            newRookCoords = BoardPoints(newRookXCoord, commonYCoord)

            rookBeingMoved = self.GetPieceAtCoordinate(oldRookCoords)
            # Update history
            self.AppendToHistory(Movement(rookBeingMoved.GetTeam(),
                                          rookBeingMoved.GetPieceEnum(),
                                          self.GetPieceAtCoordinate(newRookCoords).GetPieceEnum(),
                                          oldRookCoords,
                                          newRookCoords,
                                          self.GetLastHistoricalMove()))

            rookBeingMoved.ForceMove(newRookCoords)
            self.UpdatePieceOnBoard(rookBeingMoved)
            self.UpdatePieceOnBoard(NoPiece(oldRookCoords))
            return

    def PerformPawnPromotionCheck(self, pieceBeingMoved):
        isPromotion = False
        if pieceBeingMoved.GetPieceEnum() == PieceEnums.Pawn:
            xCoord = pieceBeingMoved.GetCoordinates().GetX()
            yCoord = pieceBeingMoved.GetCoordinates().GetY()
            if yCoord == 0 or yCoord == Miscellaneous.Constants.MAXIMUM_Y_SQUARES - 1:
                self.UpdatePieceOnBoard(Queen(pieceBeingMoved.GetTeam(), BoardPoints(xCoord, yCoord)))
                isPromotion = True
        return isPromotion

    # region History related

    def AppendToHistory(self, movement):
        self.__history.AppendMovement(movement)

    def GetLastHistoricalMove(self):
        return self.__history.GetLastMove()

    def GetHistoricalMoves(self):
        return self.__history.GetHistoricalMoves()

    def GetHistory(self):
        return self.__history

    # endregion

    def ResetToDefault(self):

        logger.debug("Entered ResetToDefault")

        # set team
        self.SetTeamsTurn(TeamEnum.White)

        # clear history
        self.__history.Clear()

        # Set empty pieces first

        yIndexNoPieces = [2, 3, 4, 5]

        for yIndex in yIndexNoPieces:
            for xIndex in range(Miscellaneous.Constants.MAXIMUM_X_SQUARES):
                self.UpdatePieceOnBoard(NoPiece(BoardPoints(xIndex, yIndex)))

        for xIndex in range(Miscellaneous.Constants.MAXIMUM_X_SQUARES):
            self.UpdatePieceOnBoard(Pawn(TeamEnum.White, BoardPoints(xIndex, Miscellaneous.Constants.WHITE_PAWNS_Y_ARRAY_COORDINATE)))

        for xIndex in range(Miscellaneous.Constants.MAXIMUM_X_SQUARES):
            self.UpdatePieceOnBoard(Pawn(TeamEnum.Black, BoardPoints(xIndex, Miscellaneous.Constants.BLACK_PAWNS_Y_ARRAY_COORDINATE)))

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

        logger.debug("End ResetToDefault")

    def RemoveAllPieces(self):
        for yCoord in reversed(range(Miscellaneous.Constants.MAXIMUM_Y_SQUARES)):
            # cycle over y coordinates
            for xCoord in range(Miscellaneous.Constants.MAXIMUM_X_SQUARES):
                self.UpdatePieceOnBoard(NoPiece(BoardPoints(xCoord, yCoord)))

    def GetFenRepresentation(self):

        fenRepresentation = ""
        for yCoord in reversed(range(Miscellaneous.Constants.MAXIMUM_Y_SQUARES)):
            if yCoord != Miscellaneous.Constants.MAXIMUM_Y_SQUARES-1:
                fenRepresentation += "/"

            countOfEmptySpaces = 0
            for xCoord in range(Miscellaneous.Constants.MAXIMUM_X_SQUARES):
                piece = self.GetPieceAtCoordinate(BoardPoints(xCoord, yCoord))
                if piece.GetPieceEnum() == PieceEnums.NoPiece:
                    countOfEmptySpaces += 1
                    if xCoord == Miscellaneous.Constants.MAXIMUM_X_SQUARES-1:
                        fenRepresentation += str(countOfEmptySpaces)
                else:
                    if countOfEmptySpaces > 0:
                        fenRepresentation += str(countOfEmptySpaces)
                        countOfEmptySpaces = 0
                    fenRepresentation += piece.GetFenRepresentation()

        fenRepresentation += " "

        teamStr = "w" if self.GetTeamsTurn() == TeamEnum.White else "b"
        fenRepresentation += teamStr

        fenRepresentation += " "
        whiteKingArray = BoardHelpers.GetPieceByPieceType(self, PieceEnums.King, TeamEnum.White)
        if whiteKingArray is None or len(whiteKingArray) == 0:
            return ""
        whiteKing = whiteKingArray[0]

        blackKingArray = BoardHelpers.GetPieceByPieceType(self, PieceEnums.King, TeamEnum.Black)
        if blackKingArray is None or len(blackKingArray) == 0:
            return ""
        blackKing = blackKingArray[0]

        castleStr = ""
        if whiteKing.CanPotentiallyKingSideCastleInTheFuture(self):
            castleStr += "K"
        if whiteKing.CanPotentiallyQueenSideCastleInTheFuture(self):
            castleStr += "Q"
        if blackKing.CanPotentiallyKingSideCastleInTheFuture(self):
            castleStr += "k"
        if blackKing.CanPotentiallyQueenSideCastleInTheFuture(self):
            castleStr += "q"

        if not castleStr:
            castleStr = "-"

        fenRepresentation += castleStr
        fenRepresentation += " "

        # check if move is two step
        enPassantStr = ""
        lastMove = self.GetLastHistoricalMove()
        if lastMove is not None and lastMove.IsTwoStepPawnMove():
            yDisplacement = lastMove.GetYMovement()
            if yDisplacement > 0:
                directionBehindDoubleStep = -1
            else:
                directionBehindDoubleStep = 1
            point = BoardPoints(lastMove.GetToCoord().GetX(), lastMove.GetToCoord().GetY()+ directionBehindDoubleStep)
            enPassantStr = (str(point.GetXBoard()) + str(point.GetYBoard())).lower()

        if not enPassantStr:
            enPassantStr = "-"

        fenRepresentation += enPassantStr
        fenRepresentation += " "

        # half move clock (moves since last pawn move or capture, just set this to 0.
        fenRepresentation += "0"
        fenRepresentation += " "

        # number of moves each player has made.
        fenRepresentation += str(self.GetHistory().GetNumberofTurns())
        return fenRepresentation

    def PrintBoard(self):

        # Top reference coordinates
        boardReferenceAlphabeticalDigits = "\t\t"
        for index in range(len(Miscellaneous.Constants.ALPHABETICAL_BOARD_ORDINATES)):
            boardReferenceAlphabeticalDigits += Miscellaneous.Constants.ALPHABETICAL_BOARD_ORDINATES[index] + "|" + str(index) + "\t"

        logger.error(boardReferenceAlphabeticalDigits)
        logger.error("")

        for yCoord in reversed(range(Miscellaneous.Constants.MAXIMUM_Y_SQUARES)):
            # cycle over y coordinates
            boardReferenceNumericalDigits = str(yCoord+1) + "|" + str(yCoord) + "\t"
            lineToPrint = boardReferenceNumericalDigits
            for xCoord in range(Miscellaneous.Constants.MAXIMUM_X_SQUARES):
                lineToPrint += self.GetPieceAtCoordinate(BoardPoints(xCoord, yCoord)).GetPieceStr() + "\t"
            lineToPrint += "  " + boardReferenceNumericalDigits
            logger.error(lineToPrint)

        # Bottom reference coordinates
        logger.error("")
        logger.error(boardReferenceAlphabeticalDigits)

        logger.error(self.GetFenRepresentation())

    def PrintHistory(self):
        self.__history.PrintHistory()

    def GetTeamsTurn(self):
        return self.__teamsTurn

    def SetTeamsTurn(self, teamsTurn):
        self.__teamsTurn = teamsTurn
