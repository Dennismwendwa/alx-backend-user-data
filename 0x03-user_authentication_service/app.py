#!/usr/bin/env python3
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


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


@app.route("/sessions", methods=["POST", "DELETE"], strict_slashes=False)
def login_logout():
    """This route is for user login"""
    if request.method == "POST":
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
    elif request.method == "DELETE":
        """This route logout users"""
        session_id = request.cookies.get("session_id")

        try:
            user = AUTH.get_user_from_session_id(session_id)
            if user is not None:
                AUTH.destroy_session(user.id)
                return redirect("/")
            abort(403)
        except Exception as e:
            abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """This route is for user profile"""
    session_id = request.cookies.get("session_id")

    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            response_data = {"email": user.email}
            return jsonify(response_data), 200
        else:
            abort(403)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """This route is for reseting password"""
    email = request.form.get("email")
    try:
        user = AUTH._db.find_user_by(email=email)
        rest_token = AUTH.get_reset_password_token(email)
        response = make_response(
            jsonify({"email": user.email, "reset_token": rest_token}))
        return response
    except NoResultFound:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def reset_password():
    """This route reset the user password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        response_data = {"email": email, "message": "Password updated"}
        return jsonify(response_data), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
