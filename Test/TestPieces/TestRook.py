import unittest
from Board.ChessBoard import ChessBoard
from Pieces.Rook import Rook
from Pieces.King import King
from Pieces.EmptyPiece import EmptyPiece
from Board.Constants import TeamEnum
from Miscellaneous.BoardPoints import BoardPoints
from Utilities.BoardHelpers import BoardHelpers
from Test.Helpers.Helper import Helper
from Board.History import History


class TestRook(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()

        BoardHelpers.UpdateVariables(History())

    def tearDown(self):
        BoardHelpers.UpdateVariables(None)

    # region GetValidMoves tests

    def test_GetValidMoves__CastlingNotAnOption_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Put a new rook in middle
        rook = Rook(TeamEnum.White, BoardPoints(3, 3))
        self.chessBoard.UpdatePieceOnBoard(rook)

        expectedValidMoves = []

        # Top
        expectedValidMoves.append(BoardPoints(3, 4))
        expectedValidMoves.append(BoardPoints(3, 5))
        expectedValidMoves.append(BoardPoints(3, 6))
        expectedValidMoves.append(BoardPoints(3, 7))

        # Left
        expectedValidMoves.append(BoardPoints(2, 3))
        expectedValidMoves.append(BoardPoints(1, 3))
        expectedValidMoves.append(BoardPoints(0, 3))

        # Bottom
        expectedValidMoves.append(BoardPoints(3, 2))
        expectedValidMoves.append(BoardPoints(3, 1))
        expectedValidMoves.append(BoardPoints(3, 0))

        # Right
        expectedValidMoves.append(BoardPoints(4, 3))
        expectedValidMoves.append(BoardPoints(5, 3))
        expectedValidMoves.append(BoardPoints(6, 3))
        expectedValidMoves.append(BoardPoints(7, 3))

        expectedValidMoves.sort()

        validMoves = rook.GetValidMoves(self.chessBoard, False)
        validMoves.sort()
        self.assertEqual(validMoves, expectedValidMoves)

    def test_GetValidMoves__LeftCastlingIsAnOption_ReturnsValidMoves(self):

        self.chessBoard.RemoveAllPieces()

        # Remove pieces between rooks and king
        rook = Rook(TeamEnum.White, BoardPoints(0, 0))
        self.chessBoard.UpdatePieceOnBoard(rook)

        king = King(TeamEnum.White, BoardPoints(4, 0))
        self.chessBoard.UpdatePieceOnBoard(king)

        expectedValidMoves = []

        # Top
        expectedValidMoves.append(BoardPoints(0, 1))
        expectedValidMoves.append(BoardPoints(0, 2))
        expectedValidMoves.append(BoardPoints(0, 3))
        expectedValidMoves.append(BoardPoints(0, 4))
        expectedValidMoves.append(BoardPoints(0, 5))
        expectedValidMoves.append(BoardPoints(0, 6))
        expectedValidMoves.append(BoardPoints(0, 7))

        # Right
        expectedValidMoves.append(BoardPoints(1, 0))
        expectedValidMoves.append(BoardPoints(2, 0))
        expectedValidMoves.append(BoardPoints(3, 0))

        expectedValidMoves.sort()

        validMoves = rook.GetValidMoves(self.chessBoard, False)
        validMoves.sort()
        # valid Moves will have some duplicate entries due to castling moves being appended without uniqueness check
        uniqueValidMoves = Helper.GetUniqueElements(validMoves)
        self.assertEqual(uniqueValidMoves, expectedValidMoves)

    # endregion

    # region GetCastleMoves tests

    def test_GetCastleMoves_CannotCastle_ReturnsEmptyList(self):

        leftRookCoordinates = BoardPoints(0,0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # remove possibilities of castling by moving rook
        rook.Move(self.chessBoard, BoardPoints(1,0))
        # move back
        rook.Move(self.chessBoard, BoardPoints(0,0))

        validMoves = rook.GetCastleMoves(self.chessBoard, False)
        expectedList = []
        self.assertEqual(expectedList, validMoves)

    def test_GetCastleMoves_IsLeftCastle_ReturnsCoords(self):

        leftRookCoordinates = BoardPoints(0,0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Clear out the left pieces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        validMoves = rook.GetCastleMoves(self.chessBoard, False)
        expectedList = [BoardPoints(3, 0)]
        self.assertEqual(expectedList, validMoves)

    def test_GetCastleMoves_IsRightCastle_ReturnsCoords(self):

        rightRookCoordinates = BoardPoints(7, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(rightRookCoordinates)

        # Clear out the right spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(5, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(6, 0)))

        validMoves = rook.GetCastleMoves(self.chessBoard, False)
        expectedList = [BoardPoints(5, 0)]
        self.assertEqual(expectedList, validMoves)

    # endregion

    # region CanCastle tests

    def test_CanCastle_CanNeverCastlePieceSetToTrue_ReturnsFalse(self):

        rightRookCoordinates = BoardPoints(0, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(rightRookCoordinates)

        # Clear out the right spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        rook.SetCanNeverCastleThisPiece(True)
        canCastle = rook.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)

    def test_CanCastle_RookHasMovedBefore_ReturnsFalse(self):

        leftRookCoordinates = BoardPoints(0, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Clear out the right spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        rook.Move(self.chessBoard, BoardPoints(1,0))

        canCastle = rook.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertTrue(rook.GetCanNeverCastleThisPiece())

    def test_CanCastle_KingIsInCheck_ReturnsFalse(self):
        leftRookCoordinates = BoardPoints(7, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Clear out the right spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        # Place another teams Rook right in front of the white king
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.Black, BoardPoints(4,1)))

        canCastle = rook.CanCastle(self.chessBoard, True)
        self.assertFalse(canCastle)
        self.assertFalse(rook.GetCanNeverCastleThisPiece())

    def test_CanCastle_KingHasMoved_ReturnsFalse(self):
        leftRookCoordinates = BoardPoints(0, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Clear out the right spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        king = self.chessBoard.GetPieceAtCoordinate(BoardPoints(4,0))
        king.Move(self.chessBoard, BoardPoints(3, 0))
        king.Move(self.chessBoard, BoardPoints(4, 0))

        canCastle = rook.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertTrue(rook.GetCanNeverCastleThisPiece())

    def test_CanCastle_PieceBetweenRookAndKingNonEmpty_ReturnsFalse(self):
        leftRookCoordinates = BoardPoints(0, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Only clear out one space between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        canCastle = rook.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(rook.GetCanNeverCastleThisPiece())

    def test_CanCastle_KingInCheckInTheMiddleOfCastle_ReturnsFalse(self):
        leftRookCoordinates = BoardPoints(0, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Clear out the right spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        # put an opposing team rook so that the King is in check in the middle of the move
        self.chessBoard.UpdatePieceOnBoard(Rook(TeamEnum.Black, BoardPoints(2,0)))

        canCastle = rook.CanCastle(self.chessBoard, False)
        self.assertFalse(canCastle)
        self.assertFalse(rook.GetCanNeverCastleThisPiece())

    def test_CanCastle_LeftRook_CastlingConditionsSatisfied_ReturnsTrue(self):
        leftRookCoordinates = BoardPoints(0, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Clear out the right spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(1, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(2, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(3, 0)))

        canCastle = rook.CanCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    def test_CanCastle_RightRook_CastlingConditionsSatisfied_ReturnsTrue(self):
        leftRookCoordinates = BoardPoints(7, 0)
        rook = self.chessBoard.GetPieceAtCoordinate(leftRookCoordinates)

        # Clear out the left spaces between rook and king
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(6, 0)))
        self.chessBoard.UpdatePieceOnBoard(EmptyPiece(BoardPoints(5, 0)))

        canCastle = rook.CanCastle(self.chessBoard, False)
        self.assertTrue(canCastle)

    # endregion
