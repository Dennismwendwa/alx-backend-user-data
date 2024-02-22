#!/usr/bin/env python3
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """This is the home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_users():
    """This route register new users"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """This route is for user login"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)

            response = make_response(
                jsonify({"email": email, "message": "logged in"}))
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)
    except Exception:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
