from flask import Flask, render_template, request
import api
import generate

app = Flask(__name__)


@app.route("/")
def index():
    # GET FROM MAWINTER-API
    mes = api.getBase()

    # IT IS DUMMY
    connectionMessage = "ver hoge"
    id = [5, 4, 3, 2, 1]
    cat_name = ["食費", "食費", "食費", "食費", "食費"]
    price = [1000, 2000, 3000, 4000, 5000]
    date = ["2023-03-01", "2023-03-01", "2023-03-01", "2023-03-01", "2023-03-01"]
    cat_opts = ["200 - 食費", "201 - 生活用品"]

    return render_template(
        "index.html",
        connectionMessage=connectionMessage,
        resultMessage="ここに送信結果が出ることになっています",
        recent_data=zip(id, cat_name, price, date),
        cat_opts=cat_opts,
    )
