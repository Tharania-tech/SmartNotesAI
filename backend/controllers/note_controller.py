from flask import request, jsonify

from models.note_model import NoteModel

from services.note_service import NoteService
from services.ocr_correction_service import correct_ocr_text

class NoteController:

    @staticmethod
    def _owned_note(note_id):
        note = NoteModel.get_note_by_id(note_id)
        if not note:
            return None, (jsonify({"error": "Note not found"}), 404)

        user_id = str(request.user.get("user_id", ""))
        if str(note.get("user_id", "")) != user_id:
            return None, (jsonify({"error": "Note not found"}), 404)

        return note, None

    @staticmethod
    def get_note(note_id):
        note, error = NoteController._owned_note(note_id)
        if error:
            return error

        return jsonify({
            "note": {
                "note_id": str(note.get("_id")),
                "title": note.get("title", "Untitled Note"),
                "filename": note.get("filename", ""),
                "file_type": note.get("file_type", ""),
                "summary": note.get("summary", ""),
                "keywords": note.get("keywords", []),
                "flashcards": note.get("flashcards", []),
                "quiz": note.get("quiz", []),
                "created_at": note.get("created_at"),
            }
        }), 200

    # =========================================================
    # GET NOTES
    # =========================================================

    @staticmethod
    def get_notes():

        try:

            user_id = str(request.user.get("user_id", ""))

            notes = NoteService.get_notes(
                user_id
            )

            return jsonify({
                "notes": notes
            }), 200

        except Exception as e:

            print(
                "GET NOTES ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to get notes",
                "details": str(e)
            }), 500

    # =========================================================
    # UPLOAD NOTE
    # =========================================================

    @staticmethod
    def upload_note():

        try:

            if "file" not in request.files:

                return jsonify({
                    "error": "No file provided"
                }), 400

            file = request.files["file"]

            if not file or not file.filename:

                return jsonify({
                    "error": "No file selected"
                }), 400

            user_id = str(request.user.get("user_id", ""))

            title = request.form.get("title", "").strip()

            response, status = (
                NoteService.save_note(
                    file,
                    user_id,
                    title
                )
            )

            return jsonify(
                response
            ), status

        except Exception as e:

            print(
                "UPLOAD NOTE ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to upload note",
                "details": str(e)
            }), 500

    # =========================================================
    # DELETE NOTE
    # =========================================================

    @staticmethod
    def delete_note(note_id):

        _, ownership_error = NoteController._owned_note(note_id)
        if ownership_error:
            return ownership_error


        try:

            response, status = (
                NoteService.delete_note(
                    note_id
                )
            )

            return jsonify(
                response
            ), status

        except Exception as e:

            print(
                "DELETE NOTE CONTROLLER ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to delete note",
                "details": str(e)
            }), 500

    # =========================================================
    # SUMMARY
    # =========================================================

    @staticmethod
    def summarize_note(note_id):

        _, ownership_error = NoteController._owned_note(note_id)
        if ownership_error:
            return ownership_error


        try:

            response, status = (
                NoteService.summarize_note(
                    note_id
                )
            )

            return jsonify(
                response
            ), status

        except Exception as e:

            print(
                "SUMMARY CONTROLLER ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to generate summary",
                "details": str(e)
            }), 500

    # =========================================================
    # KEY CONCEPTS / KEYWORDS
    # =========================================================

    @staticmethod
    def extract_keywords(note_id):

        _, ownership_error = NoteController._owned_note(note_id)
        if ownership_error:
            return ownership_error


        try:

            response, status = (
                NoteService.extract_note_keywords(
                    note_id
                )
            )

            return jsonify(
                response
            ), status

        except Exception as e:

            print(
                "KEYWORDS CONTROLLER ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to generate key concepts",
                "details": str(e)
            }), 500

    # =========================================================
    # FLASHCARDS
    # =========================================================

    @staticmethod
    def generate_flashcards(note_id):

        _, ownership_error = NoteController._owned_note(note_id)
        if ownership_error:
            return ownership_error


        try:

            response, status = (
                NoteService.generate_note_flashcards(
                    note_id
                )
            )

            return jsonify(
                response
            ), status

        except Exception as e:

            print(
                "FLASHCARDS CONTROLLER ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to generate flashcards",
                "details": str(e)
            }), 500

    # =========================================================
    # QUIZ
    # =========================================================

    @staticmethod
    def generate_quiz(note_id):

        _, ownership_error = NoteController._owned_note(note_id)
        if ownership_error:
            return ownership_error


        try:

            # -------------------------------------------------
            # Get JSON request body
            # -------------------------------------------------

            data = request.get_json(
                silent=True
            )

            if not data:

                data = {}

            # -------------------------------------------------
            # Get difficulty
            # -------------------------------------------------

            difficulty = data.get(
                "difficulty",
                "intermediate"
            )

            # -------------------------------------------------
            # Get question count
            # -------------------------------------------------

            question_count = data.get(
                "question_count",
                10
            )

            # -------------------------------------------------
            # Validate difficulty
            # -------------------------------------------------

            difficulty = str(
                difficulty
            ).strip().lower()

            allowed_difficulties = [
                "beginner",
                "intermediate",
                "advanced"
            ]

            if difficulty not in allowed_difficulties:

                difficulty = "intermediate"

            # -------------------------------------------------
            # Validate question count
            # -------------------------------------------------

            try:

                question_count = int(
                    question_count
                )

            except Exception:

                question_count = 10

            allowed_counts = [
                5,
                10,
                15,
                20
            ]

            if question_count not in allowed_counts:

                question_count = 10

            # -------------------------------------------------
            # Print request details
            # -------------------------------------------------

            print(
                "========================================"
            )

            print(
                "QUIZ REQUEST"
            )

            print(
                "========================================"
            )

            print(
                "Note ID:",
                note_id
            )

            print(
                "Difficulty:",
                difficulty
            )

            print(
                "Question Count:",
                question_count
            )

            print(
                "========================================"
            )

            # -------------------------------------------------
            # Generate quiz
            # -------------------------------------------------

            response, status = (
                NoteService.generate_note_quiz(
                    note_id=note_id,
                    difficulty=difficulty,
                    question_count=question_count
                )
            )

            return jsonify(
                response
            ), status

        except Exception as e:

            print(
                "QUIZ CONTROLLER ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to generate quiz",
                "details": str(e)
            }), 500

    # =========================================================
    # CHAT WITH NOTE
    # =========================================================

    @staticmethod
    def chat_with_note(note_id):

        _, ownership_error = NoteController._owned_note(note_id)
        if ownership_error:
            return ownership_error


        try:

            data = request.get_json(
                silent=True
            )

            if not data:

                return jsonify({
                    "error":
                        "Request body is required"
                }), 400

            question = data.get(
                "question",
                ""
            )

            if not question or not question.strip():

                return jsonify({
                    "error":
                        "Question is required"
                }), 400

            response, status = (
                NoteService.chat_with_note(
                    note_id,
                    question
                )
            )

            return jsonify(
                response
            ), status

        except Exception as e:

            print(
                "CHAT CONTROLLER ERROR:",
                str(e)
            )

            return jsonify({
                "error": "Unable to answer question",
                "details": str(e)
            }), 500

    # =========================================================
    # SUBMIT QUIZ
    # =========================================================

    @staticmethod
    def submit_quiz(note_id):

        _, ownership_error = NoteController._owned_note(note_id)
        if ownership_error:
            return ownership_error


        try:

            data = request.get_json(
                silent=True
            )

            if not data:

                return jsonify({
                    "error":
                        "Request body is required"
                }), 400

            if "answers" not in data:

                return jsonify({
                    "error":
                        "answers are required"
                }), 400

            answers = data.get(
                "answers"
            )

            if not isinstance(
                answers,
                dict
            ):

                return jsonify({
                    "error":
                        "answers must be an object"
                }), 400

            result = (
                NoteService.submit_quiz(
                    note_id,
                    answers
                )
            )

            if result is None:

                return jsonify({
                    "error":
                        "Quiz not found"
                }), 404

            return jsonify({

                "message":
                    "Quiz submitted successfully",

                "note_id":
                    note_id,

                "result":
                    result

            }), 200

        except Exception as e:

            print(
                "SUBMIT QUIZ CONTROLLER ERROR:",
                str(e)
            )

            return jsonify({
                "error":
                    "Unable to submit quiz",
                "details":
                    str(e)
            }), 500