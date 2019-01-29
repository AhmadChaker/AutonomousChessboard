import logging
import logging.handlers
import os


class LogListener:

    @staticmethod
    def Configure():
        rootLogger = logging.getLogger()
        handler = logging.FileHandler('..\log.txt', 'w', 'utf-8')
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(thread)d %(levelname)-8s %(name)s %(funcName)s %(message)s')
        handler.setFormatter(formatter)
        rootLogger.addHandler(handler)

    @staticmethod
    def Listen(logQueue):
        LogListener.Configure()
        rootLogger = logging.getLogger(__name__)
        rootLogger.error("Started log process, PID: " + str(os.getpid()))
        while True:
            try:
                record = logQueue.get()
                if record is None:  # We send this as a sentinel to tell the listener to quit.
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)  # No level or filter logic applied - just do it!
            except Exception:
                import sys, traceback
                print('Whoops! Problem:', file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
