from os.path import join, exists
from csv import DictReader, DictWriter
from utils import DB_DIR

class File:

    def __init__(self, name: str, headers: tuple[str], path: str = DB_DIR, type: str = 'csv'):
        self.__file_path = join(path, f"{name}.{type}")
        self.__headers = headers
        if not exists(self.__file_path): self.recreate()

    def recreate(self) -> None:
        with open(self.__file_path, 'w', newline='\n') as file:
            DictWriter(file, fieldnames=self.__headers).writeheader()

    def all_data(self) -> list[dict[str, str]]:
        with open(self.__file_path) as file:
            return list(DictReader(file))
        
    def get_rows(self, fields: dict[str, str]) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for row in self.all_data():
            for key, value in fields.items():
                if row[key] != value: break
            else: result.append(row)
        
        return result
    
    def get_row(self, fields: dict[str, str]) -> dict[str, str] | None:
        if not (record := self.get_rows(fields)): return None
        return record[0]

    
    def append_row(self, field_values: tuple[str]) -> None:
        with open(self.__file_path, 'a', newline='\n') as file:
            DictWriter(file, fieldnames=self.__headers).writerow({
                field: field_value
                for field, field_value in zip(self.__headers, field_values)
            })

    
    def save_record(self, keys: dict[str, str], values: dict[str, str]) -> None:
        rows = self.all_data()
        for row in rows:
            for key_key, key_value in keys.items():
                if row[key_key] != key_value: break
            else:
                for value_key, value_value in values.items(): row[value_key] = value_value
                break
        else:
            self.append_row(tuple(values.values()))
            return

        with open(self.__file_path, 'w', newline='\n') as file:
            writer = DictWriter(file, fieldnames=self.__headers)
            writer.writeheader()
            writer.writerows(rows)

            

