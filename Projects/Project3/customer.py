from file import File

class Customer:
    
    customer_file = File('customers', ('username', 'password'))

    @staticmethod
    def get_password(user_name: str) -> str | None:
        customer_record = Customer.customer_file.get_rows({'username': user_name})
        if not customer_record: return None
        
        return customer_record[0]['password']
    
    @staticmethod
    def register(user_name: str, password: str) -> None:
        Customer.customer_file.append_row((user_name, password))