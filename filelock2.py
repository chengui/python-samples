import os
import errno
import fcntl

class LockError(Exception):
    pass

class FileLock(object):
    """ A file locking implementation

        a fixed file locker droped singleton pattern
    """
    # share states by class global variable
    __shared__ = {}

    def __init__(self, fpath):
        """ Initialize the globals and the instance variables """
        if not self.__shared__:
            # initial the globals
            self.__shared__['lockpath'] = fpath

            if not os.path.exists(fpath):
                lockfile = os.open(fpath, os.O_CREAT | os.O_RDWR)
            else:
                lockfile = os.open(fpath, os.O_RDWR)
            self.__shared__['lockfile'] = lockfile
            self.__shared__['counter'] = 0

        # override instance __dict__ with the global __shared__
        self.__dict__ = self.__shared__
        # set lock flags default to False
        self.islocked = False
        # increase the count of active instances
        # NOTE: the process context doesn't change
        self.counter += 1

    def acquire(self):
        """ Acquire a lock """
        if not self.islocked:
            fcntl.flock(self.lockfile, fcntl.LOCK_EX)
            self.islocked = True

    def release(self):
        """ Release lock """
        if self.islocked:
            fcntl.flock(self.lockfile, fcntl.LOCK_UN)
            self.islocked = False

    def __enter__(self):
        """ Activated when entering the with statement """
        if not self.islocked:
            self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        """ Activated when leaving the with statement """
        if self.islocked:
            self.release()

    def __del__(self):
        """ Clean up the left stuff when all instances exit """
        # decrease the count of active instance
        self.counter -= 1
        if self.counter != 0:
            return
        # when no instance left in current process context,
        # clean up the lock file
        if self.lockfile:
            os.close(self.lockfile)
        try:
            os.unlink(self.lockpath)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
