from flask import Flask, render_template, request
import api
import generate

app = Flask(__name__)


@app.route("/")
def index():
    # GET FROM MAWINTER-API
    mes = api.getBase()
    alphabet = ["A", "B", "C", "D", "E"]
    no = ["One", "Two", "Three", "Four", "Five"]

    return render_template(
        "index.html",
        connectionMessage="ここにAPIサーバとの接続状態が表示されます",
        resultMessage="ここに送信結果が出ることになっています",
        data=zip(alphabet, no),
    )
