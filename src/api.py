import os
import requests

BASE_URL = str(os.getenv("BASE_URL", "http://192.168.1.21:8080/"))


def getBase():
    url = BASE_URL
    response = requests.get(url)
    return response.text
