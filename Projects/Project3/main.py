from restaurant_management_system import RMS
from utils import initial_setup, exit_system

def main() -> None:
    initial_setup()
    rms = RMS()

    while True:
        rms.show_main_menu()
        option_no = rms.get_main_menu_choice()
        if option_no == None: continue
        
        match option_no:
            case 0: exit_system()
            case 1: rms.sign_in()
            case 2: rms.sign_up()
        
        if not rms.customer_signed_in(): continue

        while True:
            rms.show_restaurant_menu()
            if (option_no := rms.get_res_menu_choice()) == None: continue

            match option_no:
                case 0: exit_system()
                case 1: rms.show_all_food_items()
                case 2: rms.show_cart()
                case 3: rms.add_into_cart()
                case 4: rms.update_quantity()
                case 5: rms.remove_from_cart()
                case 6: rms.clear_cart()
                case 7: rms.place_order()
                case 8: rms.show_order_history()
                case 9: 
                    rms.sign_out()
                    break

if __name__ == '__main__': main()

# total 75 methods.