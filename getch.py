def linux_getch():
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def windows_getch():
    import msvcrt
    return msvcrt.getch()

def get_getch():
    try:
        return windows_getch()
    except ImportError:
        return linux_getch()

getch = get_getch()
