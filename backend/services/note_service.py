import os
import uuid
import json
import re
import threading
import tempfile

from werkzeug.utils import secure_filename

import pymupdf
from docx import Document
from ollama import chat

from services.concept_service import ConceptService
from models.note_model import NoteModel
from models.progress_model import ProgressModel
from database.db import mongo


from services.weak_topic_flashcard_service import (
    WeakTopicFlashcardService
)

from services.adaptive_quiz_service import (
    AdaptiveQuizService
)

from services.quiz_result_service import (
    QuizResultService
)

from services.ocr_service import OCRService
from services.chat_service import ChatService
from services.quiz_service import QuizService
from services.flashcard_service import FlashcardService

from services.summarization_service import (
    SummarizationService
)


ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "png",
    "jpg",
    "jpeg"
}


class NoteService:

    OCR_REFRESH_LOCK = threading.Lock()

    # =========================================================
    # QWEN MODEL
    # =========================================================

    QWEN_MODEL = "qwen2.5:3b-instruct-q4_0"

    # =========================================================
    # FILE VALIDATION
    # =========================================================

    @staticmethod
    def allowed_file(filename):

        if not filename:
            return False

        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in ALLOWED_EXTENSIONS
        )

    # =========================================================
    # GET NOTES
    # =========================================================

    @staticmethod
    def get_notes(user_id):

        notes = NoteModel.get_notes_by_user(user_id)

        result = []

        for note in notes:

            result.append({
                "note_id": str(note.get("_id")),
                "title": note.get(
                    "title",
                    "Untitled Note"
                ),
                "filename": note.get(
                    "filename",
                    ""
                ),
                "file_type": note.get(
                    "file_type",
                    ""
                )
            })

        return result

    # =========================================================
    # DELETE NOTE
    # =========================================================

    @staticmethod
    def delete_note(note_id):

        try:

            note = NoteModel.get_note_by_id(
                note_id
            )

            if not note:

                return {
                    "message": "Note not found"
                }, 404

            result = NoteModel.delete_note(
                note_id
            )

            if result is None:

                return {
                    "message": "Invalid note ID"
                }, 400

            if result.deleted_count == 0:

                return {
                    "message": "Unable to delete note"
                }, 500

            # -------------------------------------------------
            # Delete uploaded file from disk
            # -------------------------------------------------

            file_path = note.get(
                "file_path",
                ""
            )

            if file_path:

                try:

                    if os.path.exists(file_path):

                        os.remove(file_path)

                        print(
                            "Uploaded file deleted:",
                            file_path
                        )

                except Exception as file_error:

                    print(
                        "File delete warning:",
                        str(file_error)
                    )

            return {
                "message":
                    "Note deleted successfully",
                "note_id":
                    note_id
            }, 200

        except Exception as e:

            print(
                "DELETE NOTE ERROR:",
                str(e)
            )

            return {
                "message":
                    "Failed to delete note",
                "error":
                    str(e)
            }, 500

    # =========================================================
    # SOURCE TEXT CLEANING / QUALITY CHECK
    # =========================================================

    @staticmethod
    def clean_extracted_text(text):

        if not text:
            return ""

        lines = str(text).replace("\r", "\n").splitlines()
        cleaned_lines = []
        seen_lines = set()

        watermark_patterns = [
            r"engg\s*tree\s*\.?\s*com",
            r"downloaded\s+from\s+engg",
            r"downloaded\s+by\s+engg",
            r"www\s*\.?\s*engg",
            r"ge\s*3791\s*-?\s*hve"
        ]

        for line in lines:

            line = re.sub(r"\s+", " ", line).strip()

            if not line:
                continue

            if re.fullmatch(r"\d+", line):
                continue

            if re.fullmatch(
                r"page\s+\d+",
                line,
                flags=re.IGNORECASE
            ):
                continue

            lower_line = line.lower()
            watermark_only = False

            for pattern in watermark_patterns:

                if re.fullmatch(
                    pattern,
                    lower_line,
                    flags=re.IGNORECASE
                ):
                    watermark_only = True
                    break

            if watermark_only:
                continue

            for pattern in watermark_patterns:

                line = re.sub(
                    pattern,
                    " ",
                    line,
                    flags=re.IGNORECASE
                )

            line = re.sub(
                r"\s+",
                " ",
                line
            ).strip()

            if not line:
                continue

            key = line.lower()

            if key in seen_lines:
                continue

            seen_lines.add(key)
            cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()

    @staticmethod
    def is_low_quality_extraction(text):

        if not text or not str(text).strip():
            return True

        cleaned = NoteService.clean_extracted_text(text)

        if not cleaned:
            return True

        words = re.findall(
            r"[A-Za-z]{2,}",
            cleaned
        )

        if len(words) < 20:
            return True

        return False

    @staticmethod
    def save_refreshed_extracted_text(
        note_id,
        extracted_text
    ):

        try:

            note = NoteModel.get_note_by_id(
                note_id
            )

            if not note:
                return

            mongo.db.notes.update_one(
                {"_id": note["_id"]},
                {
                    "$set": {
                        "extracted_text": extracted_text
                    }
                }
            )

            print(
                "Stored refreshed extracted text in MongoDB."
            )

        except Exception as error:

            print(
                "EXTRACTED TEXT SAVE WARNING:",
                str(error)
            )

    @staticmethod
    def refresh_note_extracted_text(
        note_id,
        note,
        current_text
    ):

        current_cleaned = NoteService.clean_extracted_text(
            current_text
        )

        if not NoteService.is_low_quality_extraction(
            current_cleaned
        ):
            return current_cleaned

        file_path = note.get(
            "file_path",
            ""
        )

        extension = str(
            note.get(
                "file_type",
                ""
            )
        ).lower().strip()

        if not file_path or not os.path.exists(file_path):

            print(
                "ORIGINAL FILE NOT AVAILABLE FOR OCR:",
                file_path
            )

            return current_cleaned

        # Prevent two browser requests from OCR-processing the
        # same note at the same time.
        with NoteService.OCR_REFRESH_LOCK:

            # Another request may have completed OCR while this
            # request was waiting for the lock. Re-read MongoDB
            # before starting OCR again.
            latest_note = NoteModel.get_note_by_id(
                note_id
            )

            if latest_note:

                latest_text = latest_note.get(
                    "extracted_text",
                    ""
                )

                latest_cleaned = NoteService.clean_extracted_text(
                    latest_text
                )

                if not NoteService.is_low_quality_extraction(
                    latest_cleaned
                ):

                    print(
                        "OCR text already refreshed by another request."
                    )

                    return latest_cleaned

            print("\n" + "=" * 60)
            print("STORED TEXT IS LOW QUALITY")
            print("RE-RUNNING DOCUMENT EXTRACTION / OCR")
            print("=" * 60)

            try:

                if extension == "pdf":

                    refreshed_text = NoteService.extract_pdf_text(
                        file_path
                    )

                else:

                    refreshed_text = NoteService.extract_text(
                        file_path,
                        extension
                    )

                refreshed_text = NoteService.clean_extracted_text(
                    refreshed_text
                )

                print(
                    "Refreshed usable characters:",
                    len(refreshed_text)
                )

                if refreshed_text:

                    NoteService.save_refreshed_extracted_text(
                        note_id,
                        refreshed_text
                    )

                    return refreshed_text

            except Exception as error:

                print(
                    "OCR REFRESH ERROR:",
                    str(error)
                )

            return current_cleaned

    # =========================================================
    # EXTRACT TEXT FROM PDF
    # =========================================================

    @staticmethod
    def extract_pdf_text(file_path):

        # -----------------------------------------------------
        # 1. Try normal PDF text extraction first.
        # -----------------------------------------------------
        text_parts = []

        document = pymupdf.open(
            file_path
        )

        try:

            for page in document:

                page_text = page.get_text()

                if page_text:
                    text_parts.append(page_text)

        finally:

            document.close()

        raw_text = "\n".join(text_parts)

        direct_text = NoteService.clean_extracted_text(
            raw_text
        )

        print("\n" + "=" * 60)
        print("PDF TEXT EXTRACTION")
        print("=" * 60)
        print(
            "PyMuPDF raw characters:",
            len(raw_text)
        )
        print(
            "PyMuPDF usable characters:",
            len(direct_text)
        )

        if not NoteService.is_low_quality_extraction(
            direct_text
        ):

            print("Readable PDF text detected.")
            print("OCR fallback not required.")
            print("=" * 60)
            return direct_text

        # -----------------------------------------------------
        # 2. PyMuPDF only found watermark/metadata.
        # Render each PDF page as an image and pass the image
        # through the same OCR method that already works for
        # standalone JPG/PNG files in this project.
        # -----------------------------------------------------
        print("PyMuPDF text is insufficient.")
        print("Starting page-image OCR fallback...")

        ocr_pages = []
        ocr_document = pymupdf.open(
            file_path
        )

        temp_dir = tempfile.TemporaryDirectory(
            prefix="smartnotes_ocr_"
        )

        try:

            total_pages = len(ocr_document)

            for page_index, page in enumerate(
                ocr_document,
                start=1
            ):

                print(
                    "OCR processing page "
                    + str(page_index)
                    + "/"
                    + str(total_pages)
                    + "..."
                )

                image_path = os.path.join(
                    temp_dir.name,
                    "page_"
                    + str(page_index)
                    + ".png"
                )

                # 2x render gives handwriting OCR more pixels
                # to work with without keeping every page in RAM.
                matrix = pymupdf.Matrix(
                    2.0,
                    2.0
                )

                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False
                )

                pixmap.save(
                    image_path
                )

                page_text = OCRService.extract_text_from_image(
                    image_path
                )

                page_text = NoteService.clean_extracted_text(
                    page_text
                )

                if page_text:

                    ocr_pages.append(
                        page_text
                    )

                print(
                    "Page "
                    + str(page_index)
                    + " usable characters:",
                    len(page_text)
                )

        finally:

            ocr_document.close()
            temp_dir.cleanup()

        ocr_text = "\n\n".join(
            ocr_pages
        ).strip()

        ocr_text = NoteService.clean_extracted_text(
            ocr_text
        )

        print(
            "PaddleOCR usable characters:",
            len(ocr_text)
        )

        if ocr_text:

            print(
                "OCR extraction completed successfully."
            )
        else:
            print(
                "OCR returned no usable text."
            )

        print("=" * 60)

        return ocr_text

    # =========================================================
    # EXTRACT TEXT FROM DOCX
    # =========================================================

    @staticmethod
    def extract_docx_text(file_path):

        document = Document(
            file_path
        )

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return NoteService.clean_extracted_text(
            text
        )

    # =========================================================
    # GENERAL TEXT EXTRACTION
    # =========================================================

    @staticmethod
    def extract_text(
        file_path,
        extension
    ):

        extension = str(
            extension
        ).lower().strip()

        if extension == "pdf":

            return NoteService.extract_pdf_text(
                file_path
            )

        if extension == "docx":

            return NoteService.extract_docx_text(
                file_path
            )

        if extension in {
            "png",
            "jpg",
            "jpeg"
        }:

            print("\n" + "=" * 60)
            print("IMAGE OCR EXTRACTION")
            print("=" * 60)

            image_text = OCRService.extract_text_from_image(
                file_path
            )

            image_text = NoteService.clean_extracted_text(
                image_text
            )

            print(
                "PaddleOCR usable characters:",
                len(image_text)
            )

            print("=" * 60)

            return image_text

        raise ValueError(
            "Unsupported file type"
        )

    # =========================================================
    # CLEAN QUIZ TEXT
    # =========================================================

    @staticmethod
    def clean_quiz_text(text):

        if not text:

            return ""

        lines = text.splitlines()

        cleaned_lines = []

        seen_lines = set()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # -------------------------------------------------
            # Remove standalone page numbers
            # -------------------------------------------------

            if re.fullmatch(
                r"\d+",
                line
            ):

                continue

            if re.fullmatch(
                r"page\s+\d+",
                line,
                flags=re.IGNORECASE
            ):

                continue

            # -------------------------------------------------
            # Remove URLs
            # -------------------------------------------------

            if re.fullmatch(
                r"https?://\S+",
                line,
                flags=re.IGNORECASE
            ):

                continue

            if re.fullmatch(
                r"www\.\S+",
                line,
                flags=re.IGNORECASE
            ):

                continue

            # -------------------------------------------------
            # Remove email addresses
            # -------------------------------------------------

            if re.fullmatch(
                r"[\w\.-]+@[\w\.-]+\.\w+",
                line
            ):

                continue

            # -------------------------------------------------
            # Normalize spaces
            # -------------------------------------------------

            normalized = re.sub(
                r"\s+",
                " ",
                line
            ).strip()

            normalized_key = (
                normalized.lower()
            )

            # -------------------------------------------------
            # Remove duplicate lines
            # -------------------------------------------------

            if normalized_key in seen_lines:

                continue

            seen_lines.add(
                normalized_key
            )

            cleaned_lines.append(
                normalized
            )

        return "\n".join(
            cleaned_lines
        )

    # =========================================================
    # PREPARE CONTENT FOR QWEN
    # =========================================================

    @staticmethod
    def prepare_quiz_content(
        text,
        max_characters=8000
    ):

        cleaned_text = (
            NoteService.clean_quiz_text(
                text
            )
        )

        if not cleaned_text:

            return ""

        if len(cleaned_text) <= max_characters:

            return cleaned_text

        half = max_characters // 2

        beginning = cleaned_text[:half]

        ending = cleaned_text[-half:]

        return (
            beginning
            + "\n\n"
            + "[Middle section omitted]\n\n"
            + ending
        )

    # =========================================================
    # PARSE QWEN JSON
    # =========================================================

    @staticmethod
    def parse_quiz_json(model_text):

        if not model_text:

            return []

        text = model_text.strip()

        # -------------------------------------------------
        # Remove Markdown code fences
        # -------------------------------------------------

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        text = text.strip()

        # -------------------------------------------------
        # Find JSON object
        # -------------------------------------------------

        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end == -1:

            print(
                "Qwen did not return JSON."
            )

            print(
                "MODEL OUTPUT:"
            )

            print(text)

            return []

        json_text = text[
            start:end + 1
        ]

        try:

            data = json.loads(
                json_text
            )

        except json.JSONDecodeError as e:

            print(
                "Qwen JSON parsing failed:"
            )

            print(
                str(e)
            )

            print(
                "MODEL OUTPUT:"
            )

            print(text)

            return []

        if not isinstance(
            data,
            dict
        ):

            return []

        quiz = data.get(
            "quiz",
            []
        )

        if not isinstance(
            quiz,
            list
        ):

            return []

        return quiz

    # =========================================================
    # VALIDATE ONE QUIZ QUESTION
    # =========================================================

    @staticmethod
    def validate_quiz_question(question):

        if not isinstance(
            question,
            dict
        ):

            return False

        # -------------------------------------------------
        # Question text
        # -------------------------------------------------

        question_text = str(
            question.get(
                "question",
                ""
            )
        ).strip()

        if not question_text:

            return False

        # -------------------------------------------------
        # Options
        # -------------------------------------------------

        options = question.get(
            "options",
            {}
        )

        if not isinstance(
            options,
            dict
        ):

            return False

        normalized_options = {}

        for letter in [
            "A",
            "B",
            "C",
            "D"
        ]:

            value = None

            if letter in options:

                value = options[
                    letter
                ]

            elif letter.lower() in options:

                value = options[
                    letter.lower()
                ]

            if value is None:

                return False

            if isinstance(
                value,
                dict
            ):

                value = (
                    value.get("text")
                    or value.get("label")
                    or value.get("value")
                    or ""
                )

            value = str(
                value
            ).strip()

            if not value:

                return False

            normalized_options[
                letter
            ] = value

        # -------------------------------------------------
        # Correct answer
        # -------------------------------------------------

        correct_answer = str(
            question.get(
                "correct_answer",
                ""
            )
        ).strip().upper()

        if correct_answer not in [
            "A",
            "B",
            "C",
            "D"
        ]:

            return False

        # -------------------------------------------------
        # Prevent duplicate options
        # -------------------------------------------------

        option_values = [
            normalized_options["A"].lower(),
            normalized_options["B"].lower(),
            normalized_options["C"].lower(),
            normalized_options["D"].lower()
        ]

        if len(
            set(option_values)
        ) != 4:

            return False

        # -------------------------------------------------
        # Normalize question object
        # -------------------------------------------------

        question["question"] = (
            question_text
        )

        question["options"] = (
            normalized_options
        )

        question["correct_answer"] = (
            correct_answer
        )

        question["explanation"] = str(
            question.get(
                "explanation",
                ""
            )
        ).strip()

        question["concept"] = str(
            question.get(
                "concept",
                "General"
            )
        ).strip()

        question["difficulty"] = str(
            question.get(
                "difficulty",
                "intermediate"
            )
        ).strip().lower()

        return True

    # =========================================================
    # VALIDATE COMPLETE QUIZ
    # =========================================================

    @staticmethod
    def validate_quiz(
        quiz,
        number_of_questions
    ):

        if not isinstance(
            quiz,
            list
        ):

            return False

        valid_quiz = []

        seen_questions = set()

        for question in quiz:

            if not NoteService.validate_quiz_question(
                question
            ):

                print(
                    "Rejected invalid question:"
                )

                print(
                    question
                )

                continue

            # -------------------------------------------------
            # Normalize question for duplicate checking
            # -------------------------------------------------

            question_key = re.sub(
                r"[^a-z0-9\s]",
                "",
                question["question"].lower()
            )

            question_key = re.sub(
                r"\s+",
                " ",
                question_key
            ).strip()

            if question_key in seen_questions:

                print(
                    "Rejected duplicate question:"
                )

                print(
                    question["question"]
                )

                continue

            seen_questions.add(
                question_key
            )

            valid_quiz.append(
                question
            )

            if len(valid_quiz) >= number_of_questions:

                break

        if len(valid_quiz) < number_of_questions:

            return False

        return valid_quiz

    # =========================================================
    # GENERATE QUIZ USING QWEN
    # =========================================================

    @staticmethod
    def generate_qwen_quiz(
        content,
        number_of_questions,
        difficulty
    ):

        if not content:

            return []

        # -----------------------------------------------------
        # Validate number
        # -----------------------------------------------------

        try:

            number_of_questions = int(
                number_of_questions
            )

        except Exception:

            number_of_questions = 10

        if number_of_questions not in [
            5,
            10,
            15,
            20
        ]:

            number_of_questions = 10

        # -----------------------------------------------------
        # Validate difficulty
        # -----------------------------------------------------

        difficulty = str(
            difficulty
        ).strip().lower()

        if difficulty not in [
            "beginner",
            "intermediate",
            "advanced"
        ]:

            difficulty = "intermediate"

        # -----------------------------------------------------
        # Prepare smaller content
        # -----------------------------------------------------

        content = NoteService.prepare_quiz_content(
            content,
            max_characters=5000
        )

        if not content:

            return []

        # -----------------------------------------------------
        # Generate in batches
        # -----------------------------------------------------

        batch_size = 5

        all_questions = []

        remaining = number_of_questions

        batch_number = 1

        max_batches = 6

        while (
            remaining > 0
            and batch_number <= max_batches
        ):

            current_batch = min(
                batch_size,
                remaining
            )

            print(
                "========================================"
            )

            print(
                "QWEN QUIZ BATCH"
            )

            print(
                "========================================"
            )

            print(
                "Batch:",
                batch_number
            )

            print(
                "Questions:",
                current_batch
            )

            print(
                "Difficulty:",
                difficulty
            )

            # -------------------------------------------------
            # Difficulty instructions
            # -------------------------------------------------

            if difficulty == "beginner":

                difficulty_text = (
                    "Use definitions, basic facts, "
                    "identification and direct understanding."
                )

            elif difficulty == "advanced":

                difficulty_text = (
                    "Use reasoning, analysis, application, "
                    "comparison and scenario-based questions."
                )

            else:

                difficulty_text = (
                    "Use conceptual understanding, "
                    "comparison and basic application."
                )

            # -------------------------------------------------
            # Prompt
            # -------------------------------------------------

            prompt = f"""
You are an expert educational assessment generator.

Create exactly {current_batch} multiple-choice questions
from the study material provided below.

Difficulty level:
{difficulty}

Difficulty guidance:
{difficulty_text}

Rules:

1. Use only information from the study material.
2. Do not use outside knowledge.
3. Every question must be educational.
4. Do not repeat questions.
5. Avoid nearly identical questions.
6. Each question must have exactly four options.
7. Options must be A, B, C and D.
8. Exactly one option must be correct.
9. correct_answer must be exactly A, B, C or D.
10. The correct answer must match the correct option.
11. Wrong options must be plausible.
12. Keep explanations short.
13. Include the main concept.
14. Return only valid JSON.
15. Do not return Markdown.
16. Do not write anything outside the JSON.
17. Create exactly {current_batch} questions.

Return this exact structure:

{{
    "quiz": [
        {{
            "question": "Question text",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "A",
            "explanation": "Short explanation",
            "concept": "Main concept",
            "difficulty": "{difficulty}"
        }}
    ]
}}

STUDY MATERIAL:

{content}
"""

            try:

                print(
                    "Sending request to Ollama..."
                )

                response = chat(
                    model=NoteService.QWEN_MODEL,

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    format="json",

                    options={
                        "temperature": 0.1,
                        "num_predict": 1200
                    }
                )

                print(
                    "Ollama response received."
                )

                # -------------------------------------------------
                # Get model output
                # -------------------------------------------------

                model_text = (
                    response["message"]["content"]
                )

                print(
                    "Qwen output length:",
                    len(model_text)
                )

                # -------------------------------------------------
                # Parse
                # -------------------------------------------------

                raw_quiz = (
                    NoteService.parse_quiz_json(
                        model_text
                    )
                )

                print(
                    "Raw questions:",
                    len(raw_quiz)
                )

                # -------------------------------------------------
                # Validate each question
                # -------------------------------------------------

                for question in raw_quiz:

                    if not NoteService.validate_quiz_question(
                        question
                    ):

                        print(
                            "Invalid question skipped."
                        )

                        continue

                    question_key = re.sub(
                        r"[^a-z0-9\s]",
                        "",
                        question["question"].lower()
                    )

                    question_key = re.sub(
                        r"\s+",
                        " ",
                        question_key
                    ).strip()

                    # -------------------------------------------------
                    # Compare with previous questions
                    # -------------------------------------------------

                    duplicate = False

                    for existing in all_questions:

                        existing_key = re.sub(
                            r"[^a-z0-9\s]",
                            "",
                            existing["question"].lower()
                        )

                        existing_key = re.sub(
                            r"\s+",
                            " ",
                            existing_key
                        ).strip()

                        if (
                            question_key
                            == existing_key
                        ):

                            duplicate = True

                            break

                    if duplicate:

                        print(
                            "Duplicate question skipped:"
                        )

                        print(
                            question["question"]
                        )

                        continue

                    all_questions.append(
                        question
                    )

                    if (
                        len(all_questions)
                        >= number_of_questions
                    ):

                        break

            except Exception as e:

                print(
                    "========================================"
                )

                print(
                    "QWEN ERROR"
                )

                print(
                    "========================================"
                )

                print(
                    str(e)
                )

                print(
                    "========================================"
                )

                break

            # -------------------------------------------------
            # Check if enough questions generated
            # -------------------------------------------------

            if (
                len(all_questions)
                >= number_of_questions
            ):

                break

            remaining = (
                number_of_questions
                - len(all_questions)
            )

            batch_number += 1

        # -----------------------------------------------------
        # Final result
        # -----------------------------------------------------

        print(
            "========================================"
        )

        print(
            "QUIZ GENERATION FINISHED"
        )

        print(
            "Requested:",
            number_of_questions
        )

        print(
            "Generated:",
            len(all_questions)
        )

        print(
            "========================================"
        )

        if len(all_questions) < number_of_questions:

            return []

        return all_questions[
            :number_of_questions
        ]

    # =========================================================
    # SAVE NOTE
    # =========================================================

    @staticmethod
    def save_note(
        file,
        user_id,
        title=""
    ):

        original_filename = file.filename or ""

        if not original_filename:

            return {
                "error":
                    "No file selected"
            }, 400

        filename = secure_filename(original_filename)

        if not filename:

            return {
                "error":
                    "Invalid filename"
            }, 400

        if not NoteService.allowed_file(
            filename
        ):

            return {
                "error":
                    "Only PDF, DOCX, PNG, JPG and JPEG files are allowed"
            }, 400

        extension = (
            filename
            .rsplit(
                ".",
                1
            )[1]
            .lower()
        )

        upload_folder = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            "uploads"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        stored_filename = (
            uuid.uuid4().hex
            + "_"
            + filename
        )

        file_path = os.path.join(
            upload_folder,
            stored_filename
        )

        file.save(file_path)

        try:

            extracted_text = (
                NoteService.extract_text(
                    file_path,
                    extension
                )
            )

        except Exception as e:

            print(
                "TEXT EXTRACTION ERROR:",
                str(e)
            )

            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )

            return {
                "error":
                    "Unable to extract text from uploaded file",
                "details":
                    str(e)
            }, 400

        note_data = {

            "user_id":
                user_id,

            "title":
                (
                    str(title).strip()
                    if str(title).strip()
                    else os.path.splitext(filename)[0]
                ),

            "filename":
                filename,

            "file_type":
                extension,

            "file_path":
                file_path,

            "extracted_text":
                extracted_text
        }

        result = NoteModel.create_note(
            note_data
        )

        return {

            "message":
                "Note uploaded successfully",

            "note_id":
                str(
                    result.inserted_id
                ),

            "filename":
                filename

        }, 201

    # =========================================================
    # SUMMARY
    # =========================================================

    @staticmethod
    def summarize_note(
        note_id
    ):

        note = NoteModel.get_note_by_id(
            note_id
        )

        if not note:

            return {
                "error":
                    "Note not found"
            }, 404

        extracted_text = note.get(
            "extracted_text",
            ""
        )

        # Repair old notes that were uploaded before OCR
        # integration or whose stored text contains only noise.
        extracted_text = (
            NoteService.refresh_note_extracted_text(
                note_id,
                note,
                extracted_text
            )
        )

        if not extracted_text.strip():

            return {
                "error":
                    "No usable text available. OCR could not recover text from this file."
            }, 400

        summary = (
            SummarizationService.summarize_text(
                extracted_text
            )
        )

        NoteModel.update_summary(
            note_id,
            summary
        )

        return {

            "message":
                "Summary generated successfully",

            "note_id":
                note_id,

            "summary":
                summary

        }, 200

    # =========================================================
    # KEY CONCEPTS
    # =========================================================

    @staticmethod
    def extract_note_keywords(
        note_id
    ):

        note = NoteModel.get_note_by_id(
            note_id
        )

        if not note:

            return {
                "error":
                    "Note not found"
            }, 404

        extracted_text = note.get(
            "extracted_text",
            ""
        )

        extracted_text = NoteService.refresh_note_extracted_text(
            note_id,
            note,
            extracted_text
        )

        if not extracted_text.strip():

            return {
                "error":
                    "No extracted text available"
            }, 400

        concepts = (
            ConceptService.extract_concepts(
                extracted_text,
                top_k=15
            )
        )

        if not concepts:

            return {
                "error":
                    "Unable to extract key concepts"
            }, 400

        keywords = []

        for item in concepts:

            if isinstance(
                item,
                dict
            ):

                concept = item.get(
                    "concept",
                    ""
                )

                if concept:

                    keywords.append(
                        concept
                    )

        if not keywords:

            return {
                "error":
                    "Unable to extract key concepts"
            }, 400

        NoteModel.update_keywords(
            note_id,
            keywords
        )

        return {

            "message":
                "Key concepts generated successfully",

            "note_id":
                note_id,

            "keywords":
                keywords,

            "count":
                len(keywords)

        }, 200

    # =========================================================
    # FLASHCARDS
    # =========================================================

    @staticmethod
    def generate_note_flashcards(
        note_id
    ):

        note = NoteModel.get_note_by_id(
            note_id
        )

        if not note:

            return {
                "error":
                    "Note not found"
            }, 404

        extracted_text = note.get(
            "extracted_text",
            ""
        )

        extracted_text = NoteService.refresh_note_extracted_text(
            note_id,
            note,
            extracted_text
        )

        if not extracted_text.strip():

            return {
                "error":
                    "No extracted text available"
            }, 400

        flashcards = (
            FlashcardService.generate_flashcards(
                extracted_text,
                number_of_cards=20
            )
        )

        if not flashcards:

            return {
                "error":
                    "Unable to generate flashcards"
            }, 400

        NoteModel.update_flashcards(
            note_id,
            flashcards
        )

        return {

            "message":
                "Flashcards generated successfully",

            "note_id":
                note_id,

            "flashcards":
                flashcards,

            "count":
                len(flashcards)

        }, 200

    # =========================================================
    # QUIZ
    # =========================================================

    @staticmethod
    def generate_note_quiz(
        note_id,
        difficulty="intermediate",
        question_count=10
    ):

        # -----------------------------------------------------
        # 1. Get note
        # -----------------------------------------------------

        note = NoteModel.get_note_by_id(
            note_id
        )

        if not note:

            return {
                "error":
                    "Note not found"
            }, 404

        # -----------------------------------------------------
        # 2. Get extracted text
        # -----------------------------------------------------

        extracted_text = note.get(
            "extracted_text",
            ""
        )

        extracted_text = NoteService.refresh_note_extracted_text(
            note_id,
            note,
            extracted_text
        )

        if not extracted_text.strip():

            return {
                "error":
                    "No extracted text available"
            }, 400

        # -----------------------------------------------------
        # 3. Validate difficulty
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # 4. Validate question count
        # -----------------------------------------------------

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

        print(
            "========================================"
        )

        print(
            "QUIZ GENERATION REQUEST"
        )

        print(
            "========================================"
        )

        print(
            "Difficulty:",
            difficulty
        )

        print(
            "Question count:",
            question_count
        )

        print(
            "========================================"
        )

        # -----------------------------------------------------
        # 5. Prepare content
        # -----------------------------------------------------

        quiz_content = (
            NoteService.prepare_quiz_content(
                extracted_text,
                max_characters=8000
            )
        )

        if not quiz_content.strip():

            return {
                "error":
                    "No useful educational content available for quiz generation"
            }, 400

        # -----------------------------------------------------
        # 6. Generate quiz
        # -----------------------------------------------------

        quiz = (
            NoteService.generate_qwen_quiz(
                content=quiz_content,
                number_of_questions=question_count,
                difficulty=difficulty
            )
        )

        # -----------------------------------------------------
        # 7. Retry once
        # -----------------------------------------------------

        if not quiz:

            print(
                "Qwen quiz generation failed."
            )
            return {"error":"The AI could not generate the quiz. Please try again."}, 400


        # -----------------------------------------------------
        # 8. Final validation
        # -----------------------------------------------------

        if not quiz:

            return {
                "error":
                    "Unable to generate a valid quiz"
            }, 400

        # -----------------------------------------------------
        # 9. Save quiz
        # -----------------------------------------------------

        NoteModel.update_quiz(
            note_id,
            quiz
        )

        return {

            "message":
                "Quiz generated successfully",

            "note_id":
                note_id,

            "difficulty":
                difficulty,

            "question_count":
                len(quiz),

            "quiz":
                quiz

        }, 200

    # =========================================================
    # CHAT WITH NOTE
    # =========================================================

    @staticmethod
    def chat_with_note(
        note_id,
        question
    ):

        note = NoteModel.get_note_by_id(
            note_id
        )

        if not note:

            return {
                "error":
                    "Note not found"
            }, 404

        extracted_text = note.get(
            "extracted_text",
            ""
        )

        extracted_text = NoteService.refresh_note_extracted_text(
            note_id,
            note,
            extracted_text
        )

        if not extracted_text.strip():

            return {
                "error":
                    "No note content available"
            }, 400

        if not question or not question.strip():

            return {
                "error":
                    "Question is required"
            }, 400

        result = (
            ChatService.answer_question(
                question,
                extracted_text
            )
        )

        return {

            "message":
                "Answer generated successfully",

            "note_id":
                note_id,

            "question":
                question,

            "answer":
                result.get(
                    "answer",
                    ""
                ),

            "relevant_context":
                result.get(
                    "relevant_context",
                    ""
                )

        }, 200

    # =========================================================
    # SUBMIT QUIZ
    # =========================================================

    @classmethod
    def submit_quiz(
        cls,
        note_id,
        answers
    ):

        # -----------------------------------------------------
        # 1. Get note
        # -----------------------------------------------------

        note = NoteModel.get_note_by_id(
            note_id
        )

        if not note:

            return None

        # -----------------------------------------------------
        # 2. Get saved quiz
        # -----------------------------------------------------

        quiz = note.get(
            "quiz"
        )

        if not quiz:

            return None

        # -----------------------------------------------------
        # 3. Evaluate answers
        # -----------------------------------------------------

        result = (
            QuizResultService.evaluate_quiz(
                quiz=quiz,
                answers=answers
            )
        )
        # -----------------------------------------------------
