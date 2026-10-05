import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/smartnotes_ai")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_MB", "25")) * 1024 * 1024
