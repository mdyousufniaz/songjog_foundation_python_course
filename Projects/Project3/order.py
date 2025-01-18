from file import File
from cart import Cart

from datetime import datetime

class Order:

    ORDER_FILE = File('orders', ('username', 'food_ids', 'date', 'time'))

    @staticmethod
    def place_order(user_name: str) -> None:
        record = Cart.get_cart(user_name)
        curr_date_time = datetime.now()
        record['date'] = curr_date_time.strftime("%d %B %Y")
        record['time'] = curr_date_time.strftime("%I:%M:%S %p")
        Order.ORDER_FILE.append_row(tuple(record.values()))

    @staticmethod
    def total_order(user_name: str) -> int:
        return len(Order.ORDER_FILE.get_rows({'username': user_name}))