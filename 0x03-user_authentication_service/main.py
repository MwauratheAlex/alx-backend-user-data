#!/usr/bin/env python3
"""End to end integration test for authentication service"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test register user"""
    res = requests.post(
        f'{URL}/users', data={'email': email, 'password': password})
    assert res.status_code == 200
    assert res.json().get('email') == email
    assert res.json().get('message') == 'user created'
    print("test success: register user")


def log_in_wrong_password(email: str, password: str) -> None:
    """test log in with wrong password"""
    res = requests.post(
        f"{URL}/sessions", data={'email': email, 'password': password})
    assert res.status_code == 401
    print("test success: login with wrong password")


def log_in(email: str, password: str) -> str:
    """Test log in with correct password"""
    res = requests.post(
        f"{URL}/sessions", data={'email': email, 'password': password})
    assert res.status_code == 200
    assert res.json().get('email') == email
    assert res.json().get('message') == "logged in"
    session_id = res.cookies.get('session_id', None)
    assert session_id is not None
    print("test success: login with correct email and password")
    return session_id


def profile_unlogged() -> None:
    """Test get profile while not logged in"""
    res = requests.get(
        f"{URL}/profile")
    assert res.status_code == 403
    print("test success: get profile while not logged in")


def profile_logged(session_id: str) -> None:
    """Test get profile while logged in"""
    res = requests.get(
        f"{URL}/profile", cookies={'session_id': session_id})
    assert res.status_code == 200
    assert res.json().get('email') == EMAIL
    print("test success: get profile while logged in")


def log_out(session_id: str) -> None:
    """Test log out"""
    res = requests.delete(
        f"{URL}/sessions", cookies={'session_id': session_id})
    assert res.status_code == 200
    assert res.json().get('message') == 'Bienvenue'
    print("test success: log out")


def reset_password_token(email: str) -> str:
    """Test get reset password  token"""
    res = requests.post(
        f"{URL}/reset_password", data={'email': email})
    assert res.status_code == 200
    assert res.json().get('email') == email
    reset_token = res.json().get('reset_token', None)
    assert reset_token is not None
    print("test success: get reset password token")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update password"""
    res = requests.put(
        f"{URL}/reset_password",
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        }
    )
    assert res.status_code == 200
    assert res.json().get('email') == email
    assert res.json().get('message') == 'Password updated'
    print("test success: update password")


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
