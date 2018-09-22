from Pieces.Constants import PieceEnums
from Pieces.BasePiece import IBasePiece


class EmptyPiece(IBasePiece):

    def GetPieceStr(self):
        return "-"

    def GetPieceEnum(self):
        return PieceEnums.Empty
