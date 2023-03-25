from flask import Flask, render_template, request
import api

app = Flask(__name__)

# GET API VERSION
ver_info_text = api.getVersion()

cat_opts = [
    "210 - 食費",
    "230 - コンピュータリソース",
    "231 - 通信費",
    "240 - 生活用品",
    "250 - 娯楽費",
    "251 - 交友費",
    "260 - 書籍・勉強",
    "270 - 交通費",
    "280 - 衣服等",
    "220 - 電気代",
    "221 - ガス代",
    "222 - 水道代",
    "300 - 保険・税金",
    "400 - 医療・衛生",
    "500 - 雑費",
    "100 - 給与",
    "101 - ボーナス",
    "110 - 雑所得",
    "600 - 家賃用貯金",
    "601 - PC用貯金",
    "700 - NISA入出金",
    "701 - NISA変動",
]


@app.route("/", methods=["GET"])
def index_get():
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
