from flask import Flask, render_template, request
import api

app = Flask(__name__)


@app.route("/")
def index():
    # GET FROM MAWINTER-API
    mes = api.getBase()
    return render_template(
        "index.html",
        connectionMessage="ここにAPIサーバとの接続状態が表示されます",
        resultMessage="ここに送信結果が出ることになっています",
    )
