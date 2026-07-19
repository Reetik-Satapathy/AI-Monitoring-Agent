from time import time

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    g
)

from config import Config
from models import mysql, save_contact

EXCLUDED_PATHS = {"/metrics", "/health"}

from metrics import (
    homepage_visits,
    contact_submissions,
    invalid_contact_submissions,
    http_requests,
    request_duration,
    active_requests,
    database_inserts,
    database_insert_failures,
    database_insert_duration
)

from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

mysql.init_app(app)


# =====================================================
# Request Hooks
# =====================================================

@app.before_request
def before_request():
    if request.path in EXCLUDED_PATHS:
        return

    g.start_time = time()
    active_requests.inc()


@app.after_request
def after_request(response):
    if request.path in EXCLUDED_PATHS:
        return response

    active_requests.dec()

    request_duration.labels(
        request.method,
        request.path
    ).observe(time() - g.start_time)

    http_requests.labels(
        request.method,
        request.path,
        response.status_code
    ).inc()

    return response

# @app.teardown_request
# def teardown_request(exception):
#     if request.path in EXCLUDED_PATHS:
#         return

#     if hasattr(g, "start_time"):
#         try:
#             active_requests.dec()
#         except ValueError:
#             # Prevent the gauge from going below zero
#             pass


# =====================================================
# Routes
# =====================================================

@app.route("/")
def home():

    homepage_visits.inc()

    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    message = request.form["message"].strip()

    if not name or not email or not message:

        invalid_contact_submissions.inc()

        flash("All fields are required.")

        return redirect(url_for("home"))

    try:

        start = time()

        save_contact(name, email, message)

        database_insert_duration.observe(
            time() - start
        )

        database_inserts.inc()

        contact_submissions.inc()

        flash("Request stored successfully.")

    except Exception:

        database_insert_failures.inc()

        flash("Failed to store request.")

    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )