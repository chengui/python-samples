""" A simple console handler dispatching different messages """

import os
import sys
import logging


class ConsoleHandler(logging.StreamHandler):
    """ A console handler that dispatch logging record

    This handler will dispatch all messages, ERROR messages and above
    will log to sys.stderr, the other messages will log to sys.stdout
    """

    def __init__(self):
        logging.StreamHandler.__init__(self)
        # reset self.stream, it's not assigned before dispatch
        self.stream = None

    def emit(self, record):
        """ Dispatch the log record to different stream """
        if record.levelno >= logging.ERROR:
            self.__emit(record, sys.stderr)
        else:
            self.__emit(record, sys.stdout)

    def __emit(self, record, stream):
        """ Call parent emit """
        self.stream = stream
        logging.StreamHandler.emit(self, record)

def test():
    """ test ConsoleHandler """
    logger = logging.Logger('consolelog', logging.DEBUG)
    logger.addHandler(ConsoleHandler())

    # redirect stderr to /dev/null
    nul = open(os.devnull, 'w')
    err = os.dup(2)
    os.dup2(nul.fileno(), 2)

    # logging messages
    print("======== redirect =========")
    logger.debug('a debug message')
    logger.info('an info message')
    logger.warning('a warning message')
    logger.error('an error message')

    # restore stderr
    os.dup2(err, 2)

    # logging messages again
    print("======== after redirect =========")
    logger.debug('a debug message')
    logger.info('an info message')
    logger.warning('a warning message')
    logger.error('an error message')

if __name__ == "__main__":
    test()
