from flask import Blueprint

from controllers.progress_controller import ProgressController


progress_bp = Blueprint("progress", __name__)


progress_bp.route("", methods=["GET"])(ProgressController.get_progress)
