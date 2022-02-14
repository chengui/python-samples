"""
TeeHandler is supposed to log messages from stdout/stderr
as well as logging module, and the log target will be both
stdout/stderr and file, just like what 'tee' do in linux
"""

import sys
import logging

class TeeStream(object):
    """ Tee-like stream that sync output to standard stream and file """
    def __init__(self, stream, streamfd=0):
        self.stream = stream
        self.streamfd = streamfd
        if self.streamfd == 1:
            self.stdstream = sys.stdout
            sys.stdout = self
        if self.streamfd == 2:
            self.stdstream = sys.stderr
            sys.stderr = self

    def __del__(self):
        if self.streamfd == 1:
            sys.stdout = self.stdstream
        if self.streamfd == 2:
            sys.stderr = self.stdstream

    def write(self, data):
        """ Write data to file and standard stream """
        if self.streamfd in (1, 2):
            self.stream.write(data)
            self.stdstream.write(data)

    def flush(self):
        pass


class TeeHandler(logging.FileHandler):
    """ Handler that log output from stdout/stderr via TeeStream """
    def __init__(self, filename, streamfd=0, **kwargs):
        logging.FileHandler.__init__(self, filename, **kwargs)
        self.stream = TeeStream(self.stream, streamfd)


def test():
    """ Test routine """
    logger = logging.Logger('root', logging.DEBUG)
    handler = TeeHandler('./log', 1, mode='w')
    logger.addHandler(handler)

    print("hello, stderr", file=sys.stderr)
    print("hello, stdout", file=sys.stdout)

    logger.debug("a debug message")
    logger.info("an info message")
    logger.warning("a warning message")
    logger.error("an error message")

if __name__ == "__main__":
    test()