# Save quiz attempt for progress tracking
# -----------------------------------------------------

        try:

              user_id = note.get(
        "user_id",
        ""
    )
              if user_id:

                  ProgressModel.create_quiz_attempt(
            user_id=user_id,
            note_id=note_id,
            quiz=quiz,
            answers=answers,
            result=result)
        except Exception as progress_error:
            print(
        "Progress tracking warning:",
        str(progress_error)
    )

        # -----------------------------------------------------
        # 4. Score
        # -----------------------------------------------------

        score = result.get(
            "score_percentage"

        )

        # -----------------------------------------------------
        # 5. Adaptive level
        # -----------------------------------------------------

        next_quiz_info = (
            AdaptiveQuizService.get_next_quiz_level(
                score
            )
        )

        next_level = (
            next_quiz_info.get(
                "level",
                "intermediate"
            )
        )

        next_question_count = (
            next_quiz_info.get(
                "question_count",
                10
            )
        )

        # -----------------------------------------------------
        # 6. Note text
        # -----------------------------------------------------

        extracted_text = note.get(
            "extracted_text",
            ""
        )

        # -----------------------------------------------------
        # 7. Weak topics
        # -----------------------------------------------------

        weak_topics = result.get(
            "weak_topics",
            []
        )

        weak_concept_names = []

        for item in weak_topics:

            if isinstance(
                item,
                dict
            ):

                concept = item.get(
                    "concept",
                    ""
                )

            else:

                concept = str(
                    item
                )

            if concept:

                concept = concept.strip()

                if concept:

                    weak_concept_names.append(
                        concept
                    )

        # -----------------------------------------------------
        # 8. Generate adaptive quiz
        # -----------------------------------------------------

        if weak_concept_names:

            next_quiz = (
                QuizService.generate_adaptive_quiz(
                    text=extracted_text,
                    weak_topics=weak_concept_names,
                    number_of_questions=next_question_count,
                    difficulty=next_level
                )
            )

        else:

            next_quiz = (
                QuizService.generate_quiz(
                    text=extracted_text,
                    number_of_questions=next_question_count,
                    difficulty=next_level
                )
            )

        # -----------------------------------------------------
        # 9. Generate weak-topic flashcards
        # -----------------------------------------------------

        weak_topic_flashcards = (
            WeakTopicFlashcardService.generate_flashcards(
                extracted_text,
                weak_topics
            )
        )

        # -----------------------------------------------------
        # 10. Add next quiz
        # -----------------------------------------------------

        result[
            "next_quiz"
        ] = {

            "level":
                next_level,

            "question_count":
                next_question_count,

            "focus_topics":
                weak_concept_names,

            "quiz":
                next_quiz
        }

        # -----------------------------------------------------
        # 11. Add weak-topic flashcards
        # -----------------------------------------------------

        result[
            "weak_topic_flashcards"
        ] = weak_topic_flashcards

        # -----------------------------------------------------
        # 12. Return
        # -----------------------------------------------------

        return result