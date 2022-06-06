from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route("/")
def root() -> str:
    return "Online!"


def run() -> None:
    app.run(host="0.0.0.0", port=8080)


def keep_alive() -> None:
    Thread(target=run).start()
