import os
import time
import click
from multiprocessing import Process
from locks.filelock_class_singleton import FileLock as FileLockCS
from locks.filelock_shared_dict import FileLock as FileLockSD


def func(FileLock, count, n=10):
    for i in range(n):
        with FileLock('{}.lock'.format(count)) as _:
            file = open(count, "r+")
            # increment the counter
            counter = int(file.readline()) + 1
            # write the counter
            file.seek(0)
            file.write(str(counter))
            file.close()
            print(os.getpid(), "=>", counter)
        #time.sleep(0.1)


@click.command()
@click.option('-l', '--lock', default='singleton', help='filelock type')
@click.option('-c', '--count', default='counter.txt', help='counter file')
@click.option('-n', '--num', type=int, default=5, help='process count')
def cli(lock, count, num):
    mapping = {
        'singleton': FileLockCS,
        'sharedict': FileLockSD,
    }

    if lock not in mapping:
        return cli.echo('lock not found!')

    FileLock = mapping[lock]

    if not os.path.exists(count):
        f = open(count, 'w')
        f.write('0')
        f.close()

    lst_proc = []
    for i in range(num):
        p = Process(target=func, args=(FileLock, count))
        p.start()
        lst_proc.append(p)
    for p in lst_proc:
        p.join()


if __name__ == '__main__':
    cli()
