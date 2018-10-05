import Utilities.Points
import Utilities.Constants
import Pieces.Constants
from Pieces.IBasePiece import IBasePiece
import logging
logger = logging.getLogger(__name__)


class Knight(IBasePiece):

    WhiteString = u'\u2658'
    BlackString = u'\u265E'
    MoveIterations = 1

    def __init__(self, team, coords):
        IBasePiece.__init__(self, team, coords)

    def GetPieceStr(self):
        team = self.GetTeam()
        if team == Utilities.Constants.TeamEnum.White:
            return Knight.WhiteString
        elif team == Utilities.Constants.TeamEnum.Black:
            return Knight.BlackString

        return Pieces.Constants.BOARD_ERROR_STRING

    def GetPieceEnum(self):
        return Pieces.Constants.PieceEnums.Knight

    def GetValidMoves(self):
        validMoves = []
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(2, 1), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, 2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, 2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-2, 1), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-2, -1), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(-1, -2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(1, -2), Knight.MoveIterations))
        validMoves.extend(Pieces.PieceHelpers.PieceHelpers.GetValidMoves(self, Utilities.Points.Points(2, -1), Knight.MoveIterations))

        logger.info("Printing valid moves (" + str(len(validMoves)) + "), FromCoord: " + self.GetCoordinates().ToString())
        for validMove in validMoves:
            logger.info(validMove.ToString())

        return validMoves
