from os import get_terminal_size, system, name as os_name, makedirs
from typing import Any

TERM_WIDTH = get_terminal_size().columns
DB_DIR = 'Database'
PRESS_ENTER_TO = "Press 'Enter' to"

def print_border() -> None:
    print('-' * TERM_WIDTH)

def center_aligned_text(text: str) -> str:
    return text.center(TERM_WIDTH)

def center_print(text: str, pause: bool = False) -> None:
    print(center_aligned_text(text))
    if pause: press_enter_to_continue()

def print_banner(title: str) -> None:
    print_border()
    center_print(title)
    print_border()
    print()

def clear_screen() -> None:
    system('cls' if os_name == 'nt' else 'clear')

def initial_setup() -> None:
    makedirs(DB_DIR, exist_ok=True)

def print_row(row: tuple[Any]) -> str:
    center_print(''.join(tuple(str(value).center(50) for value in row)))

def print_as_table(rows: list[tuple[Any]]) -> None:
    print_border()
    print_row(rows.pop(0))
    print_border()
    for row in rows:
        print_row(row)
    print_border()

def ask(reason: str, work: str) -> None:
    input(f"{reason}, {PRESS_ENTER_TO} {work}!")

def ask_to_continue(reason: str) -> None:
    ask(reason, 'continue')

def show_success_msg(task: str) -> None:
    ask_to_continue(f"Successfully {task}")

def ask_to_try_again(reason: str) -> None:
    ask(reason, "try again")

def show_invalid_msg(invalid_reason: str) -> None:
    ask_to_try_again(f"Invalid {invalid_reason}")

def right_print(text: str) -> None:
    print(text.rjust(TERM_WIDTH))

def get_choice(options_len: int, field_name: str = "choice", start: int = 0) -> int | None:
    choice = input(f"Enter {field_name}[{start}-{options_len}]: ")
    invalid_choice = False

    try: option_num = int(choice)
    except ValueError: invalid_choice = True
    else: 
        if option_num not in range(start, options_len + 1): invalid_choice = True

    if invalid_choice:
        show_invalid_msg(field_name)
        return None
    
    return option_num

def not_blank_field(field_name: str = 'field') -> str | None:
    reponse = input(f"Enter {field_name}: ")
    if not reponse:
        ask_to_try_again(f"{field_name} can not be blank")
        return None
    return reponse

def exit_system() -> None:
    center_print("Thank You for using this system!")
    exit()

def press_enter_to_continue() -> None:
    input(f"{PRESS_ENTER_TO} continue!")

def yes_or_no(question: str) -> bool | None:
    answers = 'yes', 'no'
    if (answer := input(f"{question}? [Yes/No]: ").lower()) not in answers:
        show_invalid_msg('choice')
        return None
    if answer == 'no': return False
    return True

def expand_numbers(numbers: str) -> tuple[int]:
    return tuple(map(lambda num: int(num), numbers.split(',')))

def compress_numbers(numbers: tuple[int]) -> str:
    return ','.join(tuple(map(str, numbers)))

def get_quantity(prmopt: str) -> int | None:
    user_input = input(prmopt)
    wrong_amount = False
    try: amount = int(user_input)
    except ValueError: wrong_amount = True
    else:
        if amount < 1 and not wrong_amount: wrong_amount = True
    
    if wrong_amount:
        show_invalid_msg(f"amount '{user_input}'")
        return None
    return amount