from abc import ABC, abstractmethod
from typing import List, Dict, Any
from tabulate import tabulate


class BaseReport(ABC):

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    @abstractmethod
    def generate(self) -> List[Dict[str, Any]]:
        pass

    def display(self, result: List[Dict[str, Any]]) -> None:
        if result:
            headers = result[0].keys()
            rows = [list(item.values()) for item in result]
            print(tabulate(rows, headers=headers, tablefmt='grid'))
        else:
            print("Нет данных для отображения")