from datetime import datetime, timezone

from database.db import mongo


class ProgressModel:

    # =========================================================
    # SAVE QUIZ ATTEMPT
    # =========================================================

    @staticmethod
    def create_quiz_attempt(
        user_id,
        note_id,
        quiz,
        answers,
        result
    ):

        topic_performance = (
            ProgressModel.calculate_topic_performance(
                quiz,
                answers
            )
        )

        weak_topics = []

        raw_weak_topics = (
            result.get(
                "weak_topics",
                []
            )
            if isinstance(
                result,
                dict
            )
            else []
        )

        for item in raw_weak_topics:

            if isinstance(
                item,
                dict
            ):

                concept = (
                    item.get(
                        "concept",
                        ""
                    )
                )

            else:

                concept = str(
                    item
                )

            concept = str(
                concept
            ).strip()

            if concept:

                weak_topics.append(
                    concept
                )

        document = {

            "user_id":
                str(
                    user_id
                ),

            "note_id":
                str(
                    note_id
                ),

            "score_percentage":
                float(
                    result.get(
                        "score_percentage",
                        0
                    )
                ),

            "correct_answers":
                int(
                    result.get(
                        "correct_answers",
                        0
                    )
                ),

            "wrong_answers":
                int(
                    result.get(
                        "wrong_answers",
                        0
                    )
                ),

            "total_questions":
                int(
                    result.get(
                        "total_questions",
                        len(quiz)
                    )
                ),

            "difficulty":
                str(
                    result.get(
                        "difficulty",
                        "intermediate"
                    )
                ),

            "weak_topics":
                weak_topics,

            "topic_performance":
                topic_performance,

            "submitted_at":
                datetime.now(
                    timezone.utc
                )
        }

        return mongo.db.quiz_attempts.insert_one(
            document
        )


    # =========================================================
    # CALCULATE TOPIC PERFORMANCE
    # =========================================================

    @staticmethod
    def calculate_topic_performance(
        quiz,
        answers
    ):

        if not isinstance(
            quiz,
            list
        ):

            return []

        if not isinstance(
            answers,
            dict
        ):

            answers = {}

        topic_data = {}

        for index, question in enumerate(
            quiz
        ):

            if not isinstance(
                question,
                dict
            ):

                continue

            concept = (
                question.get(
                    "concept",
                    "General"
                )
            )

            concept = str(
                concept
            ).strip()

            if not concept:

                concept = "General"

            correct_answer = (
                question.get(
                    "correct_answer",
                    question.get(
                        "correctAnswer",
                        ""
                    )
                )
            )

            correct_answer = str(
                correct_answer
            ).strip().upper()

            user_answer = (
                ProgressModel.get_user_answer(
                    answers,
                    index
                )
            )

            if concept not in topic_data:

                topic_data[concept] = {

                    "concept":
                        concept,

                    "total_questions":
                        0,

                    "correct_answers":
                        0
                }

            topic_data[concept][
                "total_questions"
            ] += 1

            if (
                user_answer
                and
                correct_answer
                and
                user_answer
                == correct_answer
            ):

                topic_data[concept][
                    "correct_answers"
                ] += 1

        result = []

        for concept in topic_data:

            item = (
                topic_data[
                    concept
                ]
            )

            total_questions = (
                item[
                    "total_questions"
                ]
            )

            correct_answers = (
                item[
                    "correct_answers"
                ]
            )

            accuracy = 0

            if total_questions > 0:

                accuracy = (
                    correct_answers
                    /
                    total_questions
                ) * 100

            result.append({

                "concept":
                    concept,

                "total_questions":
                    total_questions,

                "correct_answers":
                    correct_answers,

                "accuracy_percentage":
                    round(
                        accuracy,
                        2
                    )
            })

        return result


    # =========================================================
    # GET USER ANSWER
    # =========================================================

    @staticmethod
    def get_user_answer(
        answers,
        index
    ):

        # -----------------------------------------------------
        # One-based key
        # Example: question 1 -> "1"
        # -----------------------------------------------------

        one_based_key = str(
            index + 1
        )

        if (
            one_based_key
            in answers
        ):

            return str(
                answers[
                    one_based_key
                ]
            ).strip().upper()


        # -----------------------------------------------------
        # Numeric one-based key
        # -----------------------------------------------------

        one_based_number = (
            index + 1
        )

        if (
            one_based_number
            in answers
        ):

            return str(
                answers[
                    one_based_number
                ]
            ).strip().upper()


        # -----------------------------------------------------
        # Zero-based fallback
        # -----------------------------------------------------

        zero_based_key = str(
            index
        )

        if (
            zero_based_key
            in answers
        ):

            return str(
                answers[
                    zero_based_key
                ]
            ).strip().upper()


        # -----------------------------------------------------
        # Numeric zero-based fallback
        # -----------------------------------------------------

        if (
            index
            in answers
        ):

            return str(
                answers[
                    index
                ]
            ).strip().upper()


        return ""