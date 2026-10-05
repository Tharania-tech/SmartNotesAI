from flask import Blueprint, jsonify, request
from bson import ObjectId

from database.db import mongo

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}

        message = (data.get("message") or "").strip()
        note_id = data.get("noteId")

        if not message:
            return jsonify({
                "message": "Question is required"
            }), 400

        if not note_id:
            return jsonify({
                "message": "Note ID is required"
            }), 400

        # Convert frontend string ID to MongoDB ObjectId
        try:
            object_id = ObjectId(note_id)
        except Exception:
            return jsonify({
                "message": "Invalid Note ID"
            }), 400

        # Find the note
        note = mongo.db.notes.find_one({
            "_id": object_id
        })

        if not note:
            return jsonify({
                "message": "Note not found"
            }), 404

        note_text = (
            note.get("cleaned_text")
            or note.get("extracted_text")
            or note.get("raw_text")
            or ""
        )

        if not note_text.strip():
            return jsonify({
                "message": "No extracted text available for this note"
            }), 400

        answer = answer_question(message, note_text)

        return jsonify({
            "answer": answer,
            "noteId": str(note["_id"])
        }), 200

    except Exception as e:
        print("AI Tutor Error:", e)

        return jsonify({
            "message": "AI Tutor failed",
            "error": str(e)
        }), 500


def answer_question(question, note_text):
    import re

    question_words = set(
        re.findall(r"[A-Za-z0-9]{3,}", question.lower())
    )

    sentences = re.split(
        r"(?<=[.!?])\s+",
        note_text
    )

    scored_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence.split()) < 5:
            continue

        sentence_words = set(
            re.findall(
                r"[A-Za-z0-9]{3,}",
                sentence.lower()
            )
        )

        overlap = len(
            question_words & sentence_words
        )

        if overlap > 0:
            scored_sentences.append(
                (overlap, sentence)
            )

    scored_sentences.sort(
        key=lambda item: item[0],
        reverse=True
    )

    best_sentences = [
        sentence
        for _, sentence in scored_sentences[:3]
    ]

    if not best_sentences:
        return (
            "I couldn't find a direct answer in your uploaded notes. "
            "Please try asking with a specific topic or keyword from the note."
        )

    return " ".join(best_sentences)