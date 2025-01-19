from abc import ABC, abstractmethod

class FoodItem(ABC):

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def name(self) -> str:
        return self._name

    @abstractmethod
    def price(self) -> float:
        pass


class Food(FoodItem):

    def __init__(self, name: str, price: float) -> None:
        super().__init__(name)
        self.__price = price

    def price(self) -> float:
        return self.__price
    
class Combo(FoodItem):

    def __init__(self, name: str, foods: tuple[Food]) -> None:
        super().__init__(name)
        self.__foods = foods

    def price(self) -> float:
        return sum(map(lambda food: food.price(), self.__foods))
    
    def name(self) -> str:
        return f"{self._name} ({' + '.join(map(lambda food: food.name(), self.__foods))})"