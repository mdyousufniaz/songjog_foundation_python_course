from file import File
from collections import defaultdict
from utils import expand_numbers, compress_numbers

class Cart:

    CART_FILE = File('cart', ('username', 'food_ids', 'quantities'))

    @staticmethod
    def get_cart(user_name: str) -> dict[str, str] | None:
        return Cart.CART_FILE.get_row({'username': user_name})

    @staticmethod
    def load_cart(user_name: str) -> defaultdict[int, int] | None:
        if (record := Cart.get_cart(user_name)) is None or not record['food_ids']: return None
        return defaultdict(
            int,
            {food_id: quantity for food_id, quantity in zip(
                expand_numbers(record['food_ids']),
                expand_numbers(record['quantities'])
            )}
        )
    
    @staticmethod
    def save_cart(user_name: str, cart: defaultdict[int, int]) -> None:
        Cart.CART_FILE.save_record(
            {'username': user_name},
            {'username': user_name, 'food_ids': compress_numbers(tuple(cart.keys())), 'quantities': compress_numbers(tuple(cart.values()))}
        )