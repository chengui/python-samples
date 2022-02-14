import os
import errno
import fcntl


class FileLock(object):
    """ A file locking implementation

        the mechanism enabled context-manager support so that you can use it in
        a with statement, and it utilized fcntl.flock to lock/unlock, a singleton
        is used to share states between all instances as well
    """
    _instance = None

    def __new__(cls, *kargs, **kwargs):
        """ Create singleton instance """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, fpath):
        """ Initialize lock file and status """
        self.islocked = False
        self.lockpath = fpath

        if not os.path.exists(self.lockpath):
            self.lockfile = os.open(self.lockpath, os.O_CREAT | os.O_RDWR)
        else:
            self.lockfile = os.open(self.lockpath, os.O_RDWR)

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
        """ Clean up the lock file left """
        # FIXME: __del__ will never be called since cls._instance won't be gone
        try:
            if self.lockfile:
                os.close(self.lockfile)
            os.unlink(self.lockpath)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

