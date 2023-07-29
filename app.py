import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, error

import api_request

# Configure application
app = Flask(__name__)
db = SQL("sqlite:///currency.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

flags = api_request.flags()

def flag(symbol):
    for item in flags:
        if item["symbol"] == symbol:
            return item["flag"]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("layout.html", flags=flags)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        if not username:
            return error("Must provide username", 403)

        elif not password:
            return error("Must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return error("Invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        session["base"] = rows[0]["fav"]
        session["base_flag"] = flag(session["base"])
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username:
            return error("Must provide username", 400)

        elif not password:
            return error("Must provide password", 400)

        elif not confirm_password:
            return error("Must confirm password", 400)

        if password != confirm_password:
            return error("Passwords don't match", 400)

        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return error("Username already taken", 400)

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hash)

        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/change", methods=["GET","POST"])
@login_required
def change():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not current_password:
            return error("Must provide current password", 403)

        # Ensure password was submitted
        elif not password:
            return error("Must provide password", 403)

        # Ensure password was submitted
        elif not confirm_password:
            return error("Must confirm password", 403)

        if password != confirm_password:
            return error("Passwords don't match", 403)

        user = db.execute("SELECT * FROM users WHERE id = ?", session.get("user_id"))
        if not check_password_hash(user[0]["hash"], current_password):
            return error("Current password invalid", 403)

        hash = generate_password_hash(password)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user[0]["id"])

        return redirect("/login")

    else:
        return render_template("change.html", flags=flags)


@app.route("/process_selected_item", methods=["POST"])
def process_selected_item():
    if request.method == "POST":
        data = request.json
        selected_item = data.get("selected_item")
        session["base"] = selected_item
        session["base_flag"] = flag(session["base"])
        db.execute("UPDATE users SET fav = ? WHERE id = ?",selected_item,session["user_id"])