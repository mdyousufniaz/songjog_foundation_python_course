from os import get_terminal_size, system, name as os_name, makedirs
from os.path import exists, join
from csv import DictReader, DictWriter
from getpass import getpass
from sys import exit

TERM_WIDTH = get_terminal_size().columns
USERS_FILE = 'users.csv'
DB_DIR = 'Database'
DB_FILES: dict[str, tuple[str]] = {
    'users': ('username', 'password'),
    'contact_details': ('name', 'phone_number', 'email', 'username')
}

MAIN_MENU_OPTIONS = "Login", "Sign up"
CONTACT_MANAGE_OPTIONS = "Show all contacts", "Add a contact", "Remove a existing contact", "Update a existing contact", "Log out"

current_user: str | None = None

def initial_setup() -> None:
    makedirs(DB_DIR, exist_ok=True)
    
    for file_name, headers in DB_FILES.items():
        full_file_name = get_file_path(file_name)
        if not exists(full_file_name): recreate_file(full_file_name, headers)

def recreate_file(file_path: str, file_headers: tuple[str]) -> None:
    with open(file_path, 'w', newline='\n') as file:
        DictWriter(file, fieldnames=file_headers).writeheader()


def get_file_path(file_name: str) -> str:
    return join(DB_DIR, file_name + '.csv')

def print_border() -> None:
    print('-' * TERM_WIDTH)

def center_aligned_text(text: str) -> str:
    return text.center(TERM_WIDTH)

def center_print(text: str) -> None:
    print(center_aligned_text(text))

def print_banner(title: str) -> None:
    print_border()
    center_print(title)
    print_border()

def show_menu(menu_title: str, menu_options: tuple[str]) -> None:
    clear_screen()
    print_banner("Welcome to Contact Manager System")

    login_status = f"Logged in as '{current_user}'" if logged_in() else "Not logged in"
    print(f"login_status: {login_status}".rjust(TERM_WIDTH))

    print(f"Showing {menu_title}")
    for option_no, option in enumerate(menu_options, 1):
        print(f"\t{option_no}. {option}")
    print("\t0. Exit this system", end='\n' * 2)

def clear_screen() -> None:
    system('cls' if os_name == 'nt' else 'clear')

def get_password(user_name: str) -> str | None:
    with open(get_file_path('users')) as users_file:
        for row in DictReader(users_file):
            if row['username'] == user_name: return row['password']
    return None

def ask_to_retry(reason: str) -> None:
    input(f"{reason}, press 'Enter' to try again!")

def show_success_msg(task: str) -> None:
    input(f"successfully {task}, press Enter to continue!")

def login(user_name: str) -> None:
    global current_user
    current_user = user_name
    show_success_msg(f"logged in as '{user_name}'")

def register(user_name: str, password: str) -> None:
    with open(get_file_path('users'), 'a', newline='\n') as users_file:
        DictWriter(users_file, fieldnames=('username', 'password')).writerow({
            'username': user_name,
            'password': password
        })
    show_success_msg(f"registerd as '{user_name}'")

def show_invalid_msg(invalid_reason: str) -> None:
    ask_to_retry(f"Invalid {invalid_reason}")

def logged_in() -> bool:
    return current_user is not None

def log_out() -> None:
    global current_user
    prev_user = current_user
    current_user = None
    show_success_msg(f"logged out as '{prev_user}'")
    
def can_not_be_blank(component: str) -> None:
    ask_to_retry(f"{component} can not be blank")

def get_all_contacts() -> list[dict[str, str]]:
    with open(get_file_path('contact_details')) as contacts_file:
        return list(DictReader(contacts_file))

def get_current_contacts() -> list[dict[str, str]]:
    return list(filter(lambda contact: contact['username'] == current_user, get_all_contacts()))
        

def add_contact(name: str, phone_num: str, email: str) -> None:
    with open(get_file_path('contact_details'), 'a', newline='\n') as contacts_file:
        DictWriter(contacts_file, fieldnames=DB_FILES['contact_details']).writerow({
            'name': name,
            'phone_number': phone_num,
            'email': email,
            'username': current_user
        })
    
    show_success_msg(f"added contact for '{name}'")


def make_row(row: list[str]) -> str:
    return ''.join([cell.center(30) for cell in row])

def show_contacts() -> None:
    contacts = get_current_contacts()
    if not contacts:
        center_print("No contacts added Yet!")
    else:
        headers: tuple[str] = ('Index', ) + DB_FILES['contact_details'][:-1]
        print_banner(make_row([header.upper() for header in headers]))
        for index, contact in enumerate(contacts, 1):
            contact.pop('username')
            center_print(make_row([str(index)] + list(contact.values())))
            print_border()
    
    input("Press Enter to continue!")

