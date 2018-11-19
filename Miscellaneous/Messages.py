class Status:
    Report = 1
    NoReport = 2


class CanMoveEnum:
    Success = 1
    FromCoordOutOfRange = 2
    ToCoordOutOfRange = 3
    SlotHasNoTeam = 4
    WrongTeam = 5
    InvalidPieceCentricMove = 6


class MoveEnum:
    Success = 1
    FailedToMove = 2
    CheckMate = 3
    Check = 4
    Draw = 5


CanMoveMessageDictionary = {
    CanMoveEnum.Success: "CanMove successful",
    CanMoveEnum.FromCoordOutOfRange: "Invalid move, from coordinate is out of range",
    CanMoveEnum.ToCoordOutOfRange: "Invalid move, to coordinate is out of range",
    CanMoveEnum.SlotHasNoTeam: "Invalid move, attempted to move an empty slot",
    CanMoveEnum.WrongTeam: "Invalid move, wrong team tried to move",
    CanMoveEnum.InvalidPieceCentricMove: "Invalid move, piece can't move to this location"
}

MoveMessageDictionary = {
    MoveEnum.Success: "Move successful",
    MoveEnum.FailedToMove: "Failed to move, try again",
    MoveEnum.CheckMate: "Checkmate! Game over",
    MoveEnum.Check: "Player is in check",
    MoveEnum.Draw: "Draw has been declared",
}
