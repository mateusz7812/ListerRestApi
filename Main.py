from multiprocessing import Process

from flask import Flask, request, make_response
from flask.json import jsonify

import DataBases.MongoDB

app = Flask(__name__)

account_db = DataBases.MongoDB.MongoDB("accounts", {"id", "nick", "login", "password"})


@app.route('/accounts/<string:account_id>', methods=["GET", "PUT", "DELETE"])
def account(account_id):
    account_dicts = account_db.select({"id": account_id})
    if not account_dicts:
        return make_response(jsonify({"error": "account not found"}), 404)

    if request.method == "GET":
        return make_response(jsonify(account_dicts[0]), 200)
    elif request.method == "PUT":
        return account_put_handle(account_id)
    elif request.method == "DELETE":
        return account_delete_handle(account_id)
    return make_response(jsonify({}), 405)


def account_put_handle(account_id):
    account_updated_data_dict = request.json

    bad_columns = list(set(account_updated_data_dict) - account_db.columns)
    if bad_columns:
        return make_response(jsonify({"error": str(bad_columns) + " columns not found"}), 400)

    update_result = account_db.update({"id": account_id}, account_updated_data_dict)
    if not update_result:
        return make_response(jsonify({"error": "database failure"}), 500)
    return make_response(jsonify(update_result), 200)


def account_delete_handle(account_id):
    delete_result = account_db.delete({"id": account_id})
    if not delete_result:
        return make_response(jsonify({"error": "database failure"}), 500)
    return make_response('', 204)


@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    if request.method == "GET":
        return accounts_get_handle()
    elif request.method == "POST":
        return accounts_post_handle()
    return make_response(jsonify({}), 405)


def accounts_post_handle():
    account_data_dict = request.json

    bad_columns = list(set(account_data_dict) - account_db.columns)
    if bad_columns:
        return make_response(jsonify({"error": str(bad_columns) + " columns not found"}), 400)

    if 'id' in list(account_data_dict.keys()):
        return make_response(jsonify({"error": "id in account data dict"}), 400)

    insert_result = account_db.insert(account_data_dict)

    if not insert_result:
        return make_response(jsonify({"error": "database failure"}), 500)

    return make_response(jsonify(insert_result), 201)


def accounts_get_handle():
    account_dicts = account_db.select({})
    response_content = jsonify(account_dicts)
    return make_response(response_content, 200)


server = None


def _run():
    app.run(port=7000)


def run():
    global server
    server = Process(target=_run)
    server.start()


def stop():
    global server
    if server:
        server.terminate()
        server = None


if __name__ == '__main__':
    run()
