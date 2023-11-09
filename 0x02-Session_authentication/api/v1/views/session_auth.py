#!/usr/bin/env python3
""" Session authentication view module"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles user login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400

    if password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        user_id = user[0].id
        session_id = auth.create_session(user_id)

        out = jsonify(user[0].to_json())
        out.set_cookie(getenv('SESSION_NAME'), session_id)
        return out
