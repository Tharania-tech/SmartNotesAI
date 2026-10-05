from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone

from database.db import mongo


class NoteModel:

    # =========================================================
    # CREATE NOTE
    # =========================================================

    @staticmethod
    def create_note(note_data):

        note_data.setdefault("created_at", datetime.now(timezone.utc))
        return mongo.db.notes.insert_one(note_data)

    # =========================================================
    # GET ALL NOTES FOR USER
    # =========================================================

    @staticmethod
    def get_notes_by_user(user_id):

        notes = mongo.db.notes.find(
            {
                "user_id": user_id
            }
        ).sort(
            "_id",
            -1
        )

        return list(notes)

    # =========================================================
    # GET NOTE BY ID
    # =========================================================

    @staticmethod
    def get_note_by_id(note_id):

        try:

            object_id = ObjectId(
                note_id
            )

        except (InvalidId, TypeError):

            return None

        return mongo.db.notes.find_one(
            {
                "_id": object_id
            }
        )

    # =========================================================
    # DELETE NOTE
    # =========================================================

    @staticmethod
    def delete_note(note_id):

        try:

            object_id = ObjectId(
                note_id
            )

        except (InvalidId, TypeError):

            return None

        return mongo.db.notes.delete_one(
            {
                "_id": object_id
            }
        )

    # =========================================================
    # UPDATE SUMMARY
    # =========================================================

    @staticmethod
    def update_summary(
        note_id,
        summary
    ):

        try:

            object_id = ObjectId(
                note_id
            )

        except (InvalidId, TypeError):

            return None

        return mongo.db.notes.update_one(
            {
                "_id": object_id
            },
            {
                "$set": {
                    "summary": summary
                }
            }
        )

    # =========================================================
    # UPDATE KEYWORDS
    # =========================================================

    @staticmethod
    def update_keywords(
        note_id,
        keywords
    ):

        try:

            object_id = ObjectId(
                note_id
            )

        except (InvalidId, TypeError):

            return None

        return mongo.db.notes.update_one(
            {
                "_id": object_id
            },
            {
                "$set": {
                    "keywords": keywords
                }
            }
        )

    # =========================================================
    # UPDATE FLASHCARDS
    # =========================================================

    @staticmethod
    def update_flashcards(
        note_id,
        flashcards
    ):

        try:

            object_id = ObjectId(
                note_id
            )

        except (InvalidId, TypeError):

            return None

        return mongo.db.notes.update_one(
            {
                "_id": object_id
            },
            {
                "$set": {
                    "flashcards": flashcards
                }
            }
        )

    # =========================================================
    # UPDATE QUIZ
    # =========================================================

    @staticmethod
    def update_quiz(
        note_id,
        quiz
    ):

        try:

            object_id = ObjectId(
                note_id
            )

        except (InvalidId, TypeError):

            return None

        return mongo.db.notes.update_one(
            {
                "_id": object_id
            },
            {
                "$set": {
                    "quiz": quiz
                }
            }
        )