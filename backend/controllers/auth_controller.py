from flask import request, jsonify

from services.auth_service import AuthService


class AuthController:

    @staticmethod
    def register():
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        response, status = AuthService.register(data)

        return jsonify(response), status

    @staticmethod
    def login():
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        response, status = AuthService.login(data)

        return jsonify(response), status