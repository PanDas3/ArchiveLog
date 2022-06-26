from logging import getLogger
from logging import basicConfig
from logging import error
from logging import info
from logging import warning
from logging import ERROR
from logging import INFO
from logging import WARNING
from logging import DEBUG
from logging import exception
from time import strftime
from os import mkdir, path

class Log():
    def __init__(self) -> None:
        self.currentdate = strftime("%Y%m%d")
        self.log = getLogger("Logger")
        if(path.isdir("Logs") == False):
            mkdir("Logs")

    def error(self, msg):
        self.log.setLevel(ERROR)
        basicConfig(filename=f"Logs\\ArchiveLog{self.currentdate}.log", level=ERROR, format="%(asctime)s \t %(levelname)s: \t %(message)s")
        error(msg)

    def info(self, msg):
        self.log.setLevel(INFO)
        basicConfig(filename=f"Logs\\ArchiveLog{self.currentdate}.log", level=INFO, format="%(asctime)s \t %(levelname)s: \t\t %(message)s")
        info(msg)

    def warning(self, msg):
        self.log.setLevel(WARNING)
        basicConfig(filename=f"Logs\\ArchiveLog{self.currentdate}.log", level=WARNING, format="%(asctime)s \t %(levelname)s: \t %(message)s")
        warning(msg)

    def exception(self, msg):
        self.log.setLevel(DEBUG)
        basicConfig(filename=f"Logs\\ArchiveLog{self.currentdate}.log", level=DEBUG, format="%(asctime)s \t %(levelname)s: \t %(message)s")
        exception(msg)

    def __del__(self):
        del self.log
        del self.currentdate