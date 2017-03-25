# bultin library
import datetime
from uuid import uuid4
import os

# external libraries
from sanic import Sanic
from sanic.response import html, redirect, text
from jinja2 import Environment, PackageLoader
import pyqrcode

env = Environment(
    loader=PackageLoader("app", "templates"),
)

app = Sanic(__name__)

app.static("/static", "./static")

DB = list()


@app.route("/")
async def start(request):
    template = env.get_template("start.html")
    html_content = template.render()
    return html(html_content)


@app.route("/sign_up", methods=["GET", "POST"])
async def sign_up(request, invalid=False):
    if request.method == "GET":
        token = uuid4().hex
        DB.append(token)
        inet_list = [
            z
            for x in os.popen("ifconfig").read().split("\n\n")
            for z in x.split(" ")
            if "inet:" in z
        ]
        host = max(inet_list, key=len).strip("inet:")
        url = pyqrcode.create(f"http://{host}:8000/login?token={token}")
        url.svg(f"static/temp_img/{token}.svg", scale=8)
        template = env.get_template("sign_up.html")
        html_content = template.render(token=token)
        return html(html_content)


@app.route("/login", methods=["GET", "POST"])
async def login(request):
    if request.method == "GET":
        template = env.get_template("login.html")
        if request.args['token'][0] in DB:
            r = "Hola papu como estás"
        else:
            r = "Mucha pedazo de mierda"
        html_content = template.render(r=r)
        return html(html_content)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
