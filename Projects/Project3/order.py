from file import File
from cart import Cart
from utils import expand_numbers

from datetime import datetime

class Order:

    ORDER_FILE = File('orders', ('username', 'food_ids', 'quantities', 'date', 'time'))

    @staticmethod
    def place_order(user_name: str) -> None:
        record = Cart.get_cart(user_name)
        curr_date_time = datetime.now()
        record['date'] = curr_date_time.strftime("%d %B %Y")
        record['time'] = curr_date_time.strftime("%I:%M:%S %p")
        Order.ORDER_FILE.append_row(tuple(record.values()))

    @staticmethod
    def get_all_order(user_name: str) -> list[dict[str, str]]:
        return Order.ORDER_FILE.get_rows({'username': user_name})

    @staticmethod
    def total_order(user_name: str) -> int:
        return len(Order.get_all_order(user_name))
    
    @staticmethod
    def get_order(user_name: str, order_id: int) -> dict[str, tuple[int] | str]:
        order = Order.get_all_order(user_name)[order_id]
        order.pop('username')
        order['food_ids'] = expand_numbers(order['food_ids'])
        order['quantities'] = expand_numbers(order['quantities'])
        return order
