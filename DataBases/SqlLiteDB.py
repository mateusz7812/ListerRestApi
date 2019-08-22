from typing import List, Dict

import DataBases.DataBaseInterface


class SqlLiteDB(DataBases.DataBaseInterface.DataBaseInterface):
    def insert(self, data: dict) -> bool:
        pass

    def select(self, where: dict) -> List[Dict]:
        pass

    def update(self, update: dict, where: dict) -> bool:
        pass

    def delete(self, where: dict) -> bool:
        pass
