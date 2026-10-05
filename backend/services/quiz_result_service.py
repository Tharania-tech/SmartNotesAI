import re


class QuizResultService:

    # =========================================================
    # VALID EDUCATIONAL CONCEPTS
    # =========================================================

    VALID_CONCEPTS = {
        "html",
        "css",
        "javascript",
        "xml",
        "xhtml",
        "dhtml",
        "dom",
        "http",
        "https",
        "url",
        "uri",
        "api",
        "jdbc",
        "odbc",
        "jsp",
        "servlets",
        "servlet",
        "cgi",
        "rmi",
        "sax",
        "xpath",
        "xsl",
        "xslt",
        "dtd",
        "xsd",
        "mvc",
        "mime",
        "ide",
        "jdk",
        "java",
        "web",
        "web technologies",
        "html tags",
        "attributes",
        "xml schema",
        "httpservletrequest",
        "httpservletresponse"
    }

    # =========================================================
    # CHECK VALID CONCEPT
    # =========================================================

    @classmethod
    def is_valid_concept(cls, concept):

        if not concept:
            return False

        concept = str(concept).strip()

        if not concept:
            return False

        normalized = concept.lower()

        # Direct known concept
        if normalized in cls.VALID_CONCEPTS:
            return True

        # Remove punctuation and compare again
        normalized_clean = re.sub(
            r"[^a-z0-9+#.-]+",
            " ",
            normalized
        )

        normalized_clean = re.sub(
            r"\s+",
            " ",
            normalized_clean
        ).strip()

        if normalized_clean in cls.VALID_CONCEPTS:
            return True

        # Reject normal English words
        invalid_words = {
            "a",
            "an",
            "the",
            "this",
            "that",
            "these",
            "those",
            "which",
            "what",
            "where",
            "when",
            "why",
            "how",
            "who",
            "statement",
            "concept",
            "page",
            "pages",
            "size",
            "list",
            "effective",
            "anchor",
            "button",
            "element",
            "format",
            "selector",
            "sheet",
            "there",
            "here",
            "model",
            "code",
            "interpreter",
            "script",
            "browser",
            "file",
            "function",
            "expression",
            "condition",
            "method",
            "event",
            "form",
            "object",
            "time",
            "array",
            "capability",
            "validation",
            "language",
            "document",
            "data",
            "value",
            "attributes",
            "schema",
            "path",
            "program",
            "development",
            "introduction",
            "technology",
            "technologies",
            "type"
        }

        if normalized_clean in invalid_words:
            return False

        return False

    # =========================================================
    # EVALUATE QUIZ
    # =========================================================

    @classmethod
    def evaluate_quiz(cls, quiz, answers):

        if not quiz:
            return {
                "total_questions": 0,
                "correct": 0,
                "incorrect": 0,
                "unanswered": 0,
                "score_percentage": 0,
                "performance": "Needs Improvement",
                "topic_results": [],
                "weak_topics": [],
                "question_results": []
            }

        if not answers:
            answers = {}

        total_questions = len(quiz)

        correct = 0
        incorrect = 0
        unanswered = 0

        question_results = []

        # Topic statistics
        topic_stats = {}

        # =====================================================
        # PROCESS EACH QUESTION
        # =====================================================

        for index, question in enumerate(
            quiz,
            start=1
        ):

            question_number = str(index)

            selected_answer = answers.get(
                question_number
            )

            correct_answer = question.get(
                "correct_answer"
            )

            concept = question.get(
                "concept",
                "General"
            )

            # Normalize concept
            concept = str(
                concept
            ).strip()

            # -------------------------------------------------
            # Determine answer status
            # -------------------------------------------------

            if not selected_answer:

                status = "unanswered"

                unanswered += 1

            elif (
                str(selected_answer).strip().upper()
                ==
                str(correct_answer).strip().upper()
            ):

                status = "correct"

                correct += 1

            else:

                status = "incorrect"

                incorrect += 1

            # -------------------------------------------------
            # Question result
            # -------------------------------------------------

            question_results.append({

                "question_number": index,

                "concept": concept,

                "selected_answer": selected_answer,

                "correct_answer": correct_answer,

                "is_correct": (
                    status == "correct"
                )
            })

            # -------------------------------------------------
            # Topic statistics
            # -------------------------------------------------

            if concept not in topic_stats:

                topic_stats[concept] = {
                    "total": 0,
                    "correct": 0,
                    "incorrect": 0
                }

            topic_stats[concept]["total"] += 1

            if status == "correct":

                topic_stats[concept]["correct"] += 1

            elif status == "incorrect":

                topic_stats[concept]["incorrect"] += 1

        # =====================================================
        # SCORE
        # =====================================================

        if total_questions > 0:

            score_percentage = round(
                (correct / total_questions) * 100,
                2
            )

        else:

            score_percentage = 0

        # =====================================================
        # PERFORMANCE
        # =====================================================

        if score_percentage >= 90:

            performance = "Excellent"

        elif score_percentage >= 75:

            performance = "Good"

        elif score_percentage >= 60:

            performance = "Average"

        else:

            performance = "Needs Improvement"

        # =====================================================
        # TOPIC RESULTS
        # =====================================================

        topic_results = []

        weak_topics = []

        for concept, stats in topic_stats.items():

            # Ignore meaningless concepts
            if not cls.is_valid_concept(
                concept
            ):
                continue

            topic_total = stats["total"]

            topic_correct = stats["correct"]

            topic_incorrect = stats["incorrect"]

            if topic_total > 0:

                percentage = round(
                    (topic_correct / topic_total) * 100,
                    2
                )

            else:

                percentage = 0

            # -------------------------------------------------
            # Topic status
            # -------------------------------------------------

            if percentage < 60:

                topic_status = "weak"

            elif percentage < 80:

                topic_status = "needs_practice"

            else:

                topic_status = "strong"

            topic_result = {

                "concept": concept,

                "total": topic_total,

                "correct": topic_correct,

                "incorrect": topic_incorrect,

                "percentage": percentage,

                "status": topic_status
            }

            topic_results.append(
                topic_result
            )

            # -------------------------------------------------
            # Weak topics
            # -------------------------------------------------

            if topic_status == "weak":

                weak_topics.append(
                    topic_result
                )

        # =====================================================
        # SORT TOPICS
        # Weakest first
        # =====================================================

        topic_results.sort(
            key=lambda item: item["percentage"]
        )

        weak_topics.sort(
            key=lambda item: item["percentage"]
        )

        # =====================================================
        # FINAL RESULT
        # =====================================================

        return {

            "total_questions": total_questions,

            "correct": correct,

            "incorrect": incorrect,

            "unanswered": unanswered,

            "score_percentage": score_percentage,

            "performance": performance,

            "topic_results": topic_results,

            "weak_topics": weak_topics,

            "question_results": question_results
        }