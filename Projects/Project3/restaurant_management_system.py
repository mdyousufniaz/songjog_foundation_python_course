from utils import center_print, print_as_table, ask_to_try_again, show_invalid_msg, show_success_msg, right_print, get_choice, not_blank_field, clear_screen, print_banner, press_enter_to_continue, print_row, yes_or_no, print_border, get_quantity, ask_to_continue
from customer import Customer
from fooditem import Food, Combo
from cart import Cart
from order import Order

from collections import defaultdict
from typing import Any

class RMS:
    __MAIN_OPTIONS = "Sign In", "Sign Up"
    __RESTAURANT_OPTIONS = "Show all food items", "Show cart", "Add a food item in cart", "Update Quantity", "Remove a food item in cart", "Clear Cart", "Place order", "Show order history", "Sign out"

    def __init__(self, res_name: str ="My Restaurant") -> None:
        self.__res_name = res_name
        self.__current_user_name : str | None = None
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

    def __print_sign_in_status(self) -> None:
        right_print(f"Signed in as '{self.__current_user_name}'" if self.customer_signed_in() else "Not Signed in")
        print()

    def __show_menu(self, title: str, options: tuple[str]) -> None:
        clear_screen()
        print_banner(f"Welcome to {self.__res_name}")
        self.__print_sign_in_status()
        print(f"Showing {title} menu options:")

        for index, option in enumerate(options, 1): print(f"\t {index}. {option}")
        print("\t 0. Exit")

    def __load_cart(self) -> None:
        if (cart := Cart.load_cart(self.__current_user_name)) is None:
            self.__cart = defaultdict(int)
            return
        
        self.__cart = cart

    def __show_foods_with_quantity(self, food_ids: tuple[int], quantities: tuple[int], pause: bool) -> None:
        rows: list[tuple[Any]] = [(food_id + 1, self.__food_items[food_id].name(), f"{self.__food_items[food_id].price()} X {quantity}", self.__food_items[food_id].price() * quantity) for food_id, quantity in zip(food_ids, quantities)]
        rows.insert(0, ('FOOD_ID', 'NAME', 'BASE PRICE(in tk) X Quantity', 'PRICE(in tk)'))

        print_as_table(rows)
        total = sum(tuple(map(lambda food_id, quantity: self.__food_items[food_id].price() * quantity, food_ids, quantities)))
        print_row(('', '', 'TOTAL = ', total))
        print_border()

        if pause: press_enter_to_continue()
    
    def __is_cart_empty(self) -> bool:
        if not self.__cart:
            center_print("Cart is empty!", True)
            return True
        return False

    def __get_food_id(self) -> int | None:
        if (food_id := get_choice(len(self.__food_items), "Food ID", 1)) is None: return None
        return food_id - 1
    
    def __save_cart(self) -> None:
        Cart.save_cart(self.__current_user_name, self.__cart)

    def __food_with_quantity(self, food_id: int) -> str:
        return f"'{self.__food_items[food_id].name()}: x{self.__cart[food_id]}'"
    
    def __get_cart_food_id(self) -> int | None:
        food_id = input("Enter food id: ")
        invalid_food_id = False
        try: food_id = int(food_id) - 1
        except ValueError: invalid_food_id = True
        else:
            if food_id not in self.__cart.keys() and not invalid_food_id: invalid_food_id = True

        if invalid_food_id:
            show_invalid_msg(f"Food id: {food_id}")
            return  None
        return food_id    
    
    def __check_n_show_cart(self) -> bool:
        if self.__is_cart_empty(): return False
        self.show_cart(False)
        return True
    
    def __do_sign_in(self, user_name: str) -> None:
        self.__current_user_name = user_name
        self.__load_cart()
        show_success_msg(f"Signed in as '{user_name}'")

    def show_main_menu(self) -> None:
        self.__show_menu('Main', self.__MAIN_OPTIONS)

    def get_main_menu_choice(self) -> int | None:
        return get_choice(len(self.__MAIN_OPTIONS))

    def sign_in(self) -> None:
        user_name = input("Enter Your Username: ")
        
        if (password := Customer.get_password(user_name)) is None: 
            show_invalid_msg(f"username '{user_name}'")
            return

        if password != input("Enter Your Password: "): 
            show_invalid_msg('password')
            return

        self.__do_sign_in(user_name)

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
        print(f"Successfully signed up as '{user_name}'!")

        if (answer := yes_or_no("Do you want to sign in now")) is None: return
        if not answer:
            ask_to_continue("sign in failed")
            return
        
        self.__do_sign_in(user_name)

    def customer_signed_in(self) -> bool:
        return self.__current_user_name is not None
    
    def show_restaurant_menu(self) -> None:
        self.__show_menu('Restaurant', self.__RESTAURANT_OPTIONS)

    def get_res_menu_choice(self) -> int | None:
        return get_choice(len(self.__RESTAURANT_OPTIONS))

    def show_all_food_items(self, pause: bool = True) -> None:
        print("Available food_items: ")
        rows: list[tuple[Any]] = [(food_id, food.name(), food.price()) for food_id, food in enumerate(self.__food_items, 1)]
        rows.insert(0, ('FOOD_ID', 'NAME', 'BASE PRICE(in tk)'))
        print_as_table(rows)

        if pause: press_enter_to_continue()

    def show_cart(self, pause: bool = True) -> None:
        if self.__is_cart_empty(): return
        print("Showing Cart:")
        self.__show_foods_with_quantity(self.__cart.keys(), self.__cart.values(), pause)

    def add_into_cart(self) -> None:
        self.show_all_food_items(False)

        if (food_id := self.__get_food_id()) is None: return
        food_name = self.__food_items[food_id].name()

        if food_id in self.__cart.keys():
            print(f"Food Item '{food_name}' already exist in your cart(quantity: {self.__cart[food_id]})") 
            if not yes_or_no("Do you want to add more"): return

        if (amount := get_quantity(f"Enter how many do you want to add[{food_name}]: ")) is None: return
        
        self.__cart[food_id] += amount
        self.__save_cart()
        show_success_msg(f"added Food Item {self.__food_with_quantity(food_id)} in your cart")
    
    def update_quantity(self) -> None:
        if not self.__check_n_show_cart(): return
        if (food_id := self.__get_cart_food_id()) is None: return

        print(f"Food Item {self.__food_with_quantity(food_id)} found.")
        if (new_amount := get_quantity("Enter new quantity: ")) is None: return
        self.__cart[food_id] = new_amount
        self.__save_cart()
        show_success_msg(f"updated quantity for {self.__food_with_quantity(food_id)}")
        
    def remove_from_cart(self) -> None:
        if not self.__check_n_show_cart(): return
        if (food_id := self.__get_cart_food_id()) is None: return
        
        self.__cart.pop(food_id)
        self.__save_cart()
        show_success_msg(f"removed Food Item '{self.__food_items[food_id].name()}' in your cart")

    def clear_cart(self) -> None:
        if self.__is_cart_empty(): return
        self.__cart = defaultdict(int)
        self.__save_cart()
        show_success_msg("Cleared cart")

    def place_order(self) -> None:
        if not self.__check_n_show_cart(): return
        if (answer := yes_or_no("Do you really want to place order")) is None: return
        if not answer: 
            ask_to_continue("Order could not be placed")
            return
        
        Order.place_order(self.__current_user_name)
        print(f"Successfully Placed order as order_{Order.total_order(self.__current_user_name)}")

        if (answer := yes_or_no("Do you want to clear cart")) is None: return
        if not answer: 
            ask_to_continue("Cart could not be cleared")
            return
        
        self.clear_cart()
    
    def show_order_history(self) -> None:
        if not (total_orders := Order.total_order(self.__current_user_name)):
            center_print("You have not placed any orders!", True)
            return
        print("Showing all orders:")
        ORDER_RANGE = range(1, total_orders + 1)
        for order_id in ORDER_RANGE:
            print(f"\t{order_id}. order_{order_id}")

        order_id = input("Enter order_id: ")
        invalid_order_id = False
        try: order_id = int(order_id)
        except ValueError: invalid_order_id = True
        else:
            if order_id not in ORDER_RANGE: invalid_order_id = True
        
        if invalid_order_id: 
            show_invalid_msg(f"{order_id :}")
            return
        
        order = Order.get_order(self.__current_user_name, order_id - 1)
        print(f"\nShowing order_{order_id}: ")
        right_print(f"Order Date: {order['date']}, Time: {order['time']}")
        self.__show_foods_with_quantity(order['food_ids'], order['quantities'], True)

    def sign_out(self) -> None:
        show_success_msg(f"Signed out as '{self.__current_user_name}'")
        self.__current_user_name = None