from enum import Enum

BOARD_ERROR_STRING = "Err"

# Valid chess board coordinates
ALPHABETICAL_BOARD_ORDINATES = "ABCDEFGH"
NUMERICAL_BOARD_ORDINATES = "12345678"

# Board related
MAXIMUM_X_SQUARES = 8
MAXIMUM_Y_SQUARES = 8
WHITE_PAWNS_Y_ARRAY_COORDINATE = 1
BLACK_PAWNS_Y_ARRAY_COORDINATE = 6

# Gameplay constants
DRAW_CONDITION_TOTAL_MOVES = 150

# Castling related constants
KING_CASTLE_SQUARE_MOVES = 2
BISHOP_CASTLE_LEFT_TO_RIGHT_MOVES = 3
BISHOP_CASTLE_RIGHT_TO_LEFT_MOVES = 2

# Pawn constants
MAXIMUM_PAWN_FORWARD_MOVEMENT = 2

# Miscellaneous constants
STRING_CHARACTERS_IN_COORDINATE = 2


class TeamEnum(Enum):
    NoTeam = 1
    White = 2
    Black = 3


class PlayerEnum(Enum):
    Unknown = 1
    AI = 2
    Human = 3


class GameType(Enum):
    Unknown = 1
    AIvsHuman = 2
    HumanvsHuman = 3
    AIvsAI = 4


# Piece specific constants
class PieceEnums(Enum):
    NoPiece = 1
    Pawn = 2
    Rook = 3
    Knight = 4
    Bishop = 5
    Queen = 6
    King = 7
