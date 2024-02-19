#!/usr/bin/env python3
"""Module contais a flask app"""
from flask import Flask, jsonify, make_response, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
