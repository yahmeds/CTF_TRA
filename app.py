import base64

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


@app.route("/private/archive")
def archive():
    cleartext = (
        "Reminder to self: base64 is not encryption. "
        "If you can read this, you already knew that. "
        "traces{b4s3_s1xty_f0ur_1s_n0t_crypt0}"
    )
    payload = base64.b64encode(cleartext.encode()).decode()
    return render_template("archive.html", payload=payload)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)