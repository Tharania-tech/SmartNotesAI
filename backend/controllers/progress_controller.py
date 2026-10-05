from flask import jsonify

from models.progress_model import ProgressModel


class ProgressController:

    @staticmethod
    def get_progress():
        try:
            # Keep this consistent with the current NoteController implementation.
            # Replace this with the authenticated user id when auth middleware is enabled.
            user_id = "test_user"

            data = ProgressModel.get_dashboard_data(user_id)

            return jsonify(data), 200

        except Exception as error:
            print("PROGRESS CONTROLLER ERROR:", str(error))
            return jsonify({
                "error": "Unable to load learning progress",
                "details": str(error),
            }), 500
