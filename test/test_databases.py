import copy
from unittest import TestCase

from DataBases.MongoDB import MongoDB


class MongoDBTests(TestCase):
    def setUp(self) -> None:
        self.db = MongoDB("accounts", ["id", "name", "test"])
        self.db.coll.drop()

    def tearDown(self) -> None:
        self.db.coll.drop()

    def test_insert(self):
        data = {"name": "cat", "test": "test"}

        response = self.db.insert(copy.deepcopy(data))

        self.assertEqual(str, type(response.pop("id")))
        self.assertEqual(data, response)

    def test_insert_existed(self):
        data = {"id": "asd", "name": "cat", "test": "test"}
        self.db.insert(copy.deepcopy(data))

        response = self.db.insert(copy.deepcopy(data))

        self.assertEqual({}, response)

    def test_insert_none(self):
        data1 = {"test": "test"}
        data2 = {"name": "cat"}
        self.db.insert(copy.deepcopy(data1))
        self.db.insert(copy.deepcopy(data2))

        result = self.db.select({})

        for r in result:
            r.pop("id")

        self.assertEqual(
            [
                {'test': 'test', 'name': None},
                {'name': 'cat', 'test': None}
            ],
            result)

    def test_select(self):
        data = {"name": "cat", "test": "test"}
        self.db.insert(copy.deepcopy(data))
        self.db.insert(copy.deepcopy(data))
        self.db.insert(copy.deepcopy(data))

        response = self.db.select({"test": "test"})

        self.assertEqual(3, len(response))
        self.assertEqual("test", response[0]["test"])
        self.assertEqual(str, type(response[0]["id"]))

    def test_update(self):
        data = {"name": "cat", "test": "test"}
        self.db.insert(copy.deepcopy(data))

        response = self.db.update({"test": "work"}, {"name": "cat"})

        self.assertEqual(str, type(response.pop("id")))
        self.assertEqual({"name": "cat", "test": "work"}, response)

    def test_update_two_dicts(self):
        data = {"name": "cat", "test": "test"}
        self.db.insert(copy.deepcopy(data))
        self.db.insert(copy.deepcopy(data))

        response = self.db.update({"test": "work"}, {"name": "cat"})

        self.assertEqual({}, response)

    def test_delete(self):
        data = {"name": "cat", "test": "test"}
        self.db.insert(copy.deepcopy(data))

        response = self.db.delete({"name": "cat"})

        self.assertTrue(response)
        self.assertEqual(0, len(self.db.select({})))

    def test_delete_two_dicts(self):
        data = {"name": "cat", "test": "test"}
        self.db.insert(copy.deepcopy(data))
        self.db.insert(copy.deepcopy(data))

        response = self.db.delete({"name": "cat"})

        self.assertFalse(response)
        self.assertEqual(2, len(self.db.select({})))
