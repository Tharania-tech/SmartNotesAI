import json
import os
import re

from dotenv import load_dotenv
from google import genai
from services.text_chunk_service import TextChunkService

# =========================================================
# LOAD .ENV
# =========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BACKEND_DIR = os.path.dirname(
    CURRENT_DIR
)

ENV_PATH = os.path.join(
    BACKEND_DIR,
    ".env"
)

load_dotenv(
    ENV_PATH
)


class LearningContentService:

    _client = None

    MODEL_NAME = "gemini-3.6-flash"

    # =====================================================
    # GET GEMINI CLIENT
    # =====================================================

    @classmethod
    def get_client(cls):

        if cls._client is None:

            api_key = os.getenv(
                "GEMINI_API_KEY"
            )

            if not api_key:

                raise ValueError(
                    "GEMINI_API_KEY is not configured. "
                    f"Checked: {ENV_PATH}"
                )

            cls._client = genai.Client(
                api_key=api_key
            )

        return cls._client

    # =====================================================
    # PARSE JSON RESPONSE
    # =====================================================

    @staticmethod
    def parse_json(text):

        if not text:

            raise ValueError(
                "Gemini returned an empty response."
            )

        text = text.strip()

        # Remove markdown code fences
        if text.startswith("```"):

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

        try:

            return json.loads(
                text
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "Gemini returned invalid JSON.\n"
                f"Response:\n{text}"
            ) from exc

    # =====================================================
    # NORMALIZE CONCEPT
    # =====================================================

    @staticmethod
    def normalize_concept(concept):

        if not concept:
            return ""

        concept = concept.lower().strip()

        # Remove question-style suffixes
        removable_suffixes = [
            " acronym",
            " function",
            " purpose",
            " classification",
            " primary functions",
            " structural components",
            " basic concept",
            " definition",
            " overview"
        ]

        for suffix in removable_suffixes:

            if concept.endswith(suffix):

                concept = concept[
                    :-len(suffix)
                ].strip()

        # Normalize whitespace
        concept = " ".join(
            concept.split()
        )

        return concept

    # =====================================================
    # CLEAN TEXT FOR PROMPTS
    # =====================================================

    @staticmethod
    def clean_input_text(text):

        if not text:
            return ""

        text = text.replace(
            "\x00",
            " "
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =====================================================
    # GENERATE KEY CONCEPTS
    # =====================================================
    @classmethod
    def generate_keywords(cls, text, count=15):
        """
        Generate meaningful study concepts from large text.

        The text is divided into chunks, Gemini analyzes each chunk,
        and the results are combined and cleaned before returning.
        """

        chunks = TextChunkService.chunk_text(
            text,
            max_words=700,
            overlap_words=100
        )

        if not chunks:
            return []

        print(f"Total chunks: {len(chunks)}")

        # Temporarily process only 5 chunks for testing
        chunks = chunks[:5]

        all_keywords = []

        for index, chunk in enumerate(chunks, start=1):

            print(f"Processing chunk {index}/{len(chunks)}...")

            prompt = f"""
You are an expert academic note analyzer.

Analyze the following study material and extract the most important
concepts that a student should remember.

Rules:
- Return only genuine academic or technical concepts.
- Each concept must be short: 1 to 4 words.
- Prefer important topics, technologies, definitions, components,
  methods, protocols, or major ideas.
- Do NOT return complete sentences.
- Do NOT return generic words.
- Do NOT return code fragments.
- Do NOT return HTML/XML tags.
- Do NOT return duplicate concepts.
- Do NOT invent concepts that are not supported by the notes.
- Return JSON only.

Study material:
{chunk}

Return this exact format:

{{
    "keywords": [
        "concept 1",
        "concept 2",
        "concept 3"
    ]
}}
"""

            try:

                response = cls.get_client().models.generate_content(
                    model=cls.MODEL_NAME,
                    contents=prompt
                )

                print(
                    f"Gemini response received for chunk {index}"
                )

                parsed = cls.parse_json(response.text)

                if not parsed:
                    continue

                keywords = parsed.get("keywords", [])

                if isinstance(keywords, list):
                    all_keywords.extend(keywords)

            except Exception as e:

                print(
                    f"Keyword generation failed for chunk {index}: {e}"
                )

        # =====================================================
        # CLEAN AND REMOVE DUPLICATES
        # =====================================================

        final_keywords = []
        seen = set()

        blocked_words = {
            "information",
            "system",
            "process",
            "method",
            "example",
            "object",
            "data",
            "thing",
            "user",
            "client",
            "source"
        }

        for keyword in all_keywords:

            keyword = str(keyword).strip()

            if not keyword:
                continue

            keyword = cls.normalize_concept(keyword)

            if not keyword:
                continue

            # Maximum 4 words
            if len(keyword.split()) > 4:
                continue

            # Remove generic words
            if keyword.lower() in blocked_words:
                continue

            key = keyword.lower()

            # Remove exact duplicates
            if key in seen:
                continue

            seen.add(key)
            final_keywords.append(keyword)

        print("\n========================================")
        print("FINAL KEY CONCEPTS")
        print("========================================")

        for number, keyword in enumerate(final_keywords, start=1):
            print(f"{number}. {keyword}")

        print("========================================")

        return final_keywords[:count]

    # =====================================================
    # GENERATE QUIZ
    # =====================================================

    @classmethod
    def generate_quiz(
        cls,
        text,
        count=20
    ):

        if not text or not text.strip():

            raise ValueError(
                "Study text cannot be empty."
            )

        text = cls.clean_input_text(
            text
        )

        client = cls.get_client()

        prompt = f"""
You are an expert educational quiz generator.

Read ONLY the study notes below.

Create exactly {count} high-quality multiple-choice
questions when there is enough information.

IMPORTANT GOAL:

Every question must test a DIFFERENT important concept.

Rules:

1. Use ONLY information supported by the notes.
2. Do not invent facts.
3. Do not use college names or metadata.
4. Do not use page numbers.
5. Do not use headers or footers.
6. Do not create questions from code examples unless
   the underlying technical concept is being taught.
7. Do not repeat or nearly repeat questions.
8. Cover different topics and sections.
9. Use simple student-friendly English.
10. Exactly four options: A, B, C, D.
11. Exactly one correct answer.
12. Do not use "All of the above".
13. Do not use "None of the above".
14. Add a short explanation.
15. Include the concept being tested.
16. Return JSON only.

If the notes do not contain enough distinct information
for {count} valid questions, return only the number that
can be supported. Do NOT invent questions.

JSON FORMAT:

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
            "explanation": "Short explanation based on the notes.",
            "concept": "Main concept"
        }}
    ]
}}

STUDY NOTES:

{text}
"""

        response = client.models.generate_content(
            model=cls.MODEL_NAME,
            contents=prompt
        )

        result = cls.parse_json(
            response.text
        )

        quiz = result.get(
            "quiz",
            []
        )

        if not isinstance(
            quiz,
            list
        ):

            raise ValueError(
                "Invalid quiz format."
            )

        valid_quiz = []

        seen_questions = set()
        seen_concepts = set()

        for item in quiz:

            if not isinstance(
                item,
                dict
            ):
                continue

            question = str(
                item.get(
                    "question",
                    ""
                )
            ).strip()

            options = item.get(
                "options",
                {}
            )

            correct_answer = str(
                item.get(
                    "correct_answer",
                    ""
                )
            ).strip().upper()

            explanation = str(
                item.get(
                    "explanation",
                    ""
                )
            ).strip()

            concept = str(
                item.get(
                    "concept",
                    ""
                )
            ).strip()

            if not question:
                continue

            if not isinstance(
                options,
                dict
            ):
                continue

            required = {
                "A",
                "B",
                "C",
                "D"
            }

            if set(options.keys()) != required:
                continue

            if correct_answer not in required:
                continue

            if not explanation or not concept:
                continue

            normalized_question = (
                " ".join(
                    question.lower().split()
                )
            )

            if normalized_question in seen_questions:
                continue

            normalized_concept = (
                cls.normalize_concept(
                    concept
                )
            )

            # At most one question per concept
            if normalized_concept in seen_concepts:
                continue

            option_values = [
                str(
                    options[key]
                ).strip()
                for key in [
                    "A",
                    "B",
                    "C",
                    "D"
                ]
            ]

            if any(
                not value
                for value in option_values
            ):
                continue

            normalized_options = [
                value.lower()
                for value in option_values
            ]

            if len(
                set(normalized_options)
            ) != 4:
                continue

            # Reject all/none above
            if any(
                value.lower()
                in {
                    "all of the above",
                    "none of the above"
                }
                for value in option_values
            ):
                continue

            explanation = " ".join(
                explanation.split()
            )

            if len(explanation) > 300:

                explanation = (
                    explanation[:297]
                    .rstrip()
                    + "..."
                )

            seen_questions.add(
                normalized_question
            )

            seen_concepts.add(
                normalized_concept
            )

            valid_quiz.append({
                "question": question,
                "options": {
                    "A": option_values[0],
                    "B": option_values[1],
                    "C": option_values[2],
                    "D": option_values[3]
                },
                "correct_answer": correct_answer,
                "explanation": explanation,
                "concept": concept
            })

            if len(valid_quiz) >= count:
                break

        return valid_quiz

    # =====================================================
    # GENERATE FLASHCARDS
    # =====================================================

    @classmethod
    def generate_flashcards(
        cls,
        text,
        count=20
    ):

        if not text or not text.strip():

            raise ValueError(
                "Study text cannot be empty."
            )

        text = cls.clean_input_text(
            text
        )

        client = cls.get_client()

        prompt = f"""
You are an expert educational flashcard generator.

Read ONLY the study notes below.

Generate exactly {count} flashcards if the notes
contain enough distinct concepts.

VERY IMPORTANT:

Each flashcard must test ONE UNIQUE CONCEPT.

Do not generate multiple cards for different aspects
of the same concept.

For example, these should NOT all be separate cards:

HTML acronym
HTML purpose
HTML function
HTML usage
HTML structure

These are variations of one concept: HTML.

Instead, use different concepts such as:

HTML
CSS
JavaScript
XML
JSP
HTTP Request
HTTP Response
Web Server
Servlet API
XML Schema

Rules:

1. Use ONLY information supported by the notes.
2. Do not invent facts.
3. One concept per card.
4. Avoid duplicate concepts.
5. Avoid nearly identical questions.
6. Cover different parts of the notes.
7. Use simple student-friendly English.
8. Front should be a clear question.
9. Back should be a concise answer.
10. Do not include college names.
11. Do not include page numbers.
12. Do not include headers or footers.
13. Do not use source-code fragments as concepts.
14. Do not create cards from random example code.
15. Return JSON only.

If there are not enough distinct concepts for {count}
flashcards, return only the number that can be supported.
Do NOT invent cards just to reach the requested count.

FORMAT:

{{
    "flashcards": [
        {{
            "concept": "HTML",
            "front": "What does HTML stand for?",
            "back": "HyperText Markup Language."
        }}
    ]
}}

STUDY NOTES:

{text}
"""

        response = client.models.generate_content(
            model=cls.MODEL_NAME,
            contents=prompt
        )

        result = cls.parse_json(
            response.text
        )

        flashcards = result.get(
            "flashcards",
            []
        )

        if not isinstance(
            flashcards,
            list
        ):

            raise ValueError(
                "Invalid flashcard format."
            )

        valid_cards = []

        seen_concepts = set()
        seen_fronts = set()

        for item in flashcards:

            if not isinstance(
                item,
                dict
            ):
                continue

            concept = str(
                item.get(
                    "concept",
                    ""
                )
            ).strip()

            front = str(
                item.get(
                    "front",
                    ""
                )
            ).strip()

            back = str(
                item.get(
                    "back",
                    ""
                )
            ).strip()

            if not concept:
                continue

            if not front:
                continue

            if not back:
                continue

            concept_key = cls.normalize_concept(
                concept
            )

            front_key = (
                " ".join(
                    front.lower().split()
                )
            )

            if not concept_key:
                continue

            # Exact duplicate concept
            if concept_key in seen_concepts:
                continue

            # Exact duplicate question
            if front_key in seen_fronts:
                continue

            # -----------------------------------------
            # Avoid concept variants
            # -----------------------------------------

            concept_words = set(
                concept_key.split()
            )

            variant_duplicate = False

            for existing in seen_concepts:

                existing_words = set(
                    existing.split()
                )

                if (
                    concept_words.issubset(
                        existing_words
                    )
                    or
                    existing_words.issubset(
                        concept_words
                    )
                ):

                    variant_duplicate = True
                    break

            if variant_duplicate:
                continue

            # -----------------------------------------
            # Clean answer
            # -----------------------------------------

            back = " ".join(
                back.split()
            )

            if len(back) > 350:

                back = (
                    back[:347]
                    .rstrip()
                    + "..."
                )

            # -----------------------------------------
            # Save
            # -----------------------------------------

            seen_concepts.add(
                concept_key
            )

            seen_fronts.add(
                front_key
            )

            valid_cards.append({
                "concept": concept,
                "front": front,
                "back": back
            })

            if len(valid_cards) >= count:
                break

        return valid_cards