""" A simple colored logging class with colored levelname """

import os
import sys
import logging

# terminal color definition
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)

COLOR_SEQ = "\033[%dm"  # common color sequence
RESET_SEQ = "\033[0m"   # reset color sequence

# map from levelname to color
LOGCOLORS = {
    'WARNING':  COLOR_SEQ % YELLOW,
    'INFO':     COLOR_SEQ % GREEN,
    'DEBUG':    COLOR_SEQ % BLUE,
    'CRITICAL': COLOR_SEQ % YELLOW,
    'ERROR':    COLOR_SEQ % RED,
}


class LevelFilter(logging.Filter):
    """ Filter for output selective levels """

    def __init__(self, name='', levels=None):
        logging.Filter.__init__(self, name)
        self.levels = levels

    def filter(self, record):
        """ Show the records in self.levels filtering """
        if self.levels:
            return record.levelname in self.levels
        return False


class ColorFormatter(logging.Formatter):
    """ Formatter with colored levelname """

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        """ Colorizing formatter """
        if record.levelname in LOGCOLORS:
            colorlevel = LOGCOLORS[record.levelname] + \
                record.levelname + RESET_SEQ
            record.levelname = colorlevel
        return logging.Formatter.format(self, record)


class ColorLogger(logging.Logger):
    """ Logger class with colored levelname """

    def __init__(self, name, *args, **kwargs):
        logging.Logger.__init__(self, name, *args, **kwargs)
        self._formatter = ColorFormatter(fmt="%(levelname)s: %(message)s")

        self._default_handlers = [
            logging.StreamHandler(sys.stdout),
            logging.StreamHandler(sys.stderr),
        ]

        self._default_handlers[0].addFilter(LevelFilter(['DEBUG', 'INFO']))
        self._default_handlers[0].addFilter(
            LevelFilter(['WARNING', 'CRITICAL', 'ERROR']))

        for handler in self._default_handlers:
            handler.setFormatter(self._formatter)
            self.addHandler(handler)


# initialize logger module
logging.setLoggerClass(ColorLogger)
LOGGER = logging.getLogger('colorlog')

def error(msg):
    """ Logs a message with level ERROR on the colorlog logger """
    LOGGER.error(msg)


def warning(msg):
    """ Logs a message with level WARNING on the colorlog logger """
    LOGGER.warning(msg)


def info(msg):
    """ Logs a message with level INFO on the colorlog logger """
    LOGGER.info(msg)


def debug(msg):
    """ Logs a message with level DEBUG on the colorlog logger """
    LOGGER.debug(msg)


def setLevel(level):
    """ Set logger level """
    LOGGER.setLevel(level)

def test():
    import sys
    log = sys.modules[__name__]
    log.setLevel("DEBUG")
    log.debug("a debug message")
    log.info("an info message")
    log.warning("a warning message")
    log.error("an error message")

if __name__ == '__main__':
    test()
