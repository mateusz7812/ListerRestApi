from flask_testing import TestCase

import Main


class FunctionalTests(TestCase):
    def create_app(self):
        app = Main.app
        app.config['TESTING'] = True
        app.secret_key = 'super secret key'
        app.config['SESSION_TYPE'] = 'filesystem'
        return app

    def test_basic(self):
        client = self.app.test_client()
        response = client.get("http://localhost:7000/accounts")
        all_accounts = response.json

        account_dict = {"nick": "asd", "login": "qwe", "password": hash(123)}
        response = client.post(
            "http://localhost:7000/accounts",
            json=account_dict
        )

        added_account = response.json
        self.assertEqual(account_dict["nick"], added_account["nick"])
        self.assertEqual(account_dict["login"], added_account["login"])
        self.assertEqual(account_dict["password"], added_account["password"])

        all_accounts.append(added_account)

        response = client.get("http://localhost:7000/accounts")

        self.assertEqual(all_accounts, response.json)
