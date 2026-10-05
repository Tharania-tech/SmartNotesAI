from flask import Blueprint, request, jsonify
from services.ocr_correction_service import correct_ocr_text

ocr_bp = Blueprint("ocr", __name__)


@ocr_bp.route("/ocr/correct", methods=["POST"])
def correct_ocr():
    try:
        if not request.is_json:
            return jsonify({
                "message": "OCR correction failed",
                "error": "Content-Type must be application/json"
            }), 415

        data = request.get_json(silent=True) or {}
        text = data.get("text", "")

        if not isinstance(text, str):
            return jsonify({
                "message": "OCR correction failed",
                "error": "The 'text' field must be a string"
            }), 400

        text = text.strip()

        if not text:
            return jsonify({
                "message": "OCR correction failed",
                "error": "Text is required"
            }), 400

        corrected_text = correct_ocr_text(text)

        return jsonify({
            "message": "OCR correction successful",
            "original_text": text,
            "corrected_text": corrected_text
        }), 200

    except Exception as e:
        print("OCR correction error:", str(e))

        return jsonify({
            "message": "OCR correction failed",
            "error": str(e)
        }), 500