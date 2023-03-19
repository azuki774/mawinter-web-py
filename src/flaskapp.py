from flask import Flask, render_template, request
import api
import generate

app = Flask(__name__)

# GET API VERSION
ver_info_text = api.getVersion()


@app.route("/")
def index():
    # IT IS DUMMY
    id = [5, 4, 3, 2, 1]
    cat_name = ["食費", "食費", "食費", "食費", "食費"]
    price = [1000, 2000, 3000, 4000, 5000]
    date = ["2023-03-01", "2023-03-01", "2023-03-01", "2023-03-01", "2023-03-01"]
    cat_opts = ["200 - 食費", "201 - 生活用品"]

    return render_template(
        "index.html",
        connectionMessage=ver_info_text,
        resultMessage="ここに送信結果が出ることになっています",
        recent_data=zip(id, cat_name, price, date),
        cat_opts=cat_opts,
    )
