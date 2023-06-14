import keyboard
import shutil
import time
import os

STATUS_WIDTH = 80

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def hide_cursor():
    print('\033[?25l', end='')

def show_cursor():
    print('\033[?25h', end='')

def print_vertical_space(offset=3):
    print('\n' * (shutil.get_terminal_size().lines // 2 - offset))

def print_centered(text, offset=0, end=None):
    print(' ' * ((shutil.get_terminal_size().columns - len(text) - offset) // 2) + text, end=end)

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def wait_release():
    while True:
        try:
            if keyboard.is_pressed('\n') or keyboard.is_pressed('esc'):
                time.sleep(0.1)
            else:
                break
        except:
            break

def login(users):
    cls()
    flush_input()
    show_cursor()
    wait_release()
    print_vertical_space()
    print_centered('Name: ', 12, end='')
    name = input()
    for user in users:
        if name.lower().strip() == user.lower().strip():
            return user
    return ''

def print_menu(selected, *args):
    cls()
    print_vertical_space()
    for i, arg in enumerate(args):
        print_centered(('> ' if selected == i + 1 else '  ') + arg.ljust(15))
    hide_cursor()

def menu(print_menu, data=[0, 0]):
    selected = 1
    wait_release()
    print_menu(selected, data)
    while True:
        try:
            if keyboard.is_pressed('down') or keyboard.is_pressed('right'):
                selected = min(selected + 1, len(data))
                print_menu(selected, data)
                time.sleep(0.1)
            if keyboard.is_pressed('up') or keyboard.is_pressed('left'):
                selected = max(selected - 1, 1)
                print_menu(selected, data)
                time.sleep(0.1)
            if keyboard.is_pressed('esc'):
                cls()
                return None
            if keyboard.is_pressed('\n'):
                return selected
        except:
            break

def print_status(index, statuses):
    cls()
    print('\n' * 3)
    status = statuses[index - 1]
    link = (status["link"][:STATUS_WIDTH - 9] + (status["link"][STATUS_WIDTH - 9:] and "...")) if status["link"] == status["link"] else ''
    print_centered('<' + f'{index}/{len(statuses)}'.center(STATUS_WIDTH - 2) + '>')
    print_centered('-' * STATUS_WIDTH, end='\n\n')
    print_centered(f'Publisher: {status["author"]}'.ljust(STATUS_WIDTH), end='\n')
    print_centered(f'Published: {status["date"]}'.ljust(STATUS_WIDTH), end='\n\n')
    print_centered(f'Link: {link}'.ljust(STATUS_WIDTH), end='\n\n')
    row_length = len('Message: ')
    line = 'Message: '
    for word in status['message'].split():
        row_length += len(word) + 1
        if row_length > STATUS_WIDTH:
            print_centered(line.ljust(STATUS_WIDTH))
            row_length = 0
            line = ''
        else:
            line += word + ' '
    print_centered(line.ljust(STATUS_WIDTH))

def print_welcome_menu(option, _):
    print_menu(option, 'Be anonymous', 'Log In')

def print_app_menu(option, _):
    print_menu(option, 'View feed', 'Search feed')

def show_feed(statuses):
    menu(print_status, statuses)

def welcome_menu():
    return menu(print_welcome_menu)

def app_menu():
    return menu(print_app_menu)

def show_search(statuses):
    pass