def save_contacts(contacts: list[dict[str, str]]) -> None:
    contacts_file_path = get_file_path('contact_details')
    contacts_file_headers = DB_FILES['contact_details']
    recreate_file(contacts_file_path, contacts_file_headers)

    with open(contacts_file_path, 'a', newline='\n') as contacts_file:
        DictWriter(contacts_file, fieldnames=contacts_file_headers).writerows(contacts)

def remove_contact(contact_name: str) -> None:
    contacts = get_all_contacts()
    for contact in get_current_contacts():
        if contact['name'] == contact_name:
            contacts.remove(contact)
            break
    else: 
        input(f"contact name: '{contact_name}' is not found, press 'Enter to try again!")
        return

    save_contacts(contacts)
    show_success_msg(f"removed contact for '{contact_name}'")

def main() -> None:
    initial_setup()
    while True:
        show_menu("Main Menu", MAIN_MENU_OPTIONS)
        main_menu_opns_len = len(MAIN_MENU_OPTIONS)
        choice = input(f"Enter Your choice [0-{main_menu_opns_len}]: ")
        print()
        wrong_choice = False

        try: option_no: int = int(choice)
        except ValueError: wrong_choice = True

        if option_no == 0:
            center_print("Thank You for using this system!")
            exit()

        if option_no not in range(1, main_menu_opns_len + 1) and not wrong_choice: wrong_choice = True

        if wrong_choice:
            show_invalid_msg('choice')
            continue
        
        match option_no:
            case 1:
                user_name: str = input("Enter your username: ")
                password: str | None = get_password(user_name)
                if password is None:
                    ask_to_retry("username not found")
                    continue

                if  getpass("Enter password: ") != password:
                    show_invalid_msg('password')
                    continue

                login(user_name)
            
            case 2:
                user_name = input("Enter your username: ")
                if not user_name:
                    can_not_be_blank('username')
                    continue

                if get_password(user_name) is not None:
                    ask_to_retry("username already in use")
                    continue

                password = input("Enter password: ")
                if not password:
                    can_not_be_blank('password')
                    continue
                
                register(user_name, password)
                login_choice = input("Do you want to login? [write 'yes' or 'no']: ").upper()

                if login_choice not in ('YES', 'NO'):
                    ask_to_retry("Invalid choice")
                    continue

                if login_choice == 'YES':
                    login(user_name)
        
        if not logged_in(): continue

        while True:
            show_menu("Contact Menu", CONTACT_MANAGE_OPTIONS)
            contact_menu_opns_len = len(CONTACT_MANAGE_OPTIONS)
            choice = input(f"Enter Your choice [0-{contact_menu_opns_len}]: ")
            print()
            wrong_choice = False

            try: option_no: int = int(choice)
            except ValueError: wrong_choice = True

            if option_no == 0:
                center_print("Thank You for using this system!")
                exit()
            
            if option_no == contact_menu_opns_len:
                log_out()
                break
                
            if option_no not in range(1, contact_menu_opns_len + 1) and not wrong_choice: wrong_choice = True

            if wrong_choice:
                show_invalid_msg('choice')
                continue

            match option_no:
                case 1:
                    show_contacts()
                case 2:
                    contact_name = input("Enter contact user name: ")
                    if not contact_name:
                        can_not_be_blank('contact user name')
                    
                    phone_number = input("Enter phone number: ")
                    try: int(phone_number)
                    except ValueError:
                        show_invalid_msg("phone number")
                        continue

                    email = input("Enter email[optional]: ")

                    add_contact(contact_name, phone_number, email)
                case 3: 
                    contact_name = input("Enter contact user name: ")
                    remove_contact(contact_name)
                
                case 4:
                    contact_name = input("Enter contact name that You want to update: ")
                    contacts = get_all_contacts()
                    old_contact: list[dict[str, str]] | None = None
                    for contact in get_current_contacts():
                        if contact['name'] == contact_name:
                            old_contact = contact
                            break
                    else:
                        show_invalid_msg("contact name")
                        continue

                    UPDATE_FIELDS = 'phone_number', 'email'
                    field = input(f"Enter the field that you want to update {UPDATE_FIELDS}: ").lower()
                    if field not in UPDATE_FIELDS:
                        show_invalid_msg('field')
                        continue

                    new_value = input(f"Enter the updated value for {field}: ")

                    if old_contact[field] != new_value:
                        old_contact_index = contacts.index(old_contact)
                        old_contact[field] = new_value
                        contacts[old_contact_index] = old_contact
                        
                    save_contacts(contacts)

                    show_success_msg(f"updated contacts for '{contact_name}'")
        
        

if __name__ == '__main__': main()