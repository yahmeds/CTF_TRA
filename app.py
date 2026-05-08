from flask import Flask, Response, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/robots.txt")
def robots():
    body = "User-agent: *\nDisallow: /private/draft-2024-11-09\n"
    return Response(body, mimetype="text/plain")


@app.route("/private/draft-2024-11-09")
def hidden_draft():
    return render_template("draft.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)