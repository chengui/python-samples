import sys
import click
from streams import StringStream


@click.command()
def cli():
    fd = StringStream(stdfd=1)
    fd.open()
    for input in sys.stdin:
        print(input)
    fd.close()

    print("Restore from StringStream:")
    print(fd.read())


if __name__ == '__main__':
    cli()
