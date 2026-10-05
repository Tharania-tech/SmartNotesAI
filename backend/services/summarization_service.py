import re
from collections import Counter


# =========================================================
# OPTIONAL SPELL CHECKER
# =========================================================

try:
    from spellchecker import SpellChecker

    SPELLCHECK_AVAILABLE = True

except ImportError:

    SpellChecker = None
    SPELLCHECK_AVAILABLE = False


# =========================================================
# SUMMARIZATION SERVICE
# =========================================================

class SummarizationService:

    # =====================================================
    # SPELL CHECKER CACHE
    # =====================================================

    _spell_checker = None
    _spell_cache = {}

    # =====================================================
    # TECHNICAL WORDS
    # =====================================================

    TECHNICAL_TERMS = {
        "ai",
        "artificial",
        "intelligence",
        "machine",
        "learning",
        "deep",
        "neural",
        "network",
        "networks",
        "nlp",
        "natural",
        "language",
        "processing",

        "python",
        "java",
        "javascript",
        "typescript",
        "html",
        "html5",
        "css",
        "css3",
        "react",
        "reactjs",
        "node",
        "nodejs",
        "flask",
        "django",
        "spring",
        "springboot",
        "springframework",

        "mysql",
        "mongodb",
        "postgresql",
        "database",
        "databases",
        "sql",
        "nosql",

        "api",
        "apis",
        "rest",
        "restful",
        "http",
        "https",
        "url",
        "urls",
        "json",
        "xml",

        "ocr",
        "paddleocr",
        "opencv",

        "bart",
        "bert",
        "t5",
        "qwen",
        "llm",
        "llms",
        "transformer",
        "transformers",
        "token",
        "tokens",
        "tokenizer",
        "embedding",
        "embeddings",

        "github",
        "git",
        "npm",
        "vite",
        "jsx",
        "tsx",

        "frontend",
        "backend",
        "fullstack",
        "software",
        "hardware",
        "server",
        "client",

        "algorithm",
        "algorithms",
        "dataset",
        "datasets",
        "model",
        "models",
        "framework",
        "frameworks",
        "programming",
        "computer",
        "computing",
        "technology",
        "technologies",
    }

    # =====================================================
    # COMMON OCR SPELLING CORRECTIONS
    # =====================================================

    OCR_CORRECTIONS = {

        # Artificial intelligence
        "artifical": "artificial",
        "artificaly": "artificially",
        "inteligence": "intelligence",
        "intellgence": "intelligence",
        "intelllgence": "intelligence",

        # Machine learning
        "machlne": "machine",
        "machne": "machine",
        "learniing": "learning",
        "lernning": "learning",
        "learnlng": "learning",

        # Algorithms
        "algorlthm": "algorithm",
        "algorthm": "algorithm",
        "algoritm": "algorithm",
        "algorlthms": "algorithms",

        # Database
        "databse": "database",
        "datbase": "database",
        "datatbase": "database",
        "databases": "databases",

        # Summarization
        "summarizatlon": "summarization",
        "summarizaton": "summarization",
        "summarisation": "summarization",

        # Information
        "informtion": "information",
        "informatlon": "information",
        "informaton": "information",

        # Application
        "applicaton": "application",
        "applicatlon": "application",
        "applicatons": "applications",

        # Technology
        "technolgy": "technology",
        "technlogy": "technology",
        "technolgies": "technologies",

        # Development
        "developement": "development",
        "develpment": "development",
        "developmnt": "development",

        # Processing
        "procesing": "processing",
        "processlng": "processing",

        # Recognition
        "recogniton": "recognition",
        "recognltion": "recognition",
        "recognition": "recognition",

        # Generation
        "generaton": "generation",
        "genaration": "generation",

        # Education
        "educaton": "education",
        "educatlon": "education",

        # Student
        "studnt": "student",
        "studnts": "students",
        "studnet": "student",

        # Teacher
        "techer": "teacher",
        "teachr": "teacher",

        # Computer
        "computr": "computer",
        "compter": "computer",

        # Software
        "softwere": "software",
        "softwar": "software",

        # Hardware
        "hardwere": "hardware",

        # Network
        "netwrok": "network",
        "netowrk": "network",
        "netwrork": "network",

        # Security
        "securty": "security",
        "secrity": "security",

        # Memory
        "memmory": "memory",
        "memroy": "memory",

        # Management
        "managemnt": "management",
        "managment": "management",

        # Knowledge
        "knowladge": "knowledge",
        "knowlege": "knowledge",

        # Concept
        "concpet": "concept",
        "conecpt": "concept",
        "consept": "concept",

        # Example
        "exampe": "example",
        "exmaple": "example",

        # Different
        "diffrent": "different",
        "differnt": "different",

        # Function
        "funtion": "function",
        "fuction": "function",
        "functon": "function",

        # Structure
        "structre": "structure",

        # Architecture
        "architecure": "architecture",
        "archtecture": "architecture",

        # Methods
        "methd": "method",
        "metod": "method",

        # Parameter
        "paramter": "parameter",

        # Variable
        "variabl": "variable",
        "varible": "variable",

        # Language
        "langauge": "language",

        # Environment
        "enviroment": "environment",
        "environmnt": "environment",

        # Implementation
        "implemntation": "implementation",
        "implementaton": "implementation",

        # Advantages
        "advantge": "advantage",
        "disadvantge": "disadvantage",

        # Important
        "importnt": "important",

        # Essential
        "essentail": "essential",

        # Words from your OCR example
        "demoralic": "democratic",
        "democractic": "democratic",
        "deesnd": "does not",
        "truthworttiness": "truthfulness",
        "truthworthyness": "truthfulness",
        "dogn": "dog",
        "whar": "what",
        "cane": "can",
        "starts": "status",
        "practices": "practices",
        "religous": "religious",
        "religon": "religion",
        "socail": "social",
        "ethcs": "ethics",
        "ethcial": "ethical",
        "reasonning": "reasoning",
    }

    # =====================================================
    # STOP WORDS
    # =====================================================

    STOP_WORDS = {
        "the",
        "is",
        "are",
        "was",
        "were",
        "a",
        "an",
        "and",
        "or",
        "but",
        "of",
        "to",
        "in",
        "on",
        "for",
        "with",
        "as",
        "by",
        "from",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "be",
        "been",
        "being",
        "can",
        "could",
        "may",
        "might",
        "will",
        "would",
        "should",
        "has",
        "have",
        "had",
        "do",
        "does",
        "did",
        "they",
        "their",
        "them",
        "we",
        "our",
        "you",
        "your",
        "he",
        "she",
        "his",
        "her",
        "which",
        "who",
        "what",
        "when",
        "where",
        "how",
        "than",
        "also",
        "such",
        "into",
        "through",
        "using",
        "used",
        "use",
    }

    # =====================================================
    # GET SPELL CHECKER
    # =====================================================

    @classmethod
    def get_spell_checker(cls):

        if not SPELLCHECK_AVAILABLE:

            return None

        if cls._spell_checker is None:

            print(
                "Loading spelling correction system..."
            )

            cls._spell_checker = SpellChecker(
                distance=1
            )

            print(
                "Spelling correction system loaded."
            )

        return cls._spell_checker

    # =====================================================
    # PRESERVE CAPITALIZATION
    # =====================================================

    @staticmethod
    def preserve_case(
        original,
        corrected
    ):

        if not corrected:

            return original

        if original.isupper():

            return corrected.upper()

        if (
            original[:1].isupper()
            and original[1:].islower()
        ):

            return corrected.capitalize()

        return corrected

    # =====================================================
    # APPLY FAST OCR DICTIONARY
    # =====================================================

    @classmethod
    def apply_ocr_corrections(
        cls,
        text
    ):

        if not text:

            return ""

        def replace_word(match):

            original = match.group(0)

            lower = original.lower()

            corrected = cls.OCR_CORRECTIONS.get(
                lower
            )

            if not corrected:

                return original

            return cls.preserve_case(
                original,
                corrected
            )

        return re.sub(
            r"\b[A-Za-z]+\b",
            replace_word,
            text
        )

    # =====================================================
    # SPELLING CORRECTION
    # =====================================================

    @classmethod
    def correct_spelling(
        cls,
        text
    ):

        if not text:

            return ""

        # -------------------------------------------------
        # FAST KNOWN OCR CORRECTIONS
        # -------------------------------------------------

        text = cls.apply_ocr_corrections(
            text
        )

        spell = cls.get_spell_checker()

        if spell is None:

            print(
                "pyspellchecker not installed. "
                "Using OCR correction dictionary only."
            )

            return text

        # -------------------------------------------------
        # GET UNIQUE WORDS
        # -------------------------------------------------

        words = re.findall(
            r"\b[A-Za-z]{3,}\b",
            text
        )

        unique_words = set(
            word.lower()
            for word in words
        )

        unknown_words = []

        for word in unique_words:

            # Technical terms should never be
            # automatically changed.
            if word in cls.TECHNICAL_TERMS:

                continue

            # Already manually corrected
            if word in cls.OCR_CORRECTIONS:

                continue

            # Already cached
            if word in cls._spell_cache:

                continue

            try:

                if word not in spell:

                    unknown_words.append(word)

            except Exception:

                continue

        print(
            "Potential spelling errors:",
            len(unknown_words)
        )

        # -------------------------------------------------
        # CORRECT UNKNOWN WORDS
        # -------------------------------------------------

        for word in unknown_words:

            try:

                correction = spell.correction(
                    word
                )

                if not correction:

                    cls._spell_cache[word] = word

                    continue

                # -------------------------------------------------
                # DO NOT MAKE VERY AGGRESSIVE CHANGES
                # -------------------------------------------------

                if len(word) <= 4:

                    cls._spell_cache[word] = word

                    continue

                if abs(
                    len(correction) - len(word)
                ) > 2:

                    cls._spell_cache[word] = word

                    continue

                cls._spell_cache[word] = correction

            except Exception:

                cls._spell_cache[word] = word

        # -------------------------------------------------
        # REPLACE WORDS
        # -------------------------------------------------

        def replace_word(match):

            original = match.group(0)

            lower = original.lower()

            # Technical term
            if lower in cls.TECHNICAL_TERMS:

                return original

            # Known OCR correction
            if lower in cls.OCR_CORRECTIONS:

                corrected = cls.OCR_CORRECTIONS[
                    lower
                ]

            else:

                corrected = cls._spell_cache.get(
                    lower,
                    original
                )

            return cls.preserve_case(
                original,
                corrected
            )

        return re.sub(
            r"\b[A-Za-z]{3,}\b",
            replace_word,
            text
        )

    # =====================================================
    # CLEAN BASIC OCR TEXT
    # =====================================================

    @classmethod
    def clean_text(
        cls,
        text
    ):

        if not text:

            return ""

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        # -------------------------------------------------
        # Remove URLs
        # -------------------------------------------------

        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text,
            flags=re.IGNORECASE
        )

        # -------------------------------------------------
        # Remove emails
        # -------------------------------------------------

        text = re.sub(
            r"\S+@\S+",
            " ",
            text
        )

        # -------------------------------------------------
        # Remove page numbers
        # -------------------------------------------------

        text = re.sub(
            r"\bpage\s+\d+\b",
            " ",
            text,
            flags=re.IGNORECASE
        )

        # -------------------------------------------------
        # Remove "12 of 50"
        # -------------------------------------------------

        text = re.sub(
            r"\b\d+\s+of\s+\d+\b",
            " ",
            text,
            flags=re.IGNORECASE
        )

        # -------------------------------------------------
        # Remove excessive spaces
        # -------------------------------------------------

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n{2,}",
            "\n",
            text
        )

        return text.strip()

    # =====================================================
    # CLEAN NOTE FORMAT
    # =====================================================

    @classmethod
    def clean_note_formatting(
        cls,
        text
    ):

        if not text:

            return ""

        # -------------------------------------------------
        # Normalize line endings
        # -------------------------------------------------

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        # -------------------------------------------------
        # Remove circled numbers
        #
        # ① ② ③ ④ ⑤
        # -------------------------------------------------

        text = re.sub(
            r"[\u2460-\u2473]",
            " ",
            text
        )

        # -------------------------------------------------
        # Remove enclosed / decorative numbers
        # -------------------------------------------------

        text = re.sub(
            r"[\u2776-\u277F]",
            " ",
            text
        )

        # -------------------------------------------------
        # Remove common bullet symbols
        # -------------------------------------------------

        text = re.sub(
            r"(?m)^\s*[*•●▪◦‣➢➤►◆◇]+\s*",
            "",
            text
        )

        # -------------------------------------------------
        # Remove numbering at beginning of line
        #
        # 1. Example
        # 2) Example
        # 5 - Example
        # -------------------------------------------------

        text = re.sub(
            r"(?m)^\s*\d+\s*[\.\)]\s*",
            "",
            text
        )

        text = re.sub(
            r"(?m)^\s*\d+\s*[-–—]\s*",
            "",
            text
        )

        # -------------------------------------------------
        # Remove "Q1", "Q.1", "Question 1"
        # -------------------------------------------------

        text = re.sub(
            r"(?im)^\s*"
            r"(?:q|question)"
            r"\s*\.?\s*\d+"
            r"\s*[:.\-]?\s*",
            "",
            text
        )

        # -------------------------------------------------
        # Remove mark/question labels
        #
        # # 2mark
        # 2 mark
        # 2 marks
        # 5 mark question
        # -------------------------------------------------

        text = re.sub(
            r"(?i)"
            r"#?\s*\d+\s*"
            r"(?:marks?|mark)"
            r"(?:\s+question)?"
            r"\s*[:.\-]?\s*",
            "",
            text
        )

        # -------------------------------------------------
        # Remove standalone # @
        # -------------------------------------------------

        text = re.sub(
            r"(?m)^\s*[#@&]+\s*",
            "",
            text
        )

        # -------------------------------------------------
        # Clean UNIT headings.
        #
        # Keep the heading words but remove
        # unnecessary numbering.
        #
        # UNIT-III SCIENTIFIC VALUES
        # becomes
        # SCIENTIFIC VALUES
        # -------------------------------------------------

        text = re.sub(
            r"(?im)"
            r"^\s*unit\s*[-–—]?\s*"
            r"(?:[ivxlcdm]+|\d+)"
            r"\s*[:.\-]?\s*",
            "",
            text
        )

        # -------------------------------------------------
        # Remove excessive punctuation used as decoration
        # -------------------------------------------------

        text = re.sub(
            r"(?m)^\s*[-_=]{2,}\s*$",
            "",
            text
        )

        # -------------------------------------------------
        # Normalize spaces
        # -------------------------------------------------

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n{2,}",
            "\n",
            text
        )

        return text.strip()

    # =====================================================
    # REMOVE QUESTION-LIKE LINES
    # =====================================================

    @classmethod
    def is_question_line(
        cls,
        sentence
    ):

        if not sentence:

            return False

        clean = sentence.strip()

        # Direct question
        if clean.endswith("?"):

            return True

        # Common exam question formats
        patterns = [

            r"^\s*what\s+is\b",

            r"^\s*what\s+are\b",

            r"^\s*define\b",

            r"^\s*explain\b",

            r"^\s*describe\b",

            r"^\s*write\s+about\b",

            r"^\s*how\s+can\b",

            r"^\s*why\s+is\b",

            r"^\s*why\s+are\b",

            r"^\s*discuss\b",

            r"^\s*list\s+the\b",

        ]

        for pattern in patterns:

            if re.search(
                pattern,
                clean,
                flags=re.IGNORECASE
            ):

                return True

        return False

    # =====================================================
    # CODE-LIKE DETECTION
    # =====================================================

    @classmethod
    def is_code_like(
        cls,
        text
    ):

        if not text:

            return True

        patterns = [

            r"</?[a-zA-Z][^>]*>",

            r"<%.*?%>",

            r"\bpublic\s+(class|static|void)\b",

            r"\bprivate\s+(class|static|void)\b",

            r"\bprotected\s+(class|static|void)\b",

            r"\b(int|float|double|boolean|char)"
            r"\s+\w+\s*[=;]",

            r"\w+\.\w+\s*\(",

            r"\w+\s*\([^)]*\)\s*\{",

            r"\borg\.\w+",

            r"\b(SELECT|INSERT|UPDATE|DELETE)\b"
            r".+\b(FROM|INTO|WHERE)\b",
        ]

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                return True

        words = max(
            len(text.split()),
            1
        )

        symbols = len(
            re.findall(
                r"[{}\[\]();=<>\"']",
                text
            )
        )

        if symbols / words > 0.30:

            return True

        return False

    # =====================================================
    # SENTENCE SPLITTING
    # =====================================================

    @classmethod
    def split_sentences(
        cls,
        text
    ):

        if not text:

            return []

        # -------------------------------------------------
        # First use punctuation
        # -------------------------------------------------

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        result = []

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:

                continue

            # Ignore very short fragments
            if len(sentence.split()) < 4:

                continue

            # Ignore code
            if cls.is_code_like(sentence):

                continue

            result.append(sentence)

        # -------------------------------------------------
        # OCR often loses punctuation.
        # Try line/semicolon splitting as fallback.
        # -------------------------------------------------

        if len(result) < 3:

            parts = re.split(
                r"[;\n]+",
                text
            )

            for part in parts:

                part = part.strip()

                if len(part.split()) < 5:

                    continue

                if cls.is_code_like(part):

                    continue

                result.append(part)

        return result

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    @classmethod
    def remove_duplicate_sentences(
        cls,
        sentences
    ):

        seen = set()

        result = []

        for sentence in sentences:

            normalized = re.sub(
                r"[^a-z0-9 ]",
                "",
                sentence.lower()
            )

            normalized = re.sub(
                r"\s+",
                " ",
                normalized
            ).strip()

            if not normalized:

                continue

            if normalized in seen:

                continue

            seen.add(normalized)

            result.append(sentence)

        return result

    # =====================================================
    # WORD FREQUENCY
    # =====================================================

    @classmethod
    def calculate_frequency(
        cls,
        sentences
    ):

        frequency = Counter()

        for sentence in sentences:

            words = re.findall(
                r"\b[a-zA-Z]{3,}\b",
                sentence.lower()
            )

            for word in words:

                if word in cls.STOP_WORDS:

                    continue

                frequency[word] += 1

        return frequency

    # =====================================================
    # SENTENCE SCORE
    # =====================================================

    @classmethod
    def score_sentence(
        cls,
        sentence,
        index,
        total_sentences,
        frequency
    ):

        words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            sentence.lower()
        )

        meaningful_words = [

            word
            for word in words

            if word not in cls.STOP_WORDS
        ]

        if not meaningful_words:

            return 0

        # -------------------------------------------------
        # Frequency
        # -------------------------------------------------

        frequency_score = sum(
            frequency[word]
            for word in meaningful_words
        )

        frequency_score /= max(
            len(meaningful_words),
            1
        )

        # -------------------------------------------------
        # Definition bonus
        # -------------------------------------------------

        definition_bonus = 0

        if re.search(
            r"\b("
            r"is|are|means|refers to|"
            r"defined as|known as|"
            r"called|consists of"
            r")\b",
            sentence,
            flags=re.IGNORECASE
        ):

            definition_bonus = 3

        # -------------------------------------------------
        # Important academic keywords
        # -------------------------------------------------

        important_patterns = [

            r"\bimportant\b",

            r"\bmain\b",

            r"\bkey\b",

            r"\bprinciple\b",

            r"\bprinciples\b",

            r"\badvantage\b",

            r"\bdisadvantage\b",

            r"\bbenefit\b",

            r"\bfeatures?\b",

            r"\bpurpose\b",

            r"\bobjective\b",

            r"\bprocess\b",

            r"\btypes?\b",

            r"\bstep\b",

            r"\bsteps\b",

            r"\bmethod\b",

            r"\bexample\b",

            r"\bapplication\b",

            r"\bapplications\b",

            r"\bused for\b",

            r"\bconsists of\b",

            r"\brole\b",

            r"\bcharacteristics?\b",

            r"\bfeatures?\b",

        ]

        keyword_bonus = 0

        for pattern in important_patterns:

            if re.search(
                pattern,
                sentence,
                flags=re.IGNORECASE
            ):

                keyword_bonus += 1

        # -------------------------------------------------
        # Position bonus
        # -------------------------------------------------

        position_bonus = 0

        if total_sentences > 0:

            ratio = (
                index /
                total_sentences
            )

            if ratio < 0.10:

                position_bonus = 2

            elif ratio < 0.25:

                position_bonus = 1

        # -------------------------------------------------
        # Good sentence length
        # -------------------------------------------------

        word_count = len(
            sentence.split()
        )

        length_bonus = 0

        if 8 <= word_count <= 45:

            length_bonus = 1

        # -------------------------------------------------
        # Final score
        # -------------------------------------------------

        return (
            frequency_score
            + definition_bonus
            + keyword_bonus
            + position_bonus
            + length_bonus
        )

    # =====================================================
    # EXTRACT IMPORTANT SENTENCES
    # =====================================================

    @classmethod
    def extract_important_sentences(
        cls,
        sentences,
        max_sentences=15,
        max_words=220
    ):

        if not sentences:

            return []

        frequency = cls.calculate_frequency(
            sentences
        )

        scored = []

        total = len(sentences)

        for index, sentence in enumerate(
            sentences
        ):

            # -------------------------------------------------
            # Do not include exam questions
            # -------------------------------------------------

            if cls.is_question_line(
                sentence
            ):

                continue

            score = cls.score_sentence(
                sentence,
                index,
                total,
                frequency
            )

            scored.append(
                (
                    score,
                    index,
                    sentence
                )
            )

        # -------------------------------------------------
        # Highest score first
        # -------------------------------------------------

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        selected = scored[
            :max_sentences
        ]

        # -------------------------------------------------
        # Restore original order
        # -------------------------------------------------

        selected.sort(
            key=lambda item: item[1]
        )

        # -------------------------------------------------
        # Word limit
        # -------------------------------------------------

        final_sentences = []

        current_words = 0

        for (
            score,
            index,
            sentence
        ) in selected:

            sentence_words = len(
                sentence.split()
            )

            if (
                current_words
                + sentence_words
                > max_words
            ):

                continue

            final_sentences.append(
                sentence
            )

            current_words += sentence_words

            if len(final_sentences) >= max_sentences:

                break

        # -------------------------------------------------
        # Fallback
        # -------------------------------------------------

        if not final_sentences:

            for sentence in sentences:

                if cls.is_question_line(
                    sentence
                ):

                    continue

                final_sentences.append(
                    sentence
                )

                if len(final_sentences) >= 8:

                    break

        return final_sentences

    # =====================================================
    # FORMAT FINAL SUMMARY AS PARAGRAPH
    # =====================================================

    @classmethod
    def format_summary_as_paragraph(
        cls,
        summary
    ):

        if not summary:

            return ""

        # -------------------------------------------------
        # Run formatting cleaner again as a final safety
        # layer.
        # -------------------------------------------------

        summary = cls.clean_note_formatting(
            summary
        )

        # -------------------------------------------------
        # Remove question-like fragments
        # -------------------------------------------------

        sentences = cls.split_sentences(
            summary
        )

        clean_sentences = []

        for sentence in sentences:

            if cls.is_question_line(
                sentence
            ):

                continue

            sentence = sentence.strip()

            if sentence:

                clean_sentences.append(
                    sentence
                )

        # -------------------------------------------------
        # If sentence splitting failed,
        # use original cleaned summary.
        # -------------------------------------------------

        if clean_sentences:

            summary = " ".join(
                clean_sentences
            )

        # -------------------------------------------------
        # Normalize spaces
        # -------------------------------------------------

        summary = re.sub(
            r"\s+",
            " ",
            summary
        ).strip()

        # -------------------------------------------------
        # Remove space before punctuation
        # -------------------------------------------------

        summary = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            summary
        )

        # -------------------------------------------------
        # Add missing spaces after punctuation
        # -------------------------------------------------

        summary = re.sub(
            r"([.!?])([A-Za-z])",
            r"\1 \2",
            summary
        )

        # -------------------------------------------------
        # Remove accidental repeated punctuation
        # -------------------------------------------------

        summary = re.sub(
            r"\.{2,}",
            ".",
            summary
        )

        # -------------------------------------------------
        # Final capital letter
        # -------------------------------------------------

        if summary:

            summary = (
                summary[0].upper()
                + summary[1:]
            )

        # -------------------------------------------------
        # Final period
        # -------------------------------------------------

        if summary and summary[-1] not in ".!?":

            summary += "."

        return summary.strip()

    # =====================================================
    # MAIN SUMMARY FUNCTION
    # =====================================================

    @classmethod
    def summarize_text(
        cls,
        text,
        length="medium"
    ):

        print(
            "\n========================================"
        )

        print(
            "STARTING FAST DOCUMENT SUMMARIZATION"
        )

        print(
            "========================================"
        )

        if not text or not text.strip():

            raise ValueError(
                "Text cannot be empty."
            )

        # =================================================
        # STEP 1 - ORIGINAL TEXT
        # =================================================

        print(
            "Original characters:",
            len(text)
        )

        # =================================================
        # STEP 2 - BASIC CLEANING
        # =================================================

        cleaned_text = cls.clean_text(
            text
        )

        # =================================================
        # STEP 3 - REMOVE OCR FORMATTING
        # =================================================

        cleaned_text = cls.clean_note_formatting(
            cleaned_text
        )

        print(
            "Cleaned characters:",
            len(cleaned_text)
        )

        # =================================================
        # STEP 4 - SPELLING CORRECTION
        # =================================================

        print(
            "Starting spelling correction..."
        )

        corrected_text = cls.correct_spelling(
            cleaned_text
        )

        print(
            "Spelling correction completed."
        )

        # =================================================
        # STEP 5 - SENTENCE EXTRACTION
        # =================================================

        sentences = cls.split_sentences(
            corrected_text
        )

        print(
            "Sentences found:",
            len(sentences)
        )

        # =================================================
        # STEP 6 - REMOVE DUPLICATES
        # =================================================

        sentences = (
            cls.remove_duplicate_sentences(
                sentences
            )
        )

        print(
            "Unique sentences:",
            len(sentences)
        )

        # =================================================
        # STEP 7 - SUMMARY SIZE
        # =================================================

        if length == "short":

            max_sentences = 8
            max_words = 120

        elif length == "long":

            max_sentences = 20
            max_words = 320

        else:

            max_sentences = 15
            max_words = 220

        # =================================================
        # STEP 8 - IMPORTANT SENTENCES
        # =================================================

        important_sentences = (
            cls.extract_important_sentences(
                sentences,
                max_sentences=max_sentences,
                max_words=max_words
            )
        )

        print(
            "Important sentences:",
            len(important_sentences)
        )

        # =================================================
        # STEP 9 - JOIN AS PARAGRAPH
        # =================================================

        summary = " ".join(
            important_sentences
        )

        # =================================================
        # STEP 10 - FINAL CLEANING
        # =================================================

        summary = cls.format_summary_as_paragraph(
            summary
        )

        # =================================================
        # FALLBACK
        # =================================================

        if not summary:

            words = corrected_text.split()

            if len(words) > max_words:

                summary = " ".join(
                    words[:max_words]
                )

            else:

                summary = corrected_text

            summary = (
                cls.format_summary_as_paragraph(
                    summary
                )
            )

        # =================================================
        # FINAL RESULT
        # =================================================

        print(
            "\n========================================"
        )

        print(
            "FAST DOCUMENT SUMMARIZATION COMPLETED"
        )

        print(
            "Summary words:",
            len(summary.split())
        )

        print(
            "========================================\n"
        )

        return summary