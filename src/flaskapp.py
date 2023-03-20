from flask import Flask, render_template, request
import api

app = Flask(__name__)

# GET API VERSION
ver_info_text = api.getVersion()


@app.route("/")
def index():
    id, cat_name, price, date = api.getRecent()

    cat_opts = ["200 - 食費", "201 - 生活用品"]

    recent_data = api.getRecent()
    return render_template(
        "index.html",
        connectionMessage=ver_info_text,
        resultMessage="ここに送信結果が出ることになっています",
        recent_data=zip(id, cat_name, price, date),
        cat_opts=cat_opts,
    )
