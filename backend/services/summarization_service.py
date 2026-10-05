"""
SmartNotes AI - Advanced Academic Summarization Service

Purpose:
    Advanced summarization for:
    - PDF notes
    - OCR text
    - Handwritten notes
    - Academic notes
    - Technical notes
    - DBMS / Java / Python / AI / ML / CS subjects

Important:
    Keep the public API:
        SummarizationService.summarize_text(text, length="medium")

No frontend/API changes are required.
"""

import re
import math
from collections import Counter


class SummarizationService:

    # ============================================================
    # TECHNICAL TERMS
    # ============================================================

    TECHNICAL_TERMS = {
        # Computer Science
        "algorithm",
        "algorithms",
        "application",
        "architecture",
        "backend",
        "database",
        "databases",
        "data",
        "dataset",
        "datasets",
        "development",
        "framework",
        "frontend",
        "fullstack",
        "function",
        "functions",
        "interface",
        "model",
        "program",
        "programming",
        "software",
        "system",
        "systems",

        # DBMS
        "dbms",
        "sql",
        "nosql",
        "mysql",
        "mongodb",
        "database",
        "schema",
        "schemas",
        "relation",
        "relations",
        "relational",
        "tuple",
        "tuples",
        "attribute",
        "attributes",
        "domain",
        "domains",
        "primary",
        "foreign",
        "candidate",
        "composite",
        "super",
        "key",
        "keys",
        "normalization",
        "normalization",
        "normal",
        "functional",
        "dependency",
        "dependencies",
        "transaction",
        "transactions",
        "concurrency",
        "serializability",
        "serializable",
        "deadlock",
        "index",
        "indexes",
        "indexing",
        "query",
        "queries",
        "join",
        "joins",
        "relational",
        "algebra",
        "acid",
        "atomicity",
        "consistency",
        "isolation",
        "durability",
        "recovery",
        "checkpoint",
        "checkpointing",
        "cursor",
        "trigger",
        "view",
        "views",
        "constraint",
        "constraints",
        "entity",
        "entities",
        "relationship",
        "relationships",
        "cardinality",
        "aggregation",
        "generalization",
        "specialization",
        "hierarchical",
        "network",
        "b-tree",
        "b+",
        "mvcc",
        "ddl",
        "dml",
        "dcl",
        "tcl",
        "ansi",
        "sparc",

        # Programming
        "java",
        "python",
        "javascript",
        "typescript",
        "react",
        "node",
        "nodejs",
        "flask",
        "spring",
        "springboot",
        "html",
        "css",
        "jsx",
        "rest",
        "api",
        "http",
        "json",
        "xml",
        "git",
        "github",
        "npm",
        "vite",

        # AI / ML
        "ai",
        "artificial",
        "intelligence",
        "machine",
        "learning",
        "deep",
        "neural",
        "network",
        "networks",
        "model",
        "models",
        "llm",
        "transformer",
        "transformers",
        "embedding",
        "embeddings",
        "tokenizer",
        "ocr",
        "paddleocr",
        "opencv",
        "tensorflow",
        "pytorch",
        "classification",
        "regression",
        "prediction",
        "training",
        "validation",
        "inference",

        # Common academic technical terms
        "analysis",
        "method",
        "methods",
        "process",
        "structure",
        "structures",
        "concept",
        "concepts",
        "principle",
        "principles",
        "characteristic",
        "characteristics",
        "advantage",
        "advantages",
        "disadvantage",
        "disadvantages",
        "feature",
        "features",
        "purpose",
        "objective",
        "objectives",
        "application",
        "applications",
        "implementation",
        "implementation",
        "performance",
        "security",
        "integrity",
        "authentication",
        "authorization",
    }

    # ============================================================
    # OCR CORRECTIONS
    # ============================================================

    OCR_CORRECTIONS = {
        "artifical": "artificial",
        "artificalintelligence": "artificial intelligence",
        "intelligance": "intelligence",
        "machlne": "machine",
        "learnlng": "learning",
        "algorlthm": "algorithm",
        "algorithrn": "algorithm",
        "databse": "database",
        "databa5e": "database",
        "databaze": "database",
        "schemа": "schema",
        "scheema": "schema",
        "relaton": "relation",
        "relational": "relational",
        "normalizatlon": "normalization",
        "summarizatlon": "summarization",
        "transactlon": "transaction",
        "concurrencv": "concurrency",
        "dependencv": "dependency",
        "independance": "independence",
        "independency": "independence",
        "physlcal": "physical",
        "loglcal": "logical",
        "extemal": "external",
        "intemal": "internal",
        "extemal": "external",
        "retrievaI": "retrieval",
        "consistencv": "consistency",
        "integritv": "integrity",
        "securitv": "security",
        "authentlcation": "authentication",
        "authorizatlon": "authorization",
        "organizatlon": "organization",
        "organised": "organized",
        "orgamzed": "organized",

        # Common OCR errors
        "demoralic": "democratic",
        "deesnd": "does not",
        "truthworttiness": "truthfulness",
        "dogn": "dog",
        "whar": "what",
        "cane": "can",
        "starts": "status",
        "religous": "religious",
        "socail": "social",
        "ethcs": "ethics",
        "reasonning": "reasoning",

        # DBMS specific
        "sparc": "SPARC",
        "spare": "SPARC",
        "ansi/spare": "ANSI/SPARC",
        "ansi/sparc": "ANSI/SPARC",
        "b+tree": "B+ tree",
        "b-tree": "B-tree",
        "mvcc": "MVCC",
        "dbm": "DBMS",
        "dmbs": "DBMS",
        "ddl": "DDL",
        "dml": "DML",
        "dcl": "DCL",
        "tcl": "TCL",
    }

    # ============================================================
    # STOP WORDS
    # ============================================================

    STOP_WORDS = {
        "a", "an", "the", "and", "or", "but", "if", "then",
        "than", "that", "this", "these", "those", "is", "are",
        "was", "were", "be", "been", "being", "to", "of", "in",
        "on", "for", "from", "by", "with", "as", "at", "it",
        "its", "into", "about", "after", "before", "during",
        "through", "over", "under", "between", "within", "without",
        "can", "could", "may", "might", "must", "should", "would",
        "will", "shall", "do", "does", "did", "done",
        "has", "have", "had", "having",
        "i", "we", "you", "he", "she", "they", "them",
        "their", "our", "your", "my", "his", "her",
        "which", "who", "whom", "what", "where", "when", "why",
        "how", "all", "each", "every", "some", "any", "many",
        "more", "most", "other", "another", "such",
        "there", "here", "also", "very", "only", "just",
        "used", "using", "use"
    }

    # ============================================================
    # IMPORTANT ACADEMIC WORDS
    # ============================================================

    IMPORTANCE_WORDS = {
        "important",
        "main",
        "major",
        "key",
        "principle",
        "principles",
        "definition",
        "defined",
        "concept",
        "concepts",
        "purpose",
        "objective",
        "objectives",
        "process",
        "steps",
        "step",
        "method",
        "methods",
        "types",
        "type",
        "classification",
        "classifications",
        "characteristic",
        "characteristics",
        "feature",
        "features",
        "advantage",
        "advantages",
        "disadvantage",
        "disadvantages",
        "benefit",
        "benefits",
        "role",
        "application",
        "applications",
        "example",
        "examples",
        "consists",
        "include",
        "includes",
        "involves",
        "provides",
        "supports",
        "allows",
        "ensures",
        "prevents",
        "reduces",
        "improves",
    }

    # ============================================================
    # LENGTH SETTINGS
    # ============================================================

    LENGTH_SETTINGS = {
        "short": {
            "max_words": 180,
            "max_sentences": 10,
            "max_sections": 8,
        },
        "medium": {
            "max_words": 320,
            "max_sentences": 18,
            "max_sections": 12,
        },
        "long": {
            "max_words": 500,
            "max_sentences": 28,
            "max_sections": 16,
        },
    }

    # ============================================================
    # 1. NORMALIZE OCR TEXT
    # ============================================================

    @classmethod
    def normalize_text(cls, text):
        if not text:
            return ""

        text = str(text)

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove null characters
        text = text.replace("\x00", " ")

        # Normalize common unicode characters
        replacements = {
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u2212": "-",
            "\u2026": "...",
            "\u00a0": " ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # Fix OCR words
        text = cls.apply_ocr_corrections(text)

        # Remove URLs and emails
        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
            " ",
            text,
        )

        # Normalize repeated spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    # ============================================================
    # 2. OCR CORRECTION
    # ============================================================

    @classmethod
    def apply_ocr_corrections(cls, text):
        if not text:
            return ""

        # Longer terms first
        corrections = sorted(
            cls.OCR_CORRECTIONS.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for wrong, correct in corrections:
            pattern = r"\b" + re.escape(wrong) + r"\b"

            text = re.sub(
                pattern,
                correct,
                text,
                flags=re.IGNORECASE,
            )

        return text

    # ============================================================
    # 3. SPELLING CORRECTION
    # ============================================================

    @classmethod
    def correct_spelling(cls, text):
        """
        Conservative spelling correction.

        We deliberately do NOT aggressively correct technical words.
        """

        if not text:
            return ""

        text = cls.apply_ocr_corrections(text)

        # Optional spellchecker
        try:
            from spellchecker import SpellChecker
            spell = SpellChecker()
        except Exception:
            spell = None

        if spell is None:
            return text

        words = re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text)

        protected = {
            word.lower()
            for word in cls.TECHNICAL_TERMS
        }

        corrections = {}

        for word in words:
            lower = word.lower()

            # Protect technical vocabulary
            if lower in protected:
                continue

            # Don't modify very short words
            if len(word) <= 3:
                continue

            # Ignore mixed alphanumeric technical terms
            if re.search(r"\d", word):
                continue

            # Already known
            if lower in spell:
                continue

            candidate = spell.correction(word)

            if not candidate:
                continue

            candidate = str(candidate)

            # Avoid aggressive changes
            if abs(len(candidate) - len(word)) > 2:
                continue

            # Only accept reasonably similar changes
            if len(word) >= 6:
                corrections[word] = candidate

        for wrong, correct in corrections.items():
            text = re.sub(
                r"\b" + re.escape(wrong) + r"\b",
                correct,
                text,
            )

        return text

    # ============================================================
    # 4. DETECT HEADINGS
    # ============================================================

    @classmethod
    def is_heading(cls, line):
        if not line:
            return False

        line = line.strip()

        if len(line) < 2 or len(line) > 140:
            return False

        # Numbered headings:
        # 1. Introduction
        # 2. Database Architecture
        # 11. Indexing & File Organization
        if re.match(
            r"^\d+(?:\.\d+)*[\.)]?\s+[A-Za-z]",
            line,
        ):
            return True

        # Common academic section headings
        heading_patterns = [
            r"^three-schema architecture",
            r"^data independence",
            r"^dbms languages",
            r"^data models?",
            r"^entity[- ]relationship",
            r"^relational model",
            r"^types of keys",
            r"^integrity constraints",
            r"^relational algebra",
            r"^types of joins",
            r"^structured query language",
            r"^common ddl commands",
            r"^common dml commands",
            r"^aggregate functions",
            r"^normalization",
            r"^functional dependency",
            r"^normal forms?",
            r"^acid properties",
            r"^transaction states",
            r"^schedules",
            r"^concurrency control",
            r"^concurrency problems",
            r"^deadlock",
            r"^file organization methods",
            r"^indexing",
            r"^database recovery",
            r"^log-based recovery",
            r"^recovery techniques",
            r"^types of failures",
        ]

        lower = line.lower()

        for pattern in heading_patterns:
            if re.match(pattern, lower):
                return True

        # ALL CAPS short headings
        letters = re.sub(r"[^A-Za-z]", "", line)

        if (
            len(letters) >= 4
            and line.upper() == line
            and len(line.split()) <= 10
        ):
            return True

        return False

    # ============================================================
    # 5. CLEAN BROKEN LINES
    # ============================================================

    @classmethod
    def clean_line(cls, line):
        if not line:
            return ""

        line = line.strip()

        # Remove page-number-only lines
        if re.fullmatch(r"(page\s*)?\d+", line, flags=re.IGNORECASE):
            return ""

        # Remove decorative characters
        line = re.sub(
            r"^[•●○▪■◆◇►▶]+\s*",
            "",
            line,
        )

        # Remove repeated separators
        line = re.sub(r"^[\-\_=*]{3,}$", "", line)

        # Remove orphan closing punctuation
        line = re.sub(r"^\)+\s*", "", line)

        # IMPORTANT:
        # Remove fragments like:
        # "Bank tellers)"
        # ")"
        # "tellers)"
        #
        # only when they are clearly too short and end in punctuation.
        words = line.split()

        if (
            len(words) <= 3
            and line.endswith((")", "]", "}"))
            and not re.search(r"\b(e\.g|i\.e)\b", line, re.I)
        ):
            return ""

        # Remove leading punctuation
        line = re.sub(r"^[,;:.)\]}]+", "", line).strip()

        # Normalize spaces
        line = re.sub(r"\s+", " ", line)

        return line.strip()

    # ============================================================
    # 6. REMOVE PDF / OCR NOISE
    # ============================================================

    @classmethod
    def clean_pdf_text(cls, text):
        text = cls.normalize_text(text)

        if not text:
            return ""

        lines = text.split("\n")
        cleaned = []

        for line in lines:
            line = cls.clean_line(line)

            if not line:
                continue

            # Remove obvious table-of-contents page numbers
            line = re.sub(
                r"\.{3,}\s*\d+\s*$",
                "",
                line,
            )

            cleaned.append(line)

        # --------------------------------------------------------
        # Join wrapped lines carefully
        # --------------------------------------------------------

        final_lines = []

        for line in cleaned:

            if not final_lines:
                final_lines.append(line)
                continue

            previous = final_lines[-1]

            # Never merge headings
            if cls.is_heading(line):
                final_lines.append(line)
                continue

            if cls.is_heading(previous):
                final_lines.append(line)
                continue

            # Don't merge bullet-like lines
            if line.startswith(("-", "•", "●")):
                final_lines.append(line)
                continue

            # If previous line clearly continues
            if (
                not previous.endswith(
                    (".", "!", "?", ":", ";", ")", "]")
                )
                and len(previous.split()) < 25
            ):
                final_lines[-1] = previous + " " + line
            else:
                final_lines.append(line)

        text = "\n".join(final_lines)

        # Final whitespace cleanup
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    # ============================================================
    # 7. SPLIT INTO SECTIONS
    # ============================================================

    @classmethod
    def split_into_sections(cls, text):
        """
        Converts:

            Heading
            sentence
            sentence

            Heading
            sentence

        into structured sections.
        """

        lines = text.split("\n")

        sections = []
        current_title = "Introduction"
        current_lines = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if cls.is_heading(line):

                if current_lines:
                    sections.append({
                        "title": current_title,
                        "text": " ".join(current_lines).strip(),
                    })

                current_title = line
                current_lines = []

            else:
                current_lines.append(line)

        if current_lines:
            sections.append({
                "title": current_title,
                "text": " ".join(current_lines).strip(),
            })

        return sections

    # ============================================================
    # 8. SENTENCE SPLITTING
    # ============================================================

    @classmethod
    def split_sentences(cls, text):
        if not text:
            return []

        # Protect abbreviations
        protected = text

        abbreviations = [
            "e.g.",
            "i.e.",
            "etc.",
            "vs.",
            "Dr.",
            "Mr.",
            "Mrs.",
            "Ms.",
        ]

        for index, abbr in enumerate(abbreviations):
            protected = protected.replace(
                abbr,
                f"__ABBR{index}__",
            )

        # Sentence boundaries
        pieces = re.split(
            r"(?<=[.!?])\s+(?=[A-Z0-9])",
            protected,
        )

        sentences = []

        for piece in pieces:

            piece = piece.strip()

            for index, abbr in enumerate(abbreviations):
                piece = piece.replace(
                    f"__ABBR{index}__",
                    abbr,
                )

            if not piece:
                continue

            # Remove accidental leading punctuation
            piece = re.sub(
                r"^[,;:)\]}]+",
                "",
                piece,
            ).strip()

            # Ignore tiny fragments
            words = piece.split()

            if len(words) < 5:
                continue

            # Ignore obvious OCR garbage
            if cls.is_garbage_sentence(piece):
                continue

            sentences.append(piece)

        # If punctuation splitting failed,
        # use semicolon/newline boundaries.
        if len(sentences) < 2:

            fallback = re.split(
                r"[;\n]+",
                text,
            )

            sentences = []

            for piece in fallback:
                piece = piece.strip()

                if len(piece.split()) >= 5:
                    if not cls.is_garbage_sentence(piece):
                        sentences.append(piece)

        return sentences

    # ============================================================
    # 9. GARBAGE DETECTION
    # ============================================================

    @classmethod
    def is_garbage_sentence(cls, sentence):
        if not sentence:
            return True

        words = sentence.split()

        if len(words) < 4:
            return True

        # Too many symbols = probably OCR/code noise
        symbols = len(
            re.findall(r"[^A-Za-z0-9\s.,;:'\"()\-+/]", sentence)
        )

        if symbols > len(sentence) * 0.20:
            return True

        # Too many repeated characters
        if re.search(r"(.)\1{4,}", sentence):
            return True

        # Orphan punctuation
        if re.match(r"^[)\]}]", sentence):
            return True

        # Very high percentage of one-letter tokens
        one_letter = sum(
            1 for word in words
            if len(re.sub(r"[^A-Za-z]", "", word)) == 1
        )

        if len(words) > 8 and one_letter / len(words) > 0.4:
            return True

        return False

    # ============================================================
    # 10. TOKENIZATION
    # ============================================================

    @classmethod
    def tokenize(cls, text):
        words = re.findall(
            r"[A-Za-z][A-Za-z0-9+/#.-]*",
            text.lower(),
        )

        return [
            word
            for word in words
            if word not in cls.STOP_WORDS
            and len(word) > 2
        ]

    # ============================================================
    # 11. FREQUENCY
    # ============================================================

    @classmethod
    def calculate_frequency(cls, sentences):
        counter = Counter()

        for sentence in sentences:
            for word in cls.tokenize(sentence):
                counter[word] += 1

        if not counter:
            return {}

        max_frequency = max(counter.values())

        return {
            word: count / max_frequency
            for word, count in counter.items()
        }

    # ============================================================
    # 12. DETECT DEFINITION
    # ============================================================

    @classmethod
    def is_definition(cls, sentence):
        lower = sentence.lower()

        patterns = [
            r"\bis defined as\b",
            r"\bcan be defined as\b",
            r"\bis a\b",
            r"\bis an\b",
            r"\brefers to\b",
            r"\bmeans\b",
            r"\bis the process of\b",
            r"\bis the ability to\b",
            r"\bis a collection of\b",
            r"\bis a structure that\b",
            r"\bis software that\b",
        ]

        return any(
            re.search(pattern, lower)
            for pattern in patterns
        )

    # ============================================================
    # 13. IMPORTANT CONTENT
    # ============================================================

    @classmethod
    def is_important_content(cls, sentence):
        lower = sentence.lower()

        for word in cls.IMPORTANCE_WORDS:
            if re.search(
                r"\b" + re.escape(word) + r"\b",
                lower,
            ):
                return True

        return cls.is_definition(sentence)

    # ============================================================
    # 14. TOPIC SIMILARITY
    # ============================================================

    @classmethod
    def word_overlap(cls, first, second):
        a = set(cls.tokenize(first))
        b = set(cls.tokenize(second))

        if not a or not b:
            return 0.0

        return len(a & b) / max(
            1,
            min(len(a), len(b)),
        )

    # ============================================================
    # 15. REDUNDANCY DETECTION
    # ============================================================

    @classmethod
    def is_redundant(cls, sentence, selected):
        for previous in selected:

            similarity = cls.word_overlap(
                sentence,
                previous,
            )

            if similarity >= 0.72:
                return True

        return False

    # ============================================================
    # 16. SENTENCE SCORING
    # ============================================================

    @classmethod
    def score_sentence(
        cls,
        sentence,
        frequency,
        position,
        total_sentences,
        section_title="",
    ):

        words = cls.tokenize(sentence)

        if not words:
            return 0.0

        score = 0.0

        # --------------------------------------------------------
        # Frequency score
        # --------------------------------------------------------

        frequency_score = sum(
            frequency.get(word, 0)
            for word in words
        )

        frequency_score /= max(
            1,
            len(words),
        )

        score += frequency_score * 3.0

        # --------------------------------------------------------
        # Definition bonus
        # --------------------------------------------------------

        if cls.is_definition(sentence):
            score += 5.0

        # --------------------------------------------------------
        # Academic importance
        # --------------------------------------------------------

        importance_count = sum(
            1
            for word in words
            if word in cls.IMPORTANCE_WORDS
        )

        score += min(
            importance_count * 1.5,
            6.0,
        )

        # --------------------------------------------------------
        # Technical term bonus
        # --------------------------------------------------------

        technical_count = sum(
            1
            for word in words
            if word in cls.TECHNICAL_TERMS
        )

        score += min(
            technical_count * 1.2,
            7.0,
        )

        # --------------------------------------------------------
        # Section title relevance
        # --------------------------------------------------------

        if section_title:

            title_words = set(
                cls.tokenize(section_title)
            )

            sentence_words = set(words)

            overlap = len(
                title_words & sentence_words
            )

            score += overlap * 2.0

        # --------------------------------------------------------
        # Position bonus
        # --------------------------------------------------------

        if total_sentences > 1:

            relative_position = (
                position / (total_sentences - 1)
            )

            # Slight preference for introductory sentences
            if relative_position < 0.20:
                score += 1.5

        # --------------------------------------------------------
        # Ideal sentence length
        # --------------------------------------------------------

        word_count = len(sentence.split())

        if 10 <= word_count <= 35:
            score += 2.0

        elif word_count > 50:
            score -= 1.5

        # --------------------------------------------------------
        # Avoid question-like sentences
        # --------------------------------------------------------

        if cls.is_question(sentence):
            score -= 5.0

        # --------------------------------------------------------
        # Avoid code
        # --------------------------------------------------------

        if cls.is_code_like(sentence):
            score -= 3.0

        return score

    # ============================================================
    # 17. QUESTION DETECTION
    # ============================================================

    @classmethod
    def is_question(cls, sentence):
        lower = sentence.lower().strip()

        if "?" in sentence:
            return True

        patterns = [
            r"^what is\b",
            r"^what are\b",
            r"^why is\b",
            r"^why are\b",
            r"^how does\b",
            r"^how do\b",
            r"^how can\b",
            r"^define\b",
            r"^explain\b",
            r"^describe\b",
            r"^discuss\b",
            r"^write about\b",
            r"^list\b",
        ]

        return any(
            re.match(pattern, lower)
            for pattern in patterns
        )

    # ============================================================
    # 18. CODE DETECTION
    # ============================================================

    @classmethod
    def is_code_like(cls, sentence):
        if not sentence:
            return False

        code_patterns = [
            r"\bSELECT\b.+\bFROM\b",
            r"\bINSERT\s+INTO\b",
            r"\bUPDATE\b.+\bSET\b",
            r"\bDELETE\s+FROM\b",
            r"\bCREATE\s+TABLE\b",
            r"\bpublic\s+static\s+void\b",
            r"\bfunction\s+\w+\s*\(",
            r"=>",
            r"\{\s*[\w]+\s*:",
        ]

        for pattern in code_patterns:
            if re.search(
                pattern,
                sentence,
                flags=re.IGNORECASE,
            ):
                return True

        # Too many programming symbols
        symbols = len(
            re.findall(
                r"[{}[\]();<>:=]",
                sentence,
            )
        )

        if symbols >= 8:
            return True

        return False

    # ============================================================
    # 19. TABLE-LIKE CONTENT
    # ============================================================

    @classmethod
    def is_table_like(cls, sentence):
        """
        Detect common extracted PDF table rows.
        """

        separators = [
            "|",
            ":",
            "→",
        ]

        separator_count = sum(
            sentence.count(separator)
            for separator in separators
        )

        # DBMS command patterns
        if re.search(
            r"\b(DDL|DML|DCL|TCL)\b",
            sentence,
        ):
            return True

        if separator_count >= 2:
            return True

        return False

    # ============================================================
    # 20. SELECT SENTENCES FROM SECTION
    # ============================================================

    @classmethod
    def select_section_sentences(
        cls,
        section,
        max_sentences,
    ):

        title = section["title"]
        text = section["text"]

        sentences = cls.split_sentences(text)

        if not sentences:
            return []

        frequency = cls.calculate_frequency(
            sentences
        )

        scored = []

        for index, sentence in enumerate(sentences):

            score = cls.score_sentence(
                sentence=sentence,
                frequency=frequency,
                position=index,
                total_sentences=len(sentences),
                section_title=title,
            )

            scored.append(
                {
                    "sentence": sentence,
                    "score": score,
                    "position": index,
                }
            )

        # Highest score first
        scored.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        selected = []

        for item in scored:

            sentence = item["sentence"]

            if cls.is_redundant(
                sentence,
                selected,
            ):
                continue

            selected.append(sentence)

            if len(selected) >= max_sentences:
                break

        # Restore original order
        position_map = {
            item["sentence"]: item["position"]
            for item in scored
        }

        selected.sort(
            key=lambda sentence:
            position_map.get(sentence, 999999)
        )

        return selected

    # ============================================================
    # 21. SECTION IMPORTANCE
    # ============================================================

    @classmethod
    def score_section(cls, section):
        title = section["title"]
        text = section["text"]

        score = 0.0

        title_lower = title.lower()

        important_titles = [
            "introduction",
            "architecture",
            "data independence",
            "data model",
            "entity",
            "relational",
            "sql",
            "normalization",
            "transaction",
            "acid",
            "concurrency",
            "indexing",
            "file organization",
            "recovery",
        ]

        for keyword in important_titles:
            if keyword in title_lower:
                score += 4.0

        if cls.is_definition(text):
            score += 2.0

        score += min(
            len(cls.tokenize(text)) / 50,
            5.0,
        )

        return score

    # ============================================================
    # 22. REMOVE DUPLICATES
    # ============================================================

    @classmethod
    def remove_duplicate_sentences(cls, sentences):
        result = []

        for sentence in sentences:

            if cls.is_redundant(
                sentence,
                result,
            ):
                continue

            result.append(sentence)

        return result

    # ============================================================
    # 23. FORMAT SENTENCE
    # ============================================================

    @classmethod
    def format_sentence(cls, sentence):
        sentence = sentence.strip()

        if not sentence:
            return ""

        # Remove accidental leading punctuation
        sentence = re.sub(
            r"^[,;:)\]}]+",
            "",
            sentence,
        ).strip()

        # Normalize spaces
        sentence = re.sub(
            r"\s+",
            " ",
            sentence,
        )

        # Fix spacing around punctuation
        sentence = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            sentence,
        )

        # Capitalize if necessary
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]

        # Add period
        if not sentence.endswith(
            (".", "!", "?")
        ):
            sentence += "."

        return sentence

    # ============================================================
    # 24. FORMAT SUMMARY
    # ============================================================

    @classmethod
    def format_summary(cls, sentences):
        formatted = []

        for sentence in sentences:

            sentence = cls.format_sentence(
                sentence
            )

            if not sentence:
                continue

            if cls.is_garbage_sentence(sentence):
                continue

            formatted.append(sentence)

        return " ".join(formatted).strip()

    # ============================================================
    # 25. LIMIT WORD COUNT
    # ============================================================

    @classmethod
    def limit_words(cls, text, max_words):

        words = text.split()

        if len(words) <= max_words:
            return text

        shortened = " ".join(
            words[:max_words]
        )

        # Don't leave incomplete punctuation
        last_period = max(
            shortened.rfind("."),
            shortened.rfind("!"),
            shortened.rfind("?"),
        )

        if last_period >= max_words * 0.65:
            shortened = shortened[
                :last_period + 1
            ]

        else:
            shortened += "..."

        return shortened

    # ============================================================
    # 26. MAIN SUMMARIZATION
    # ============================================================

    @classmethod
    def summarize_text(
        cls,
        text,
        length="medium",
    ):
        """
        Main public method.

        IMPORTANT:
        This method signature remains compatible with the
        existing SmartNotes backend.
        """

        try:

            if not text:
                return ""

            # ----------------------------------------------------
            # Validate length
            # ----------------------------------------------------

            length = str(
                length or "medium"
            ).lower()

            if length not in cls.LENGTH_SETTINGS:
                length = "medium"

            settings = cls.LENGTH_SETTINGS[
                length
            ]

            # ----------------------------------------------------
            # Clean PDF/OCR text
            # ----------------------------------------------------

            cleaned_text = cls.clean_pdf_text(
                text
            )

            if not cleaned_text:
                return ""

            # ----------------------------------------------------
            # Conservative spelling correction
            # ----------------------------------------------------

            cleaned_text = cls.correct_spelling(
                cleaned_text
            )

            # ----------------------------------------------------
            # Split into academic sections
            # ----------------------------------------------------

            sections = cls.split_into_sections(
                cleaned_text
            )

            if not sections:
                sections = [{
                    "title": "Notes",
                    "text": cleaned_text,
                }]

            # ----------------------------------------------------
            # Remove useless tiny sections
            # ----------------------------------------------------

            valid_sections = []

            for section in sections:

                section_text = section["text"]

                if len(section_text.split()) < 5:
                    continue

                valid_sections.append(section)

            if valid_sections:
                sections = valid_sections

            # ----------------------------------------------------
            # Score sections
            # ----------------------------------------------------

            for section in sections:
                section["score"] = cls.score_section(
                    section
                )

            # ----------------------------------------------------
            # Important sections first
            # ----------------------------------------------------

            sections.sort(
                key=lambda item: item["score"],
                reverse=True,
            )

            sections = sections[
                :settings["max_sections"]
            ]

            # ----------------------------------------------------
            # Select content from each section
            # ----------------------------------------------------

            selected_sentences = []

            for section in sections:

                # At least one important sentence
                # from each meaningful section.
                section_sentence_limit = 2

                if length == "long":
                    section_sentence_limit = 3

                section_sentences = (
                    cls.select_section_sentences(
                        section,
                        section_sentence_limit,
                    )
                )

                for sentence in section_sentences:

                    if cls.is_redundant(
                        sentence,
                        selected_sentences,
                    ):
                        continue

                    selected_sentences.append(
                        sentence
                    )

            # ----------------------------------------------------
            # If selection is too small, fill from best sections
            # ----------------------------------------------------

            if len(selected_sentences) < 4:

                for section in sections:

                    additional = (
                        cls.select_section_sentences(
                            section,
                            4,
                        )
                    )

                    for sentence in additional:

                        if cls.is_redundant(
                            sentence,
                            selected_sentences,
                        ):
                            continue

                        selected_sentences.append(
                            sentence
                        )

                        if (
                            len(selected_sentences)
                            >= settings["max_sentences"]
                        ):
                            break

                    if (
                        len(selected_sentences)
                        >= settings["max_sentences"]
                    ):
                        break

            # ----------------------------------------------------
            # Final redundancy removal
            # ----------------------------------------------------

            selected_sentences = (
                cls.remove_duplicate_sentences(
                    selected_sentences
                )
            )

            # ----------------------------------------------------
            # Limit number of sentences
            # ----------------------------------------------------

            selected_sentences = (
                selected_sentences[
                    :settings["max_sentences"]
                ]
            )

            # ----------------------------------------------------
            # Format
            # ----------------------------------------------------

            summary = cls.format_summary(
                selected_sentences
            )

            # ----------------------------------------------------
            # Limit words
            # ----------------------------------------------------

            summary = cls.limit_words(
                summary,
                settings["max_words"],
            )

            # ----------------------------------------------------
            # Final safety cleanup
            # ----------------------------------------------------

            summary = re.sub(
                r"\s+",
                " ",
                summary,
            ).strip()

            # ----------------------------------------------------
            # Fallback
            # ----------------------------------------------------

            if not summary:

                fallback_sentences = (
                    cls.split_sentences(
                        cleaned_text
                    )
                )

                fallback_sentences = (
                    fallback_sentences[
                        :settings["max_sentences"]
                    ]
                )

                summary = cls.format_summary(
                    fallback_sentences
                )

                summary = cls.limit_words(
                    summary,
                    settings["max_words"],
                )

            return summary

        except Exception as exc:

            # Never allow summarization failure
            # to break note upload.
            print(
                "SUMMARIZATION ERROR:",
                str(exc),
            )

            # Safe fallback
            try:

                cleaned = cls.normalize_text(
                    text or ""
                )

                sentences = cls.split_sentences(
                    cleaned
                )

                summary = cls.format_summary(
                    sentences[:10]
                )

                return cls.limit_words(
                    summary,
                    200,
                )

            except Exception:

                return str(text or "")[:2000]