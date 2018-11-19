import sys
import Board.Constants
import Pieces.Constants
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Rook(IBasePiece):

    WhiteString = u'\u2656'
    BlackString = u'\u265C'
    MoveIterations = sys.maxsize

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)
        self.__canCastleInTheFuture = True

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return Rook.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return Rook.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Rook

    def SetCanCastleInTheFuture(self, canCastleInTheFuture):
        self.__canCastleInTheFuture = canCastleInTheFuture

    def CanCastleInTheFuture(self):
        return self.__canCastleInTheFuture

    def CanCastle(self, board, enforceKingUnderAttackCheck):

        # Short circuit where possible
        if not self.__canCastleInTheFuture:
            return False

        if len(self.GetHistory()) > 1:
            self.__canCastleInTheFuture = False
            logger.debug("Rook has moved, returning False")
            return False

        # Check starting x/y coord in case game is started at a certain configuration
        xCoord = self.GetCoordinates().GetX()
        yCoord = self.GetCoordinates().GetY()

        if xCoord != 0 and xCoord != Board.Constants.MAXIMUM_X_SQUARES-1:
            self.__canCastleInTheFuture = False
            return False

        if (self.GetTeam() == TeamEnum.White and yCoord != 0) or \
                (self.GetTeam() == TeamEnum.Black and yCoord != Board.Constants.MAXIMUM_Y_SQUARES-1):
            self.__canCastleInTheFuture = False
            return False

        if enforceKingUnderAttackCheck:
            if BoardHelpers.IsInCheck(board, self.GetTeam()):
                return False

        arrayKing = BoardHelpers.GetPieceByPieceType(board, Pieces.Constants.PieceEnums.King, self.GetTeam())
        if len(arrayKing) == 0:
            return False

        king = arrayKing[0]

        if len(king.GetHistory()) > 1:
            self.__canCastleInTheFuture = False
            logger.debug("King has moved, returning False")
            return False

        xCoordKing = king.GetCoordinates().GetX()
        xCoordRook = self.GetCoordinates().GetX()
        yCoordRook = self.GetCoordinates().GetY()

        isLeftRook = True if xCoordRook == 0 else False
        xRangeToConsider = range(xCoordRook + 1, xCoordKing) if isLeftRook else range(xCoordKing + 1, xCoordRook)
        kingDirectionVector = Points(-1,0) if isLeftRook else Points(1,0)

        # Ensure all spaces are empty
        for xCoord in xRangeToConsider:
            if board.GetPieceAtCoordinate(BoardPoints(xCoord, yCoordRook)).GetPieceEnum() != Pieces.Constants.PieceEnums.NoPiece:
                return False

        # Need check to see if King is in check as part of any movement
        kingValidMoves = MoveHelpers.GetValidMoves(king, board, kingDirectionVector,
                                                    Board.Constants.KING_CASTLE_SQUARE_MOVES,
                                                    enforceKingUnderAttackCheck)
        if len(kingValidMoves) != Board.Constants.KING_CASTLE_SQUARE_MOVES:
            return False

        return True

    def GetCastleMoves(self, board, enforceKingIsInCheck):
        if not self.CanCastle(board, enforceKingIsInCheck):
            return []

        xCoordRook = self.GetCoordinates().GetX()
        yCoordRook = self.GetCoordinates().GetY()

        isRookOnLeftOfBoard = True if xCoordRook == 0 else False
        if isRookOnLeftOfBoard:
            return [BoardPoints(xCoordRook + Board.Constants.BISHOP_CASTLE_LEFT_TO_RIGHT_MOVES, yCoordRook)]
        else:
            return [BoardPoints(xCoordRook - Board.Constants.BISHOP_CASTLE_RIGHT_TO_LEFT_MOVES, yCoordRook)]

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 0), Rook.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, 1), Rook.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 0), Rook.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, -1), Rook.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(self.GetCastleMoves(board, enforceKingUnderAttackCheck))
        return validMoves
