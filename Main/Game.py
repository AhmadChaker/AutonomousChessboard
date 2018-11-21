import logging
import Utilities.CoordinateConverters
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
from Pieces.Queen import Queen
from Pieces.NoPiece import NoPiece
from Board.Constants import TeamEnum
from Pieces.Constants import PieceEnums
from Miscellaneous.BoardPoints import BoardPoints
from Board.Movement import Movement
from Miscellaneous.Result import Result
from Miscellaneous.Messages import MoveEnum, MoveMessageDictionary


logger = logging.getLogger(__name__)


class Game:

    def __init__(self, history, chessBoard):
        logger.debug("Entered constructor")

        self.__history = history
        self.__board = chessBoard

        # Variables constantly checked for during game play
        self.__playersTurn = TeamEnum.White
        self.__hasGameEnded = False
        self.__isInCheckmate = False
        self.__isDraw = False
        self.__isInCheck = False

        self.ResetGame()

    def ResetGame(self):
        self.GetHistory().Clear()
        self.GetBoard().ResetToDefault()

        self.SetPlayersTurn(TeamEnum.White)
        self.SetHasGameEnded(False)
        self.SetIsInCheckmate(False)
        self.SetIsDraw(False)
        self.SetIsInCheck(False)

    def UpdatePieceOnBoard(self, piece: IBasePiece):
        self.GetBoard().UpdatePieceOnBoard(piece)

    def GetPieceAtCoordinate(self, pieceCoords:BoardPoints):
        return self.GetBoard().GetPieceAtCoordinate(pieceCoords)

    def GetBoard(self):
        return self.__board

    def CanMove(self, fromBoardCoords: str, toBoardCoords: str):
        logger.debug("Entered, FromBoardCoords: " + fromBoardCoords + ", ToBoardCoords: " + toBoardCoords)

        canMove = False

        if self.GetHasGameEnded():
            logger.error("Game has ended already")
            return Result(canMove, MoveMessageDictionary[MoveEnum.GameEnded])

        fromCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(fromBoardCoords)
        if not Utilities.CoordinateConverters.IsPointInRange(fromCoords):
            logger.error("Exiting CanMove prematurely, fromCoord not in range, fromCoord: " + fromCoords.ToString())
            return Result(canMove, MoveMessageDictionary[MoveEnum.CoordOutOfRange])

        toCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(toBoardCoords)
        if not Utilities.CoordinateConverters.IsPointInRange(toCoords):
            logger.error("Exiting CanMove prematurely, toCoord not in range, toCoord: " + toCoords.ToString())
            return Result(canMove, MoveMessageDictionary[MoveEnum.CoordOutOfRange])

        pieceBeingMoved = self.GetPieceAtCoordinate(fromCoords)

        # Check persons turn!
        if pieceBeingMoved.GetTeam() == TeamEnum.NoTeam:
            logger.error("Can't move empty piece, Go again")
            return Result(canMove, MoveMessageDictionary[MoveEnum.SlotHasNoTeam])

        if pieceBeingMoved.GetTeam() != self.GetPlayersTurn():
            logger.error("Not this players turn, not moving!")
            return Result(canMove,  MoveMessageDictionary[MoveEnum.WrongTeam])

        canMove = pieceBeingMoved.CanMove(self.GetBoard(), toCoords)
        if not canMove:
            logger.error("Not a valid piece move, returning false")
            return Result(canMove, MoveMessageDictionary[MoveEnum.InvalidPieceCentricMove])

        logger.debug("Exiting method with success")
        return Result(canMove, MoveMessageDictionary[MoveEnum.Success])

    def Move(self, fromBoardCoords: str, toBoardCoords: str):
        logger.debug("Entered, fromBoardCoords: " + fromBoardCoords + ", toBoardCoords: " + toBoardCoords)

        hasMoved = False

        if self.GetHasGameEnded():
            logger.error("Game has ended already")
            return Result(hasMoved, MoveMessageDictionary[MoveEnum.MoveEnum.GameEnded])

        fromCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(fromBoardCoords)
        toCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(toBoardCoords)

        canMoveResult = self.CanMove(fromBoardCoords, toBoardCoords)
        if not canMoveResult.IsSuccessful():
            return Result(hasMoved, canMoveResult.GetMessage())

        pieceBeingMoved = self.GetPieceAtCoordinate(fromCoords)
        hasMoved = pieceBeingMoved.Move(self.GetBoard(), toCoords)

        if not hasMoved:
            return Result(hasMoved, MoveMessageDictionary[MoveEnum.InvalidPieceCentricMove])

        self.PerformMoveProcessing(pieceBeingMoved, fromCoords, toCoords)
        self.PrintProperties()
        self.PrintHistory()

        # Change players turn
        opposingTeam = BoardHelpers.GetOpposingTeam(self.GetPlayersTurn())
        logger.error(TeamEnum(self.GetPlayersTurn()).name + " just finished their turn")
        self.SetPlayersTurn(opposingTeam)
        logger.error("Now " + TeamEnum(self.GetPlayersTurn()).name + "'s turn")

        isInCheckMate = BoardHelpers.IsInCheckMate(self.GetBoard(), self.GetPlayersTurn())
        self.SetIsInCheckmate(isInCheckMate)
        if not isInCheckMate:
            isDraw = BoardHelpers.IsDraw(self.GetBoard(), self.GetHistory().GetHistoricalMoves(), self.GetPlayersTurn())
            self.SetIsDraw(isDraw)
            if not isDraw:
                self.SetIsInCheck(BoardHelpers.IsInCheck(self.GetBoard(), self.GetPlayersTurn()))

        return Result(hasMoved, MoveMessageDictionary[MoveEnum.Success])

    def PerformPawnPromotionCheck(self, pieceBeingMoved):
        if pieceBeingMoved.GetPieceEnum() == PieceEnums.Pawn:
            xCoord = pieceBeingMoved.GetCoordinates().GetX()
            yCoord = pieceBeingMoved.GetCoordinates().GetY()
            if yCoord == 0 or yCoord == Board.Constants.MAXIMUM_Y_SQUARES - 1:
                self.UpdatePieceOnBoard(Queen(pieceBeingMoved.GetTeam, BoardPoints(xCoord, yCoord)))

    def PerformMoveProcessing(self, pieceBeingMoved, fromCoord: BoardPoints, toCoord: BoardPoints):

        logger.debug("Entered method")

        # Very basic validation just in case
        if not Utilities.CoordinateConverters.IsPointInRange(fromCoord) or not Utilities.CoordinateConverters.IsPointInRange(toCoord):
            logger.error("Points are not in range, FromCoord: " + fromCoord.ToString() + ", ToCoord: " + toCoord.ToString())
            return

        move = Movement(pieceBeingMoved.GetTeam(),
                        pieceBeingMoved.GetPieceEnum(),
                        self.GetPieceAtCoordinate(toCoord).GetPieceEnum(),
                        fromCoord,
                        toCoord,
                        self.GetHistory().GetLastMove())
        # Update history
        self.GetHistory().AppendMovement(move)

        # Update board
        self.UpdatePieceOnBoard(pieceBeingMoved)
        self.UpdatePieceOnBoard(NoPiece(fromCoord))

        if move.IsEnPassantMove():
            # Piece at new x coordinate and old y coordinate should now be empty as its captured
            self.UpdatePieceOnBoard(NoPiece(BoardPoints(toCoord.GetX(), fromCoord.GetY())))
            return

        if move.IsCastleMove():
            # It's a castle move so we need to move the corresponding rook as well.
            commonYCoord = fromCoord.GetY()
            isCastleToTheLeft = True if fromCoord.GetX() - toCoord.GetX() > 0 else False
            oldRookXCoord = 0 if isCastleToTheLeft > 0 else Board.Constants.MAXIMUM_X_SQUARES-1
            newRookXCoord = toCoord.GetX()+1 if isCastleToTheLeft else toCoord.GetX() - 1

            oldRookCoords = BoardPoints(oldRookXCoord, commonYCoord)
            newRookCoords = BoardPoints(newRookXCoord, commonYCoord)

            # Update history
            self.GetHistory().AppendMovement(Movement(self.GetPieceAtCoordinate(oldRookCoords),
                                                      self.GetPieceAtCoordinate(newRookCoords),
                                                      oldRookCoords,
                                                      newRookCoords,
                                                      self.GetHistory().GetLastMove()))

            rook = self.GetPieceAtCoordinate(oldRookCoords)
            rook.ForceMove(newRookCoords)
            self.UpdatePieceOnBoard(rook)
            self.UpdatePieceOnBoard(NoPiece(oldRookCoords))
            return

        self.PerformPawnPromotionCheck(pieceBeingMoved)

    def PrintAllValidMoves(self):
        logger.info("Printing all valid white moves")

        MoveHelpers.GetValidMovesForTeam(self.GetBoard(), Board.Constants.TeamEnum.White)
        MoveHelpers.GetValidMovesForTeam(self.GetBoard(), Board.Constants.TeamEnum.Black)

    def PrintPieceProperties(self):
        for yCoord in reversed(range(Board.Constants.MAXIMUM_Y_SQUARES)):
            # cycle over y coordinates
            for xCoord in range(Board.Constants.MAXIMUM_X_SQUARES):
                piece = self.GetPieceAtCoordinate(BoardPoints(xCoord, yCoord))
                if piece.GetPieceEnum() == PieceEnums.NoPiece:
                    continue
                logger.info("Start printing properties for: " + piece.GetPieceStr())
                logger.info("Board coordinates: " + BoardPoints(xCoord, yCoord).ToString())
                logger.info("Self reported coordinates: " + piece.GetCoordinates().ToString())
                logger.info("History: ")
                for historicalMove in piece.GetHistory():
                    logger.info(historicalMove.ToString())
                logger.info("End printing properties for: " + piece.GetPieceStr())

    def PrintProperties(self):
        self.GetBoard().PrintBoard()
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

    # region Property setters and getters

    def GetHistory(self):
        return self.__history

    def GetPlayersTurn(self):
        return self.__playersTurn

    def SetPlayersTurn(self, playersTurn):
        self.__playersTurn = playersTurn

    def GetHasGameEnded(self):
        return self.__hasGameEnded

    def SetHasGameEnded(self, hasGameEnded):
        self.__hasGameEnded = hasGameEnded

    def SetIsInCheckmate(self, isInCheckmate):
        if isInCheckmate:
            self.SetHasGameEnded(isInCheckmate)
        self.__isInCheckmate = isInCheckmate

    def GetIsInCheckmate(self):
        return self.__isInCheckmate

    def SetIsDraw(self, isDraw):
        if isDraw:
            self.SetHasGameEnded(isDraw)
        self.__isDraw = isDraw

    def GetIsDraw(self):
        return self.__isDraw

    def SetIsInCheck(self, isInCheck):
        self.__isInCheck = isInCheck

    def GetIsInCheck(self):
        return self.__isInCheck

    # endregion
