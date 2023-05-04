from flask import Flask, render_template, request, redirect, url_for
import api
from pythonjsonlogger import jsonlogger
import logging
import json

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
    income_data, outgoing_data, saving_data, invest_data = _extract_summary_data(None)
    return render_template(
        "summary.html",
        income_data=income_data,
        outgoing_data=outgoing_data,
        saving_data=saving_data,
        invest_data=invest_data,
    )


# _extract_post_data は request をもとに、record を POSTするための整形処理
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


def _extract_summary_data(request):
    res = '[{"category_id":100,"category_name":"月給","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":101,"category_name":"ボーナス","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":110,"category_name":"雑所得","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":200,"category_name":"家賃","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":210,"category_name":"食費","count":2,"price":[0,1567,0,0,0,0,0,0,0,0,0,0],"total":1567},{"category_id":220,"category_name":"電気代","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":221,"category_name":"ガス代","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":222,"category_name":"水道費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":230,"category_name":"コンピュータリソース","count":2,"price":[0,268,0,0,0,0,0,0,0,0,0,0],"total":268},{"category_id":231,"category_name":"通信費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":240,"category_name":"生活用品","count":1,"price":[0,4444,0,0,0,0,0,0,0,0,0,0],"total":4444},{"category_id":250,"category_name":"娯楽費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":251,"category_name":"交遊費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":260,"category_name":"書籍・勉強","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":270,"category_name":"交通費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":280,"category_name":"衣服等費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":300,"category_name":"保険・税金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":400,"category_name":"医療・衛生","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":500,"category_name":"雑費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":600,"category_name":"家賃用貯金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":601,"category_name":"PC用貯金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":700,"category_name":"NISA入出金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":701,"category_name":"NISA変動","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0}]'
    income_data = []
    outgoing_data = []
    saving_data = []
    invest_data = []

    # resjson = res.json()
    resjson = json.loads(res)
    for r in resjson:
        cat_id = r["category_id"]
        cat_name = r["category_name"]
        price = r["price"]
        total = r["total"]
        if cat_id in [100, 101, 110]:
            income_data.append([cat_id, cat_name, price, total])
        elif cat_id in [600, 601]:
            saving_data.append([cat_id, cat_name, price, total])
        elif cat_id in [700, 701]:
            invest_data.append([cat_id, cat_name, price, total])
        else:
            outgoing_data.append([cat_id, cat_name, price, total])

    return income_data, outgoing_data, saving_data, invest_data
