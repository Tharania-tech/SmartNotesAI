import re


class DifficultyService:

    # ---------------------------------------------------------
    # QUESTION COUNT BY LEVEL
    # ---------------------------------------------------------

    QUESTION_COUNTS = {
        "beginner": 15,
        "intermediate": 35,
        "advanced": 50
    }

    # ---------------------------------------------------------
    # ANALYZE NOTE
    # ---------------------------------------------------------

    @classmethod
    def analyze_note(cls, text):

        if not text or not text.strip():
            return {
                "level": "beginner",
                "question_count": 15,
                "score": 0
            }

        words = re.findall(
            r"\b[A-Za-z][A-Za-z0-9-]*\b",
            text
        )

        word_count = len(words)

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        sentences = [
            s.strip()
            for s in sentences
            if len(s.split()) >= 5
        ]

        sentence_count = len(sentences)

        # -----------------------------------------------------
        # TECHNICAL TERM ESTIMATION
        # -----------------------------------------------------

        technical_patterns = [
            r"\b[A-Z]{2,}\b",
            r"\b[A-Za-z]+(?:API|SQL|XML|HTML|HTTP|JSP)\b",
            r"\b(?:algorithm|architecture|framework|protocol|"
            r"database|interface|inheritance|encapsulation|"
            r"polymorphism|abstraction|authentication|"
            r"normalization|recursion|optimization)\b"
        ]

        technical_matches = set()

        for pattern in technical_patterns:

            matches = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            for match in matches:
                technical_matches.add(
                    match.lower()
                )

        technical_count = len(
            technical_matches
        )

        # -----------------------------------------------------
        # DEFINITION COUNT
        # -----------------------------------------------------

        definition_count = len(
            re.findall(
                r"\bstands for\b|\bis defined as\b|"
                r"\brefers to\b|\bis a\b|\bis an\b",
                text,
                flags=re.IGNORECASE
            )
        )

        # -----------------------------------------------------
        # COMPLEXITY INDICATORS
        # -----------------------------------------------------

        score = 0

        # Length
        if word_count >= 2500:
            score += 25
        elif word_count >= 1200:
            score += 15
        elif word_count >= 500:
            score += 8

        # Number of sentences
        if sentence_count >= 250:
            score += 20
        elif sentence_count >= 120:
            score += 12
        elif sentence_count >= 50:
            score += 6

        # Technical concepts
        if technical_count >= 40:
            score += 30
        elif technical_count >= 20:
            score += 20
        elif technical_count >= 8:
            score += 10

        # Definitions
        if definition_count >= 40:
            score += 15
        elif definition_count >= 20:
            score += 10
        elif definition_count >= 5:
            score += 5

        # -----------------------------------------------------
        # DETERMINE LEVEL
        # -----------------------------------------------------

        if score >= 55:

            level = "advanced"

        elif score >= 30:

            level = "intermediate"

        else:

            level = "beginner"

        return {
            "level": level,
            "question_count": cls.QUESTION_COUNTS[level],
            "score": score,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "technical_count": technical_count,
            "definition_count": definition_count
        }

    # ---------------------------------------------------------
    # GET QUESTION COUNT
    # ---------------------------------------------------------

    @classmethod
    def get_question_count(cls, level):

        level = level.lower().strip()

        return cls.QUESTION_COUNTS.get(
            level,
            15
        )