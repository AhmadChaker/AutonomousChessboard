import Pieces.Constants
import Board.Constants
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class King(IBasePiece):

    WhiteString = u'\u2654'
    BlackString = u'\u265A'

    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)
        self.__canCastleQueenSideInTheFuture = True
        self.__canCastleKingSideInTheFuture = True

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return King.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return King.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.King

    def SetCanCastleInTheFuture(self, canCastleInTheFuture):
        self.__canCastleKingSideInTheFuture = canCastleInTheFuture
        self.__canCastleQueenSideInTheFuture = canCastleInTheFuture

    def CanCastleInTheFuture(self):
        return self.__canCastleKingSideInTheFuture or self.__canCastleQueenSideInTheFuture

    def SetCanKingSideCastleInTheFuture(self, canCastleInTheFuture):
        self.__canCastleKingSideInTheFuture = canCastleInTheFuture

    def CanKingSideCastleInTheFuture(self):
        return self.__canCastleKingSideInTheFuture

    def SetCanQueenSideCastleInTheFuture(self, canCastleInTheFuture):
        self.__canCastleQueenSideInTheFuture = canCastleInTheFuture

    def CanQueenSideCastleInTheFuture(self):
        return self.__canCastleQueenSideInTheFuture

    def CanKingSideCastle(self, board, enforceKingIsInCheck):

        if not self.CanKingSideCastleInTheFuture():
            return False

        if not self.CanCastleBaseChecks(board):
            return False

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, Pieces.Constants.PieceEnums.Rook, self.GetTeam())
        rookToCastle = None
        for rook in arrayRooks:
            if rook.IsKingSideRookWithStartingCoordinates():
                rookToCastle = rook
                break

        if rookToCastle is None or not rookToCastle.CanCastleInTheFuture():
            self.SetCanKingSideCastleInTheFuture(False)
            return False

        return rook.CanCastle(board, enforceKingIsInCheck)

    def CanQueenSideCastle(self, board, enforceKingIsInCheck):

        if not self.CanQueenSideCastleInTheFuture():
            return False

        if not self.CanCastleBaseChecks(board):
            return False

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, Pieces.Constants.PieceEnums.Rook, self.GetTeam())
        rookToCastle = None
        for rook in arrayRooks:
            # Y coord is verified in the CanCastle method in the rook
            if rook.IsQueenSideRookWithStartingCoordinates():
                rookToCastle = rook
                break

        if rookToCastle is None or not rookToCastle.CanCastleInTheFuture():
            self.SetCanQueenSideCastleInTheFuture(False)
            return False

        return rook.CanCastle(board, enforceKingIsInCheck)

    def CanCastle(self, board, enforceKingIsInCheck):

        if not self.CanKingSideCastle(board, enforceKingIsInCheck) and not self.CanQueenSideCastle(board, enforceKingIsInCheck):
            return False

        return True

    def CanCastleBaseChecks(self, board):
        # Short circuit check
        if not self.CanCastleInTheFuture():
            return False

        if len(self.GetHistory()) > 1:
            self.SetCanCastleInTheFuture(False)
            logger.debug("King has moved, returning False")
            return False

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, Pieces.Constants.PieceEnums.Rook, self.GetTeam())
        if len(arrayRooks) == 0:
            self.SetCanCastleInTheFuture(False)
            return False

        return True

    def GetCastleMoves(self, board, enforceKingIsInCheck):

        if not self.CanCastle(board, enforceKingIsInCheck):
            return []

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, Pieces.Constants.PieceEnums.Rook, self.GetTeam())
        kingXCoordinate = self.GetCoordinates().GetX()
        kingYCoordinate = self.GetCoordinates().GetY()

        moves = []
        for rook in arrayRooks:
            if rook.CanCastle(board, enforceKingIsInCheck):
                # Rook can castle
                rookXCoord = rook.GetCoordinates().GetX()
                isLeftRook = True if rookXCoord == 0 else False
                if isLeftRook:
                    moves.append(BoardPoints(kingXCoordinate - Board.Constants.KING_CASTLE_SQUARE_MOVES, kingYCoordinate))
                else:
                    moves.append(BoardPoints(kingXCoordinate + Board.Constants.KING_CASTLE_SQUARE_MOVES, kingYCoordinate))

        return moves

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, 0), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(1, -1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, -1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, -1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 0), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(-1, 1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(MoveHelpers.GetValidMoves(self, board, Points(0, 1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(self.GetCastleMoves(board, enforceKingUnderAttackCheck))
        return validMoves
