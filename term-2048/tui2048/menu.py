import curses


class Menu(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def show(self, status):
        str_best = 'Best Score: %d' % (status['bestScore'],)
        if status['gameOver'] > 0:
            str_best += ' (WIN!)'
        elif status['gameOver'] < 0:
            str_best += ' (LOST!)'
        self.stdscr.addstr(0, 0, str_best)

        str_total = 'Total Score: %d' % (status['totalScore'],)
        self.stdscr.addstr(1, 0, str_total)

        str_tips = '(q) quit (r) reset (h) help'
        self.stdscr.addstr(2, 0, str_tips)

        self.stdscr.refresh()
