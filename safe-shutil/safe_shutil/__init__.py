import os
import shutil


def safe_copy(src, dst, symlinks=False, ignore_ptns=[]):
    """
    An safe copy for python, it can handle copy tree and file totally,
    and also provide an ignore patterns.
    """
    if symlinks and os.path.islink(src):
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        linkto = os.readlink(src)
        os.symlink(linkto, dst)
    elif os.path.isdir(src):
        src = src.rstrip('/')
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))

        # check common prefix
        if dst.startswith(src +'/'):
            ignore_ptns += os.path.basename(src)

        ignores = shutil.ignore_patterns(*ignore_ptns)
        try:
            shutil.copytree(src, dst, symlinks, ignores)
        except (OSError, IOError):
            shutil.rmtree(dst, ignore_errors=True)
            raise
    else:
        if not os.path.isdir(dst):
            os.makedirs(os.path.dirname(dst))

        shutil.copy2(src, dst)
