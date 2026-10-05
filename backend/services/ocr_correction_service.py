"""
SmartNotes AI
Advanced OCR Correction Service

Designed for:
- Handwritten notes
- Printed notes
- Scanned PDFs
- PaddleOCR output
- Academic notes
- Technical notes

Pipeline:
OCR text
    ↓
Character normalization
    ↓
Known OCR correction
    ↓
Character confusion correction
    ↓
Technical vocabulary protection
    ↓
Safe spelling correction
    ↓
Technical vocabulary restoration
    ↓
OCR garbage removal
    ↓
Final cleanup
"""

import re
from difflib import SequenceMatcher

try:
    from spellchecker import SpellChecker
    SPELLCHECKER_AVAILABLE = True
except ImportError:
    SpellChecker = None
    SPELLCHECKER_AVAILABLE = False


class OCRCorrectionService:

    # ==========================================================
    # TECHNICAL / ACADEMIC VOCABULARY
    # ==========================================================

    TECHNICAL_TERMS = {
        # DBMS
        "dbms", "database", "databases", "schema", "schemas",
        "sql", "nosql", "mysql", "mongodb",
        "relation", "relations", "relational",
        "tuple", "tuples", "attribute", "attributes",
        "domain", "domains", "primary", "foreign",
        "candidate", "composite", "superkey",
        "key", "keys", "entity", "entities",
        "relationship", "relationships", "cardinality",
        "aggregation", "generalization", "specialization",
        "normalization", "normal", "functional",
        "dependency", "dependencies", "transaction",
        "transactions", "concurrency", "serializability",
        "serializable", "deadlock", "index", "indexes",
        "indexing", "recovery", "checkpoint",
        "checkpointing", "acid", "atomicity",
        "consistency", "isolation", "durability",
        "ddl", "dml", "dcl", "tcl",
        "select", "insert", "update", "delete",
        "create", "alter", "drop", "truncate",
        "join", "joins", "query", "queries",
        "view", "views", "trigger", "triggers",
        "b-tree", "b+tree", "mvcc",

        # Programming
        "java", "python", "javascript", "typescript",
        "react", "node", "nodejs", "flask",
        "spring", "springboot", "html", "html5",
        "css", "css3", "jsx", "api", "apis",
        "rest", "http", "https", "json", "xml",
        "frontend", "backend", "fullstack", "full-stack",
        "function", "functions", "class", "classes",
        "object", "objects", "method", "methods",
        "git", "github", "npm", "vite",

        # AI / ML
        "ai", "artificial", "intelligence",
        "machine", "learning", "deep", "neural",
        "network", "networks", "model", "models",
        "dataset", "datasets", "training", "testing",
        "validation", "prediction", "classification",
        "regression", "llm", "llms", "transformer",
        "transformers", "embedding", "embeddings",
        "tokenizer", "ocr", "paddleocr", "opencv",
        "tensorflow", "pytorch",

        # Academic
        "algorithm", "algorithms", "architecture",
        "implementation", "performance", "security",
        "integrity", "authentication", "authorization",
        "analysis", "concept", "concepts",
        "principle", "principles", "process",
        "processes", "structure", "structures",
        "advantage", "advantages", "disadvantage",
        "disadvantages", "characteristic",
        "characteristics", "feature", "features",
        "objective", "objectives", "application",
        "applications",
    }

    # ==========================================================
    # COMMON OCR CORRECTIONS
    # ==========================================================

    OCR_CORRECTIONS = {

        # General OCR errors
        "artifical": "artificial",
        "artificalintelligence": "artificial intelligence",
        "intelligance": "intelligence",

        "machlne": "machine",
        "machinee": "machine",

        "learnlng": "learning",
        "leaming": "learning",
        "leaming": "learning",

        "algorlthm": "algorithm",
        "algorithrn": "algorithm",
        "algorilhm": "algorithm",

        "databse": "database",
        "databa5e": "database",
        "databaze": "database",

        "summarizatlon": "summarization",
        "summarizati0n": "summarization",

        "transactlon": "transaction",
        "transacti0n": "transaction",

        "concurrencv": "concurrency",
        "concurreney": "concurrency",
        "concurency": "concurrency",

        "dependencv": "dependency",
        "dependancy": "dependency",

        "independance": "independence",
        "independency": "independence",

        "physlcal": "physical",
        "physicaI": "physical",

        "loglcal": "logical",
        "logicaI": "logical",

        "extemal": "external",
        "intemal": "internal",

        "consistencv": "consistency",
        "consisteney": "consistency",

        "integritv": "integrity",

        "securitv": "security",

        "authentlcation": "authentication",
        "authentlcatlon": "authentication",

        "authorizatlon": "authorization",

        "organizatlon": "organization",

        # DBMS
        "dbm": "DBMS",
        "dmbs": "DBMS",
        "dbms": "DBMS",

        "sparc": "SPARC",
        "spare": "SPARC",
        "ansi/spare": "ANSI/SPARC",

        "normalizatlon": "normalization",
        "normalizaton": "normalization",

        "relaton": "relation",
        "relatlon": "relation",

        "relatonal": "relational",
        "relatlonal": "relational",

        "attrlbute": "attribute",
        "atribute": "attribute",

        "cardlnality": "cardinality",

        "serializabilty": "serializability",

        "deadlok": "deadlock",

        "lndex": "index",
        "lndexing": "indexing",

        "recoverv": "recovery",

        # AI
        "artiflcial": "artificial",
        "intelllgence": "intelligence",

        "neuraI": "neural",

        "netw0rk": "network",
        "netwrok": "network",

        # Common OCR examples
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
    }

    # ==========================================================
    # WORDS THAT SHOULD NEVER BE AUTO-CORRECTED
    # ==========================================================

    PROTECTED_WORDS = {
        "ai", "dbms", "sql", "nosql", "mysql",
        "mongodb", "ddl", "dml", "dcl", "tcl",
        "acid", "api", "rest", "json", "xml",
        "ocr", "llm", "html", "css", "jsx",
        "npm", "git", "github", "java", "python",
        "react", "flask", "spring", "node",
        "nodejs", "opencv", "tensorflow",
        "pytorch", "paddleocr", "mvcc", "sparc",
    }

    # ==========================================================
    # CONSTRUCTOR
    # ==========================================================

    def __init__(self):

        self.spellchecker = None

        if SPELLCHECKER_AVAILABLE:

            try:
                self.spellchecker = SpellChecker(distance=2)

                # Add technical vocabulary to spellchecker
                self.spellchecker.word_frequency.load_words(
                    list(self.TECHNICAL_TERMS)
                )

            except Exception as exc:

                print(
                    "Spell checker initialization failed:",
                    exc
                )

                self.spellchecker = None

    # ==========================================================
    # NORMALIZE TEXT
    # ==========================================================

    def normalize_text(self, text):

        if not text:
            return ""

        text = str(text)

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        replacements = {
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u2212": "-",
            "\u00a0": " ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = text.replace("\x00", " ")

        # Remove URLs
        text = re.sub(
            r"https?://\S+",
            " ",
            text,
            flags=re.IGNORECASE
        )

        # Remove email addresses
        text = re.sub(
            r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
            " ",
            text
        )

        # Normalize spaces while preserving new lines
        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        # Normalize blank lines
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()

    # ==========================================================
    # APPLY KNOWN OCR CORRECTIONS
    # ==========================================================

    def apply_known_corrections(self, text):

        if not text:
            return ""

        corrections = sorted(
            self.OCR_CORRECTIONS.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for wrong, correct in corrections:

            pattern = (
                r"(?<![A-Za-z0-9])"
                + re.escape(wrong)
                + r"(?![A-Za-z0-9])"
            )

            text = re.sub(
                pattern,
                correct,
                text,
                flags=re.IGNORECASE
            )

        return text

    # ==========================================================
    # PROTECTED WORD CHECK
    # ==========================================================

    def is_protected_word(self, word):

        cleaned = re.sub(
            r"[^A-Za-z0-9+#.-]",
            "",
            word
        ).lower()

        if not cleaned:
            return True

        if cleaned in self.PROTECTED_WORDS:
            return True

        technical_terms_lower = {
            term.lower()
            for term in self.TECHNICAL_TERMS
        }

        if cleaned in technical_terms_lower:
            return True

        technical_patterns = [
            r"^[a-z]+ocr$",
            r"^[a-z]+api$",
            r"^[a-z]+sql$",
            r"^[a-z]+js$",
            r"^[a-z]+ml$",
            r"^[a-z]+ai$",
        ]

        for pattern in technical_patterns:

            if re.match(pattern, cleaned):
                return True

        return False

    # ==========================================================
    # PROTECT TECHNICAL TERMS
    #
    # IMPORTANT:
    # Do NOT protect normal academic words such as:
    # machine, learning, database, algorithm.
    #
    # Only protect explicitly protected technical names.
    # ==========================================================

    def protect_terms(self, text):

        protected = {}
        counter = 0

        # Only protect words from PROTECTED_WORDS.
        protected_words = sorted(
            self.PROTECTED_WORDS,
            key=len,
            reverse=True
        )

        if not protected_words:
            return text, protected

        pattern = re.compile(
            r"(?<![A-Za-z0-9])("
            + "|".join(
                re.escape(word)
                for word in protected_words
            )
            + r")(?![A-Za-z0-9])",
            re.IGNORECASE
        )

        def replace(match):

            nonlocal counter

            word = match.group(0)

            key = f"TECHTERMPLACEHOLDER{counter}END"

            protected[key] = word

            counter += 1

            return key

        result = pattern.sub(
            replace,
            text
        )

        return result, protected

    # ==========================================================
    # RESTORE TECHNICAL TERMS
    # ==========================================================

    def restore_terms(self, text, protected):

        if not protected:
            return text

        for key, value in protected.items():

            text = text.replace(
                key,
                value
            )

        return text

    # ==========================================================
    # SAFE SPELLING CORRECTION
    # ==========================================================

    def spell_correct_word(self, word):

        if not word:
            return word

        if self.is_protected_word(word):
            return word

        if re.search(r"\d", word):
            return word

        if len(word) <= 3:
            return word

        if "-" in word:

            parts = word.split("-")

            corrected_parts = []

            for part in parts:

                corrected_parts.append(
                    self.spell_correct_word(part)
                )

            return "-".join(corrected_parts)

        if self.spellchecker is None:
            return word

        lower = word.lower()

        if lower in self.spellchecker:
            return word

        try:

            candidates = self.spellchecker.candidates(
                lower
            )

        except Exception:

            return word

        if not candidates:
            return word

        try:

            best = self.spellchecker.correction(
                lower
            )

        except Exception:

            return word

        if not best:
            return word

        best = str(best)

        length_difference = abs(
            len(best) - len(word)
        )

        if length_difference > 2:
            return word

        similarity = SequenceMatcher(
            None,
            lower,
            best.lower()
        ).ratio()

        # Conservative thresholds
        if len(word) <= 5:

            if similarity < 0.75:
                return word

        else:

            if similarity < 0.65:
                return word

        # Preserve capitalization
        if word.isupper():
            return best.upper()

        if word[0].isupper():

            return (
                best[:1].upper()
                + best[1:]
            )

        return best

    # ==========================================================
    # CORRECT INDIVIDUAL WORDS
    # ==========================================================

    def correct_words(self, text):

        if not text:
            return ""

        corrected = []

        # Correct token pattern.
        # No accidental literal "*" at the end.
        tokens = re.findall(
            r"[A-Za-z][A-Za-z0-9+#./-]*|"
            r"[^A-Za-z0-9\s]+|"
            r"\s+",
            text
        )

        for token in tokens:

            if token.isspace():

                corrected.append(token)
                continue

            if not re.search(
                r"[A-Za-z]",
                token
            ):

                corrected.append(token)
                continue

            corrected_word = self.spell_correct_word(
                token
            )

            corrected.append(
                corrected_word
            )

        return "".join(corrected)

    # ==========================================================
    # CHARACTER CONFUSIONS
    # ==========================================================

    def fix_character_confusions(self, text):

        if not text:
            return ""

        replacements = [

            (
                r"(?<=[A-Za-z])0(?=[A-Za-z])",
                "o"
            ),

            (
                r"(?<=[A-Za-z])1(?=[A-Za-z])",
                "l"
            ),

            (
                r"(?<=[A-Za-z])5(?=[A-Za-z])",
                "s"
            ),
        ]

        for pattern, replacement in replacements:

            text = re.sub(
                pattern,
                replacement,
                text
            )

        return text

    # ==========================================================
    # FIX WORD BOUNDARIES
    # ==========================================================

    def fix_word_boundaries(self, text):

        if not text:
            return ""

        merged_words = {

            "databaseis": "database is",
            "dbmsis": "DBMS is",
            "schemais": "schema is",
            "itis": "it is",
            "thisis": "this is",
            "thereare": "there are",
            "thereis": "there is",
            "canbe": "can be",
            "usedfor": "used for",
            "consistsof": "consists of",
            "refersto": "refers to",
            "definedas": "defined as",
        }

        for wrong, correct in merged_words.items():

            text = re.sub(
                r"\b"
                + re.escape(wrong)
                + r"\b",
                correct,
                text,
                flags=re.IGNORECASE
            )

        return text

    # ==========================================================
    # REMOVE OCR GARBAGE
    # ==========================================================

    def remove_ocr_garbage(self, text):

        if not text:
            return ""

        lines = text.split("\n")

        cleaned_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Page numbers
            if re.fullmatch(
                r"(page\s*)?\d+",
                line,
                flags=re.IGNORECASE
            ):
                continue

            punctuation_count = len(
                re.findall(
                    r"[^A-Za-z0-9\s]",
                    line
                )
            )

            if (
                len(line) > 10
                and punctuation_count
                > len(line) * 0.45
            ):
                continue

            # Repeated characters
            if re.search(
                r"(.)\1{4,}",
                line
            ):
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    # ==========================================================
    # FINAL CLEANUP
    # ==========================================================

    def final_cleanup(self, text):

        if not text:
            return ""

        # Remove spaces before punctuation
        text = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            text
        )

        # Add missing spaces after punctuation
        text = re.sub(
            r"([,.!?;:])([A-Za-z])",
            r"\1 \2",
            text
        )

        # Multiple spaces
        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        # Multiple blank lines
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()

    # ==========================================================
    # MAIN CORRECTION METHOD
    # ==========================================================

    def correct_text(self, text):

        if not text:
            return ""

        # 1. Normalize
        text = self.normalize_text(text)

        # 2. Known OCR corrections
        text = self.apply_known_corrections(text)

        # 3. Character-level correction
        text = self.fix_character_confusions(text)

        # 4. Fix merged words
        text = self.fix_word_boundaries(text)

        # 5. Protect only true technical identifiers
        text, protected = self.protect_terms(text)

        # 6. Spell correction
        text = self.correct_words(text)

        # 7. Restore technical vocabulary
        text = self.restore_terms(
            text,
            protected
        )

        # 8. Apply known corrections again
        text = self.apply_known_corrections(text)

        # 9. Remove OCR garbage
        text = self.remove_ocr_garbage(text)

        # 10. Final cleanup
        text = self.final_cleanup(text)

        return text

    # ==========================================================
    # LINE-BY-LINE CORRECTION
    # ==========================================================

    def correct_lines(self, text):

        if not text:
            return ""

        lines = text.split("\n")

        corrected_lines = []

        for line in lines:

            line = line.strip()

            if not line:

                corrected_lines.append("")

                continue

            corrected = self.correct_text(
                line
            )

            if corrected:

                corrected_lines.append(
                    corrected
                )

        return "\n".join(
            corrected_lines
        )


# ==============================================================
# SINGLETON INSTANCE
# ==============================================================

ocr_correction_service = OCRCorrectionService()


# ==============================================================
# EASY FUNCTION FOR OTHER FILES
# ==============================================================

def correct_ocr_text(text):

    return ocr_correction_service.correct_text(
        text
    )