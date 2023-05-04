from flask import Flask, render_template, request, redirect, url_for
import api
from pythonjsonlogger import jsonlogger
import logging

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


@app.route("/post", methods=["GET", "POST"])
def index_post():
    if request.method == "GET":
        return redirect(url_for("index.html"))

    # post 処理
    post_category_id, post_price = _extract_post_data(request=request)
    if post_price != 0:
        ret = api.post_record(post_category_id, post_price)

    return render_template(
        "post.html",
    )


@app.route("/summary", methods=["GET"])
def summary_get():
    return render_template(
        "summary.html",
    )


def _extract_post_data(request):
    post_category = request.form.getlist("category_selector")

    try:
        post_category_id = int(post_category[0][:3])
        post_price = int(request.form.get("pricebox"))
    except Exception as e:
        logger.error(e)
        return 0, 0

    logger.info(
        "post_category_id = {}, post_price = {}".format(post_category_id, post_price)
    )
    return post_category_id, post_price
