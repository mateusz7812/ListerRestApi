from typing import List, Dict, AnyStr


class DataBaseInterface:
    def __init__(self, table_name: str,  columns: List[AnyStr]):
        self.table_name = table_name
        self.columns = set(columns)

    def insert(self, data: dict) -> dict:
        raise NotImplementedError

    def select(self, where: dict) -> List[Dict]:
        raise NotImplementedError

    def update(self, update: dict, where: dict) -> dict:
        raise NotImplementedError

    def delete(self, where: dict) -> bool:
        raise NotImplementedError
