import chess.uci
import logging
from Uci.Levels import Level
logger = logging.getLogger(__name__)

# UCI protocol - GUI to engine
# 1) Uci | command will be sent once as the first command after booting, this switches engine to UCI mode
# 2) IsReady, SetOption | Engine waits for isready or setoption command to set up its internal parameters
# 3) Position | There needs to be a position command to tell the engine the current position
# 4) Go | Starts calculating


class Engine:

    def __init__(self, engineUrl):
        self.__engineUrl = engineUrl
        self.__board = chess.Board()
        self.__level = None
        self.__engine = None

    def SetLevel(self, level:Level):
        self.__level = level

    def StartEngine(self):
        self.__engine = chess.uci.popen_engine(self.__engineUrl)
        self.__SendUciCommand()
        return self.IsAlive()

    def __SendUciCommand(self):
        return self.__engine.uci()

    def IsAlive(self):
        return self.__engine.is_alive()

    def ConfigureLevel(self, level:Level):
        if level is None:
            logger.error("Failed validation checks, level is None")
            return
        self.__level = level

        if not self.IsAlive():
            logger.error("Failed validation checks, engine is dead")
            return

        return self.__engine.setoption(self.__level.GetSkill())

    def ObtainMove(self, fenRep):
        # Validation checks
        if fenRep is None:
            logger.error("Failed validation checks, fen representation is None")
            return

        if self.__level is None:
            logger.error("Failed validation checks, level is None")
            return

        if not self.IsAlive():
            logger.error("Failed validation checks, engine is dead")
            return

        self.__board.set_fen(fenRep)
        self.__engine.position(self.__board)

        # TODO: wrap this in a try catch as it could throw an exception
        goResult = self.__engine.go(movetime=self.__level.GetThinkingTime(), depth=self.__level.GetDepth())
        return goResult
