from flask import Blueprint

from controllers.note_controller import NoteController
from middleware.auth_middleware import token_required


note_bp = Blueprint("notes", __name__)


@note_bp.route("", methods=["GET"])
@token_required
def get_notes():
    return NoteController.get_notes()


@note_bp.route("/upload", methods=["POST"])
@token_required
def upload_note():
    return NoteController.upload_note()


@note_bp.route("/<note_id>", methods=["GET"])
@token_required
def get_note(note_id):
    return NoteController.get_note(note_id)


@note_bp.route("/<note_id>/summarize", methods=["POST"])
@token_required
def summarize_note(note_id):
    return NoteController.summarize_note(note_id)


@note_bp.route("/<note_id>/keywords", methods=["POST"])
@token_required
def extract_keywords(note_id):
    return NoteController.extract_keywords(note_id)


@note_bp.route("/<note_id>/flashcards", methods=["POST"])
@token_required
def generate_flashcards(note_id):
    return NoteController.generate_flashcards(note_id)


@note_bp.route("/<note_id>/quiz", methods=["POST"])
@token_required
def generate_quiz(note_id):
    return NoteController.generate_quiz(note_id)


@note_bp.route("/<note_id>/chat", methods=["POST"])
@token_required
def chat_with_note(note_id):
    return NoteController.chat_with_note(note_id)


@note_bp.route("/<note_id>/quiz/submit", methods=["POST"])
@token_required
def submit_quiz(note_id):
    return NoteController.submit_quiz(note_id)


@note_bp.route("/<note_id>", methods=["DELETE"])
@token_required
def delete_note(note_id):
    return NoteController.delete_note(note_id)
