"""Windows compatibility shim for fcntl."""
import os
import sys

LOCK_SH = 1
LOCK_EX = 2
LOCK_NB = 4
LOCK_UN = 8

def flock(fd, operation):
    if hasattr(fd, "fileno"):
        fd = fd.fileno()
    try:
        import msvcrt
        if operation & LOCK_UN:
            mode = msvcrt.LK_UNLCK
        elif operation & LOCK_NB:
            mode = msvcrt.LK_NBLCK
        else:
            mode = msvcrt.LK_LOCK

        cur_pos = os.lseek(fd, 0, os.SEEK_CUR)
        os.lseek(fd, 0, os.SEEK_SET)
        try:
            msvcrt.locking(fd, mode, 1)
        finally:
            os.lseek(fd, cur_pos, os.SEEK_SET)
    except OSError:
        raise
    except Exception:
        pass

def fcntl(fd, op, arg=0):
    return 0

def ioctl(fd, op, arg=0, mutate_flag=True):
    return 0
