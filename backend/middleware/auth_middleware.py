from functools import wraps
from flask import request, jsonify, g
import jwt

from config import Config


def token_required(view_func):
    """Require a valid Bearer JWT and expose its payload as request.user."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")

        if not header.startswith("Bearer "):
            return jsonify({"error": "Authentication required"}), 401

        token = header.split(" ", 1)[1].strip()

        if not token:
            return jsonify({"error": "Authentication required"}), 401

        try:
            payload = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Session expired. Please login again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid authentication token"}), 401

        request.user = payload
        g.user = payload
        return view_func(*args, **kwargs)

    return wrapped
