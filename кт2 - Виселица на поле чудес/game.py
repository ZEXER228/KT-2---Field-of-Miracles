from pathlib import Path
from random import choice


WORDS_FILE = "words.txt"
STAGES_FOLDER = "stages"
WORD_SEPARATOR = "|"
EMPTY_LETTER = "_"
MAX_ERRORS = 6

word = ""
description = ""
used_letters = set()
errors = 0
running = False
won = False
lost = False
load_error = ""


def get_path(name):
    return Path(__file__).parent / name


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def get_words():
    lines = read_text(get_path(WORDS_FILE)).splitlines()
    return [line.strip().split(WORD_SEPARATOR, 1) for line in lines if WORD_SEPARATOR in line]


def get_word_data():
    words = get_words()
    if words:
        return choice(words)
    return []


def reset_values():
    global used_letters, errors, running, won, lost
    used_letters = set()
    errors = 0
    running = True
    won = False
    lost = False


def set_word_data(data):
    global word, description
    word = data[0].lower().strip()
    description = data[1].strip()


def start():
    global running, load_error
    data = get_word_data()
    if data:
        reset_values()
        set_word_data(data)
    else:
        running = False
        load_error = "Не удалось загрузить слова из файла words.txt."


def is_running():
    return running


def get_stage_text():
    stage_name = f"stage_{errors}.txt"
    return read_text(get_path(STAGES_FOLDER) / stage_name)


def get_visible_word():
    return " ".join(letter if letter in used_letters else EMPTY_LETTER for letter in word)


def get_used_letters():
    return ", ".join(sorted(used_letters))


def draw_game():
    print(get_stage_text())
    print(f"Описание: {description}")
    print(f"Слово: {get_visible_word()}")
    print(f"Названные буквы: {get_used_letters()}")


def read_letter():
    return input("Введите букву: ").lower().strip()


def is_letter_valid(letter):
    return len(letter) == 1 and letter.isalpha()


def is_new_letter(letter):
    return letter not in used_letters


def can_use_letter(letter):
    return is_letter_valid(letter) and is_new_letter(letter)


def show_bad_input():
    print("Введите одну букву.")


def show_repeated_letter():
    print("Эта буква уже была.")


def ask_letter():
    letter = read_letter()
    while not can_use_letter(letter):
        if is_letter_valid(letter):
            show_repeated_letter()
        else:
            show_bad_input()
        letter = read_letter()
    return letter


def add_used_letter(letter):
    used_letters.add(letter)


def is_letter_in_word(letter):
    return letter in word


def add_error():
    global errors
    errors += 1


def show_correct_answer():
    print("Верно!")


def show_wrong_answer():
    print("Нет такой буквы.")


def is_word_opened():
    return all(letter in used_letters for letter in word)


def has_no_attempts():
    return errors >= MAX_ERRORS


def update_game_state():
    global won, lost
    won = is_word_opened()
    lost = has_no_attempts()


def play_turn():
    letter = ask_letter()
    add_used_letter(letter)
    if is_letter_in_word(letter):
        show_correct_answer()
    else:
        add_error()
        show_wrong_answer()
    update_game_state()


def player_won():
    return won


def player_lost():
    return lost


def stop_game():
    global running
    running = False


def show_result():
    if load_error:
        print(load_error)
    elif won:
        draw_game()
        print("Вы выиграли!")
    else:
        draw_game()
        print(f"Вы проиграли. Было загадано слово: {word}")
