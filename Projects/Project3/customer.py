from file import File

class Customer:
    
    customer_file = File('customers', ('username', 'password'))

    @staticmethod
    def get_password(user_name: str) -> str | None:
        if (customer_record := Customer.customer_file.get_row({'username': user_name})) is None: return None
        return customer_record['password']
    
    @staticmethod
    def register(user_name: str, password: str) -> None:
        Customer.customer_file.append_row((user_name, password))