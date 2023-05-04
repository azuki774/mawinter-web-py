import os
import requests
from requests.auth import HTTPBasicAuth
import datetime
from pythonjsonlogger import jsonlogger
import logging

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)

# BASE_URL = str(os.getenv("BASE_URL", "http://192.168.1.21:8080"))
# BASIC_AUTH_USER = str(os.getenv("BASIC_AUTH_USER", ""))
# BASIC_AUTH_PASS = str(os.getenv("BASIC_AUTH_PASS", ""))
BASE_URL = str(os.getenv("BASE_URL", "https://jinx-stg.azuki.blue/mawinter"))
BASIC_AUTH_USER = str(os.getenv("BASIC_AUTH_USER", "user"))
BASIC_AUTH_PASS = str(os.getenv("BASIC_AUTH_PASS", "ahri"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
    json_ensure_ascii=False,
)
h.setFormatter(json_fmt)
logger.addHandler(h)


def getVersion():
    url = BASE_URL + "/version"
    try:
        response = requests.get(
            url, auth=HTTPBasicAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS)
        )

        if response.status_code != 200:
            logger.warn(response.status_code)
            return "有効でないステータスコード"
        json_data = response.json()
    except Exception as e:
        logger.error(e)
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
            logger.warn(response.status_code)
            return [], [], [], []

        # ok pattern
        json_data = response.json()
    except Exception as e:
        logger.error(e)
        return ids, cat_names, prices, dates

    # reshape
    logger.info("recent fetch ok")

    if json_data == None:
        return [], [], [], []

    for jdata in json_data:
        ids.append(jdata["id"])
        cat_names.append(jdata["category_name"])
        prices.append(jdata["price"])
        dates.append(jdata["datetime"])

    return ids, cat_names, prices, dates


def post_record(category_id, price):
    logger.info("post record called")
    url = BASE_URL + "/v2/record"
    logger.info("url = {}".format(url))
    data = (
        "{"
        + '"category_id": {}, "from": "mawinter-web", "price": {}'.format(
            category_id, price
        )
        + "}"
    )
    logger.info(data)
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            url,
            auth=HTTPBasicAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS),
            data=data,
            headers=headers,
        )
        if response.status_code != 201:
            print("unexpected code: {}".format(response.status_code))
            return 1

        # ok pattern
        json_data = response.json()
    except Exception as e:
        logger.error(e)
        return 1

    logger.info("post ok")
    return 0


def get_summary(fyyear):
    logger.info("get summary called")
    url = BASE_URL + "/v2/record/summary/" + fyyear
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS),
        )
    except Exception as e:
        logger.error(e)
        return None

    summary_json = response.json()
    logger.info("get summary ok")
    return summary_json
