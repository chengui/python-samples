import os
import errno

class PIDLockFile(object):
    """ Lockfile implementation by using a PID file

        The lock file contains a single line of text, which
        is the PID of the process that acquired the lock
    """
    def __init__(self, fpath):
        self.fpath = fpath

    @property
    def lockpid(self):
        """ Get the PID of the locker process """
        return self._readpidfile()

    @property
    def thispid(self):
        """ Get the PID of this process """
        return os.getpid()

    def _readpidfile(self):
        """ Read the PID from the lock file """
        try:
            pid = int(open(self.fpath, 'r').read())
        except IOError as e:
            return None
        except ValueError as e:
            return None
        else:
            return pid

    def _writepidfile(self):
        """ Write the PID in the PID file """
        fd = os.open(self.fpath, os.O_CREAT | os.O_RDWR | os.O_EXCL)
        os.write(fd, str(self.thispid))
        os.close(fd)

    def _removepidfile(self):
        """ Remove the PID file if exists """
        try:
            os.unlink(self.fpath)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    ### public interface ###

    def ownLock(self):
        """ Check if the lock file is locked by this process """
        return self.lockpid == self.thispid

    def isLocked(self):
        """ Check if the lock file is locked """
        if self.lockpid:
            return os.path.exists('/proc/%s' % self.lockpid)
        return False

    def acquire(self):
        """ Acquire the lock """
        while True:
            try:
                self._writepidfile()
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                time.sleep(0.1)
            else:
                return

    def release(self):
        """ Release the lock """
        if self.isLocked() and self.ownLock():
            self._removepidfile()

    def __enter__(self):
        """ Activated when entering the with statement """
        self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        """ Activated when leaving the with statement """
        self.release()

    def __del__(self):
        """ Clean up the pid file """
        self._removepidfile()
