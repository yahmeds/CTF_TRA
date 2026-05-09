import base64
import time

from flask import Flask, Response, make_response, render_template, session

app = Flask(__name__)

SECRET_KEY = "k4m4l_dev_2024"
app.secret_key = SECRET_KEY


@app.after_request
def set_telemetry(resp):
    encoded_key = base64.b64encode(SECRET_KEY.encode()).decode()
    ts = int(time.time())
    resp.set_cookie("_ks", f"1.7f3e9a.{encoded_key}.{ts}", max_age=60 * 60 * 24 * 30)
    resp.headers.add("Link", '</login>; rel="login"')
    return resp


@app.route("/")
def index():
    resp = make_response(render_template("index.html"))
    resp.headers["X-Trace"] = "traces{h3ad3rs_t3ll_st0r13s}"
    return resp


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
        "read the wire."
    )
    payload = base64.b64encode(cleartext.encode()).decode()
    return render_template("archive.html", payload=payload)


@app.route("/login")
def login():
    session["role"] = "guest"
    session["user"] = "anon"
    return render_template("login.html", user=session["user"], role=session["role"])


@app.route("/admin/inbox")
def admin_inbox():
    if session.get("role") != "admin":
        return Response("forbidden\n", status=403, mimetype="text/plain")
    return render_template("inbox.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)