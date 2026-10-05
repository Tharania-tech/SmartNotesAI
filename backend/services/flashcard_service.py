import re
import unicodedata

from services.concept_service import ConceptService

# Optional dictionary-based spelling correction.
# Install once with:   pip install pyspellchecker
try:
    from spellchecker import SpellChecker
except Exception:
    SpellChecker = None


class FlashcardService:

    # =========================================================
    # RELATION RULES (used to match QUESTION <-> ANSWER)
    #
    # The text that comes IMMEDIATELY AFTER the concept decides
    # the question type. Old code searched the whole sentence,
    # which produced questions that did not match the answer.
    # =========================================================
    RELATION_RULES = [
        (r"stands?\s+for", "stand_for"),
        (r"(?:is|are)\s+defined\s+as", "define"),
        (r"refers?\s+to", "define"),
        (r"(?:is|are)\s+(?:made\s+up\s+of|composed\s+of)", "consist"),
        (r"(?:consists?\s+of|comprises?)", "consist"),
        (r"(?:is|are)\s+(?:used|utilized)\s+(?:to|for)", "used"),
        (r"(?:is|are)\s+responsible\s+for", "responsible"),
        (r"can\s+be\s+used", "can_use"),
        (r"(?:is|are)\s+(?:a|an|the)\b", "define"),
        (r"means\b", "define"),
        (r"mean\b", "define"),
        (r"(?:contains?|includes?)", "contain"),
        (r"provides?", "provide"),
        (r"allows?", "allow"),
        (r"enables?", "enable"),
        (r"helps?", "help"),
        (r"performs?", "perform"),
        (r"represents?", "represent"),
        (r"describes?", "describe"),
        (r"defines?", "define_verb"),
        (r"supports?", "support"),
    ]

    PLURAL_VERBS = {
        "are", "stand", "refer", "mean", "consist", "comprise",
        "contain", "include", "provide", "allow", "enable", "help",
        "perform", "represent", "describe", "define", "support"
    }

    LEADING_CONNECTORS = (
        r"^(?:however|also|thus|therefore|moreover|furthermore|"
        r"additionally|in addition|hence|consequently|similarly|"
        r"likewise|then|so|but|and|or|besides|finally|firstly|"
        r"secondly|thirdly)\s*,?\s+"
    )

    # =========================================================
    # SPELLING CORRECTION SUPPORT
    # =========================================================
    _spell_checker = None
    _spell_loaded = False

    @classmethod
    def _get_spell_checker(cls):
        if not cls._spell_loaded:
            cls._spell_loaded = True
            if SpellChecker is not None:
                try:
                    cls._spell_checker = SpellChecker()
                except Exception:
                    cls._spell_checker = None
        return cls._spell_checker

    # =========================================================
    # FIX LIST MARKERS MISREAD BY OCR
    # "include 9) Standards ... ; and ii) standards ..."
    #  ->  "include i) Standards ... ; and ii) standards ..."
    # =========================================================
    @staticmethod
    def fix_list_markers(text):
        if not text:
            return text

        # "9)" / "(9)" that is followed by "ii)" shortly after
        # is really the first roman numeral "i)"
        text = re.sub(
            r"(?<![\w.])\(?9\)(?=.{0,500}?(?<![\w])\(?ii\))",
            "i)",
            text,
            flags=re.DOTALL
        )

        # "1)" misread as "l)" / "I)" before "ii)"
        text = re.sub(
            r"(?<![\w.])\(?[lI]\)(?=.{0,500}?(?<![\w])\(?ii\))",
            "i)",
            text,
            flags=re.DOTALL
        )

        return text

    # =========================================================
    # PICK BEST CORRECTION FOR ONE MISSPELLED WORD
    # =========================================================
    @classmethod
    def _best_correction(cls, lower_word, doc_counts):

        spell = cls._get_spell_checker()

        # Words that appear several times in the document with
        # a good frequency are the document's own vocabulary
        # (used also when no dictionary is installed).
        if spell is None:
            return None

        if len(lower_word) <= 5:
            candidates = spell.known(
                spell.edit_distance_1(lower_word)
            )
        else:
            candidates = spell.candidates(lower_word)

        if not candidates:
            return None

        candidates = set(candidates)

        # Prefer a candidate that the document itself uses
        in_document = [
            word for word in candidates
            if doc_counts.get(word, 0) >= 2
        ]

        if in_document:
            best = max(
                in_document,
                key=lambda word: doc_counts.get(word, 0)
            )
        else:
            best = max(
                candidates,
                key=lambda word: spell.word_frequency[word]
            )

        # Keep plural / "-es" endings the OCR text still has:
        # "acdrees" -> "address" -> "addresses"
        if lower_word.endswith("s") and not best.endswith("s"):

            for suffix in ("es", "s"):

                if best + suffix in spell:
                    best = best + suffix
                    break

        elif (
            lower_word.endswith("s")
            and best.endswith("ss")
            and best + "es" in spell
        ):
            best = best + "es"

        return best

    # =========================================================
    # CORRECT SPELLING MISTAKES (OCR / extraction errors)
    #
    # Only words that are NOT in the dictionary are touched.
    # Acronyms, code, camelCase, words with digits, repeated
    # document terms and short capitalized names are protected.
    # =========================================================
    @classmethod
    def correct_spelling(cls, text):

        if not text:
            return text

        spell = cls._get_spell_checker()

        if spell is None:
            return text

        token_pattern = re.compile(
            r"(?<![\w@./\\#$%&-])[A-Za-z]{4,}(?![\w@./\\(-])"
        )

        # How often each word appears in the whole document
        doc_counts = {}

        for token in re.findall(r"[A-Za-z]+", text):

            key = token.lower()
            doc_counts[key] = doc_counts.get(key, 0) + 1

        cache = {}
        output_lines = []

        for line in text.split("\n"):

            # Do not touch code / markup lines
            if (
                cls.is_code_like(line)
                or re.search(r"[{}<>=]|\w\(\)", line)
            ):
                output_lines.append(line)
                continue

            def replace(match):

                word = match.group(0)
                lower_word = word.lower()

                # Acronyms / camelCase
                if word.isupper():
                    return word

                if re.search(r"[a-z][A-Z]", word):
                    return word

                # Already a real word
                if lower_word in spell:
                    return word

                # Repeated many times -> real technical term
                if doc_counts.get(lower_word, 0) >= 3:
                    return word

                # Short capitalized word in the middle of a
                # sentence is probably a name / technology
                if word[0].isupper() and len(word) <= 7:

                    before = line[:match.start()].rstrip(" \t")

                    sentence_start = (
                        not before
                        or before[-1] in ".!?:;)"
                    )

                    if not sentence_start:
                        return word

                if lower_word not in cache:
                    cache[lower_word] = cls._best_correction(
                        lower_word,
                        doc_counts
                    )

                corrected = cache[lower_word]

                if not corrected:
                    return word

                if word[0].isupper():
                    corrected = (
                        corrected[0].upper()
                        + corrected[1:]
                    )

                return corrected

            output_lines.append(
                token_pattern.sub(replace, line)
            )

        return "\n".join(output_lines)

    # =========================================================
    # FIX ALL OCR-STYLE ERRORS
    # =========================================================
    @classmethod
    def fix_ocr_errors(cls, text):

        text = cls.fix_list_markers(text)
        text = cls.correct_spelling(text)

        return text

    # =========================================================
    # TEXT REPAIR  (fixes spelling errors caused by PDF/DOC
    # extraction: ligatures, broken hyphenation, odd characters)
    # =========================================================
    @staticmethod
    def repair_text(text):
        if not text:
            return ""

        # Normalize unicode (fixes ligatures such as ﬁ ﬂ ﬀ ﬃ)
        text = unicodedata.normalize("NFKC", text)

        # Remove invisible / control characters
        text = text.replace("\u00ad", "")
        text = re.sub(r"[\u200b\u200c\u200d\u2060\ufeff]", "", text)
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
        text = text.replace("\ufffd", "")

        # Smart quotes / dashes to plain characters
        text = (
            text.replace("\u2018", "'")
            .replace("\u2019", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2013", "-")
            .replace("\u2014", " - ")
            .replace("\u00a0", " ")
        )

        # Join words broken by line-end hyphenation:
        # "docu-\nment" -> "document"
        text = re.sub(
            r"([A-Za-z])-[ \t]*\r?\n[ \t]*([a-z])",
            r"\1\2",
            text
        )

        # Missing space after a full stop: "end.The" -> "end. The"
        text = re.sub(
            r"([a-z])\.([A-Z][a-z])",
            r"\1. \2",
            text
        )

        return text

    # =========================================================
    # GARBLED TEXT CHECK
    # =========================================================
    @staticmethod
    def is_garbled(sentence):
        if not sentence:
            return True

        letters = sum(1 for ch in sentence if ch.isalpha())
        total = len(sentence)

        if total == 0 or letters / total < 0.6:
            return True

        words = sentence.split()

        if not words:
            return True

        single_letter_words = sum(
            1 for word in words
            if len(word.strip(".,;:()")) == 1
            and word.lower().strip(".,;:()") not in ("a", "i")
        )

        if single_letter_words / len(words) > 0.25:
            return True

        # Same character repeated many times (OCR noise)
        if re.search(r"(.)\1{4,}", sentence):
            return True

        return False

    # =========================================================
    # METADATA CHECK
    # =========================================================
    @staticmethod
    def is_metadata_sentence(sentence):
        if not sentence:
            return True

        sentence_lower = sentence.lower().strip()

        metadata_patterns = [
            r"\bpublisher\b",
            r"\bpublished by\b",
            r"\bpublication\b",
            r"\bauthor\b",
            r"\bedition\b",
            r"\bvolume\b",
            r"\bissue\b",
            r"\bdepartment\b",
            r"\bdept\.?\b",
            r"\buniversity\b",
            r"\bcollege\b",
            r"\binstitute\b",
            r"\bacademy\b",
            r"\bschool of\b",
            r"\bcopyright\b",
            r"\bwww\.",
            r"https?://",
            r"\bdoi\b",
            r"\bissn\b",
            r"\bisbn\b"
        ]

        for pattern in metadata_patterns:
            if re.search(pattern, sentence_lower):
                return True

        if re.fullmatch(
            r"https?://\S+",
            sentence_lower
        ):
            return True

        if re.fullmatch(
            r"[\w\-.]+@[\w\-.]+\.\w+",
            sentence_lower
        ):
            return True

        return False

    # =========================================================
    # CODE CHECK
    # =========================================================
    @staticmethod
    def is_code_like(sentence):
        if not sentence:
            return False

        sentence_lower = sentence.lower()

        code_patterns = [
            "public static void",
            "private static void",
            "public class",
            "private class",
            "import java.",
            "import javax.",
            "from flask import",
            "def ",
            "return ",
            "console.log",
            "system.out.println",
            "function ",
            "for (",
            "while (",
            "if (",
            "else {",
            "=>",
            "&&",
            "||",
            "==",
            "!="
        ]

        score = 0

        for pattern in code_patterns:
            if pattern in sentence_lower:
                score += 1

        return score >= 2

    # =========================================================
    # CLEAN DOCUMENT TEXT
    # =========================================================
    @classmethod
    def clean_document_text(cls, text):
        if not text:
            return ""

        # Repair extraction problems first
        text = cls.repair_text(text)

        # Fix OCR spelling mistakes and wrong list markers
        text = cls.fix_ocr_errors(text)

        lines = text.splitlines()

        cleaned_lines = []

        for line in lines:

            line = re.sub(
                r"\s+",
                " ",
                line
            ).strip()

            if not line:
                continue

            # Remove bullet symbols at the start of a line
            line = re.sub(
                r"^[\u2022\u25aa\u25cf\u00b7\u2023\u25e6•▪●■□◦]\s*",
                "",
                line
            ).strip()

            if not line:
                continue

            # Remove page numbers
            if re.fullmatch(
                r"(page\s*)?\d+",
                line.lower()
            ):
                continue

            # Remove URLs
            if re.fullmatch(
                r"https?://\S+",
                line.lower()
            ):
                continue

            cleaned_lines.append(line)

        # =====================================================
        # REMOVE REPEATED HEADER / FOOTER LINES
        # =====================================================
        frequency = {}

        for line in cleaned_lines:

            normalized = line.lower().strip()

            if len(normalized) < 4:
                continue

            frequency[normalized] = (
                frequency.get(normalized, 0) + 1
            )

        final_lines = []

        for line in cleaned_lines:

            normalized = line.lower().strip()

            if (
                frequency.get(normalized, 0) >= 3
                and len(normalized.split()) <= 10
            ):
                continue

            final_lines.append(line)

        # =====================================================
        # REJOIN LINES THAT WERE WRAPPED INSIDE A SENTENCE
        # (prevents sentences being cut in the middle, which
        #  caused incomplete / mismatched answers)
        # =====================================================
        merged_lines = []

        for line in final_lines:

            if (
                merged_lines
                and not re.search(r"[.!?:;]$", merged_lines[-1])
                and line[0].islower()
            ):
                merged_lines[-1] = (
                    merged_lines[-1] + " " + line
                )
            else:
                merged_lines.append(line)

        # =====================================================
        # END HEADINGS WITH A FULL STOP SO THAT A HEADING IS
        # NOT GLUED TO THE NEXT SENTENCE
        # =====================================================
        result_lines = []

        for index, line in enumerate(merged_lines):

            is_last = index == len(merged_lines) - 1

            if (
                not is_last
                and len(line.split()) <= 8
                and not re.search(r"[.!?:;,)\]]$", line)
                and merged_lines[index + 1][0].isupper()
            ):
                line = line + "."

            result_lines.append(line)

        return "\n".join(result_lines)

    # =========================================================
    # EXACT CONCEPT MATCH
    # =========================================================
    @staticmethod
    def concept_exists(concept, sentence):

        concept = concept.strip().lower()
        sentence = sentence.lower()

        if not concept:
            return False

        pattern = (
            r"(?<!\w)"
            + re.escape(concept)
            + r"(?!\w)"
        )

        return re.search(
            pattern,
            sentence
        ) is not None

    # =========================================================
    # GET SENTENCES
    # =========================================================
    @classmethod
    def get_useful_sentences(cls, text):

        sentences = ConceptService.split_sentences(
            text
        )

        useful_sentences = []

        for sentence in sentences:

            sentence = re.sub(
                r"\s+",
                " ",
                sentence
            ).strip()

            if not sentence:
                continue

            if cls.is_metadata_sentence(sentence):
                continue

            if cls.is_code_like(sentence):
                continue

            if cls.is_garbled(sentence):
                continue

            word_count = len(
                sentence.split()
            )

            if word_count < 5:
                continue

            if word_count > 80:
                continue

            useful_sentences.append(
                sentence
            )

        return useful_sentences

    # =========================================================
    # IMPORTANT:
    # CHECK WHETHER CONCEPT IS THE MAIN SUBJECT
    # =========================================================
    @staticmethod
    def is_main_subject(concept, sentence):

        concept_lower = concept.lower().strip()
        sentence_lower = sentence.lower().strip()

        if not concept_lower:
            return False

        # -----------------------------------------------------
        # Find exact position of concept
        # -----------------------------------------------------
        pattern = (
            r"(?<!\w)"
            + re.escape(concept_lower)
            + r"(?!\w)"
        )

        match = re.search(
            pattern,
            sentence_lower
        )

        if not match:
            return False

        concept_start = match.start()

        before = sentence_lower[
            :concept_start
        ].strip()

        # -----------------------------------------------------
        # CASE 1:
        # Concept is at the beginning
        # -----------------------------------------------------
        if not before:
            return True

        # -----------------------------------------------------
        # CASE 2:
        # "The XML is..."  /  "An XML document is..."
        # -----------------------------------------------------
        allowed_prefixes = [
            "the",
            "a",
            "an"
        ]

        before_words = before.split()

        if len(before_words) <= 2:

            if all(
                word in allowed_prefixes
                for word in before_words
            ):
                return True

        # -----------------------------------------------------
        # CASE 3:
        # "In XML, ..." is not a definition sentence
        # -----------------------------------------------------
        blocked_prefix_patterns = [
            r"\bin\s*$",
            r"\bfor\s*$",
            r"\bof\s*$",
            r"\bfrom\s*$",
            r"\bwith\s*$",
            r"\busing\s*$",
            r"\binto\s*$",
            r"\bon\s*$",
            r"\bby\s*$",
            r"\bas\s*$",
            r"\babout\s*$",
            r"\bbetween\s*$",
            r"\bthrough\s*$",
            r"\bvia\s*$",
            r"\busing\s+the\s*$",
            r"\bfor\s+the\s*$"
        ]

        for blocked_pattern in blocked_prefix_patterns:

            if re.search(
                blocked_pattern,
                before
            ):
                return False

        # -----------------------------------------------------
        # CASE 4:
        # Concept occurs after another technical subject
        # "DOM is an API for XML documents."
        # -----------------------------------------------------
        if len(before_words) > 2:

            subject_markers = [
                " is ",
                " are ",
                " was ",
                " were ",
                " means ",
                " refers to ",
                " stands for ",
                " provides ",
                " enables ",
                " allows ",
                " consists of "
            ]

            before_with_spaces = (
                " "
                + before
                + " "
            )

            for marker in subject_markers:

                if marker in before_with_spaces:
                    return False

        # -----------------------------------------------------
        # CASE 5:
        # Look at the words immediately before concept
        # -----------------------------------------------------
        previous_words = before_words[-3:]

        blocked_words = [
            "for",
            "of",
            "with",
            "from",
            "using",
            "into",
            "about",
            "between",
            "through",
            "via",
            "by",
            "as",
            "on",
            "in",
            "to"
        ]

        for word in previous_words:

            if word in blocked_words:
                return False

        # -----------------------------------------------------
        # CASE 6:
        # If concept appears very late in sentence,
        # require stronger evidence.
        # -----------------------------------------------------
        total_words = len(
            sentence_lower.split()
        )

        words_before = len(
            before_words
        )

        if total_words > 0:

            position_ratio = (
                words_before / total_words
            )

            if position_ratio > 0.55:
                return False

        # -----------------------------------------------------
        # CASE 7:
        # Another technical word starts the sentence and the
        # concept appears later -> not the concept definition.
        # Leading connectors ("However, XML is ...") are fine.
        # -----------------------------------------------------
        first_words = sentence_lower.split()

        if len(first_words) >= 2:

            first_word = first_words[0].strip(",")

            connectors = {
                "however", "also", "thus", "therefore", "moreover",
                "furthermore", "additionally", "hence", "similarly",
                "likewise", "then", "so", "but", "and", "or",
                "finally", "consequently"
            }

            if (
                first_word not in ["the", "a", "an"]
                and first_word not in connectors
                and words_before > 2
            ):
                return False

        return True

    # =========================================================
    # DETECT RELATION RIGHT AFTER THE CONCEPT
    #
    # Returns (relation_type, concept_as_written, plural_flag)
    # or None when the sentence does not describe the concept.
    # =========================================================
    @classmethod
    def detect_relation(cls, concept, sentence):

        if not concept or not sentence:
            return None

        pattern = (
            r"(?<!\w)"
            + re.escape(concept.strip())
            + r"(?!\w)"
        )

        match = re.search(
            pattern,
            sentence,
            re.IGNORECASE
        )

        if not match:
            return None

        surface = match.group(0)

        after = sentence[match.end():]

        # Skip a leading abbreviation / note in brackets:
        # "XML (Extensible Markup Language) is a ..."
        after = re.sub(
            r"^\s*\([^)]*\)",
            "",
            after
        )

        after = after.lstrip(" ,")

        # Skip simple adverbs: "XML is also ..." / "XML often ..."
        after = re.sub(
            r"^(?:also|often|typically|generally|mainly|primarily|"
            r"commonly|usually|basically|simply)\s+",
            "",
            after,
            flags=re.IGNORECASE
        )

        for rule, relation in cls.RELATION_RULES:

            rule_match = re.match(
                rule,
                after,
                re.IGNORECASE
            )

            if rule_match:

                first_token = rule_match.group(0).split()[0].lower()

                plural = first_token in cls.PLURAL_VERBS

                return relation, surface, plural

        return None

    # =========================================================
    # CHECK EDUCATIONAL SENTENCE
    # =========================================================
    @staticmethod
    def is_educational_sentence(sentence):

        sentence_lower = sentence.lower()

        educational_patterns = [
            "stands for",
            "is defined as",
            "refers to",
            "is a ",
            "is an ",
            "means ",
            "consists of",
            "contains",
            "includes",
            "comprises",
            "is made up of",
            "is used to",
            "is used for",
            "used to",
            "used for",
            "provides",
            "allows",
            "enables",
            "helps",
            "performs",
            "represents",
            "describes",
            "defines",
            "supports",
            "responsible for",
            "can be used"
        ]

        for pattern in educational_patterns:

            if pattern in sentence_lower:
                return True

        return False

    # =========================================================
    # FIND BEST EXPLANATION
    # =========================================================
    @classmethod
    def find_explanation(cls, concept, text):

        sentences = cls.get_useful_sentences(
            text
        )

        strong_candidates = []
        normal_candidates = []

        for sentence in sentences:

            # -------------------------------------------------
            # CONCEPT MUST EXIST
            # -------------------------------------------------
            if not cls.concept_exists(
                concept,
                sentence
            ):
                continue

            # -------------------------------------------------
            # Concept must actually be the main topic.
            # -------------------------------------------------
            if not cls.is_main_subject(
                concept,
                sentence
            ):
                continue

            sentence_lower = sentence.lower()

            word_count = len(
                sentence.split()
            )

            score = 0

            # -------------------------------------------------
            # RELATION DIRECTLY AFTER CONCEPT
            # (guarantees question and answer match)
            # -------------------------------------------------
            relation = cls.detect_relation(
                concept,
                sentence
            )

            if relation:
                score += 10

                if relation[0] in ("stand_for", "define"):
                    score += 5

            elif cls.is_educational_sentence(sentence):
                score += 2

            # -------------------------------------------------
            # SHORT ANSWERS ARE BETTER
            # -------------------------------------------------
            if 6 <= word_count <= 30:
                score += 4

            elif 31 <= word_count <= 50:
                score += 2

            # -------------------------------------------------
            # CONCEPT CLOSE TO BEGINNING
            # -------------------------------------------------
            concept_position = sentence_lower.find(
                concept.lower()
            )

            if concept_position <= 20:
                score += 3

            # -------------------------------------------------
            # ADD CANDIDATE
            # -------------------------------------------------
            if relation:
                strong_candidates.append(
                    (
                        score,
                        sentence
                    )
                )
            else:
                # Weak sentence: only accept when the concept
                # starts the sentence and it is long enough
                if (
                    concept_position <= 4
                    and word_count >= 8
                ):
                    normal_candidates.append(
                        (
                            score,
                            sentence
                        )
                    )

        # -----------------------------------------------------
        # STRONG CANDIDATES FIRST
        # -----------------------------------------------------
        if strong_candidates:

            strong_candidates.sort(
                key=lambda item: item[0],
                reverse=True
            )

            return strong_candidates[0][1]

        # -----------------------------------------------------
        # NORMAL VALID CANDIDATES
        # -----------------------------------------------------
        if normal_candidates:

            normal_candidates.sort(
                key=lambda item: item[0],
                reverse=True
            )

            return normal_candidates[0][1]

        # -----------------------------------------------------
        # NEVER RETURN A FAKE ANSWER
        # -----------------------------------------------------
        return None

    # =========================================================
    # CREATE QUESTION BASED ON ANSWER
    # =========================================================
    @classmethod
    def create_question(
        cls,
        concept,
        explanation
    ):

        if not explanation:
            return None

        detected = cls.detect_relation(
            concept,
            explanation
        )

        # No clear relation: neutral question that still matches
        if not detected:

            return f"Explain {concept}."

        relation, surface, plural = detected

        # Use the concept exactly as written in the answer so the
        # question never contains a different spelling/casing
        name = surface

        aux = "do" if plural else "does"
        be = "are" if plural else "is"

        if relation == "stand_for":
            return f"What {aux} {name} stand for?"

        if relation == "define":
            return f"What {be} {name}?"

        if relation == "consist":
            return f"What {aux} {name} consist of?"

        if relation == "contain":
            return f"What {aux} {name} contain?"

        if relation == "used":
            return f"What {be} {name} used for?"

        if relation == "responsible":
            return f"What {be} {name} responsible for?"

        if relation == "can_use":
            return f"How can {name} be used?"

        if relation == "provide":
            return f"What {aux} {name} provide?"

        if relation == "allow":
            return f"What {aux} {name} allow?"

        if relation == "enable":
            return f"What {aux} {name} enable?"

        if relation == "help":
            return f"How {aux} {name} help?"

        if relation == "perform":
            return f"What {aux} {name} perform?"

        if relation == "represent":
            return f"What {aux} {name} represent?"

        if relation == "describe":
            return f"What {aux} {name} describe?"

        if relation == "define_verb":
            return f"What {aux} {name} define?"

        if relation == "support":
            return f"What {aux} {name} support?"

        return f"Explain {concept}."

    # =========================================================
    # CLEAN ANSWER
    # =========================================================
    @classmethod
    def clean_answer(cls, answer):

        if not answer:
            return None

        answer = re.sub(
            r"\s+",
            " ",
            answer
        ).strip()

        # Remove bullet at start
        answer = re.sub(
            r"^[\-\*\u2022•▪●]\s*",
            "",
            answer
        )

        # Remove leading connectors: "However, XML is ..."
        answer = re.sub(
            cls.LEADING_CONNECTORS,
            "",
            answer,
            flags=re.IGNORECASE
        ).strip()

        # Remove footnote number stuck after the final full stop
        answer = re.sub(
            r"([.!?])\s*\d+$",
            r"\1",
            answer
        ).strip()

        # Remove trailing stray number without punctuation
        answer = re.sub(
            r"(?<=[A-Za-z])\s+\d{1,2}$",
            "",
            answer
        ).strip()

        # Fix spaces before punctuation: "word ." -> "word."
        answer = re.sub(
            r"\s+([.,;:!?])",
            r"\1",
            answer
        )

        if not answer:
            return None

        # Capitalize first letter
        if answer[0].islower():
            answer = answer[0].upper() + answer[1:]

        # Smart truncation (never cut in the middle of a word)
        if len(answer) > 400:

            cut = answer[:397]

            boundary = max(
                cut.rfind(". "),
                cut.rfind("; "),
                cut.rfind(", ")
            )

            if boundary > 150:
                cut = cut[:boundary]
            else:
                cut = cut[:cut.rfind(" ")] if " " in cut else cut

            answer = cut.rstrip(" ,;:") + "..."

        # Make sure the answer ends properly
        if not re.search(r"[.!?]$|\.\.\.$", answer):
            answer = answer + "."

        return answer

    # =========================================================
    # BAD CONCEPT CHECK
    # =========================================================
    @staticmethod
    def is_bad_concept(concept):

        if not concept:
            return True

        concept_lower = concept.lower().strip()

        if len(concept_lower) < 2:
            return True

        # Concepts that are only digits / symbols
        if not re.search(r"[a-z]", concept_lower):
            return True

        bad_patterns = [
            "publisher",
            "published by",
            "copyright",
            "author",
            "www.",
            "http://",
            "https://",
            ".com",
            ".org",
            ".edu"
        ]

        for pattern in bad_patterns:

            if pattern in concept_lower:
                return True

        return False

    # =========================================================
    # SIMILAR CONCEPT CHECK
    # =========================================================
    @staticmethod
    def concepts_are_similar(
        concept_one,
        concept_two
    ):

        one = set(
            concept_one.lower().split()
        )

        two = set(
            concept_two.lower().split()
        )

        if not one or not two:
            return False

        overlap = len(
            one.intersection(two)
        )

        smaller = min(
            len(one),
            len(two)
        )

        if smaller == 0:
            return False

        similarity = (
            overlap / smaller
        )

        return similarity >= 0.8

    # =========================================================
    # GENERATE FLASHCARDS
    # =========================================================
    @classmethod
    def generate_flashcards(
        cls,
        text,
        number_of_cards=20
    ):

        if not text or not text.strip():
            return []

        # -----------------------------------------------------
        # CLEAN DOCUMENT
        # -----------------------------------------------------
        cleaned_text = (
            cls.clean_document_text(
                text
            )
        )

        if not cleaned_text:
            return []

        # -----------------------------------------------------
        # EXTRACT MORE CONCEPTS THAN REQUIRED
        # -----------------------------------------------------
        concepts = (
            ConceptService.extract_concepts(
                cleaned_text,
                top_k=max(
                    number_of_cards * 3,
                    40
                )
            )
        )

        flashcards = []
        seen_concepts = []
        seen_answers = set()

        # -----------------------------------------------------
        # PROCESS EACH CONCEPT
        # -----------------------------------------------------
        for item in concepts:

            concept = item.get(
                "concept",
                ""
            ).strip()

            # -------------------------------------------------
            # BAD CONCEPT
            # -------------------------------------------------
            if cls.is_bad_concept(
                concept
            ):
                continue

            # -------------------------------------------------
            # DUPLICATE CONCEPT
            # -------------------------------------------------
            duplicate = False

            for previous_concept in seen_concepts:

                if cls.concepts_are_similar(
                    concept,
                    previous_concept
                ):
                    duplicate = True
                    break

            if duplicate:
                continue

            # -------------------------------------------------
            # FIND REAL EXPLANATION
            # -------------------------------------------------
            explanation = (
                cls.find_explanation(
                    concept,
                    cleaned_text
                )
            )

            # -------------------------------------------------
            # NO VALID EXPLANATION
            # -------------------------------------------------
            if not explanation:
                continue

            # -------------------------------------------------
            # CREATE QUESTION (from the original full sentence,
            # BEFORE it is shortened/cleaned, so that the
            # question always matches the answer)
            # -------------------------------------------------
            question = (
                cls.create_question(
                    concept,
                    explanation
                )
            )

            if not question:
                continue

            # -------------------------------------------------
            # CLEAN ANSWER
            # -------------------------------------------------
            explanation = (
                cls.clean_answer(
                    explanation
                )
            )

            if not explanation:
                continue

            # -------------------------------------------------
            # DUPLICATE ANSWER (same sentence used twice)
            # -------------------------------------------------
            answer_key = re.sub(
                r"\W+",
                " ",
                explanation.lower()
            ).strip()

            if answer_key in seen_answers:
                continue

            # -------------------------------------------------
            # FINAL QUESTION/CONCEPT CHECK
            # -------------------------------------------------
            if concept.lower() not in question.lower():

                question = (
                    f"Explain {concept}."
                )

            # -------------------------------------------------
            # ADD CARD
            # -------------------------------------------------
            flashcards.append({
                "concept": concept,
                "front": question,
                "back": explanation
            })

            seen_concepts.append(
                concept
            )

            seen_answers.add(
                answer_key
            )

            # -------------------------------------------------
            # STOP WHEN ENOUGH CARDS CREATED
            # -------------------------------------------------
            if len(flashcards) >= number_of_cards:
                break

        return flashcards