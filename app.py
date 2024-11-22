from flask import Flask, render_template, request, jsonify, redirect, url_for
import stripe

app = Flask(__name__)

# Configure Stripe API keys
stripe.api_key = "sk_test_your_secret_key"  # Replace with your Stripe Secret Key
STRIPE_PUBLIC_KEY = "pk_test_your_public_key"  # Replace with your Stripe Public Key

# Sample Products
PRODUCTS = [
    {"id": 1, "name": "Product A", "price": 1000, "currency": "usd"},  # Price in cents
    {"id": 2, "name": "Product B", "price": 1500, "currency": "usd"},
    {"id": 3, "name": "Product C", "price": 2000, "currency": "usd"},
]


@app.route("/")
def home():
    """Homepage listing products."""
    return render_template("index.html", products=PRODUCTS, stripe_public_key=STRIPE_PUBLIC_KEY)


@app.route("/checkout", methods=["POST"])
def checkout():
    """Checkout route to create a payment intent."""
    try:
        data = request.get_json()
        product_id = data.get("product_id")
        product = next((p for p in PRODUCTS if p["id"] == product_id), None)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=product["price"],
            currency=product["currency"],
            payment_method_types=["card"],
        )
        return jsonify({"client_secret": intent["client_secret"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
