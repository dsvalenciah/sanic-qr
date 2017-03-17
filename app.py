# bultin library
import datetime
from uuid import uuid4

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
        host = request.headers.get('Host')
        url = pyqrcode.create(f"{host}/login?token={token}")
        url.svg(f"static/temp_img/{token}.svg", scale=8)
        template = env.get_template("sign_up.html")
        html_content = template.render(token=token)
        return html(html_content)


@app.route("/login", methods=["GET", "POST"])
async def login(request):
    if request.method == "GET":
        template = env.get_template("login.html")
        html_content = template.render()
        return html(html_content)
    elif request.method == "POST":
        session = CRUD.login_user(
            email_or_name=request.form.get("email_or_name", ""),
            password=request.form.get("password", ""),
            expires=datetime.datetime.now() + datetime.timedelta(seconds=10)
        )
        if session:
            response = redirect(app.url_for('home'))
            response.cookies['Token'] = session.token
            response.cookies['Token']['max-age'] = (
                session.expires - datetime.datetime.now()
            ).total_seconds()
            return response
        else:
            return text(':(')


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
