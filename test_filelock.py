#
# used to test the filelock program
# run 'python <progname> & python <progname> ...' to start multiple processes

import os
import time
from filelock import FileLock

FILE = "counter.txt"

if not os.path.exists(FILE):
    # create the counter file if it doesn't exist
    file = open(FILE, "w")
    file.write("0")
    file.close()

for i in range(20):
    with FileLock('test.lock') as lock:
        file = open(FILE, "r+")
        # increment the counter
        counter = int(file.readline()) + 1
        # write the counter
        file.seek(0)
        file.write(str(counter))
        file.close()
        print os.getpid(), "=>", counter
    time.sleep(0.1)
