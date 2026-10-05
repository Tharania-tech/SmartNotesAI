from database.db import mongo

class UserModel:

    @staticmethod
    def create_user(user_data):
        return mongo.db.users.insert_one(user_data)

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({"email": email})