from flask import (
    Flask,
    request,
)
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from calculator.calculator import Calculator

app = Flask(__name__)

sentry_sdk.init(
    dsn="https://cfebadc1abce42949ffea57f12343aa5@o1420511.ingest.sentry.io/4505113561399296",
    integrations=[
        FlaskIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

app = Flask(__name__)


@app.route("/api/add", methods=["POST"])
def add():
    return operation("add", 2)


@app.route("/api/subtract", methods=["POST"])
def subtract():
    return operation("subtract", 2)


@app.route("/api/multiply", methods=["POST"])
def multiply():
    return operation("multiply", 2)


@app.route("/api/divide", methods=["POST"])
def divide():
    return operation("divide", 2)


@app.route("/debug-sentry")
def trigger_error():
    division_by_zero = 1 / 0


@app.route("/error")
def oops():
    Calculator.explode(1, 0)


def operation(method, num_factors):
    factors = []
    if num_factors == 2:
        factors.append(float(request.json.get("x")))
        factors.append(float(request.json.get("y")))

    return str(getattr(Calculator, method)(*factors))


app.run(host="0.0.0.0", port=8080)
