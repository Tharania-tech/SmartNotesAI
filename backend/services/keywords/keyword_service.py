import re
import math
from collections import Counter

from sentence_transformers import SentenceTransformer


class KeywordService:

    _model = None

    # -------------------------------------------------
    # LOAD MODEL ONCE
    # -------------------------------------------------

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print(
                "Loading keyword embedding model..."
            )

            cls._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            print(
                "Keyword model loaded successfully."
            )

        return cls._model

    # -------------------------------------------------
    # STOP WORDS
    # -------------------------------------------------

    STOPWORDS = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "if",
        "then",
        "than",
        "this",
        "that",
        "these",
        "those",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "of",
        "to",
        "in",
        "on",
        "at",
        "by",
        "for",
        "from",
        "with",
        "without",
        "as",
        "into",
        "through",
        "during",
        "about",
        "between",
        "after",
        "before",
        "over",
        "under",
        "above",
        "below",
        "can",
        "could",
        "may",
        "might",
        "must",
        "should",
        "would",
        "will",
        "shall",
        "do",
        "does",
        "did",
        "have",
        "has",
        "had",
        "having",
        "not",
        "only",
        "also",
        "very",
        "more",
        "most",
        "some",
        "such",
        "any",
        "each",
        "every",
        "all",
        "both",
        "either",
        "neither",
        "other",
        "another",
        "same",
        "different",

        # Educational/generic words
        "question",
        "questions",
        "answer",
        "answers",
        "example",
        "examples",
        "following",
        "given",
        "note",
        "notes",
        "page",
        "pages",
        "chapter",
        "unit",
        "section",
        "figure",
        "table",
        "shown",
        "used",
        "use",
        "using",
        "called",
        "known",
        "means",
        "make",
        "made",
        "important",
        "following",
        "explain",
        "describe",
        "define",
        "definition",
        "mention",
        "discuss"
    }

    # -------------------------------------------------
    # OCR / GARBAGE DETECTION
    # -------------------------------------------------

    @classmethod
    def is_valid_word(cls, word):

        word = word.lower().strip()

        if len(word) < 3:
            return False

        if word in cls.STOPWORDS:
            return False

        # Must contain alphabetic characters
        if not re.search(
            r"[a-zA-Z]",
            word
        ):
            return False

        # Reject words with excessive numbers
        digit_count = sum(
            char.isdigit()
            for char in word
        )

        if digit_count > 1:
            return False

        # Reject extremely strange character patterns
        if re.search(
            r"(.)\1\1\1",
            word
        ):
            return False

        return True

    # -------------------------------------------------
    # CLEAN TEXT
    # -------------------------------------------------

    @classmethod
    def clean_text(cls, text):

        if not text:
            return ""

        # Normalize new lines
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        # Remove strange symbols
        text = re.sub(
            r"[^a-zA-Z0-9.,:;()/%+\- ]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # -------------------------------------------------
    # SENTENCE SPLITTING
    # -------------------------------------------------

    @classmethod
    def split_sentences(cls, text):

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        return [
            sentence.strip()
            for sentence in sentences
            if len(sentence.strip()) > 20
        ]

    # -------------------------------------------------
    # CANDIDATE PHRASES
    # -------------------------------------------------

    @classmethod
    def generate_candidates(cls, text):

        sentences = cls.split_sentences(
            text
        )

        candidates = []

        for sentence in sentences:

            words = re.findall(
                r"\b[A-Za-z][A-Za-z0-9+-]*\b",
                sentence
            )

            valid_words = [
                word.lower()
                for word in words
                if cls.is_valid_word(word)
            ]

            # -----------------------------------------
            # Single words
            # -----------------------------------------

            for word in valid_words:

                candidates.append(
                    word
                )

            # -----------------------------------------
            # Two-word phrases
            # -----------------------------------------

            for i in range(
                len(valid_words) - 1
            ):

                phrase = (
                    valid_words[i]
                    + " "
                    + valid_words[i + 1]
                )

                candidates.append(
                    phrase
                )

            # -----------------------------------------
            # Three-word phrases
            # -----------------------------------------

            for i in range(
                len(valid_words) - 2
            ):

                phrase = (
                    valid_words[i]
                    + " "
                    + valid_words[i + 1]
                    + " "
                    + valid_words[i + 2]
                )

                candidates.append(
                    phrase
                )

        return candidates

    # -------------------------------------------------
    # FREQUENCY SCORE
    # -------------------------------------------------

    @classmethod
    def frequency_scores(
        cls,
        candidates
    ):

        counts = Counter(
            candidates
        )

        if not counts:
            return {}

        maximum = max(
            counts.values()
        )

        scores = {}

        for phrase, count in counts.items():

            scores[phrase] = (
                count / maximum
            )

        return scores

    # -------------------------------------------------
    # TF-IDF-LIKE SCORE
    # -------------------------------------------------

    @classmethod
    def tfidf_scores(
        cls,
        text,
        candidates
    ):

        words = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+-]*\b",
            text.lower()
        )

        word_counts = Counter(
            words
        )

        total_words = max(
            len(words),
            1
        )

        scores = {}

        for candidate in set(
            candidates
        ):

            candidate_words = (
                candidate.split()
            )

            tf = sum(
                word_counts[word]
                for word in candidate_words
            ) / total_words

            # Longer meaningful phrases get
            # slightly more importance.
            phrase_bonus = min(
                len(candidate_words) * 0.15,
                0.30
            )

            scores[candidate] = (
                tf + phrase_bonus
            )

        return scores

    # -------------------------------------------------
    # SEMANTIC RELEVANCE
    # -------------------------------------------------

    @classmethod
    def semantic_scores(
        cls,
        text,
        candidates
    ):

        model = cls.get_model()

        # Limit very large documents
        document_text = text[:15000]

        document_embedding = model.encode(
            document_text,
            normalize_embeddings=True
        )

        unique_candidates = list(
            dict.fromkeys(candidates)
        )

        if not unique_candidates:
            return {}

        candidate_embeddings = model.encode(
            unique_candidates,
            normalize_embeddings=True
        )

        scores = {}

        for index, candidate in enumerate(
            unique_candidates
        ):

            score = float(
                candidate_embeddings[index]
                @ document_embedding
            )

            scores[candidate] = max(
                0.0,
                score
            )

        return scores

    # -------------------------------------------------
    # PHRASE QUALITY
    # -------------------------------------------------

    @classmethod
    def phrase_quality(cls, phrase):

        words = phrase.split()

        score = 0.0

        # Prefer phrases over isolated words
        if len(words) == 2:
            score += 0.5

        elif len(words) == 3:
            score += 0.7

        elif len(words) == 1:
            score += 0.2

        # Penalize very short words
        for word in words:

            if len(word) >= 5:
                score += 0.1

        return min(
            score,
            1.0
        )

    # -------------------------------------------------
    # DUPLICATE / OVERLAP REMOVAL
    # -------------------------------------------------

    @classmethod
    def remove_duplicates(
        cls,
        keywords,
        limit
    ):

        selected = []

        for item in keywords:

            phrase = item["keyword"]

            phrase_words = set(
                phrase.split()
            )

            duplicate = False

            for existing in selected:

                existing_words = set(
                    existing["keyword"].split()
                )

                intersection = (
                    phrase_words
                    & existing_words
                )

                # Avoid almost identical phrases
                if (
                    len(intersection) >=
                    min(
                        len(phrase_words),
                        len(existing_words)
                    )
                ):
                    duplicate = True
                    break

            if not duplicate:

                selected.append(
                    item
                )

            if len(selected) >= limit:
                break

        return selected

    # -------------------------------------------------
    # MAIN KEYWORD EXTRACTION
    # -------------------------------------------------

    @classmethod
    def extract_keywords(
        cls,
        text,
        top_k=15
    ):

        if not text or not text.strip():

            return []

        # 1. Clean
        text = cls.clean_text(
            text
        )

        # 2. Generate candidates
        candidates = cls.generate_candidates(
            text
        )

        if not candidates:

            return []

        # 3. Scores
        frequency = cls.frequency_scores(
            candidates
        )

        tfidf = cls.tfidf_scores(
            text,
            candidates
        )

        semantic = cls.semantic_scores(
            text,
            candidates
        )

        # 4. Combine
        results = []

        unique_candidates = list(
            dict.fromkeys(candidates)
        )

        for candidate in unique_candidates:

            semantic_score = semantic.get(
                candidate,
                0
            )

            frequency_score = frequency.get(
                candidate,
                0
            )

            tfidf_score = tfidf.get(
                candidate,
                0
            )

            phrase_score = (
                cls.phrase_quality(
                    candidate
                )
            )

            final_score = (
                semantic_score * 0.55
                + frequency_score * 0.20
                + tfidf_score * 0.15
                + phrase_score * 0.10
            )

            results.append({
                "keyword": candidate,
                "score": round(
                    final_score,
                    4
                )
            })

        # 5. Sort
        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # 6. Remove overlapping phrases
        results = cls.remove_duplicates(
            results,
            top_k
        )

        return [
            item["keyword"]
            for item in results
        ]