import click
import curses
from term_clock.simple import SimpleClock
from term_clock.color import ColorClock

@click.group()
def cli():
    pass

@click.command()
def simple():
    clock = SimpleClock()
    curses.wrapper(clock)

@click.command()
def color():
    clock = ColorClock()
    curses.wrapper(clock)

cli.add_command(simple)
cli.add_command(color)

if __name__ == '__main__':
    cli()


