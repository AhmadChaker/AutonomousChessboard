import logging
import Utilities.CoordinateConverters
import Board.Constants
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
from Pieces.Queen import Queen
from Pieces.NoPiece import NoPiece
from Board.Constants import TeamEnum
from Board.ChessBoard import ChessBoard
from Pieces.Constants import PieceEnums
from Miscellaneous.BoardPoints import BoardPoints
from Board.Movement import Movement
from Miscellaneous.Result import Result
from Miscellaneous.Messages import MoveEnum


logger = logging.getLogger(__name__)


class Game:

    def __init__(self):
        logger.debug("Entered constructor")

        self.__board = ChessBoard()

        # Variables constantly checked for during game play
        self.__playersTurn = TeamEnum.White
        self.__hasGameEnded = False
        self.__isInCheckmate = False
        self.__isDraw = False
        self.__isInCheck = False

    def ResetGame(self):
        self.GetBoard().ResetToDefault()
        self.SetPlayersTurn(TeamEnum.White)
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

        if pieceBeingMoved.GetTeam() != self.GetPlayersTurn():
            logger.error("Not this players turn, not moving!")
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

        self.PerformMoveProcessing(pieceBeingMoved, fromCoords, toCoords)

        # Change players turn
        opposingTeam = BoardHelpers.GetOpposingTeam(self.GetPlayersTurn())
        logger.error(TeamEnum(self.GetPlayersTurn()).name + " just finished their turn")
        self.SetPlayersTurn(opposingTeam)
        logger.error("Now " + TeamEnum(self.GetPlayersTurn()).name + "'s turn")

        isInCheckMate = BoardHelpers.IsInCheckMate(self.GetBoard(), self.GetPlayersTurn())
        self.SetIsInCheckmate(isInCheckMate)
        if not isInCheckMate:
            isDraw = BoardHelpers.IsDraw(self.GetBoard(), self.GetPlayersTurn())
            self.SetIsDraw(isDraw)
            if not isDraw:
                self.SetIsInCheck(BoardHelpers.IsInCheck(self.GetBoard(), self.GetPlayersTurn()))

        self.PrintProperties()
        return Result(hasMoved, MoveEnum.Success)

    def PerformPawnPromotionCheck(self, pieceBeingMoved):
        if pieceBeingMoved.GetPieceEnum() == PieceEnums.Pawn:
            xCoord = pieceBeingMoved.GetCoordinates().GetX()
            yCoord = pieceBeingMoved.GetCoordinates().GetY()
            if yCoord == 0 or yCoord == Board.Constants.MAXIMUM_Y_SQUARES - 1:
                self.UpdatePieceOnBoard(Queen(pieceBeingMoved.GetTeam, BoardPoints(xCoord, yCoord)))

    def PerformMoveProcessing(self, pieceBeingMoved, fromCoord: BoardPoints, toCoord: BoardPoints):

        logger.debug("Entered method")

        lastMove = self.GetLastHistoricalMove()
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

        self.PerformPawnPromotionCheck(pieceBeingMoved)

    def PrintProperties(self):
        logger.info("Printing board")
        self.GetBoard().PrintBoard()
        logger.info("Printing all valid white moves")
        MoveHelpers.PrintValidMoves(self.GetBoard(), Board.Constants.TeamEnum.White)
        logger.info("Printing all valid black moves")
        MoveHelpers.PrintValidMoves(self.GetBoard(), Board.Constants.TeamEnum.Black)
        logger.info("Printing history")
        self.GetBoard().PrintHistory()

    # region Property setters and getters

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
