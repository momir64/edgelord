def linux_getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def windows_getch():
    return msvcrt.getwch()

isLinux = True

try:
    import sys
    import tty
    import termios
except ImportError:
    import msvcrt
    isLinux = False

def getch():
    if isLinux:
        return linux_getch()
    else:
        return windows_getch()
