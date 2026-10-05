from flask import Blueprint

from controllers.auth_controller import AuthController


auth_bp = Blueprint("auth", __name__)


# Register
auth_bp.route(
    "/register",
    methods=["POST"]
)(AuthController.register)


# Login
auth_bp.route(
    "/login",
    methods=["POST"]
)(AuthController.login)