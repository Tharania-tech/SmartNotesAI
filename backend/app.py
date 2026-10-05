from flask import Flask
from flask_cors import CORS
from datetime import datetime, timezone

from config import Config
from database.db import mongo
from routes.auth_routes import auth_bp
from routes.note_routes import note_bp
from routes.chat_routes import chat_bp
app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "*"}})
mongo.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(
    note_bp,
    url_prefix="/api/notes"
)
app.register_blueprint(chat_bp, url_prefix="/api")


@app.route("/api/health", methods=["GET"])
def health():
    try:
        mongo.cx.admin.command("ping")
        return {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, 200
    except Exception as exc:
        return {
            "status": "degraded",
            "database": "disconnected",
            "error": str(exc),
        }, 503

@app.route("/")
def home():
    try:
        mongo.cx.admin.command("ping")
        return {
            "message": "SmartNotes AI Backend Running",
            "database": "MongoDB Connected Successfully"
        }
    except Exception as e:
        return {
            "message": "Backend Running",
            "database": "MongoDB Connection Failed",
            "error": str(e)
        }, 500

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])