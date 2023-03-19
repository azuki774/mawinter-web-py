import os
import requests
from requests.auth import HTTPBasicAuth

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
