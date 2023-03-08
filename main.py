import random
from utils import getch, log, load, save
from screen import Screen, Object
import sys
import os
import time

MODES = ["ADD", "SUB", "MUL"]

RANGES = {
    "ADD": (range(1, 200), range(1, 200)),
    "SUB": (range(1, 200), range(1, 200)),
    "MUL": (range(1, 50), range(2, 7))
}

OPERATOR = {
    "ADD": (lambda a, b: a + b),
    "SUB": (lambda a, b: a - b),
    "MUL": (lambda a, b: a * b)
}

SYMBOL = {
    "ADD": "+",
    "SUB": "-",
    "MUL": "*"
}

BEST = load()

class Problem:
    def __init__(self, mode=None):
        if not mode:
            mode = MODES
        self.mode = random.choice(mode)

        self.arange, self.brange = RANGES[self.mode]
        self.a = random.choice(self.arange)
        self.b = random.choice(self.brange)

        if self.b > self.a:
            self.b, self.a = self.a, self.b

        self.ans = OPERATOR[self.mode](self.a, self.b)
        self.input_buffer = ""
        self.display_buffer = f"{self.a} {SYMBOL[self.mode]} {self.b} = "

if __name__ == "__main__":
    w, h = os.get_terminal_size() 

    mode = []
    for arg in sys.argv:
        if arg.upper() in MODES:
            mode.append(arg.upper())

    while True:
        problem = Problem(mode)
        start = None
        best = BEST[problem.mode]

        while True:
            screen = Screen(w, h-2, default_fill = " ")
            obj1 = Object([[*problem.display_buffer]], {})
            screen.draw(0, 0, obj1)

            if best is not None:
                obj2 = Object([[*f"Best: {best:.4f}s"]], {})
                screen.draw(0, 10, obj2)

            screen.display()

            if start is None:
                start = time.time()

            new_input = getch()

            if new_input == chr(0x7F):
                if not problem.input_buffer:
                    continue
                problem.display_buffer = problem.display_buffer[:-1]
                problem.input_buffer = problem.input_buffer[:-1]
            elif new_input == chr(0x3):
                exit()
            elif new_input == chr(0x20):
                break
            elif new_input in "0123456789-":
                problem.input_buffer += new_input
                problem.display_buffer += new_input

            log(problem.display_buffer)

            if problem.input_buffer.strip() == str(problem.ans):
                elapsed = time.time() - start
                if best is None or elapsed < best:
                    BEST[problem.mode] = elapsed
                    save(BEST)
                break
