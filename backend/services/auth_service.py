import bcrypt
import jwt
from datetime import datetime, timedelta

from models.user_model import UserModel
from config import Config


class AuthService:

    @staticmethod
    def register(data):

        email = data.get("email", "").strip()
        password = data.get("password", "")
        name = data.get("name", "").strip()

        if not name or not email or not password:
            return {
                "error": "Name, email and password are required"
            }, 400

        if UserModel.get_user_by_email(email):
            return {
                "error": "Email already exists"
            }, 400

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        user = {
            "name": name,
            "email": email,
            "password": hashed_password
        }

        UserModel.create_user(user)

        return {
            "message": "User Registered Successfully"
        }, 201

    @staticmethod
    def login(data):

        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not email or not password:
            return {
                "error": "Email and password are required"
            }, 400

        user = UserModel.get_user_by_email(email)

        if not user:
            return {
                "error": "Invalid email or password"
            }, 401

        stored_password = user["password"]

        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        if not bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):
            return {
                "error": "Invalid email or password"
            }, 401

        user_id = str(user.get("_id", user.get("id", "")))

        # Create JWT token
        token_payload = {
            "user_id": user_id,
            "email": user.get("email", ""),
            "name": user.get("name", ""),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        token = jwt.encode(
            token_payload,
            Config.SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user_id,
                "name": user.get("name", ""),
                "email": user.get("email", "")
            }
        }, 200