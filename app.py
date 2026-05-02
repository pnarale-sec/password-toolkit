from flask import Flask, render_template, request, redirect, session
import os

from hashing import hash_password
from policy import password_policy
from encryption import derive_key, encrypt_message, decrypt_message
from bruteforce import brute_force_simple
from dictionary_attack import dictionary_attack

app = Flask(__name__)
app.secret_key = "cybertoolkit"


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        return redirect("/dashboard")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template("index.html")


# ---------------- PASSWORD MODULE ----------------
@app.route("/password", methods=["GET", "POST"])
def password():
    if "user" not in session:
        return redirect("/")

    result = None

    if request.method == "POST":
        pwd = request.form.get("password")

        if pwd:
            result = {
                "policy": password_policy(pwd),
                "hash": hash_password(pwd)
            }

    return render_template("password.html", result=result)


# ---------------- ENCRYPTION MODULE ----------------
@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if "user" not in session:
        return redirect("/")

    result = None

    if request.method == "POST":
        password = request.form.get("password")
        message = request.form.get("message")

        if password and message:
            salt = os.urandom(16)
            key = derive_key(password, salt)

            encrypted = encrypt_message(message, key)
            decrypted = decrypt_message(encrypted, key)

            result = {
                "encrypted": encrypted,
                "decrypted": decrypted
            }

    return render_template("encrypt.html", result=result)


# ---------------- BRUTE FORCE MODULE ----------------
@app.route("/brute", methods=["GET", "POST"])
def brute():
    if "user" not in session:
        return redirect("/")

    result = None

    if request.method == "POST":
        password = request.form.get("password")

        if password:
            hashed = hash_password(password)
            result = brute_force_simple(hashed, "abc123", 4)

    return render_template("brute.html", result=result)


# ---------------- DICTIONARY ATTACK MODULE ----------------
@app.route("/dictionary", methods=["GET", "POST"])
def dictionary():
    if "user" not in session:
        return redirect("/")

    result = None

    if request.method == "POST":
        password = request.form.get("password")

        if password:
            hashed = hash_password(password)
            result = dictionary_attack(hashed, "wordlist.txt")

    return render_template("dictionary.html", result=result)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)