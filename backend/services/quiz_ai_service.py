import json
import re
from ollama import chat


class QuizAIService:

    MODEL_NAME = "qwen2.5:3b-instruct-q4_0"

    @staticmethod
    def generate_questions(
        content,
        number_of_questions=5,
        difficulty="intermediate"
    ):

        if not content or not content.strip():
            return []

        prompt = f"""
You are an educational quiz generator.

Create exactly {number_of_questions} multiple-choice
questions from the study material below.

Difficulty:
{difficulty}

STRICT RULES:

1. Questions must be based ONLY on the supplied study material.
2. Do not use outside knowledge.
3. Do not use document footer, header, page number,
   email, URL, copyright text, navigation text,
   assessment metadata, or unrelated repeated text.
4. Every question must have exactly 4 options.
5. Option labels must be A, B, C and D.
6. Exactly ONE option must be correct.
7. "correct_answer" must contain only A, B, C or D.
8. The correct_answer must match one of the four options.
9. Options must be meaningful and related to the question.
10. Do not make the correct answer always the same letter.
11. Return ONLY valid JSON.
12. Do not include markdown.
13. Do not include explanations outside the JSON.

Return exactly this structure:

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
      "explanation": "Why this answer is correct.",
      "concept": "Main concept",
      "difficulty": "{difficulty}"
    }}
  ]
}}

STUDY MATERIAL:
{content}
"""

        try:
            response = chat(
                model=QuizAIService.MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.2,
                    "num_predict": 1800
                }
            )

            text = response["message"]["content"]

            return QuizAIService.parse_json(text)

        except Exception as e:
            print("Quiz AI error:", str(e))
            return []

    @staticmethod
    def parse_json(text):

        if not text:
            return []

        text = text.strip()

        text = re.sub(
            r"^```json\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"^```\s*",
            "",
            text
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        try:
            data = json.loads(text)

            if isinstance(data, dict):
                quiz = data.get("quiz", [])

                if isinstance(quiz, list):
                    return quiz

        except json.JSONDecodeError:
            pass

        return []