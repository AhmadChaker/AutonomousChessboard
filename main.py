from guizero import App, Text, TextBox, Combo
import logging

logging.basicConfig(filename="log.txt",
                    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    filemode='w',
                    level=logging.DEBUG)

logging.warning("Test1")
logging.error("Test2")


app = App(title="Hello world", width=300, height=200, layout="grid")
film_description = Text(app, text="Which film?", grid=[0,0], align="left")
film_choice = Combo(app, options=["Star Wars", "Frozen", "Lion King"], grid=[1,0], align="left")
app.display()