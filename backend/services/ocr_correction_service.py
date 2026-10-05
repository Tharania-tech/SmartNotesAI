import re
from difflib import SequenceMatcher
from collections import Counter


class OCRCorrectionService:

    # Words that are usually safe to ignore
    STOPWORDS = {
        "the", "and", "for", "are", "was", "were",
        "with", "this", "that", "from", "have",
        "has", "had", "into", "their", "there",
        "which", "when", "where", "what", "about",
        "than", "then", "they", "them", "these",
        "those", "also", "used", "using"
    }

    # --------------------------------------------------
    # BASIC CLEANING
    # --------------------------------------------------

    @classmethod
    def clean_text(cls, text):

        if not text:
            return ""

        text = text.replace("\r\n", "\n")

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()

    # --------------------------------------------------
    # EXTRACT WORDS FROM CURRENT DOCUMENT
    # --------------------------------------------------

    @classmethod
    def get_document_vocabulary(cls, text):

        words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            text.lower()
        )

        counter = Counter(words)

        vocabulary = []

        for word, count in counter.items():

            if word in cls.STOPWORDS:
                continue

            if len(word) < 3:
                continue

            vocabulary.append(
                (word, count)
            )

        return vocabulary

    # --------------------------------------------------
    # WORD SHAPE SIMILARITY
    # --------------------------------------------------

    @classmethod
    def spelling_similarity(
        cls,
        word1,
        word2
    ):

        return SequenceMatcher(
            None,
            word1.lower(),
            word2.lower()
        ).ratio()

    # --------------------------------------------------
    # GENERATE POSSIBLE CORRECTIONS
    # --------------------------------------------------

    @classmethod
    def find_candidates(
        cls,
        word,
        vocabulary
    ):

        candidates = []

        word = word.lower()

        for candidate, frequency in vocabulary:

            # Don't compare a word with itself
            if candidate == word:
                continue

            # Length difference should not be too large
            if abs(
                len(candidate) - len(word)
            ) > 3:
                continue

            similarity = cls.spelling_similarity(
                word,
                candidate
            )

            # Candidate must be reasonably similar
            if similarity >= 0.65:

                candidates.append({
                    "word": candidate,
                    "similarity": similarity,
                    "frequency": frequency
                })

        candidates.sort(
            key=lambda x: (
                x["similarity"],
                x["frequency"]
            ),
            reverse=True
        )

        return candidates

    # --------------------------------------------------
    # CORRECT A SINGLE WORD
    # --------------------------------------------------

    @classmethod
    def correct_word(
        cls,
        word,
        vocabulary
    ):

        candidates = cls.find_candidates(
            word,
            vocabulary
        )

        if not candidates:
            return word

        best = candidates[0]

        similarity = best["similarity"]

        # High confidence
        if similarity >= 0.85:

            corrected = best["word"]

            if word[0].isupper():
                corrected = corrected.capitalize()

            return corrected

        # Medium confidence:
        # only correct if the candidate appears
        # several times in the document
        if (
            similarity >= 0.75
            and best["frequency"] >= 3
        ):

            corrected = best["word"]

            if word[0].isupper():
                corrected = corrected.capitalize()

            return corrected

        # Low confidence -> DO NOT MODIFY
        return word

    # --------------------------------------------------
    # CORRECT THE DOCUMENT
    # --------------------------------------------------

    @classmethod
    def correct_text(cls, text):

        if not text or not text.strip():
            return text

        text = cls.clean_text(
            text
        )

        vocabulary = cls.get_document_vocabulary(
            text
        )

        if not vocabulary:
            return text

        vocabulary_words = {
            word
            for word, frequency in vocabulary
        }

        def replace_word(match):

            original = match.group(0)

            lower_word = original.lower()

            # Don't modify normal words
            if lower_word in vocabulary_words:
                return original

            corrected = cls.correct_word(
                original,
                vocabulary
            )

            return corrected

        corrected_text = re.sub(
            r"\b[A-Za-z]{3,}\b",
            replace_word,
            text
        )

        return corrected_text