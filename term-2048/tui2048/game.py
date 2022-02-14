import random
import curses
from tui2048.menu import Menu
from tui2048.board import Board


KEY_UP = 0
KEY_DOWN = 1
KEY_LEFT = 2
KEY_RIGHT = 3

class Game(object):
    def __init__(self, target=64, cell=4):
        self.target = target
        self.cell = cell
        self.status = {
            'gameOver': 0,
            'bestScore': 0,
            'totalScore': 0,
        }
        self.state = [
            [0 for i in range(self.cell)] for j in range(self.cell)
        ]

    def reset(self):
        self.status = {
            'gameOver': 0,
            'bestScore': 0,
            'totalScore': 0,
        }
        self.state = [
            [0 for i in range(self.cell)] for j in range(self.cell)
        ]

    def random(self):
        return random.choice([2, 2, 2, 4])

    def chaos(self, num):
        zeros = []
        m = self.cell - 1
        for x, y in (0, 0), (0, m), (m, 0), (m, m):
            if self.state[x][y] == 0:
                zeros.append((x, y))
        if len(zeros) > 0:
            i, j = random.choice(zeros)
            self.state[i][j] = num

    def move_up(self):
        s = self.state
        m = self.cell
        for j in range(self.cell):
            arr = [s[i][j] for i in range(0, m)]
            arr = self.merge(arr)
            for i in range(0, m):
                s[i][j] = arr[i]
        return s

    def move_down(self):
        s = self.state
        m = self.cell - 1
        for j in range(self.cell):
            arr = [s[i][j] for i in range(m, -1, -1)]
            arr = self.merge(arr)
            for i in range(m, -1, -1):
                s[i][j] = arr[m-i]
        return s

    def move_left(self):
        s = self.state
        m = self.cell
        for i in range(self.cell):
            arr = [s[i][j] for j in range(0, m)]
            arr = self.merge(arr)
            for j in range(0, m):
                s[i][j] = arr[j]
        return s

    def move_right(self):
        s = self.state
        m = self.cell - 1
        for i in range(self.cell):
            arr = [s[i][j] for j in range(m, -1, -1)]
            arr = self.merge(arr)
            for j in range(m, -1, -1):
                s[i][j] = arr[m-j]
        return s

    def merge(self, arr):
        stack = []
        i = 0
        while i < len(arr):
            if arr[i] == 0:
                i += 1
            elif len(stack) > 0 and stack[-1] == arr[i]:
                stack.pop()
                arr[i] *= 2
            else:
                stack.append(arr[i])
                i += 1
        tails = len(arr) - len(stack)
        stack.extend([0 for i in range(tails)])
        return stack

    def handle(self, flag):
        if self.status['gameOver'] != 0:
            return
        s = self.state
        if flag == KEY_UP:
            self.move_up()
        elif flag == KEY_DOWN:
            self.move_down()
        elif flag == KEY_LEFT:
            self.move_left()
        elif flag == KEY_RIGHT:
            self.move_right()
        bestScore = max([max(k) for k in s])
        totalScore = sum([sum(k) for k in s])
        gameOver = 0
        if bestScore >= self.target:
            gameOver = 1
        else:
            zeros = sum([i.count(0) for i in s])
            if zeros <= 0:
                gameOver = -1
        self.status = {
            'gameOver': gameOver,
            'bestScore': bestScore,
            'totalScore': totalScore,
        }

    def __call__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(False)
        self.stdscr.clear()
        self.run()

    def run(self):
        rows, cols = self.stdscr.getmaxyx()

        win_menu = self.stdscr.subwin(3, cols, 0, 0)
        menu = Menu(win_menu)

        win_board = self.stdscr.subwin(rows-3, cols, 3, 0)
        board = Board(win_board)

        ch = ord('r')
        while True:
            if 0 < ch < 256:
                ch = chr(ch)
                if ch == 'q':
                    break
                elif ch == 'r':
                    self.reset()
                    self.chaos(self.random())
                else:
                    pass
            elif ch == curses.KEY_UP:
                self.handle(KEY_UP)
                self.chaos(self.random())
            elif ch == curses.KEY_DOWN:
                self.handle(KEY_DOWN)
                self.chaos(self.random())
            elif ch == curses.KEY_LEFT:
                self.handle(KEY_LEFT)
                self.chaos(self.random())
            elif ch == curses.KEY_RIGHT:
                self.handle(KEY_RIGHT)
                self.chaos(self.random())
            else:
                pass

            menu.show(self.status)
            board.show(self.state)

            self.stdscr.refresh()
            ch = self.stdscr.getch()
            self.stdscr.clear()
