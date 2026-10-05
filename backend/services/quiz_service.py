import re
import random

from services.difficulty_service import DifficultyService


class QuizService:

    # =========================================================
    # SENTENCE PROCESSING
    # =========================================================

    @staticmethod
    def split_sentences(text):
        """
        Split extracted note text into reasonably usable sentences.
        Removes excessive whitespace and ignores very short fragments.
        """

        if not text:
            return []

        text = re.sub(r"\s+", " ", text).strip()

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        cleaned = []

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence.split()) >= 5:
                cleaned.append(sentence)

        return cleaned

    # =========================================================
    # CLEAN PDF TEXT
    # =========================================================

    @staticmethod
    def clean_pdf_artifacts(sentence):
        """
        Remove common PDF/header/footer noise.
        """

        if not sentence:
            return ""

        # Remove common academic PDF header fragments
        patterns = [
            r"WEB TECHNOLOGIES\s+RGMCET\s+CSE DEPT\s+\d+",
            r"WEB TECHNOLOGIES\s+RGMCET\s+CSE DEPT",
            r"RAJEEV GANDHI MEMORIAL COLLEGE OF ENGG\.?\s*&?\s*TECH\.?.*?",
            r"AUTONOMOUS DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
            r"LECTURE NOTES ON WEB TECHNOLOGIES",
            r"III B\.TECH-II SEM",
            r"UNIT\s*[-–]?\s*[IVX]+",
            r"CSE DEPT\s+\d+"
        ]

        cleaned = sentence

        for pattern in patterns:
            cleaned = re.sub(
                pattern,
                " ",
                cleaned,
                flags=re.IGNORECASE
            )

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned
        ).strip()

        return cleaned

    # =========================================================
    # INVALID CONCEPT CHECK
    # =========================================================

    @staticmethod
    def is_valid_concept(concept):
        """
        Reject concepts that are usually PDF noise or meaningless
        academic metadata.
        """

        if not concept:
            return False

        concept = concept.strip()

        if len(concept) < 2:
            return False

        # Mostly numeric
        if re.fullmatch(r"[\d\s\-–./]+", concept):
            return False

        # Common noise
        invalid_terms = {
            "iii",
            "ii",
            "iv",
            "unit",
            "dept",
            "department",
            "cse",
            "ece",
            "eee",
            "me",
            "tech",
            "technologies",
            "program",
            "development",
            "introduction",
            "rgmcet",
            "gprec",
            "gpcet",
            "each client",
            "type",
            "path"
        }

        if concept.lower() in invalid_terms:
            return False

        # Too short acronym-like fragments except known useful terms
        allowed_short = {
            "HTML",
            "XML",
            "CSS",
            "JSP",
            "URL",
            "URI",
            "HTTP",
            "HTTPS",
            "JDBC",
            "ODBC",
            "DOM",
            "SAX",
            "XSL",
            "XSLT",
            "DTD",
            "CGI",
            "MVC",
            "API",
            "RMI",
            "MIME",
            "IDE",
            "JDK"
        }

        if len(concept) <= 3 and concept.upper() not in allowed_short:
            return False

        return True

    # =========================================================
    # FIND RELEVANT SENTENCE
    # =========================================================

    @classmethod
    def find_sentence(cls, concept, sentences):
        """
        Find the sentence most relevant to the supplied concept.
        """

        if not concept or not sentences:
            return None

        concept_words = set(
            re.findall(
                r"\b[a-zA-Z][a-zA-Z0-9-]*\b",
                concept.lower()
            )
        )

        best_sentence = None
        best_score = 0

        for sentence in sentences:

            sentence = cls.clean_pdf_artifacts(sentence)

            if not sentence:
                continue

            sentence_words = set(
                re.findall(
                    r"\b[a-zA-Z][a-zA-Z0-9-]*\b",
                    sentence.lower()
                )
            )

            overlap = len(
                concept_words & sentence_words
            )

            # Strong preference when the actual concept appears
            if concept.lower() in sentence.lower():
                overlap += 5

            if overlap > best_score:
                best_score = overlap
                best_sentence = sentence

        return best_sentence

    # =========================================================
    # EXTRACT DEFINITION
    # =========================================================

    @staticmethod
    def extract_definition(concept, sentence):
        """
        Extract a useful definition from patterns such as:

        HTML stands for Hypertext Markup Language.
        XML is a text-based markup language.
        DOM refers to a Document Object Model.
        """

        if not concept or not sentence:
            return None

        concept = concept.strip()
        sentence = sentence.strip()

        escaped_concept = re.escape(concept)

        patterns = [

            # X stands for Y
            rf"\b{escaped_concept}\b\s+stands\s+for\s+(.+?)(?:[.!?]|$)",

            # X is Y
            rf"\b{escaped_concept}\b\s+is\s+(.+?)(?:[.!?]|$)",

            # X refers to Y
            rf"\b{escaped_concept}\b\s+refers\s+to\s+(.+?)(?:[.!?]|$)",

            # X means Y
            rf"\b{escaped_concept}\b\s+means\s+(.+?)(?:[.!?]|$)",

            # X is used for Y
            rf"\b{escaped_concept}\b\s+is\s+used\s+for\s+(.+?)(?:[.!?]|$)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                sentence,
                re.IGNORECASE
            )

            if match:

                answer = match.group(1).strip()

                answer = re.sub(
                    r"\s+",
                    " ",
                    answer
                ).strip()

                if len(answer) >= 3:
                    return answer

        return None

    # =========================================================
    # CLEAN ANSWER
    # =========================================================

    @staticmethod
    def clean_answer(answer):

        if not answer:
            return ""

        answer = re.sub(
            r"\s+",
            " ",
            answer
        ).strip()

        # Remove obvious PDF numbering
        answer = re.sub(
            r"^\s*[\d•●○]+\s*[\).:-]?\s*",
            "",
            answer
        )

        # Remove page number fragments
        answer = re.sub(
            r"\b(?:page|pg)\s*\d+\b",
            "",
            answer,
            flags=re.IGNORECASE
        )

        answer = re.sub(
            r"\s+",
            " ",
            answer
        ).strip()

        # Keep answers manageable
        if len(answer) > 280:

            answer = (
                answer[:277]
                .rsplit(" ", 1)[0]
                .rstrip()
                + "..."
            )

        return answer

    # =========================================================
    # BUILD QUESTION
    # =========================================================

    @classmethod
    def build_question(
        cls,
        concept,
        sentence,
        difficulty="beginner"
    ):
        """
        Create a question from a meaningful concept + sentence.
        """

        if not concept or not sentence:
            return None

        concept = concept.strip()

        if not cls.is_valid_concept(concept):
            return None

        sentence = cls.clean_pdf_artifacts(
            sentence
        )

        if not sentence:
            return None

        definition = cls.extract_definition(
            concept,
            sentence
        )

        # -----------------------------------------------------
        # Beginner
        # -----------------------------------------------------

        if difficulty == "beginner":

            if definition:

                question = (
                    f"What is {concept}?"
                )

                answer = cls.clean_answer(
                    definition
                )

            else:

                question = (
                    f"Which statement correctly describes "
                    f"{concept}?"
                )

                answer = cls.clean_answer(
                    sentence
                )

        # -----------------------------------------------------
        # Intermediate
        # -----------------------------------------------------

        elif difficulty == "intermediate":

            if definition:

                question = (
                    f"Which statement correctly explains "
                    f"{concept}?"
                )

                answer = cls.clean_answer(
                    definition
                )

            else:

                question = (
                    f"Which statement about {concept} "
                    f"is correct?"
                )

                answer = cls.clean_answer(
                    sentence
                )

        # -----------------------------------------------------
        # Advanced
        # -----------------------------------------------------

        else:

            if definition:

                question = (
                    f"Which statement best describes "
                    f"the purpose or role of {concept}?"
                )

                answer = cls.clean_answer(
                    definition
                )

            else:

                question = (
                    f"Which statement best explains "
                    f"the importance or use of {concept}?"
                )

                answer = cls.clean_answer(
                    sentence
                )

        if not answer:
            return None

        return {
            "question": question,
            "answer": answer,
            "concept": concept,
            "difficulty": difficulty
        }

    # =========================================================
    # CREATE WRONG OPTIONS
    # =========================================================

    @classmethod
    def create_options(
        cls,
        correct_answer,
        candidate_answers
    ):
        """
        Create exactly 4 options:
        1 correct + 3 different wrong answers.
        """

        if not correct_answer:
            return None, None

        correct_answer = cls.clean_answer(
            correct_answer
        )

        if not correct_answer:
            return None, None

        candidates = []

        if candidate_answers:

            for answer in candidate_answers:

                if not answer:
                    continue

                answer = cls.clean_answer(
                    answer
                )

                if not answer:
                    continue

                # Don't use the correct answer again
                if (
                    answer.lower()
                    == correct_answer.lower()
                ):
                    continue

                # Remove duplicate candidates
                if any(
                    answer.lower() == existing.lower()
                    for existing in candidates
                ):
                    continue

                # Don't use extremely long fragments
                if len(answer.split()) > 60:
                    continue

                candidates.append(answer)

        if len(candidates) < 3:
            return None, None

        random.shuffle(candidates)

        incorrect = candidates[:3]

        all_options = [
            correct_answer,
            incorrect[0],
            incorrect[1],
            incorrect[2]
        ]

        random.shuffle(
            all_options
        )

        labels = [
            "A",
            "B",
            "C",
            "D"
        ]

        options = {}

        correct_label = None

        for label, option in zip(
            labels,
            all_options
        ):

            options[label] = option

            if (
                option.lower()
                == correct_answer.lower()
            ):
                correct_label = label

        if not correct_label:
            return None, None

        return options, correct_label

    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    @staticmethod
    def remove_duplicate_items(items):

        unique = []

        seen_questions = set()
        seen_concepts = set()

        for item in items:

            if not isinstance(item, dict):
                continue

            question = item.get(
                "question",
                ""
            )

            concept = item.get(
                "concept",
                ""
            )

            if not question or not concept:
                continue

            question_key = (
                question.lower()
                .strip()
            )

            concept_key = (
                concept.lower()
                .strip()
            )

            if question_key in seen_questions:
                continue

            if concept_key in seen_concepts:
                continue

            seen_questions.add(
                question_key
            )

            seen_concepts.add(
                concept_key
            )

            unique.append(
                item
            )

        return unique

    # =========================================================
    # MAIN QUIZ GENERATOR
    # =========================================================
    @classmethod
    def generate_adaptive_quiz(
        cls,
        text,
        weak_topics,
        number_of_questions=15,
        difficulty="beginner"
    ):
        """
        Generate a quiz focused on the student's weak topics.
        """

        if not text or not weak_topics:
            return []

        difficulty = str(difficulty).lower().strip()

        if difficulty not in {
            "beginner",
            "intermediate",
            "advanced"
        }:
            difficulty = "beginner"

        sentences = cls.split_sentences(text)

        if not sentences:
            return []

        # -----------------------------------------------------
        # Normalize weak topics
        # -----------------------------------------------------

        valid_topics = []

        for topic in weak_topics:

            if isinstance(topic, dict):
                topic = (
                    topic.get("concept")
                    or topic.get("topic")
                    or ""
                )

            topic = str(topic).strip()

            if not topic:
                continue

            if not cls.is_valid_concept(topic):
                continue

            valid_topics.append(topic)

        # Remove duplicate topics
        unique_topics = []

        seen_topics = set()

        for topic in valid_topics:

            key = topic.lower()

            if key in seen_topics:
                continue

            seen_topics.add(key)
            unique_topics.append(topic)

        if not unique_topics:
            return []

        # -----------------------------------------------------
        # Find note sentences related to weak topics
        # -----------------------------------------------------

        topic_sentences = []

        for topic in unique_topics:

            for sentence in sentences:

                cleaned_sentence = cls.clean_pdf_artifacts(
                    sentence
                )

                if not cleaned_sentence:
                    continue

                # Topic must actually occur in the sentence
                if topic.lower() not in cleaned_sentence.lower():
                    continue

                if len(cleaned_sentence.split()) < 6:
                    continue

                topic_sentences.append(
                    (topic, cleaned_sentence)
                )

        # -----------------------------------------------------
        # Remove duplicate sentences
        # -----------------------------------------------------

        unique_pairs = []

        seen_pairs = set()

        for topic, sentence in topic_sentences:

            key = (
                topic.lower(),
                sentence.lower()
            )

            if key in seen_pairs:
                continue

            seen_pairs.add(key)

            unique_pairs.append(
                (topic, sentence)
            )

        if not unique_pairs:
            return []

        # -----------------------------------------------------
        # Build question items
        # -----------------------------------------------------

        quiz_items = []

        for topic, sentence in unique_pairs:

            item = cls.build_question(
                concept=topic,
                sentence=sentence,
                difficulty=difficulty
            )

            if not item:
                continue

            quiz_items.append(item)

        # -----------------------------------------------------
        # Remove duplicate concepts/questions
        # -----------------------------------------------------

        quiz_items = cls.remove_duplicate_items(
            quiz_items
        )

        if not quiz_items:
            return []

        # -----------------------------------------------------
        # Create answer pool
        # -----------------------------------------------------

        answer_pool = []

        for item in quiz_items:

            answer = item.get(
                "answer",
                ""
            )

            if answer:
                answer_pool.append(answer)

        # -----------------------------------------------------
        # Generate final questions
        # -----------------------------------------------------

        final_quiz = []

        for item in quiz_items:

            correct_answer = item.get(
                "answer",
                ""
            )

            if not correct_answer:
                continue

            wrong_answers = [
                answer
                for answer in answer_pool
                if answer.lower()
                != correct_answer.lower()
            ]

            options, correct_label = (
                cls.create_options(
                    correct_answer,
                    wrong_answers
                )
            )

            if not options:
                continue

            final_quiz.append({

                "question": item["question"],

                "options": options,

                "correct_answer": correct_label,

                "explanation": correct_answer,

                "concept": item["concept"],

                "difficulty": difficulty

            })

            if len(final_quiz) >= number_of_questions:
                break

        return final_quiz

    @classmethod
    def generate_quiz(
        cls,
        text,
        number_of_questions=None,
        difficulty=None
    ):
        """
        Generate an adaptive quiz.

        Beginner     -> 15
        Intermediate -> 35
        Advanced     -> 50
        """

        if not text or not text.strip():
            return []

        # -----------------------------------------------------
        # Determine difficulty automatically when not supplied
        # -----------------------------------------------------

        if not difficulty:

            difficulty_info = (
                DifficultyService.analyze_note(
                    text
                )
            )

            difficulty = (
                difficulty_info["level"]
            )

        difficulty = difficulty.lower().strip()

        if difficulty not in {
            "beginner",
            "intermediate",
            "advanced"
        }:
            difficulty = "beginner"

        # -----------------------------------------------------
        # Determine question count
        # -----------------------------------------------------

        if number_of_questions is None:

            number_of_questions = (
                DifficultyService.get_question_count(
                    difficulty
                )
            )

        # -----------------------------------------------------
        # Split and clean sentences
        # -----------------------------------------------------

        raw_sentences = cls.split_sentences(
            text
        )

        sentences = []

        for sentence in raw_sentences:

            cleaned = cls.clean_pdf_artifacts(
                sentence
            )

            if not cleaned:
                continue

            if len(cleaned.split()) < 6:
                continue

            sentences.append(
                cleaned
            )

        if not sentences:
            return []

        # -----------------------------------------------------
        # Build possible concepts from sentences
        # -----------------------------------------------------

        candidates = []

        for sentence in sentences:

            # Pattern:
            # HTML stands for Hypertext Markup Language
            match = re.search(
                r"\b([A-Za-z][A-Za-z0-9+#.-]{1,30})\b"
                r"\s+stands\s+for\s+",
                sentence,
                re.IGNORECASE
            )

            if match:

                concept = (
                    match.group(1)
                    .strip()
                )

                if cls.is_valid_concept(
                    concept
                ):
                    candidates.append(
                        (
                            concept,
                            sentence
                        )
                    )

                continue

            # Pattern:
            # XML is a text-based markup language
            match = re.search(
                r"\b([A-Za-z][A-Za-z0-9+#.-]{1,30})\b"
                r"\s+is\s+",
                sentence,
                re.IGNORECASE
            )

            if match:

                concept = (
                    match.group(1)
                    .strip()
                )

                if cls.is_valid_concept(
                    concept
                ):
                    candidates.append(
                        (
                            concept,
                            sentence
                        )
                    )

                continue

            # Pattern:
            # DOM refers to ...
            match = re.search(
                r"\b([A-Za-z][A-Za-z0-9+#.-]{1,30})\b"
                r"\s+refers\s+to\s+",
                sentence,
                re.IGNORECASE
            )

            if match:

                concept = (
                    match.group(1)
                    .strip()
                )

                if cls.is_valid_concept(
                    concept
                ):
                    candidates.append(
                        (
                            concept,
                            sentence
                        )
                    )

        # -----------------------------------------------------
        # Remove duplicate concepts
        # -----------------------------------------------------

        unique_candidates = []

        seen = set()

        for concept, sentence in candidates:

            key = concept.lower()

            if key in seen:
                continue

            seen.add(key)

            unique_candidates.append(
                (
                    concept,
                    sentence
                )
            )

        candidates = unique_candidates

        # -----------------------------------------------------
        # If definition candidates are not enough,
        # use meaningful topic-like phrases from sentences.
        # -----------------------------------------------------

        if len(candidates) < number_of_questions:

            for sentence in sentences:

                words = re.findall(
                    r"\b[A-Za-z][A-Za-z0-9+#.-]*\b",
                    sentence
                )

                if not words:
                    continue

                # Prefer capitalized / technical-looking words
                for word in words:

                    if len(word) < 3:
                        continue

                    if cls.is_valid_concept(
                        word
                    ):

                        concept = word

                        key = concept.lower()

                        if key in seen:
                            continue

                        # Make sure sentence actually discusses it
                        if (
                            concept.lower()
                            not in sentence.lower()
                        ):
                            continue

                        seen.add(key)

                        unique_candidates.append(
                            (
                                concept,
                                sentence
                            )
                        )

                        break

                if len(
                    unique_candidates
                ) >= number_of_questions:
                    break

        candidates = unique_candidates

        # -----------------------------------------------------
        # Build questions
        # -----------------------------------------------------

        quiz_items = []

        for concept, sentence in candidates:

            question_data = cls.build_question(
                concept=concept,
                sentence=sentence,
                difficulty=difficulty
            )

            if not question_data:
                continue

            quiz_items.append(
                question_data
            )

        # -----------------------------------------------------
        # Remove duplicate questions/concepts
        # -----------------------------------------------------

        quiz_items = cls.remove_duplicate_items(
            quiz_items
        )

        # -----------------------------------------------------
        # Need enough questions
        # -----------------------------------------------------

        if not quiz_items:
            return []

        # -----------------------------------------------------
        # Generate options using answers from other questions
        # -----------------------------------------------------

        answers_pool = [
            item["answer"]
            for item in quiz_items
            if item.get("answer")
        ]

        final_quiz = []

        for item in quiz_items:

            correct_answer = item["answer"]

            wrong_candidates = [
                answer
                for answer in answers_pool
                if answer.lower() != correct_answer.lower()
            ]

            options, correct_label = (
                cls.create_options(
                    correct_answer,
                    wrong_candidates
                )
            )

            if not options:
                continue

            final_quiz.append({
                "question": item["question"],
                "options": options,
                "correct_answer": correct_label,
                "explanation": correct_answer,
                "concept": item["concept"],
                "difficulty": difficulty
            })

            if len(final_quiz) >= number_of_questions:
                break

        # -----------------------------------------------------
        # Return final quiz
        # -----------------------------------------------------

        return final_quiz