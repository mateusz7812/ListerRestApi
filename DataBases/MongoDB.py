from typing import List, Dict

from pymongo import MongoClient

import DataBases.DataBaseInterface


def prepare_id(raw_dict: dict):
    raw_dict["_id"] = raw_dict.pop("id")
    return raw_dict


def convert_id_for_response(raw_dict: dict):
    raw_dict["id"] = str(raw_dict.pop("_id"))
    return raw_dict


class MongoDB(DataBases.DataBaseInterface.DataBaseInterface):
    def __init__(self, table_name: str, columns):
        super().__init__(table_name, columns)
        client = MongoClient("10.0.75.1")
        self.coll = client.admin[table_name]

    def insert(self, data: dict) -> dict:
        if "id" in data.keys():
            if self.coll.count_documents({"_id": data["id"]}):
                return {}
            data = prepare_id(data)
        for col in self.columns:
            if col not in data.keys():
                data[col] = None
        response = self.coll.insert_one(data)
        inserted = self.coll.find({"_id": response.inserted_id})
        if not inserted:
            return {}
        return convert_id_for_response(inserted[0])

    def select(self, where: dict) -> List[Dict]:
        raw_dicts = list(self.coll.find(where))
        return list(map(convert_id_for_response, raw_dicts))

    def update(self, update: dict, where: dict) -> dict:
        if self.coll.count_documents(where) != 1:
            return {}
        self.coll.update_one(where, {'$set': update})
        data_dict = self.coll.find(where)[0]
        return convert_id_for_response(data_dict)

    def delete(self, where: dict) -> bool:
        if self.coll.count_documents(where) != 1:
            return False
        return self.coll.delete_one(where).deleted_count == 1
