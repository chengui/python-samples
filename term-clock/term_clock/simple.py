import time
import random
import curses
from curses import textpad
from datetime import datetime

class SimpleClock(object):
    def __init__(self, width=16, height=3):
        self.width = width
        self.height = height

    def __call__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(False)

        self.stdscr.clear()
        self.stdscr.border()

        Y, X = self.stdscr.getmaxyx()
        self.center_Y = Y // 2
        self.center_X = X // 2

        self.run()

    def run(self):
        self.stdscr.nodelay(True)
        while True:
            if self.stdscr.getch() != -1:
                break
            self.tick()
            time.sleep(0.1)

    def tick(self):
        rect_uly = self.center_Y - (self.height // 2)
        rect_ulx = self.center_X - (self.width // 2) - 1
        rect_lry = self.center_Y + (self.height // 2)
        rect_lrx = self.center_X + (self.width // 2)
        textpad.rectangle(self.stdscr, rect_uly, rect_ulx, rect_lry, rect_lrx)

        str_time = datetime.now().strftime("%H:%M:%S.%f")[:-5]
        time_y = self.center_Y
        time_x = self.center_X - (len(str_time) // 2)
        self.stdscr.addstr(time_y, time_x, str_time)

        self.stdscr.refresh()
