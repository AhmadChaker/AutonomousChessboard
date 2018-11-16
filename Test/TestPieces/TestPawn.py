import unittest
import Miscellaneous.BoardPoints
from Pieces.NoPiece import NoPiece
from Pieces.Pawn import Pawn
from Board.Constants import TeamEnum
from Board.ChessBoard import ChessBoard
from Board.Movement import Movement
from Miscellaneous.BoardPoints import BoardPoints
from Utilities.BoardHelpers import BoardHelpers
from Board.History import History


class TestPawn(unittest.TestCase):

    def setUp(self):
        # Initialise chess board 2D structure
        self.chessBoard = ChessBoard()
        self.history = History()
        BoardHelpers.UpdateVariables(self.history)

    def tearDown(self):
        # get rid of persisted variables
        BoardHelpers.History = None

    # region Tests of IBase methods
    # IBasePiece methods tested only in this class as they require implementations of abstract methods

    def test_IBasePiece_Constructor_HistorySetToInitialCoordinate(self):
        pawnCoordinate = BoardPoints(2,2)
        pawn = Pawn(TeamEnum.White, pawnCoordinate)

        expectedHistoryLength = 1
        self.assertEqual(len(pawn.GetHistory()), expectedHistoryLength)
        self.assertEqual(pawn.GetHistory()[0], pawnCoordinate)

    def test_IBasePiece_CanMove_ToMovePointUndefined_ReturnsFalse(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        toMoveCoordinate = Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED
        canMove = pawn.CanMove(self.chessBoard, toMoveCoordinate)

        self.assertFalse(canMove)

    def test_IBasePiece_CanMove_NoValidMoves_ReturnsFalse(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        toMoveCoordinate = BoardPoints(2, 2)

        # Put a black piece right in front of the primary pawn so that it can't move anywhere.
        pawnBlack = Pawn(TeamEnum.Black, toMoveCoordinate)
        self.chessBoard.UpdatePieceOnBoard(pawnBlack)

        canMove = pawn.CanMove(self.chessBoard, toMoveCoordinate)

        self.assertFalse(canMove)

    def test_IBasePiece_CanMove_CanMoveCoordinateNotInValidMoveList_ReturnsFalse(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        # To move coordinate is not in the validMoves list
        toMoveCoordinate = BoardPoints(7, 7)

        canMove = pawn.CanMove(self.chessBoard, toMoveCoordinate)

        self.assertFalse(canMove)

    def test_IBasePiece_CanMove_ValidMove_ReturnsTrue(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        # To move coordinate is not in the validMoves list
        toMoveCoordinate = BoardPoints(2, 2)

        canMove = pawn.CanMove(self.chessBoard, toMoveCoordinate)

        self.assertTrue(canMove)

    def test_IBasePiece_Move_CantMove_ReturnsFalse(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        # To move coordinate is not in the validMoves list
        toMoveCoordinate = BoardPoints(2, 7)

        coordinatePrevMove = BoardPoints(2,1)   # Duplicate of previous
        hasMoved = pawn.Move(self.chessBoard, toMoveCoordinate)

        self.assertFalse(hasMoved)
        # Verify History is still unmodified and that coordinate is still unmoved
        self.assertEqual(coordinatePrevMove, pawn.GetCoordinates())
        self.assertEqual(1, len(pawn.GetHistory()))

    def test_IBasePiece_Move_ValidMove_ReturnsTrue(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        toMoveCoordinate = BoardPoints(2, 2)

        hasMoved = pawn.Move(self.chessBoard, toMoveCoordinate)

        self.assertTrue(hasMoved)
        self.assertEqual(toMoveCoordinate, pawn.GetCoordinates())
        self.assertEqual(2, len(pawn.GetHistory()))

    def test_IBasePiece_ForceMove_ReturnsTrue(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        # For tests case, set to an invalid coordinate
        toMoveCoordinate = BoardPoints(2, 7)

        hasMoved = pawn.ForceMove(toMoveCoordinate)

        self.assertTrue(hasMoved)
        self.assertEqual(toMoveCoordinate, pawn.GetCoordinates())
        self.assertEqual(2, len(pawn.GetHistory()))

    def test_IBasePiece_ForceMoveNoHistory_ReturnsTrue(self):
        pawnCoordinate = BoardPoints(2, 1)
        pawn = self.chessBoard.GetPieceAtCoordinate(pawnCoordinate)

        # For tests case, set to an invalid coordinate
        toMoveCoordinate = BoardPoints(2, 7)

        hasMoved = pawn.ForceMoveNoHistory(toMoveCoordinate)

        self.assertTrue(hasMoved)
        self.assertEqual(toMoveCoordinate, pawn.GetCoordinates())
        self.assertEqual(1, len(pawn.GetHistory()))

    # end region

    # Due to unidirectional nature of Pawns, test white and then black Pawns for each case

    # region White Pawn specific
    def test_GetValidMoves_WhitePawn_NoHistory_ReturnsTwoMoves(self):
        whitePawnCoord = BoardPoints(1,1)
        whitePawn = self.chessBoard.GetPieceAtCoordinate(whitePawnCoord)
        actualValidMoves = whitePawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        expectedValidMoves.append(BoardPoints(1,2))
        expectedValidMoves.append(BoardPoints(1,3))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_WhitePawn_HasHistory_ReturnsOneMove(self):
        whitePawnCoord = BoardPoints(1,1)
        whitePawn = self.chessBoard.GetPieceAtCoordinate(whitePawnCoord)

        # add some nonsense history
        whitePawn.GetHistory().append(BoardPoints(2,3))
        whitePawn.GetHistory().append(BoardPoints(1,3))

        actualValidMoves = whitePawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        expectedValidMoves.append(BoardPoints(1, 2))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_WhitePawn_NoHistory_AttackingLeft_ReturnsThreeMoves(self):

        whitePawnCoord = BoardPoints(1,1)
        whitePawn = self.chessBoard.GetPieceAtCoordinate(whitePawnCoord)

        blackPiece = Pawn(TeamEnum.Black, BoardPoints(0,2))
        self.chessBoard.UpdatePieceOnBoard(blackPiece)

        actualValidMoves = whitePawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(1, 2))
        expectedValidMoves.append(BoardPoints(1, 3))
        # Attack move
        expectedValidMoves.append(BoardPoints(0,2))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_WhitePawn_NoHistory_AttackingRight_ReturnsThreeMoves(self):

        whitePawnCoord = BoardPoints(1,1)
        whitePawn = self.chessBoard.GetPieceAtCoordinate(whitePawnCoord)

        blackPiece = Pawn(TeamEnum.Black, BoardPoints(2,2))
        self.chessBoard.UpdatePieceOnBoard(blackPiece)

        actualValidMoves = whitePawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(1, 2))
        expectedValidMoves.append(BoardPoints(1, 3))
        # Attack move
        expectedValidMoves.append(BoardPoints(2,2))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_WhitePawn_EnPassantAttack_Success(self):

        whitePawnCoord = BoardPoints(2, 4)
        whitePawn = Pawn(TeamEnum.White, whitePawnCoord)
        self.chessBoard.UpdatePieceOnBoard(whitePawn)

        # Need this to be a double step move
        # Previous
        blackPawnCoordBeforeMove = BoardPoints(1, 6)
        blackPawnBeforeMove = Pawn(TeamEnum.Black, blackPawnCoordBeforeMove)

        # After
        coordAfterMove = BoardPoints(1, 4)
        blackPawnAfterMove = Pawn(TeamEnum.Black, coordAfterMove)
        self.chessBoard.UpdatePieceOnBoard(blackPawnAfterMove)

        # Last move needs to have been a double step from black

        movement = Movement(blackPawnBeforeMove.GetTeam(), blackPawnBeforeMove.GetPieceEnum(), NoPiece(coordAfterMove).GetPieceEnum(), blackPawnCoordBeforeMove, coordAfterMove, False)
        self.history.AppendMovement(movement)

        actualValidMoves = whitePawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(2, 5))
        # En-passant attack move
        expectedValidMoves.append(BoardPoints(1, 5))

        self.assertEqual(actualValidMoves, expectedValidMoves)
    # end region

    # region Black Pawn

    def test_GetValidMoves_BlackPawn_NoHistory_ReturnsTwoMoves(self):
        blackPawnCoord = BoardPoints(1,6)
        blackPawn = self.chessBoard.GetPieceAtCoordinate(blackPawnCoord)
        actualValidMoves = blackPawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        expectedValidMoves.append(BoardPoints(1,5))
        expectedValidMoves.append(BoardPoints(1,4))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_BlackPawn_HasHistory_ReturnsOneMove(self):
        blackPawnCoord = BoardPoints(1,6)
        blackPawn = self.chessBoard.GetPieceAtCoordinate(blackPawnCoord)

        # add some nonsense history
        blackPawn.GetHistory().append(BoardPoints(2,3))
        blackPawn.GetHistory().append(BoardPoints(1,3))

        actualValidMoves = blackPawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        expectedValidMoves.append(BoardPoints(1, 5))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_BlackPawn_NoHistory_AttackingLeft_ReturnsThreeMoves(self):

        blackPawnCoord = BoardPoints(1,6)
        blackPawn = self.chessBoard.GetPieceAtCoordinate(blackPawnCoord)

        whitePiece = Pawn(TeamEnum.White, BoardPoints(0,5))
        self.chessBoard.UpdatePieceOnBoard(whitePiece)

        actualValidMoves = blackPawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(1, 5))
        expectedValidMoves.append(BoardPoints(1, 4))
        # Attack move
        expectedValidMoves.append(BoardPoints(0,5))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_BlackPawn_NoHistory_AttackingRight_ReturnsThreeMoves(self):

        blackPawnCoord = BoardPoints(1,6)
        blackPawn = self.chessBoard.GetPieceAtCoordinate(blackPawnCoord)

        whitePiece = Pawn(TeamEnum.White, BoardPoints(2,5))
        self.chessBoard.UpdatePieceOnBoard(whitePiece)

        actualValidMoves = blackPawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(1, 5))
        expectedValidMoves.append(BoardPoints(1, 4))
        # Attack move
        expectedValidMoves.append(BoardPoints(2,5))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    def test_GetValidMoves_BlackPawn_EnPassantAttack_Success(self):

        blackPawnCoord = BoardPoints(1, 3)
        blackPawn = Pawn(TeamEnum.Black, blackPawnCoord)
        self.chessBoard.UpdatePieceOnBoard(blackPawn)

        # Need this to be a double step move
        # Previous
        whitePawnCoordBeforeMove = BoardPoints(2, 1)
        whitePawnBeforeMove = Pawn(TeamEnum.White, whitePawnCoordBeforeMove)

        # After
        coordAfterMove = BoardPoints(2, 3)
        whitePawnAfterMove = Pawn(TeamEnum.White, coordAfterMove)
        self.chessBoard.UpdatePieceOnBoard(whitePawnAfterMove)

        # Last move needs to have been a double step from white
        movement = Movement(whitePawnBeforeMove.GetTeam(), whitePawnBeforeMove.GetPieceEnum(), NoPiece(coordAfterMove).GetPieceEnum(), whitePawnCoordBeforeMove, coordAfterMove, False)
        self.history.AppendMovement(movement)

        actualValidMoves = blackPawn.GetValidMoves(self.chessBoard, False)

        expectedValidMoves = []
        # Directly ahead
        expectedValidMoves.append(BoardPoints(1, 2))
        # En-passant attack move
        expectedValidMoves.append(BoardPoints(2, 2))

        self.assertEqual(actualValidMoves, expectedValidMoves)

    # end region
