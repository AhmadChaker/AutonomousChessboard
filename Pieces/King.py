import Miscellaneous.Constants
from Miscellaneous.Constants import PieceEnums, TeamEnum
from Miscellaneous.BoardPoints import BoardPoints
from Miscellaneous.Points import Points
from Utilities.BoardHelpers import BoardHelpers
from Utilities.MoveHelpers import MoveHelpers
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class King(IBasePiece):

    WhitePieceString = u'\u2654'
    BlackPieceString = u'\u265A'
    WhitePieceFenString = 'K'
    BlackPieceFenString = 'k'

    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__( self, team, coords)
        self.CanCastleQueenSideInTheFuture = True
        self.CanCastleKingSideInTheFuture = True

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return King.WhitePieceString
        elif team == TeamEnum.Black:
            return King.BlackPieceString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetFenRepresentation(self):
        team = self.GetTeam()
        if team == TeamEnum.White:
            return King.WhitePieceFenString
        elif team == TeamEnum.Black:
            return King.BlackPieceFenString

        return Miscellaneous.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return PieceEnums.King

    # region CanPotentiallyCastleInTheFutureBaseChecks

    # sideToCastle will either be queen or king side
    def CanPotentiallyCastleInTheFutureBaseCheck(self, board, sideToCastle):
        if len(self.GetHistory()) > 1:
            logger.debug("King has moved, returning False")
            return False

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Rook, self.GetTeam())
        if len(arrayRooks) == 0:
            return False

        rookToCastle = None
        for rook in arrayRooks:
            if (sideToCastle == PieceEnums.Queen and rook.IsQueenSideRookWithStartingCoordinates()) or \
                    (sideToCastle == PieceEnums.King and rook.IsKingSideRookWithStartingCoordinates()):
                rookToCastle = rook
                break

        if rookToCastle is None or not rookToCastle.CanCastleInTheFuture():
            return False

        return True

    # endregion

    # region Queen side castling properties/methods

    def CanPotentiallyQueenSideCastleInTheFuture(self, board):
        # short circuit check
        if not self.CanCastleQueenSideInTheFuture:
            return False

        if not self.CanPotentiallyCastleInTheFutureBaseCheck(board, PieceEnums.Queen):
            self.CanCastleQueenSideInTheFuture = False
            return False

        return True

    def CanQueenSideCastle(self, board, enforceKingIsInCheck):
        if not self.CanPotentiallyQueenSideCastleInTheFuture(board):
            return False

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Rook, self.GetTeam())
        rookToCastle = None
        for rook in arrayRooks:
            # Y coord is verified in the CanCastle method in the rook
            if rook.IsQueenSideRookWithStartingCoordinates():
                rookToCastle = rook
                break

        return rookToCastle.CanCastle(board, enforceKingIsInCheck)

    # endregion

    # region King side castling properties/methods

    def CanPotentiallyKingSideCastleInTheFuture(self, board):
        # short circuit check
        if not self.CanCastleKingSideInTheFuture:
            return False

        if not self.CanPotentiallyCastleInTheFutureBaseCheck(board, PieceEnums.King):
            self.CanCastleKingSideInTheFuture = False
            return False

        return True

    def CanKingSideCastle(self, board, enforceKingIsInCheck):
        if not self.CanPotentiallyKingSideCastleInTheFuture(board):
            return False

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Rook, self.GetTeam())
        rookToCastle = None
        for rook in arrayRooks:
            # Y coord is verified in the CanCastle method in the rook
            if rook.IsKingSideRookWithStartingCoordinates():
                rookToCastle = rook
                break

        return rookToCastle.CanCastle(board, enforceKingIsInCheck)

    # endregion

    def CanCastle(self, board, enforceKingIsInCheck):
        if not self.CanKingSideCastle(board, enforceKingIsInCheck) and not self.CanQueenSideCastle(board, enforceKingIsInCheck):
            return False

        return True

    def GetCastleMoves(self, board, enforceKingIsInCheck):

        if not self.CanCastle(board, enforceKingIsInCheck):
            return []

        arrayRooks = BoardHelpers.GetPieceByPieceType(board, PieceEnums.Rook, self.GetTeam())
        kingXCoordinate = self.GetCoordinates().GetX()
        kingYCoordinate = self.GetCoordinates().GetY()

        moves = []
        for rook in arrayRooks:
            if rook.CanCastle(board, enforceKingIsInCheck):
                # Rook can castle
                rookXCoord = rook.GetCoordinates().GetX()
                isLeftRook = True if rookXCoord == 0 else False
                if isLeftRook:
                    moves.append(BoardPoints(kingXCoordinate - Miscellaneous.Constants.KING_CASTLE_SQUARE_MOVES, kingYCoordinate))
                else:
                    moves.append(BoardPoints(kingXCoordinate + Miscellaneous.Constants.KING_CASTLE_SQUARE_MOVES, kingYCoordinate))

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
