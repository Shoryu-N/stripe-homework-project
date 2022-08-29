import os
import stripe

from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")

if STRIPE_SECRET_KEY is None or STRIPE_PUB_KEY is None:
    raise Exception(
        "You have to add secret key and pub key in your .env file."
    )
else:
    stripe.api_key = STRIPE_SECRET_KEY

app = Flask(
    __name__,
    static_url_path="",
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"),
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/checkout", methods=["GET"])
def checkout():
    title, amount, error = None, None, None
    item_id = request.args.get("item", type=int)

    if item_id < 1 or item_id > 3:
        error = "The item with the given id does not exist"
    else:
        item = _get_item(item_id)
        title, amount = item["title"], item["amount"]

    return render_template("checkout.html", title=title, amount=amount, error=error)

@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    data = request.json
    if data["item"] < 1 or data["item"] > 3:
        return jsonify({"clientSecret": "", "error": "The item with the given id does not exist"})
    else:    
        intent = stripe.PaymentIntent.create(
            amount= _get_item(data["item"])["amount"],
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        return jsonify({"clientSecret": intent["client_secret"], "error":""})

@app.route("/items/<int:id>", methods=["GET"])
def get_item(id):
    if id < 1 or id > 3:
        return jsonify({"error": "The item with the given id does not exist"})    
    return jsonify({"item": _get_item(id)})

@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")

def _get_item(item_id):
    title, amount, img = None, None, None
    if item_id == 1:
        title = "The Art of Doing Science and Engineering"
        amount = 2300
        img = "art-science-eng.jpg"
    elif item_id == 2:
        title = "The Making of Prince of Persia: Journals 1985-1993"
        amount = 2500
        img = "prince-of-persia.jpg"
    elif item_id == 3:
        title = "Working in Public: The Making and Maintenance of Open Source"
        amount = 2800
        img = "working-in-public.jpg"

    return { "title": title, "amount": amount, "img": img } 

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
