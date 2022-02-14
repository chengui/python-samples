import sys
import curses
from curses.textpad import rectangle

class Board(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.Y, self.X = self.stdscr.getmaxyx()
        self.Y = self.Y - 1
        self.X = self.X - 1

    def show(self, state):
        cell_len = len(state)
        cell_Y = self.Y // cell_len
        cell_X = self.X // cell_len
        for i in range(cell_len):
            uly, lry = i * cell_Y, (i + 1) * cell_Y
            for j in range(cell_len):
                ulx, lrx = j * cell_X, (j + 1) * cell_X
                rectangle(self.stdscr, uly, ulx, lry, lrx)
                str_cell = str(state[i][j])
                ty = (uly + lry) // 2
                tx = (ulx + lrx - len(str_cell)) // 2 + 1
                self.stdscr.addstr(ty, tx, str_cell)
        self.stdscr.refresh()
