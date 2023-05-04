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
    fyyear = "2023"
    summary_json = api.get_summary(fyyear)
    income_data, outgoing_data, saving_data, invest_data = _separate_summary_data(
        summary_json
    )

    (
        income_data_sum,
        outgoing_data_sum,
        saving_data_sum,
        invest_data_sum,
        all_pure_sum,
        all_sum,
    ) = _sum_category(income_data, outgoing_data, saving_data, invest_data)

    return render_template(
        "summary.html",
        income_data=income_data,
        outgoing_data=outgoing_data,
        saving_data=saving_data,
        invest_data=invest_data,
        income_data_sum=income_data_sum,
        outgoing_data_sum=outgoing_data_sum,
        saving_data_sum=saving_data_sum,
        invest_data_sum=invest_data_sum,
        all_pure_sum=all_pure_sum,
        all_sum=all_sum,
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


# _separate_summary_data は APIからのレスポンスをカテゴリごとに分類する
def _separate_summary_data(summary_json):
    income_data = []
    outgoing_data = []
    saving_data = []
    invest_data = []

    for r in summary_json:
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


def _sum_category(income_data, outgoing_data, saving_data, invest_data):
    # 集計用のカテゴリ各月合計の配列を返す

    # output: [[4,5,6,7,8,9,10,11,12,1,2,3],all]
    income_data_sum = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0]
    outgoing_data_sum = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0]
    saving_data_sum = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0]
    invest_data_sum = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0]
    all_pure_sum = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0]  # 純粋の額
    all_sum = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0]  # 貯金等調整後の額

    for r in income_data:
        for i in range(12):
            income_data_sum[0][i] += int(r[2][i])
            all_pure_sum[0][i] -= int(r[2][i])
            all_sum[0][i] -= int(r[2][i])
        income_data_sum[1] += int(r[3])
        all_pure_sum[1] -= int(r[3])
        all_sum[1] -= int(r[3])

    for r in outgoing_data:
        for i in range(12):
            outgoing_data_sum[0][i] += int(r[2][i])
            all_pure_sum[0][i] -= int(r[2][i])
            all_sum[0][i] -= int(r[2][i])
        outgoing_data_sum[1] += int(r[3])
        all_pure_sum[1] -= int(r[3])
        all_sum[1] -= int(r[3])

    for r in saving_data:
        for i in range(12):
            saving_data_sum[0][i] += int(r[2][i])
            all_pure_sum[0][i] -= int(r[2][i])
        saving_data_sum[1] += int(r[3])
        all_pure_sum[1] -= int(r[3])

    for r in invest_data:
        for i in range(12):
            invest_data_sum[0][i] += int(r[2][i])
            all_pure_sum[0][i] -= int(r[2][i])
        invest_data_sum[1] += int(r[3])
        all_pure_sum[1] -= int(r[3])

    return (
        income_data_sum,
        outgoing_data_sum,
        saving_data_sum,
        invest_data_sum,
        all_pure_sum,
        all_sum,
    )
