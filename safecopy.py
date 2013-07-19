#!/usr/bin/python
"""
An safe copy for python, it can handle copy tree and file totally,
and also provide an ignore patterns.
"""
import os
import sys
import shutil

def safecopy(src, dst, symlinks=False, ignore_ptns=[]):
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
            makedirs(os.path.dirname(dst))

        shutil.copy2(src, dst)

