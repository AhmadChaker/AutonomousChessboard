import logging
import Chessboard
import Utilities.Points
import Utilities.CoordinateConverters
from guizero import App, Text, TextBox, Combo

# setup logger
logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(name)s %(funcName)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG)

t1 = Chessboard.ChessBoard()
t1.PrintBoard()

app = App(title="Hello Sheena", width=600, height=600, layout="grid")
film_description = Text(app, text="What destination?", grid=[0,0], align="left")
film_choice = Combo(app, options=["Singapore", "Phuket", "Bangkok"], grid=[1,0], align="left")
app.display()