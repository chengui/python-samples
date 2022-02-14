""" A file-like stream like StringIO """

import sys
from io import StringIO

STDOUT = 1
STDERR = 2

class StringStream(object):
    """ Stream based StringIO, support stdout and stderr redirect """

    def __init__(self, stdfd=0):
        self.stdfd = stdfd
        self.stream = StringIO()
        self._stdfunc = [
            (),
            (STDOUT,),
            (STDERR,),
            (STDOUT, STDERR),
        ]

    def __redirect(self, stream, restore=False):
        """ Redirect or resotre stdout or stderr stream

        @stream: stream directive, STDOUT or STDERR
        @restore: if true restore the specified stream
        """
        if stream == STDOUT:
            sys.stdout = sys.__stdout__ if restore else self.stream
        elif stream == STDERR:
            sys.stderr = sys.__stderr__ if restore else self.stream
        else:
            raise Exception("redirect error")

    def open(self):
        """ Enable stream redirect """
        for stream in self._stdfunc[self.stdfd]:
            self.__redirect(stream, False)
        return self

    def close(self):
        """ Disable stream redirect """
        for stream in self._stdfunc[self.stdfd]:
            self.__redirect(stream, True)

    def read(self, size=None):
        """ Read the stored value from StringStream """
        return self.stream.getvalue()

    def write(self, data=None):
        """ Write the data to StringStream """
        return self.stream.write(data)

