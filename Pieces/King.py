import Pieces.Constants
import Miscellaneous.Points
import Board.Constants
from Miscellaneous.Points import Points
from Utilities.BoardHelpers import BoardHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class King(IBasePiece):

    WhiteString = u'\u2654'
    BlackString = u'\u265A'

    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)
        self.__isCastlingPossibleForPiece = True

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Board.Constants.TeamEnum.White:
            return King.WhiteString
        elif team == Board.Constants.TeamEnum.Black:
            return King.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.King

    def CanCastle(self, board, enforceKingIsInCheck):
        # Short circuit check
        if not self.__isCastlingPossibleForPiece:
            return False

        if len(self.GetHistory()) > 1:
            self.__isCastlingPossibleForPiece = False
            logger.debug("King has moved, returning False")
            return False

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, Pieces.Constants.PieceEnums.Rook, self.GetTeam())
        if len(arrayRooks) == 0:
            return False

        rooksThatCanCastle = []
        hasAnyRookRemainedStationary = False
        for rook in arrayRooks:
            if len(rook.GetHistory()) <= 1:
                hasAnyRookRemainedStationary = True
            if rook.CanCastle(board, enforceKingIsInCheck):
                rooksThatCanCastle.append(rook)

        if not hasAnyRookRemainedStationary:
            self.__isCastlingPossibleForPiece = False
            return False

        if len(rooksThatCanCastle) == 0:
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
                    moves.append(Points(kingXCoordinate - Board.Constants.KING_CASTLE_SQUARE_MOVES, kingYCoordinate))
                else:
                    moves.append(Points(kingXCoordinate + Board.Constants.KING_CASTLE_SQUARE_MOVES, kingYCoordinate))

        return moves

    def GetValidMoves(self, board, enforceKingUnderAttackCheck):
        validMoves = []
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(1, 1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(1, 0), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(1, -1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(0, -1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(-1, -1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(-1, 0), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(-1, 1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(BoardHelpers.GetValidMoves(self, board, Miscellaneous.Points.Points(0, 1), King.MoveIterations, enforceKingUnderAttackCheck))
        validMoves.extend(self.GetCastleMoves(board, enforceKingUnderAttackCheck))
        return validMoves
