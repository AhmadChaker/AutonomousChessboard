import logging
import Utilities.CoordinateConverters
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
from Board.Constants import TeamEnum
from Board.ChessBoard import ChessBoard
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Result import Result
from Miscellaneous.Messages import MoveEnum


logger = logging.getLogger(__name__)


class Game:

    def __init__(self, board):
        logger.debug("Entered constructor")

        self.__board = board

        # Variables constantly checked for during game play
        self.__hasGameEnded = False
        self.__isInCheckmate = False
        self.__isDraw = False
        self.__isInCheck = False

    def ResetGame(self):
        self.GetBoard().ResetToDefault()
        self.SetHasGameEnded(False)
        self.SetIsInCheckmate(False)
        self.SetIsDraw(False)
        self.SetIsInCheck(False)

    # region Board interfaces

    def UpdatePieceOnBoard(self, piece: IBasePiece):
        self.GetBoard().UpdatePieceOnBoard(piece)

    def GetPieceAtCoordinate(self, pieceCoords:BoardPoints):
        return self.GetBoard().GetPieceAtCoordinate(pieceCoords)

    def AppendToHistory(self, movement):
        self.GetBoard().AppendToHistory(movement)

    def GetLastHistoricalMove(self):
        return self.GetBoard().GetLastHistoricalMove()

    def GetTeamsTurn(self):
        return self.GetBoard().GetTeamsTurn()

    def GetBoard(self):
        return self.__board

    # endregion

    def CanMove(self, fromBoardCoords: str, toBoardCoords: str):
        logger.debug("Entered, FromBoardCoords: " + fromBoardCoords + ", ToBoardCoords: " + toBoardCoords)

        canMove = False

        if self.GetHasGameEnded():
            logger.error("Game has ended already")
            return Result(canMove, MoveEnum.GameEnded)

        fromCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(fromBoardCoords)
        if not Utilities.CoordinateConverters.IsPointInRange(fromCoords):
            logger.error("Exiting CanMove prematurely, fromCoord not in range, fromCoord: " + fromCoords.ToString())
            return Result(canMove, MoveEnum.CoordOutOfRange)

        toCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(toBoardCoords)
        if not Utilities.CoordinateConverters.IsPointInRange(toCoords):
            logger.error("Exiting CanMove prematurely, toCoord not in range, toCoord: " + toCoords.ToString())
            return Result(canMove, MoveEnum.CoordOutOfRange)

        pieceBeingMoved = self.GetPieceAtCoordinate(fromCoords)

        # Check persons turn!
        if pieceBeingMoved.GetTeam() == TeamEnum.NoTeam:
            logger.error("Can't move empty piece, Go again")
            return Result(canMove, MoveEnum.SlotHasNoTeam)

        if pieceBeingMoved.GetTeam() != self.GetTeamsTurn():
            logger.error("Not this teams turn, not moving!")
            return Result(canMove,  MoveEnum.WrongTeam)

        canMove = pieceBeingMoved.CanMove(self.GetBoard(), toCoords)
        if not canMove:
            logger.error("Not a valid piece move, returning false")
            return Result(canMove, MoveEnum.InvalidPieceCentricMove)

        logger.debug("Exiting method with success")
        return Result(canMove, MoveEnum.Success)

    def Move(self, fromBoardCoords: str, toBoardCoords: str):
        logger.debug("Entered, fromBoardCoords: " + fromBoardCoords + ", toBoardCoords: " + toBoardCoords)

        hasMoved = False

        if self.GetHasGameEnded():
            logger.error("Game has ended already")
            return Result(hasMoved, MoveEnum.GameEnded)

        fromCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(fromBoardCoords)
        toCoords = Utilities.CoordinateConverters.ConvertInputToPointCoordinates(toBoardCoords)

        canMoveResult = self.CanMove(fromBoardCoords, toBoardCoords)
        if not canMoveResult.IsSuccessful():
            return Result(hasMoved, canMoveResult.GetStatusCode())

        pieceBeingMoved = self.GetPieceAtCoordinate(fromCoords)
        hasMoved = pieceBeingMoved.Move(self.GetBoard(), toCoords)

        if not hasMoved:
            # Really should never hit here as if canMove succeeds, this should never fail.
            return Result(hasMoved, MoveEnum.InvalidPieceCentricMove)

        self.GetBoard().PerformMoveProcessing(pieceBeingMoved, fromCoords, toCoords)

        isInCheckMate = BoardHelpers.IsInCheckMate(self.GetBoard(), self.GetTeamsTurn())
        self.SetIsInCheckmate(isInCheckMate)
        if not isInCheckMate:
            isDraw = BoardHelpers.IsDraw(self.GetBoard(), self.GetTeamsTurn())
            self.SetIsDraw(isDraw)
            if not isDraw:
                self.SetIsInCheck(BoardHelpers.IsInCheck(self.GetBoard(), self.GetTeamsTurn()))

        self.PrintProperties()
        return Result(hasMoved, MoveEnum.Success)

    def PrintProperties(self):
        logger.info("Printing board")
        self.GetBoard().PrintBoard()
        logger.info("Printing all valid white moves")
        MoveHelpers.PrintValidMoves(self.GetBoard(), Board.Constants.TeamEnum.White)
        logger.info("Printing all valid black moves")
        MoveHelpers.PrintValidMoves(self.GetBoard(), Board.Constants.TeamEnum.Black)
        logger.info("Printing history")
        self.GetBoard().PrintHistory()

    # region Game play properties

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
