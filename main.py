import logging
import Game
import Utilities.CoordinateConverters
import Miscellaneous.Points
from Utilities.BoardHelpers import BoardHelpers
from guizero import App, Text, TextBox, PushButton

# setup logger
logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s %(funcName)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG)

t1 = Game.Game()
BoardHelpers.UpdateVariables(t1.GetHistory())

t1.PrintBoard()


def ClickedButton():
    fromCoordValue = FromCoordinateTextBox.value
    toCoordValue = ToCoordinateTextBox.value

    fromArrayCoords = Utilities.CoordinateConverters.ConvertChessToArrayCoordinates(fromCoordValue)
    if fromArrayCoords == Miscellaneous.Points.POINTS_UNDEFINED:
        logging.error("Invalid FromCoord: " + str(fromCoordValue))
        return

    toArrayCoords = Utilities.CoordinateConverters.ConvertChessToArrayCoordinates(toCoordValue)
    if toArrayCoords == Miscellaneous.Points.POINTS_UNDEFINED:
        logging.error("Invalid ToCoord: " + str(toCoordValue))
        return

    t1.Move(fromArrayCoords, toArrayCoords)


app = App(title="Sheena", width=600, height=600, layout="grid")
FromCoordinateTextBlock = Text(app, text="From Coordinates", grid=[0,0], align="left")
FromCoordinateTextBox = TextBox(app, grid=[1,0], align="left")
ToCoordinateTextBlock = Text(app, text="To Coordinates", grid=[2,0], align="left")
ToCoordinateTextBox = TextBox(app, grid=[3,0], align="left")
GoButton = PushButton(app, grid=[4,0], text="Go", command=ClickedButton)
app.display()

