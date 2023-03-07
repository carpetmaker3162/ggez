import os

def _unix_getch():
    """
    Read a single character of input from stdin without the need of pressing ENTER, without printing
    the inputted character out on the screen
    """
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def _win_getch():
    """
    Same as _unix_getch() but for Windows
    """
    return msvcrt.getch().decode("utf-8")

if os.name == "nt":
    import msvcrt
    getch = _win_getch
else:
    import sys, tty, termios
    getch = _unix_getch
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
 
def log(content="", end="\n"):
    with open("debug_logs.txt", "a") as f:
        f.write(str(content) + end)
