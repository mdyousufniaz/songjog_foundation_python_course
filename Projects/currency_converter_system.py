"""
Currency Converter System Project
made by: @mdyousufniaz
"""

def draw_banner(banner_title: str, border_length: int, border_symbol: str='-') -> None:
    BORDER: str = border_symbol * border_length
    print(f"""
{BORDER}
{banner_title.center(border_length)}
{BORDER}"""
    )

def show_as_row(row_datas: tuple[str | float], col_length: int=20) -> str:
    return ''.join(tuple(str(data).center(col_length) for data in row_datas))

def show_as_table(title: str, headers: tuple[str], datas: list[dict[str, str | float]]) -> None:
    print(title.capitalize())

    table_header: str = show_as_row(headers)
    draw_banner(table_header, 20 * len(headers))

    for row in datas:
        print(show_as_row(row.values()))

    
currencies: list[dict[str, str | float]] = [
        {'name': 'USD', 'per_$': 1},
        {'name': 'AFN', 'per_$': 0.014},
        {'name': 'BDT', 'per_$': 0.0083},
        {'name': 'DZD', 'per_$': 0.0074}
    ]

def get_currency(curr_name: str) -> dict[str, str | float] | None:
    curr_name = curr_name.upper()
    for currency in currencies:
        if currency['name'] == curr_name: return currency

    return None

def show_invalid_msg(text: str) -> None:
    print(f"Invalid {text}, Please try again!")

def show_status_msg(curr_name: str, status: str) -> None:
    print(f"'{curr_name}' currency has been successfully {status}!")


MENU_OPTIONS: tuple[str] = "View all currencies and rate", "Convert currency", "Add a currency", "Remove a currency", "Modify currency rate"

draw_banner("Welcome to Currency Converter System", 60)

while True:
    print("\n*Available options*")
    for opn_no, option in enumerate(MENU_OPTIONS, 1):
        print(f"\t{opn_no}. {option}.")
    print("\t0. Exit this system.", end="\n\n")

    choice: str = input("Enter an option: ")
    print()
    is_wrong_choice: bool = False

    try: 
        option_no: int = int(choice)
    except ValueError:
        is_wrong_choice = True
    else:
        if option_no == 0: 
            print("\tThank you for using this system!")
            break
        if (option_no < 0 or option_no > len(MENU_OPTIONS)) and not is_wrong_choice: is_wrong_choice = True

    if is_wrong_choice:
        show_invalid_msg('choice')
        continue
    match(option_no):
        case 1: show_as_table('available currencies', ('Name', 'Rate(in $)'), currencies)
        case 2:
            print("\tConvert currency ")

            temp_currencies = {
                'from': {},
                'to': {}
            }

            for option in temp_currencies.keys():
                curr_name: str = input(f"{option}: ")
                currency = get_currency(curr_name)
                if currency == None:
                    show_invalid_msg(f"currency name '{curr_name}'")
                    break
                temp_currencies[option] = currency
            else:
                print(f'\t"Converting currency: {temp_currencies['from']['name']} -> {temp_currencies['to']['name']}"')
                try: amount: float = float(input("Enter amount: "))
                except ValueError: show_invalid_msg('amount')
                else: 
                    converted_amount: float = round(amount * temp_currencies['from']['per_$'] / temp_currencies['to']['per_$'], 4)
                    print(f"{amount} {temp_currencies['from']['name']} = {converted_amount} {temp_currencies['to']['name']}")
            
        case 3:
            curr_name: str = input("Enter new currency name(3 words, uppercase recommanded): ")
            if len(curr_name) != 3:
                show_invalid_msg(f"currency name '{curr_name}' (must be 3 words long)")
                continue
            if not curr_name.isupper(): curr_name = curr_name.upper()

            try: curr_per_dollar_rate: float = float(input("Enter per $ rate: "))
            except ValueError: show_invalid_msg('dollar rate')
            else: 
                currencies.append({'name': curr_name, 'per_$': curr_per_dollar_rate})
                show_status_msg(curr_name, 'added')

        case 4:
            curr_name: str = input("Enter currency name(3 words): ")
            currency = get_currency(curr_name)
            if currency == None:
                show_invalid_msg(f"currency name '{curr_name}'")
                continue
            currencies.remove(currency)
            show_status_msg(currency['name'], 'removed')

        case 5:
            curr_name: str = input("Enter currency name(3 words): ")
            currency = get_currency(curr_name)
            if currency == None:
                show_invalid_msg(f"currency name '{curr_name}'")
                continue
            try: curr_per_dollar_rate: float = float(input("Enter new per $ rate: "))
            except ValueError: show_invalid_msg('dollar rate')
            else: 
                currency['per_$'] = curr_per_dollar_rate
                show_status_msg(currency['name'], 'modified')
