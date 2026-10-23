"""Bean & Brew - a small cafe website built with Flask."""

import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MENU = [
    {"id": 1, "name": "Flat White", "price": 3.80, "tag": "Coffee", "desc": "Velvety microfoam over a double ristretto."},
    {"id": 2, "name": "Cold Brew", "price": 4.20, "tag": "Coffee", "desc": "Steeped for 18 hours, served over ice."},
    {"id": 3, "name": "Masala Chai", "price": 3.50, "tag": "Tea", "desc": "Slow-simmered with cardamom, ginger and clove."},
    {"id": 4, "name": "Matcha Latte", "price": 4.60, "tag": "Tea", "desc": "Ceremonial-grade matcha with oat milk."},
    {"id": 5, "name": "Almond Croissant", "price": 3.90, "tag": "Bakery", "desc": "Baked every morning, filled with frangipane."},
    {"id": 6, "name": "Banana Bread", "price": 3.20, "tag": "Bakery", "desc": "Warm, with a little brown butter."},
]


@app.get("/")
def home():
    return render_template("index.html", featured=MENU[:3])


@app.get("/menu")
def menu():
    tag = request.args.get("tag", "")
    items = [m for m in MENU if not tag or m["tag"].lower() == tag.lower()]
    return render_template("menu.html", items=items, tag=tag, tags=sorted({m["tag"] for m in MENU}))


@app.get("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    errors, form = {}, {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("name", "email", "message")}
        if not 2 <= len(form["name"]) <= 60:
            errors["name"] = "Please enter your name (2-60 characters)."
        if "@" not in form["email"] or len(form["email"]) > 120:
            errors["email"] = "Please enter a valid email address."
        if not 10 <= len(form["message"]) <= 1000:
            errors["message"] = "Your message should be 10-1000 characters."
        if not errors:
            return render_template("thanks.html", name=form["name"])
    return render_template("contact.html", errors=errors, form=form), (400 if errors else 200)


@app.get("/api/menu")
def api_menu():
    return jsonify(MENU)


@app.get("/health")
def health():
    return jsonify(status="ok", items=len(MENU))


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
