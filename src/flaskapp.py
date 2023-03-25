from flask import Flask, render_template, request
import api

app = Flask(__name__)

# GET API VERSION
ver_info_text = api.getVersion()


@app.route("/", methods=["GET"])
def index_get():
    cat_opts = ["200 - 食費", "201 - 生活用品"]
    resultMessage = "入力してください"
    ids, cat_names, prices, dates = api.getRecent()
    return render_template(
        "index.html",
        connectionMessage=ver_info_text,
        resultMessage=resultMessage,
        recent_data=zip(ids, cat_names, prices, dates),
        cat_opts=cat_opts,
    )


@app.route("/post", methods=["POST"])
def index_post():
    # post 処理
    post_category_id, post_price = _extract_post_data()
    if post_price != 0:
        ret = api.post_record(post_category_id, post_price)

    return render_template(
        "post.html",
    )


def _extract_post_data():
    post_category = request.form.getlist("category_selector")

    try:
        post_category_id = int(post_category[0][:3])
    except Exception as e:
        print(e)
        return "", 0

    post_price = request.form.get("pricebox")
    print("post_category_id = {}, post_price = {}".format(post_category_id, post_price))
    return post_category_id, post_price
