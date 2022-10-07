""" Настройки драйвера журналирования"""

import logging
from enum import Enum
import sys
from pydantic import BaseSettings

class CustomFormatter(logging.Formatter):
    """Logging colored formatter, 
    from https://alexandra-zaharia.github.io/posts/make-your-own-custom-color-formatter-with-python-logging/"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.blue + self.fmt + self.reset,
            logging.INFO: self.grey+ self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LogLevel(Enum):
    notset = 'notset'
    debug = 'debug'
    info = 'info'
    warning = 'warning'
    error = 'error'
    critical = 'critical'

class Severity(Enum):
    notset = logging.NOTSET
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL

class StreamName(Enum):
    stdout = 'stdout'
    stderr = 'stderr'

class Stream(Enum):
    stdout = sys.stdout
    stderr = sys.stderr

class Settings(BaseSettings):
    log_format: str = '%(levelname)s: [%(asctime)s - %(name)s] %(message)s'
    stream_handler: bool = True
    file_handler: bool = False
    stream_severity: LogLevel = LogLevel.debug
    file_severity: LogLevel = LogLevel.warning
    filename: str = "app.log"
    stream: StreamName = StreamName.stdout.value

    class Config:
        env_file = "log_config.env"

# _log_format = f'%(levelname)s: [%(asctime)s - %(name)s] %(message)s'

conf = Settings()

def get_file_handler(
    filename: str = conf.filename, 
    severity: str = conf.file_severity.value, 
    format = conf.log_format):
    
    logLevel = Severity[severity].value
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logLevel)
    file_handler.setFormatter(logging.Formatter(format))
    return file_handler

def get_stream_handler(
    streamname: str = conf.stream.value,
    severity: str = conf.stream_severity.value,
    format: str = conf.log_format):

    logLevel = Severity[severity].value
    stream = Stream[streamname].value
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setLevel(logLevel)
    stream_handler.setFormatter(CustomFormatter(format))
    return stream_handler

def get_logger(name: str, severity: str):
    logLevel = Severity[severity].value
    logger = logging.getLogger(name)
    logger.setLevel(logLevel)
    if conf.file_handler:
        logger.addHandler(get_file_handler())
    if conf.stream_handler:
        logger.addHandler(get_stream_handler())
    return logger

