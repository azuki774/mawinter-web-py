from flask import Flask, render_template, request
import api

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", message="not sent")


@app.route("/post", methods=["POST"])
def post():
    # GET FROM MAWINTER-API
    mes = api.getBase()
    return render_template("index.html", message=mes)
