from unittest.mock import Mock, MagicMock

from flask_testing import TestCase

import Main

val = None


class RestApiTest(TestCase):
    def create_app(self):
        app = Main.app
        app.config['TESTING'] = True
        app.secret_key = 'super secret key'
        app.config['SESSION_TYPE'] = 'filesystem'
        return app

    def test_accounts_get(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        accounts_dicts_list = [{"id": '1', "nick": "asd", "login": "qwe", "password": hash(123)},
                               {"id": '1', "nick": "asd", "login": "qwe", "password": hash(123)}]
        account_db_mock.select.return_value = accounts_dicts_list
        Main.account_db = account_db_mock

        response = client.get("http://localhost:7000/accounts")

        account_db_mock.select.assert_called_once_with({})
        self.assertEqual(200, response.status_code)
        self.assertEqual(accounts_dicts_list, response.json)

    def test_accounts_post(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_dict = {"nick": "asd", "login": "qwe", "password": hash(123)}
        account_db_mock.insert.return_value = account_dict
        Main.account_db = account_db_mock

        response = client.post(
            "http://localhost:7000/accounts",
            json=account_dict
        )

        account_db_mock.insert.assert_called_once_with(account_dict)
        self.assertEqual(201, response.status_code)
        self.assertEqual(account_dict, response.json)

    def test_accounts_post_with_bad_column(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.insert.return_value = {}
        account_db_mock.columns = {"id", "nick", "login", "password"}
        Main.account_db = account_db_mock

        account_dict = {"nick": "asd", "login": "qwe", "password": hash(123), "email": "asdsasd@gmail.com"}

        response = client.post(
            "http://localhost:7000/accounts",
            json=account_dict
        )

        account_db_mock.insert.assert_not_called()
        self.assertEqual(400, response.status_code)
        self.assertEqual({"error": "['email'] columns not found"}, response.json)

    def test_accounts_post_with_id(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_dict = {"id": '1', "nick": "asd", "login": "qwe", "password": hash(123)}
        account_db_mock.insert.return_value = {}
        Main.account_db = account_db_mock

        response = client.post(
            "http://localhost:7000/accounts",
            json=account_dict
        )

        account_db_mock.insert.assert_not_called()
        self.assertEqual(400, response.status_code)
        self.assertEqual({"error": "id in account data dict"}, response.json)

    def test_accounts_post_with_db_fault(self):
        client = self.app.test_client()
        account_db_mock = Mock()
        account_db_mock.columns = {"id", "nick", "login", "password"}
        account_db_mock.insert.return_value = False
        Main.account_db = account_db_mock

        response = client.post(
            "http://localhost:7000/accounts",
            json={"nick": "asd", "login": "qwe", "password": hash(123)}
        )

        self.assertEqual(500, response.status_code)
        self.assertEqual({"error": "database failure"}, response.json)

    def test_account_get(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        accounts_dicts = [{"id": '1', "nick": "asd", "login": "qwe", "password": hash(123)}]
        account_db_mock.select.return_value = accounts_dicts
        Main.account_db = account_db_mock

        response = client.get("http://localhost:7000/accounts/1")

        account_db_mock.select.assert_called_once_with({"id": '1'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(accounts_dicts[0], response.json)

    def test_account_get_bad_column(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        accounts_dicts = [{"id": '1', "nick": "asd", "login": "qwe", "password": hash(123)}]
        account_db_mock.select.return_value = accounts_dicts
        Main.account_db = account_db_mock

        response = client.get("http://localhost:7000/accounts/1")

        account_db_mock.select.assert_called_once_with({"id": '1'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(accounts_dicts[0], response.json)

    def test_account_get_not_found_account(self):
        Main.account_db.select = lambda x: []
        client = self.app.test_client()

        response = client.get("http://localhost:7000/accounts/2")

        self.assertEqual(404, response.status_code)
        self.assertEqual({"error": "account not found"}, response.json)

    def test_account_put_account(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.columns = {"id", "nick", "login", "password"}
        account_dict = {"id": '2', "name": "asd", "login": "qwe", "password": hash(123)}
        modified_account_dict = {"id": '2', "name": "asd", "login": "ewq", "password": hash(123)}
        account_db_mock.select.return_value = [account_dict]
        account_db_mock.update.return_value = [modified_account_dict]
        Main.account_db = account_db_mock

        response = client.put("http://localhost:7000/accounts/2",
                              json={"login": "ewq"})

        account_db_mock.select.assert_called_once_with({"id": '2'})
        account_db_mock.update.assert_called_once_with({"id": '2'}, {"login": "ewq"})
        self.assertEqual(200, response.status_code)
        self.assertEqual([modified_account_dict], response.json)

    def test_account_put_account_bad_column(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.columns = {"id", "nick", "login", "password"}
        account_dict = {"id": '2', "name": "asd", "login": "qwe", "password": hash(123)}
        modified_account_dict = {"id": '2', "name": "asd", "login": "ewq", "password": hash(123)}
        account_db_mock.select.return_value = [account_dict]
        account_db_mock.update.return_value = [modified_account_dict]
        Main.account_db = account_db_mock

        response = client.put("http://localhost:7000/accounts/2",
                              json={"login": "ewq", "email": "asdasd@gamil.com"})

        account_db_mock.select.assert_called_once_with({"id": '2'})
        account_db_mock.update.assert_not_called()
        self.assertEqual(400, response.status_code)
        self.assertEqual({"error": "['email'] columns not found"}, response.json)

    def test_account_put_account_user_not_found(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.select.return_value = []
        Main.account_db = account_db_mock

        response = client.put("http://localhost:7000/accounts/2",
                              json={"login": "ewq"})

        account_db_mock.select.assert_called_once_with({"id": '2'})
        account_db_mock.update.assert_not_called()
        self.assertEqual(404, response.status_code)
        self.assertEqual({"error": "account not found"}, response.json)

    def test_account_put_account_update_error(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.select.return_value = [{"id": '2'}]
        account_db_mock.update.return_value = False
        Main.account_db = account_db_mock

        response = client.put("http://localhost:7000/accounts/2",
                              json={"login": "ewq"})

        account_db_mock.select.assert_called_once_with({"id": '2'})
        account_db_mock.update.assert_called_once_with({"id": '2'}, {"login": "ewq"})
        self.assertEqual(500, response.status_code)
        self.assertEqual({"error": "database failure"}, response.json)

    def test_account_delete(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.select.return_value = [{"id": '2'}]
        account_db_mock.delete.return_value = True
        Main.account_db = account_db_mock

        response = client.delete("http://localhost:7000/accounts/2")

        account_db_mock.select.assert_called_once_with({"id": '2'})
        account_db_mock.delete.assert_called_once_with({"id": '2'})
        self.assertEqual(204, response.status_code)
        self.assertEqual(b'', response.data)

    def test_account_delete_db_failure(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.select.return_value = [{"id": '2'}]
        account_db_mock.delete.return_value = False
        Main.account_db = account_db_mock

        response = client.delete("http://localhost:7000/accounts/2")

        account_db_mock.select.assert_called_once_with({"id": '2'})
        account_db_mock.delete.assert_called_once_with({"id": '2'})
        self.assertEqual(500, response.status_code)
        self.assertEqual({"error": "database failure"}, response.json)

    def test_account_delete_account_not_found(self):
        client = self.app.test_client()
        account_db_mock = MagicMock()
        account_db_mock.select.return_value = []
        Main.account_db = account_db_mock

        response = client.delete("http://localhost:7000/accounts/2")

        account_db_mock.select.assert_called_once_with({"id": '2'})
        account_db_mock.delete.assert_not_called()
        self.assertEqual(404, response.status_code)
        self.assertEqual({"error": "account not found"}, response.json)
