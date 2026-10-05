class AdaptiveQuizService:

    @staticmethod
    def determine_level(score_percentage):
        """
        Determine the next quiz difficulty based on the student's score.
        """

        if score_percentage < 60:
            return "beginner"

        elif score_percentage < 80:
            return "intermediate"

        else:
            return "advanced"

    @staticmethod
    def get_question_count(level):
        """
        Return the number of questions for each difficulty.
        """

        question_counts = {
            "beginner": 15,
            "intermediate": 35,
            "advanced": 50
        }

        return question_counts.get(level, 15)

    @classmethod
    def get_next_quiz_level(cls, score_percentage):
        """
        Return level + question count for the next quiz.
        """

        level = cls.determine_level(score_percentage)
        question_count = cls.get_question_count(level)

        return {
            "level": level,
            "question_count": question_count
        }