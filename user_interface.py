from getch import getch
import keyboard
import shutil
import time
import os
import re

GRAY_ON = '\033[90m'
STYLE_OFF = '\033[0m'
STYLE_ON = '\033[1;3;4m'
UNDERLINE_ON = '\033[4m'
CLEAR_TO_END = '\033[K'
NUMBER_OF_SUGGESTIONS = 5
MIN_STATUS_WIDTH = 75


def is_enclosed(text):
    return text.count(STYLE_ON) <= text.count(STYLE_OFF)

def get_position(text, word, position):
    return position + len(word) + len([c for c in text[position:text.lower().find(word.lower().split()[-1])] if not c.isalnum() and c != ' '])

def underline_word(text, word):
    position = 0
    clean_position = 0
    clean_text = re.sub(r'\s\s+', ' ', re.sub(r'[^\w\s]+', ' ', text)).strip().lower()
    clean_word = re.sub(r'\s\s+', ' ', re.sub(r'[^\w\s]+', ' ', word)).strip().lower()
    while clean_text.find(clean_word, clean_position) != -1:
        clean_position = clean_text.find(clean_word, clean_position) + len(clean_word)
        position = text.lower().find(word.lower().split()[0], position)
        if is_enclosed(text[:position]):
            text = text[:position] + STYLE_ON + text[position:get_position(text, word, position)] + STYLE_OFF + text[get_position(text, word, position):]
        position += len(STYLE_ON + word + STYLE_OFF)
    return text

def underline(text, words):
    for word in words:
        text = underline_word(text, word)
    return text

def without_underline(text):
    return text.replace(STYLE_ON, '').replace(STYLE_OFF, '')

def without_underline_len(text):
    return len(without_underline(text))

def get_console_width():
    return shutil.get_terminal_size().columns

def get_status_width():
    return max(MIN_STATUS_WIDTH, shutil.get_terminal_size().columns // 2)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def hide_cursor():
    print('\033[?25l', end='')

def show_cursor():
    print('\033[?25h', end='')

def print_vertical_space(offset=2):
    print(f'\033[{shutil.get_terminal_size().lines // 2 - offset};0H')

def print_centered(text, offset=0, end=None):
    print(f'\r\033[{(get_console_width() - without_underline_len(text) - offset) // 2}C{text}', end=end)

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
        if keyboard.is_pressed('\n') or keyboard.is_pressed('esc'):
            time.sleep(0.1)
        else:
            break

def login_prompt(users):
    cls()
    flush_input()
    hide_cursor()
    wait_release()
    print_vertical_space()
    print_centered('Name: ', 12, end='')
    show_cursor()
    name = input()
    for user in users:
        if name.lower().strip() == user.lower().strip():
            return user
    return ''

def print_menu(selected, *args):
    cls()
    hide_cursor()
    print_vertical_space()
    for i, arg in enumerate(args):
        print_centered(('> ' if selected == i + 1 else '  ') + arg.ljust(15))

def menu(print_menu, *data):
    selected = 1
    wait_release()
    width = get_console_width()
    print_menu(selected, *data)
    while True:
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
        if width != get_console_width():
            print_menu(selected, *data)
            width = get_console_width()
            time.sleep(0.1)

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
    print('\n')
    hide_cursor()
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
        print_centered((f' 👍 {str(status["likes"])   .ljust(4)}' +
                       f' ❤️  {str(status["loves"])   .ljust(5)}' +
                        f' 😆 {str(status["hahas"])   .ljust(4)}' +
                        f' 😮 {str(status["wows"])    .ljust(4)}' +
                        f' 😢 {str(status["sads"])    .ljust(4)}' +
                        f' 😠 {str(status["angrys"])  .ljust(4)}' +
                        f' 🐸 {str(status["special"]) .ljust(4)}').ljust(50) +
                       (f' 💬 {str(status["comments"]).ljust(4)}' +
                        f' 🔗 {str(status["shares"])  .ljust(4)}').rjust(get_status_width() - 60), offset=8)

def print_welcome_menu(option, *_):
    print_menu(option, 'Be anonymous', 'Log In')

def print_app_menu(option, *_):
    print_menu(option, 'View feed', 'Search feed')

def show_statuses(statuses, underline_words=[]):
    menu(print_status, statuses, underline_words)

def login_menu():
    return menu(print_welcome_menu)

def app_menu():
    return menu(print_app_menu)

def print_sugestion(trie, text, x, y, option=0):
    sufix = ''
    prefix = text.split()[-1].replace('"', '').lower()
    words = trie.get_suggestion(prefix)
    option = min(option, max(0, min(len(words), NUMBER_OF_SUGGESTIONS)))
    if words:
        if option:
            sufix = words[option - 1][len(prefix):]
            print(f'\033[{y};{x + len(text)}H', end='')
            print(UNDERLINE_ON + GRAY_ON + sufix[0] + STYLE_OFF + GRAY_ON + sufix[1:] + STYLE_OFF, end=CLEAR_TO_END)

        for i, word in enumerate(words[:NUMBER_OF_SUGGESTIONS]):
            print(f'\033[{y + i + 1};{x}H', end='')
            print(GRAY_ON + text + word[len(prefix):] + STYLE_OFF, end=CLEAR_TO_END)

    return option, sufix

def clear_sugestion(x, y):
    for i in range(5):
        print(f'\033[{y + i + 1};{x}H', end='')
        print('', end=CLEAR_TO_END)

def show_search(trie):
    cls()
    hide_cursor()
    flush_input()
    wait_release()
    print_vertical_space()
    print_centered('Search: ' + GRAY_ON + '_' + STYLE_OFF, 32, end='')
    x, y = (get_console_width() - 29) // 2 + 1, shutil.get_terminal_size().lines // 2 - 1
    position = 1
    option = 0
    char = ''
    text = ''
    while char != '\r' and char != '\n':
        print(f'\r\033[{y};{x}H', end='')
        if position < len(text):
            print(f'{text[:position] + UNDERLINE_ON + text[position] + STYLE_OFF+ text[position + 1:]}', end=CLEAR_TO_END)
        else:
            print(f'{text}{GRAY_ON}_{STYLE_OFF}', end=CLEAR_TO_END)
        clear_sugestion(x, y)
        option, sufix = print_sugestion(trie, text, x, y, option) if text and text[-1] != ' ' and text[-1] != '"' else (0, '')
        print(f'\033[{y};{x + position}H', end='')

        print(f'\r\033[0;0H', end=CLEAR_TO_END)
        char = getch()
        if char == '\b' and text != '' and position:
            text = text[:position - 1] + text[position:]
            position = max(0, position - 1)
        elif char == 'à':
            char = getch()
            if char == 'K':
                position = max(0, position - 1)
            elif char == 'M':
                position = min(len(text), position + 1)
            elif char == 'H':
                option = max(0, option - 1)
            elif char == 'P':
                option += 1
            elif char == 'S':
                text = text[:position] + text[position + 1:]
        elif char.isalnum() or char == ' ' or char == '"':
            text = text[:position] + char + text[position:]
            position += 1
            option = 0
        elif char == '\t':
            text += sufix
            position = len(text)
            option = 0
        elif char == '\x1b':
            return None

    return text.strip()
