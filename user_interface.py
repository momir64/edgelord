import keyboard
import shutil
import time
import os

UNDERLINE_ON = '\x1B[1;3;4m'
UNDERLINE_OFF = '\x1B[0m'

def is_enclosed(text):
    return text.count(UNDERLINE_ON) <= text.count(UNDERLINE_OFF)

def underline_word(text, word):
    position = 0
    while text.lower().find(word.lower(), position) != -1:
        position = text.lower().find(word.lower(), position)
        if is_enclosed(text[:position]):
            text = text[:position] + UNDERLINE_ON + text[position:position + len(word)] + UNDERLINE_OFF + text[position + len(word):]
        position += len(UNDERLINE_ON + word + UNDERLINE_OFF)
    return text

def underline(text, words):
    for word in words:
        text = underline_word(text, word)
    return text

def without_underline(text):
    return text.replace(UNDERLINE_ON, '').replace(UNDERLINE_OFF, '')

def without_underline_len(text):
    return len(without_underline(text))

def get_status_width():
    return max(72, shutil.get_terminal_size().columns // 2)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def hide_cursor():
    print('\033[?25l', end='')

def show_cursor():
    print('\033[?25h', end='')

def print_vertical_space(offset=3):
    print('\n' * (shutil.get_terminal_size().lines // 2 - offset))

def print_centered(text, offset=0, end=None):
    print(' ' * ((shutil.get_terminal_size().columns - without_underline_len(text) - offset) // 2) + text, end=end)

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

def menu(print_menu, *data):
    selected = 1
    wait_release()
    print_menu(selected, *data)
    while True:
        try:
            if keyboard.is_pressed('down') or keyboard.is_pressed('right'):
                selected = min(selected + (10 if keyboard.is_pressed('shift') else 1), len(data[0]) if data else 2)
                print_menu(selected, *data)
                time.sleep(0.1)
            if keyboard.is_pressed('up') or keyboard.is_pressed('left'):
                selected = max(selected - (10 if keyboard.is_pressed('shift') else 1), 1)
                print_menu(selected, *data)
                time.sleep(0.1)
            if keyboard.is_pressed('r') or keyboard.is_pressed('h') or keyboard.is_pressed('f5'):
                selected = 1
                print_menu(selected, *data)
                time.sleep(0.1)
            if keyboard.is_pressed('esc'):
                cls()
                return None
            if keyboard.is_pressed('\n') or keyboard.is_pressed(' '):
                return selected
        except:
            break

def print_empty_status():
    print_centered('<' + '0/0'.center(get_status_width() - 2) + '>')
    print_centered('-' * get_status_width(), end='\n\n\n')
    print_centered('Publisher:   ...'.ljust(get_status_width()), end='\n')
    print_centered('Published:   ...'.ljust(get_status_width()), end='\n\n')
    print_centered('Link:        ...'.ljust(get_status_width()), end='\n\n')
    print_centered('Message:     ...'.ljust(get_status_width()), end='\n\n')
    print_centered('-' * get_status_width(), end='\n\n')
    print_centered(('👍 0'.ljust(7) + '❤️  0'.ljust(9) + '😆 0'.ljust(7) + '😮 0'.ljust(7) + '😢 0'.ljust(7) + '😠 0'.ljust(7) + '🐸 0'.ljust(7)).ljust(50) +
                   ('💬 0'.ljust(7) + '🔗 0'.ljust(7)).rjust(get_status_width() - 57), offset=4)

def print_status(index, statuses, underline_words):
    cls()
    print('\n' * 2)
    if not statuses:
        print_empty_status()
    else:
        status = statuses[index - 1]
        link = (status["link"][:get_status_width() - 9] + (status["link"][get_status_width() - 9:] and "...")) if status["link"] == status["link"] else ''
        print_centered('<' + f'{index}/{len(statuses)}'.center(get_status_width() - 2) + '>')
        print_centered('-' * get_status_width(), end='\n\n\n')
        print_centered(f'Publisher: {status["author"]}'.ljust(get_status_width()), end='\n')
        print_centered(f'Published: {status["date"]}'.ljust(get_status_width()), end='\n\n')
        print_centered(f'Link: {link}'.ljust(get_status_width()), end='\n\n')
        row_length = len('Message: ')
        line = 'Message: '
        for word in status['message'].split():
            row_length += len(word) + 1
            if row_length > get_status_width():
                print_centered(underline(line, underline_words) + (' ' * (get_status_width() - len(line))))
                row_length = len(word) + 1
                line = word + ' '
            else:
                line += word + ' '
        print_centered(underline(line, underline_words) + (' ' * (get_status_width() - len(line))), end='\n\n\n')
        print_centered('-' * get_status_width(), end='\n\n')
        print_centered((f'👍 {str(status["likes"])   .ljust(5)}' +
                       f'❤️  {str(status["loves"])   .ljust(6)}' +
                        f'😆 {str(status["hahas"])   .ljust(5)}' +
                        f'😮 {str(status["wows"])    .ljust(5)}' +
                        f'😢 {str(status["sads"])    .ljust(5)}' +
                        f'😠 {str(status["angrys"])  .ljust(5)}' +
                        f'🐸 {str(status["special"]) .ljust(5)}').ljust(50) +
                       (f'💬 {str(status["comments"]).ljust(5)}' +
                        f'🔗 {str(status["shares"])  .ljust(5)}').rjust(get_status_width() - 60), offset=7)
    hide_cursor()

def print_welcome_menu(option, *_):
    print_menu(option, 'Be anonymous', 'Log In')

def print_app_menu(option, *_):
    print_menu(option, 'View feed', 'Search feed')

def show_statuses(statuses, underline_words=[]):
    menu(print_status, statuses, underline_words)

def welcome_menu():
    return menu(print_welcome_menu)

def app_menu():
    return menu(print_app_menu)

def show_search(statuses):
    pass
