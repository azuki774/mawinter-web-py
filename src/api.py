import os
import requests
from requests.auth import HTTPBasicAuth
import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)

BASE_URL = str(os.getenv("BASE_URL", "http://192.168.1.21:8080"))
BASIC_AUTH_USER = str(os.getenv("BASIC_AUTH_USER", ""))
BASIC_AUTH_PASS = str(os.getenv("BASIC_AUTH_PASS", ""))


def getVersion():
    url = BASE_URL + "/version"
    try:
        response = requests.get(
            url, auth=HTTPBasicAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS)
        )

        if response.status_code != 200:
            print(response.status_code)
            return "有効でないステータスコード"
        json_data = response.json()
    except Exception as e:
        print(e)
        return "接続エラー"

    return "API Version: {}, Revision: {}".format(
        json_data["version"], json_data["revision"]
    )


def getRecent():
    ids = []
    cat_names = []
    prices = []
    dates = []

    # yyyymm = "200007"  # test
    yyyymm = now.strftime("%Y%m")
    url = BASE_URL + "/v2/record/" + yyyymm + "/recent"
    try:
        response = requests.get(
            url, auth=HTTPBasicAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS)
        )
        if response.status_code != 200:
            print(response.status_code)
            return [], [], [], []

        # ok pattern
        json_data = response.json()
    except Exception as e:
        print(e)
        return ids, cat_names, prices, dates

    # reshape
    print("recent fetch ok")

    if json_data == None:
        return [], [], [], []

    for jdata in json_data:
        ids.append(jdata["id"])
        cat_names.append(jdata["category_name"])
        prices.append(jdata["price"])
        dates.append(jdata["datetime"])

    return ids, cat_names, prices, dates


def post_record(category_id, price):
    print("post record called")
    url = BASE_URL + "/v2/record"
    data = (
        "{"
        + '"category_id": {}, "from": "mawinter-web", "price": {}'.format(
            category_id, price
        )
        + "}"
    )
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=data, headers=headers)
    try:
        response = requests.post(
            url, auth=HTTPBasicAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS)
        )
        if response.status_code != 201:
            return 1

        # ok pattern
        json_data = response.json()
    except Exception as e:
        print(e)
        return 1

    print("post ok")
    return 0
