import unittest
import Miscellaneous.BoardPoints
import Utilities.CoordinateConverters
from Miscellaneous.BoardPoints import BoardPoints


class TestCoordinateConverters(unittest.TestCase):

    # region IsPointInRange Tests
    def test_IsPointInRange_XYInRange_ReturnsValid(self):
        boardPoint = BoardPoints(5,5)
        self.assertTrue(Utilities.CoordinateConverters.IsPointInRange(boardPoint))

    def test_IsPointInRange_XNotInRange_ReturnsInvalid(self):
        boardPoint = BoardPoints(-1,5)
        self.assertFalse(Utilities.CoordinateConverters.IsPointInRange(boardPoint))

    def test_IsPointInRange_YNotInRange_ReturnsInvalid(self):
        boardPoint = BoardPoints(1,-5)
        self.assertFalse(Utilities.CoordinateConverters.IsPointInRange(boardPoint))

    # endregion

    # region ConvertInputToPointCoordinates

    def test_ConvertInputToPointCoordinates_InputIncorrectLength_ReturnsInvalid(self):
        input = "A11"
        self.assertEqual(Utilities.CoordinateConverters.ConvertInputToPointCoordinates(input),
                         Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED)

    def test_ConvertInputToPointCoordinates_FirstPartInputIsNumerical_ReturnsInvalid(self):
        input = "22"
        self.assertEqual(Utilities.CoordinateConverters.ConvertInputToPointCoordinates(input),
                         Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED)

    def test_ConvertInputToPointCoordinates_SecondPartInputIsAlphabetical_ReturnsInvalid(self):
        input = "AC"
        self.assertEqual(Utilities.CoordinateConverters.ConvertInputToPointCoordinates(input),
                         Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED)

    def test_ConvertInputToPointCoordinates_FirstPartInputIsLowerCase_ReturnsValid(self):
        input = "a5"
        expectedOutput = BoardPoints(0,4)
        self.assertEqual(Utilities.CoordinateConverters.ConvertInputToPointCoordinates(input),
                         expectedOutput)

    def test_ConvertInputToPointCoordinates_FirstPartInputIsOutOfAlphaRange_ReturnsValid(self):
        input = "P3"
        self.assertEqual(Utilities.CoordinateConverters.ConvertInputToPointCoordinates(input),
                         Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED)

    def test_ConvertInputToPointCoordinates_SecondPartInputIsOutOfNumericalRange_ReturnsValid(self):
        input = "A9"
        self.assertEqual(Utilities.CoordinateConverters.ConvertInputToPointCoordinates(input),
                         Miscellaneous.BoardPoints.BOARD_POINTS_UNDEFINED)

    def test_ConvertInputToPointCoordinates_ArgumentValid_ReturnsValid(self):
        input = "B3"
        expectedOutput = BoardPoints(1,2)
        self.assertEqual(Utilities.CoordinateConverters.ConvertInputToPointCoordinates(input),
                         expectedOutput)
    # endregion
