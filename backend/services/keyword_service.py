import re
from keybert import KeyBERT


class KeywordService:

    _model = None

    # =========================================================
    # MODEL
    # =========================================================

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("Loading KeyBERT model...")

            cls._model = KeyBERT(
                model="all-MiniLM-L6-v2"
            )

            print("KeyBERT model loaded successfully.")

        return cls._model

    # =========================================================
    # TEXT CLEANING
    # =========================================================

    @classmethod
    def clean_text(cls, text):

        if not text:
            return ""

        # Remove URLs
        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text
        )

        # Remove emails
        text = re.sub(
            r"\S+@\S+",
            " ",
            text
        )

        # Remove excessive whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =========================================================
    # CODE DETECTION
    # =========================================================

    @classmethod
    def is_code_like(cls, text):

        if not text:
            return True

        patterns = [

            # HTML/XML
            r"<\/?[a-zA-Z][^>]*>",

            # JSP
            r"<%.*?%>",

            # Java
            r"\bpublic\s+(class|static|void)\b",
            r"\bprivate\s+(class|static|void)\b",
            r"\bprotected\s+(class|static|void)\b",

            # Java package
            r"\borg\.[a-zA-Z0-9_.]+",

            # Method call
            r"\w+\.\w+\s*\(",

            # Variable declaration
            r"\b(int|float|double|boolean|char)\s+\w+\s*[=;]",

            # SQL
            r"\bSELECT\b.+\bFROM\b",
            r"\bINSERT\b.+\bINTO\b",
            r"\bUPDATE\b.+\bSET\b",
            r"\bDELETE\b.+\bFROM\b"
        ]

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):
                return True

        # Too many programming symbols
        symbols = len(
            re.findall(
                r"[{}[\]();=<>\"]",
                text
            )
        )

        words = max(
            len(text.split()),
            1
        )

        if symbols / words > 0.30:
            return True

        return False

    # =========================================================
    # SPLIT SENTENCES
    # =========================================================

    @classmethod
    def get_sentences(cls, text):

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        result = []

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence.split()) < 5:
                continue

            if cls.is_code_like(sentence):
                continue

            result.append(sentence)

        return result

    # =========================================================
    # CONCEPT CONTEXT
    # =========================================================

    @classmethod
    def concept_score(
        cls,
        keyword,
        sentences
    ):

        score = 0

        keyword = keyword.lower()

        concept_patterns = [

            r"\bstands for\b",
            r"\bis defined as\b",
            r"\brefers to\b",
            r"\bis a\b",
            r"\bis an\b",
            r"\bare\b",
            r"\bknown as\b",
            r"\bcalled\b",
            r"\bused to\b",
            r"\bused for\b",
            r"\bused in\b",
            r"\bprovides\b",
            r"\ballows\b",
            r"\benables\b",
            r"\bconsists of\b",
            r"\bincludes\b",
            r"\barchitecture\b",
            r"\bframework\b",
            r"\bprotocol\b",
            r"\blanguage\b",
            r"\btechnology\b"
        ]

        for sentence in sentences:

            if keyword not in sentence.lower():
                continue

            # Keyword occurs in meaningful sentence
            score += 1

            # Sentence explains a concept
            for pattern in concept_patterns:

                if re.search(
                    pattern,
                    sentence,
                    re.IGNORECASE
                ):

                    score += 2
                    break

        return score

    # =========================================================
    # FREQUENCY
    # =========================================================

    @classmethod
    def get_frequency(
        cls,
        keyword,
        text
    ):

        pattern = (
            r"\b"
            + re.escape(keyword)
            + r"\b"
        )

        return len(
            re.findall(
                pattern,
                text,
                re.IGNORECASE
            )
        )

    # =========================================================
    # GENERIC WORD FILTER
    # =========================================================

    @classmethod
    def is_generic(cls, keyword):

        generic_words = {

            "define",
            "defined",
            "definition",
            "using",
            "used",
            "use",
            "uses",
            "provide",
            "provides",
            "provided",
            "allows",
            "allow",
            "helps",
            "help",
            "example",
            "examples",
            "following",
            "above",
            "below",
            "various",
            "different",
            "important",
            "information",
            "content",
            "document",
            "documents",
            "page",
            "pages",
            "text",
            "value",
            "values",
            "name",
            "names",
            "string",
            "strings",
            "message",
            "messages",
            "method",
            "methods",
            "object",
            "objects",
            "element",
            "elements",
            "property",
            "properties",
            "creating",
            "thing",
            "things",
            "just"
        }

        words = keyword.lower().split()

        # Single generic word
        if len(words) == 1:
            return words[0] in generic_words

        # More than half generic
        generic_count = sum(
            word in generic_words
            for word in words
        )

        return (
            generic_count / len(words)
        ) >= 0.60

    # =========================================================
    # VALIDATE CANDIDATE
    # =========================================================

    @classmethod
    def valid_candidate(
        cls,
        keyword,
        text
    ):

        keyword = keyword.strip()

        if len(keyword) < 3:
            return False

        words = keyword.split()

        # Maximum phrase length
        if len(words) > 4:
            return False

        # Repeated words
        lower_words = [
            word.lower()
            for word in words
        ]

        if len(lower_words) != len(
            set(lower_words)
        ):
            return False

        # Code fragment
        if cls.is_code_like(keyword):
            return False

        # Generic phrase
        if cls.is_generic(keyword):
            return False

        # Programming syntax
        if re.search(
            r"[{}[\]();=<>\"]",
            keyword
        ):
            return False

        # Must actually exist in document
        if cls.get_frequency(
            keyword,
            text
        ) == 0:
            return False

        return True

    # =========================================================
    # REMOVE SIMILAR KEYWORDS
    # =========================================================

    @classmethod
    def remove_duplicates(
        cls,
        keywords
    ):

        final = []

        for keyword in keywords:

            duplicate = False

            keyword_words = set(
                keyword.lower().split()
            )

            for existing in final:

                existing_words = set(
                    existing.lower().split()
                )

                if not keyword_words:
                    continue

                intersection = (
                    keyword_words
                    &
                    existing_words
                )

                union = (
                    keyword_words
                    |
                    existing_words
                )

                similarity = (
                    len(intersection)
                    /
                    len(union)
                )

                if similarity >= 0.60:

                    duplicate = True
                    break

            if not duplicate:
                final.append(keyword)

        return final

    # =========================================================
    # MAIN FUNCTION
    # =========================================================
    @classmethod
    def extract_keywords(
        cls,
        text,
        top_n=20
    ):
        """
        Extract meaningful academic/technical keywords from note text.

        Uses KeyBERT for semantic candidate generation, then applies
        strict filtering, scoring, and duplicate removal.
        """

        if not text or not text.strip():
            raise ValueError("No note content available.")

        print("\n========================================")
        print("Starting key concept extraction...")
        print("========================================")

        # -----------------------------------------------------
        # CLEAN TEXT
        # -----------------------------------------------------

        cleaned_text = cls.clean_text(text)

        print(
            f"Cleaned text length: {len(cleaned_text)} characters"
        )

        # -----------------------------------------------------
        # SENTENCES
        # -----------------------------------------------------

        sentences = cls.get_sentences(cleaned_text)

        if not sentences:
            raise ValueError(
                "No meaningful content found."
            )

        analysis_text = " ".join(sentences)

        # -----------------------------------------------------
        # LOAD KEYBERT
        # -----------------------------------------------------

        model = cls.get_model()

        # -----------------------------------------------------
        # GENERATE CANDIDATES
        # -----------------------------------------------------

        print("Generating keyword candidates...")

        candidates = model.extract_keywords(
            analysis_text,
            keyphrase_ngram_range=(1, 3),
            stop_words="english",
            use_mmr=True,
            diversity=0.70,
            top_n=100
        )

        print(
            f"Generated {len(candidates)} candidate keywords."
        )

        # -----------------------------------------------------
        # ADDITIONAL WORDS THAT SHOULD NOT BE KEYWORDS
        # -----------------------------------------------------

        blocked_exact = {
            "information",
            "system",
            "process",
            "method",
            "example",
            "examples",
            "object",
            "objects",
            "data",
            "thing",
            "things",
            "user",
            "users",
            "client",
            "clients",
            "source",
            "sources",
            "content",
            "document",
            "documents",
            "text",
            "page",
            "pages",
            "value",
            "values",
            "name",
            "names",
            "message",
            "messages",
            "string",
            "strings"
        }

        # Words that usually indicate a sentence fragment
        blocked_words = {
            "use",
            "uses",
            "used",
            "using",
            "provide",
            "provides",
            "provided",
            "allow",
            "allows",
            "allowed",
            "helps",
            "help",
            "create",
            "creates",
            "creating",
            "define",
            "defines",
            "defined",
            "represent",
            "represents",
            "represented",
            "exchange",
            "exchanges",
            "control",
            "controls",
            "include",
            "includes",
            "included",
            "support",
            "supports",
            "enable",
            "enables",
            "enabled",
            "make",
            "makes",
            "making",
            "contain",
            "contains",
            "contained"
        }

        scored = []

        # -----------------------------------------------------
        # PROCESS CANDIDATES
        # -----------------------------------------------------

        for keyword, semantic_score in candidates:

            keyword = keyword.strip()

            if not keyword:
                continue

            # Normalize spaces
            keyword = " ".join(
                keyword.split()
            )

            words = keyword.lower().split()

            # -------------------------------------------------
            # LENGTH FILTER
            # -------------------------------------------------

            if len(keyword) < 3:
                continue

            if len(words) > 4:
                continue

            # -------------------------------------------------
            # CODE FILTER
            # -------------------------------------------------

            if cls.is_code_like(keyword):
                continue

            # -------------------------------------------------
            # GENERIC FILTER
            # -------------------------------------------------

            if cls.is_generic(keyword):
                continue

            # -------------------------------------------------
            # EXACT BLOCKED WORD
            # -------------------------------------------------

            if keyword.lower() in blocked_exact:
                continue

            # -------------------------------------------------
            # REJECT PHRASES CONTAINING FRAGMENT WORDS
            # -------------------------------------------------

            if any(
                word in blocked_words
                for word in words
            ):
                continue

            # -------------------------------------------------
            # REPEATED WORDS
            # -------------------------------------------------

            if len(words) != len(set(words)):
                continue

            # -------------------------------------------------
            # SYMBOLS / PROGRAMMING SYNTAX
            # -------------------------------------------------

            if re.search(
                r"[{}[\]();=<>\"]",
                keyword
            ):
                continue

            # -------------------------------------------------
            # MUST EXIST IN ACTUAL DOCUMENT
            # -------------------------------------------------

            frequency = cls.get_frequency(
                keyword,
                cleaned_text
            )

            if frequency == 0:
                continue

            # -------------------------------------------------
            # CONTEXT SCORE
            # -------------------------------------------------

            context = cls.concept_score(
                keyword,
                sentences
            )

            # -------------------------------------------------
            # FREQUENCY SCORE
            # -------------------------------------------------

            frequency_score = min(
                frequency,
                5
            ) / 5

            # -------------------------------------------------
            # CONTEXT SCORE NORMALIZATION
            # -------------------------------------------------

            context_score = min(
                context,
                6
            ) / 6

            # -------------------------------------------------
            # PHRASE SCORE
            # -------------------------------------------------

            if len(words) == 1:
                phrase_score = 0.60

            elif len(words) == 2:
                phrase_score = 1.00

            elif len(words) == 3:
                phrase_score = 0.95

            else:
                phrase_score = 0.80

            # -------------------------------------------------
            # DEFINITION BONUS
            # -------------------------------------------------

            definition_bonus = 0

            keyword_lower = keyword.lower()

            for sentence in sentences:

                sentence_lower = sentence.lower()

                if keyword_lower not in sentence_lower:
                    continue

                if re.search(
                    rf"\b{re.escape(keyword_lower)}\b"
                    r".*\bstands for\b",
                    sentence_lower
                ):
                    definition_bonus += 0.30

                elif re.search(
                    rf"\b{re.escape(keyword_lower)}\b"
                    r".*\bis (a|an|the)\b",
                    sentence_lower
                ):
                    definition_bonus += 0.20

                elif re.search(
                    rf"\b{re.escape(keyword_lower)}\b"
                    r".*\brefers to\b",
                    sentence_lower
                ):
                    definition_bonus += 0.20

                elif re.search(
                    rf"\b{re.escape(keyword_lower)}\b"
                    r".*\bis defined as\b",
                    sentence_lower
                ):
                    definition_bonus += 0.20

            definition_bonus = min(
                definition_bonus,
                0.50
            )

            # -------------------------------------------------
            # FINAL SCORE
            # -------------------------------------------------

            final_score = (
                semantic_score * 0.45
                + frequency_score * 0.20
                + context_score * 0.20
                + phrase_score * 0.10
                + definition_bonus * 0.05
            )

            scored.append(
                (
                    keyword,
                    final_score,
                    frequency,
                    context
                )
            )

        # -----------------------------------------------------
        # SORT BY SCORE
        # -----------------------------------------------------

        scored.sort(
            key=lambda item: item[1],
            reverse=True
        )

        # -----------------------------------------------------
        # GET SORTED KEYWORDS
        # -----------------------------------------------------

        ranked_keywords = [
            item[0]
            for item in scored
        ]

        # -----------------------------------------------------
        # REMOVE SIMILAR KEYWORDS
        # -----------------------------------------------------

        keywords = cls.remove_duplicates(
            ranked_keywords
        )

        # -----------------------------------------------------
        # FINAL RESULT
        # -----------------------------------------------------

        keywords = keywords[:top_n]

        print("\n========================================")
        print("FINAL KEY CONCEPTS")
        print("========================================")

        if not keywords:
            print("No suitable keywords found.")

        for index, keyword in enumerate(
            keywords,
            start=1
        ):
            print(
                f"{index}. {keyword}"
            )

        print("========================================")

        return keywords