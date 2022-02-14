import time
import random
import curses
from curses import textpad
from datetime import datetime

class ColorClock(object):
    week_abbr = [
        'Sun.',
        'Mon.',
        'Tur.',
        'Wed.',
        'Thu.',
        'Fri.',
        'Sat.',
    ]

    def __init__(self, cycle=60, width=12, height=5):
        self.cycle = cycle
        self.width = width
        self.height = height

    def __call__(self, stdscr):
        self.stdscr = stdscr

        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_RED, 0)
            curses.init_pair(2, curses.COLOR_GREEN, 0)
            curses.init_pair(3, curses.COLOR_YELLOW, 0)
            curses.init_pair(4, curses.COLOR_BLUE, 0)
            curses.init_pair(5, curses.COLOR_CYAN, 0)
            curses.init_pair(6, curses.COLOR_MAGENTA, 0)
        curses.curs_set(False)

        self.stdscr.clear()
        self.stdscr.border()

        Y, X = self.stdscr.getmaxyx()
        self.center_Y = Y // 2
        self.center_X = X // 2

        self.run()

    def run(self):
        self.stdscr.nodelay(True)
        i = 0
        while True:
            if self.stdscr.getch() != -1:
                break
            self.tick(i)
            i = (i + 1) % self.cycle
            time.sleep(1)

    def tick(self, k=0):
        now = datetime.now()
        str_date = now.strftime("%Y/%m/%d")
        str_time = now.strftime("%H:%M:%S")
        str_week = self.week_abbr[now.weekday()]

        if curses.has_colors():
            self.stdscr.attrset(curses.color_pair(random.randrange(1, 6)))

        rect_uly = self.center_Y - (self.height // 2)
        rect_ulx = self.center_X - (self.width // 2) - 1
        rect_lry = self.center_Y + (self.height // 2)
        rect_lrx = self.center_X + (self.width // 2)
        self.stdscr.addstr(rect_uly, rect_ulx, '*' * (rect_lrx - rect_ulx + 1))
        self.stdscr.addstr(rect_lry, rect_ulx, '*' * (rect_lrx - rect_ulx + 1))
        for y in range(rect_uly+1, rect_lry):
            self.stdscr.addstr(y, rect_ulx, '*')
            self.stdscr.addstr(y, rect_lrx, '*')

        time_y = self.center_Y - 1
        time_x = self.center_X - 4
        self.stdscr.addstr(time_y, time_x, str_time)

        week_y = self.center_Y
        week_x = self.center_X - 2
        self.stdscr.addstr(week_y, week_x, str_week)

        date_y = self.center_Y + 1
        date_x = self.center_X - 5
        self.stdscr.addstr(date_y, date_x, str_date)

        if curses.has_colors():
            self.stdscr.attrset(0)

        self.stdscr.refresh()
