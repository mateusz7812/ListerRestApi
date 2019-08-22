from typing import List, Dict, AnyStr


class DataBaseInterface:
    def __init__(self, columns: List[AnyStr]):
        self.columns = columns

    def insert(self, data: dict) -> bool:
        raise NotImplementedError

    def select(self, where: dict) -> List[Dict]:
        raise NotImplementedError

    def update(self, update: dict, where: dict) -> bool:
        raise NotImplementedError

    def delete(self, where: dict) -> bool:
        raise NotImplementedError
