import curses
from tui2048.game import Game


if __name__ == '__main__':
    game = Game()
    curses.wrapper(game)
