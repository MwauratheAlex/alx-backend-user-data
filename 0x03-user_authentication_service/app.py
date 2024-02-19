#!/usr/bin/env python3
"""Module contais a flask app"""
from flask import Flask, jsonify, make_response, redirect, request, abort
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """GET /"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """POST /users"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not (email and password):
        return jsonify({'error': 'email and password are required'}), 400
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """POST /sessions"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not (email and password):
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    if session_id:
        response.set_cookie('session_id', session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """DELETE /sessions"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(location="/")


@app.route("/profile", methods=["GET"])
def profile():
    """GET /profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """POST /reset_password"""
    email = request.form.get("email")
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(
            {"email": email, "reset_token": reset_token})
    except Exception:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """PUT /reset_password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if not (email and reset_token and new_password):
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
