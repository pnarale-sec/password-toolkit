
from flask import Blueprint, render_template, request, redirect, session
from hashing import hash_password, verify_password

auth = Blueprint("auth", __name__, template_folder="templates")

# simple memory storage (can upgrade to DB later)
users = {}

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and verify_password(password, users[username]):
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users[username] = hash_password(password)
        return redirect("/login")

    return render_template("register.html")


@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")