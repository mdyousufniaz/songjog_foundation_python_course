from utils import center_print, print_as_table, ask_to_try_again, show_invalid_msg, show_success_msg, right_print, get_choice, not_blank_field, clear_screen, print_banner, press_enter_to_continue, print_row, yes_or_no, print_border
from customer import Customer
from fooditem import Food, Combo
from cart import Cart
from order import Order

from collections import defaultdict
from typing import Any

class RMS:
    MAIN_OPTIONS = "Sign In", "Sign Up"
    RESTAURANT_OPTIONS = "Show all food items", "Show cart", "Add a food item in cart", "Remove a food item in cart", "Clear Cart", "Place order", "Show order history", "Log out"
    
    

    def __init__(self, res_name: str ="My Restaurant") -> None:
        self.res_name = res_name
        self.current_user_name : str | None = None
        self.__cart: defaultdict[int, int] = defaultdict(int)
        self.__food_items: tuple[Food | Combo] = (
            burger := Food('Burger', 100),
            sandwitch := Food('Sandwitch', 150),
            Food('Pizza', 200),
            chicken_fry := Food('Chicken Fry', 175),
            Food('Shawarma', 80),
            water := Food('Water 500 ml', 20),
            coffee := Food('Coffee', 60),
            Food('Tea', 20),
            Combo('Combo1', (burger, sandwitch, water)),
            Combo('Combo2', (chicken_fry, coffee))
        )

    def load_cart(self) -> None:
        if (cart := Cart.load_cart(self.current_user_name)) is None:
            self.__cart = defaultdict(int)
            return
        
        self.__cart = cart

    def show_foods_with_quantity(self):...

    def show_food_items_in_table(self, food_ids: list[int], show_total: bool, pause: bool) -> None:
        rows: list[tuple[Any]] = [(food_id + 1, self.__food_items[food_id].name(), self.__food_items[food_id].price()) for food_id in food_ids]
        rows.insert(0, ('FOOD_ID', 'NAME', 'PRICE(in tk)'))
        print_as_table(rows)

        if show_total:
            total = sum(tuple(map(lambda food_id: self.__food_items[food_id].price(),self.__cart)))
            print_row(('', 'TOTAL = ', total))
            print_border()

        if pause: press_enter_to_continue()
    
    def is_cart_empty(self) -> bool:
        if not self.__cart:
            center_print("Cart is empty!")
            press_enter_to_continue()
            return True
        return False

    def show_cart(self, pause: bool = False) -> None:
        if self.is_cart_empty(): return
        print("Showing Cart:")
        self.show_food_items_in_table(self.__cart, True)
        total = sum(tuple(map(lambda food_id: self.__food_items[food_id].price(),self.__cart)))
        print_row(('', 'TOTAL = ', total))
        if not pause: press_enter_to_continue()

    def get_food_id(self) -> int | None:
        if (food_id := get_choice(len(self.__food_items), "Food ID", 1)) is None: return None
        return food_id - 1
    
    def save_cart(self) -> None:
        Cart.save_cart(self.current_user_name, self.__cart)

    def add_into_cart(self) -> None:
        self.show_all_food_items(True)

        if (food_id := self.get_food_id()) is None: return
        food = self.__food_items[food_id]

        if food_id in self.__cart:
            ask_to_try_again(f"Food Item '{food.name()}' already added!")
            return
        
        self.__cart.append(food_id)
        self.save_cart()
        show_success_msg(f"added Food Item '{food.name()}' in your cart")


    def show_all_food_items(self, pause: bool = False) -> None:
        print("Available food_items: ")
        self.show_food_items_in_table(list(range(len(self.__food_items))), pause)
        
    def remove_from_cart(self) -> None:
        self.show_cart(True)
        if (food_id := self.get_food_id()) is None: return
        food = self.__food_items[food_id]

        if food_id not in self.__cart:
            ask_to_try_again(f"Food Item '{food.name()}' does not exist in your cart")
            return
        self.__cart.remove(food_id)
        self.save_cart()
        show_success_msg(f"removed Food Item '{food.name()}' in your cart")

    def clear_cart(self) -> None:
        self.__cart = []
        self.save_cart()
        show_success_msg("Cleared cart")

    def customer_signed_in(self) -> bool:
        return self.current_user_name is not None

    def print_sign_in_status(self) -> None:
        right_print(f"Signed in as '{self.current_user_name}'" if self.customer_signed_in() else "Not Signed in")
        print()

    def show_menu(self, title: str, options: tuple[str]) -> None:
        clear_screen()
        print_banner(f"Welcome to {self.res_name}")
        self.print_sign_in_status()
        print(f"Showing {title} menu options:")

        for index, option in enumerate(options, 1): print(f"\t {index}. {option}")
        print("\t 0. Exit")

    def show_main_menu(self) -> None:
        self.show_menu('Main', self.MAIN_OPTIONS)

    def show_restaurant_menu(self) -> None:
        self.show_menu('Restaurant', self.RESTAURANT_OPTIONS)

    def get_menu_choice(self, options: tuple[Any], field_name: str = "choice", start: int = 0) -> int | None:
        options_count = len(options)
        choice = input(f"Enter {field_name}[{start}-{options_count}]: ")
        invalid_choice = False

        try: option_num = int(choice)
        except ValueError: invalid_choice = True
        else: 
            if option_num not in range(start, options_count + 1): invalid_choice = True

        if invalid_choice:
            self.show_invalid_msg(field_name)
            return None
        
        return option_num

    def get_main_menu_choice(self) -> int | None:
        return get_choice(len(self.MAIN_OPTIONS))
    
    def get_res_menu_choice(self) -> int | None:
        return get_choice(len(self.RESTAURANT_OPTIONS))
    
    def sign_in(self) -> None:
        user_name = input("Enter Your Username: ")
        
        if (password := Customer.get_password(user_name)) is None: 
            show_invalid_msg(f"username '{user_name}'")
            return

        if password != input("Enter Your Password: "): 
            show_invalid_msg('password')
            return

        self.current_user_name = user_name
        self.load_cart()
        show_success_msg(f"Signed in as '{user_name}'")


    def sign_up(self) -> None:
        if (user_name := not_blank_field('Username')) is None: return
        if Customer.get_password(user_name) is not None:
            ask_to_try_again(f"username '{user_name}' already exists")
            return
        
        if (password := not_blank_field('Password')) is None: return

        if input("Confirm Password: ") != password:
            ask_to_try_again("confirm password and password do not match")
            return
        
        Customer.register(user_name, password)
        show_success_msg(f"Signed up as '{user_name}'")

    def place_order(self) -> None:
        if self.is_cart_empty(): return

        self.show_cart(True)
        if not (answer := yes_or_no("Do you really want to place order")): return
        
        Order.place_order(self.current_user_name)
        print(f"Successfully Placed order as order_{Order.total_order(self.current_user_name)}")

        if not (answer := yes_or_no("Do you want to clear cart")): return
        self.clear_cart()





        
