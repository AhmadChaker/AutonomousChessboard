import logging
import sys
import configparser


logger = logging.getLogger(__name__)


class OSConfiguration:

    WindowsHeadingName = "windows"
    LinuxHeadingName = "linux"
    ConfigFile = "..\config.ini"
    VariableNamePathToEngine = "PathToEngine"

    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.PathToEngine = None

    def ReadConfiguration(self):
        self.__config.read(OSConfiguration.ConfigFile)

        if OSConfiguration.IsWindows():
            if OSConfiguration.WindowsHeadingName not in self.__config:
                logger.error("Windows heading name is not found in the config file")
                return

            if OSConfiguration.VariableNamePathToEngine not in self.__config[OSConfiguration.WindowsHeadingName]:
                logger.error("PathToEngine is not found in the config file")

            self.PathToEngine = self.__config[OSConfiguration.WindowsHeadingName][OSConfiguration.VariableNamePathToEngine]
        elif OSConfiguration.IsUnix():
            if OSConfiguration.LinuxHeadingName not in self.__config:
                logger.error("Linux heading name is not found in the config file")
                return

            if OSConfiguration.VariableNamePathToEngine not in self.__config[OSConfiguration.LinuxHeadingName]:
                logger.error("PathToEngine is not found in the config file")

            self.PathToEngine = self.__config[OSConfiguration.LinuxHeadingName][OSConfiguration.VariableNamePathToEngine]
        else:
            logger.error("Unknown reported os: " + sys.platform)

    @staticmethod
    def IsWindows():
        if sys.platform.startswith('win'):
            return True
        return False

    @staticmethod
    def IsUnix():
        if sys.platform.startswith('linux'):
            return True
        return False

