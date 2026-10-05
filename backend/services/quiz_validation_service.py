class QuizValidationService:

    VALID_LETTERS = {
        "A",
        "B",
        "C",
        "D"
    }

    @staticmethod
    def validate_question(question):

        if not isinstance(question, dict):
            return False

        question_text = question.get(
            "question",
            ""
        )

        options = question.get(
            "options",
            {}
        )

        correct_answer = question.get(
            "correct_answer",
            ""
        )

        if not question_text:
            return False

        if not isinstance(options, dict):
            return False

        if set(options.keys()) != {
            "A",
            "B",
            "C",
            "D"
        }:
            return False

        for value in options.values():

            if not isinstance(value, str):
                return False

            if not value.strip():
                return False

        if correct_answer not in (
            QuizValidationService.VALID_LETTERS
        ):
            return False

        correct_text = options[
            correct_answer
        ].strip().lower()

        option_texts = [
            value.strip().lower()
            for value in options.values()
        ]

        if len(set(option_texts)) != 4:
            return False

        if correct_text not in option_texts:
            return False

        return True

    @staticmethod
    def validate_quiz(quiz):

        valid_questions = []

        for question in quiz:

            if QuizValidationService.validate_question(
                question
            ):
                valid_questions.append(
                    question
                )

        return valid_questions
    