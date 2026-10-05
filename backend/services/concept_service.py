import re
from collections import Counter


class ConceptService:

    # =========================================================
    # STOPWORDS
    # =========================================================

    STOPWORDS = {
        "the", "a", "an", "and", "or", "but",
        "is", "are", "was", "were", "be",
        "been", "being", "of", "to", "in",
        "on", "for", "from", "with", "by",
        "as", "at", "this", "that", "these",
        "those", "it", "its", "they", "their",
        "them", "which", "when", "where",
        "what", "why", "who", "how",
        "than", "then", "also", "only",
        "into", "through", "during",

        "used", "using", "use",
        "example", "examples",
        "following", "given",
        "important", "note", "notes",
        "question", "questions",
        "answer", "answers",
        "page", "pages",
        "chapter", "unit",
        "figure", "table"
    }

    # =========================================================
    # GENERIC WORDS
    # =========================================================

    GENERIC_WORDS = {
        "language",
        "structure",
        "create",
        "creating",
        "used",
        "using",
        "use",
        "provide",
        "provides",
        "allows",
        "allow",
        "helps",
        "help",
        "called",
        "known",
        "means",
        "stands",
        "contains",
        "include",
        "includes",
        "information",
        "content",
        "document",
        "documents",
        "web",
        "page",
        "pages",
        "data",
        "thing",
        "things",
        "way",
        "ways",
        "output",
        "input",
        "name",
        "names",
        "value",
        "values",
        "message",
        "messages",
        "body",
        "head",
        "title",
        "line",
        "lines",
        "about",
        "does",
        "file",
        "files",
        "application",
        "applications"
    }

    # =========================================================
    # BAD PHRASES
    # =========================================================

    BAD_PHRASES = {
        "information about",
        "does not",
        "does not describe",
        "output web",
        "control presentation",
        "presentation appearance",
        "uses tags",
        "exchange structured",
        "elements define",
        "tags elements",
        "web pages",
        "web applications"
    }

    # =========================================================
    # WORDS THAT OFTEN PRODUCE SENTENCE FRAGMENTS
    # =========================================================

    FRAGMENT_WORDS = {
        "use",
        "uses",
        "used",
        "using",
        "create",
        "creates",
        "creating",
        "provide",
        "provides",
        "provided",
        "allow",
        "allows",
        "helps",
        "help",
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
        "contain",
        "contains",
        "contained",
        "describe",
        "describes",
        "called",
        "known",
        "stands"
    }

    # =========================================================
    # CLEAN TEXT
    # =========================================================

    @classmethod
    def clean_text(cls, text):

        if not text:
            return ""

        text = text.replace("\r\n", "\n")

        # Remove URLs
        text = re.sub(
            r"https?://\S+|www\.\S+",
            " ",
            text,
            flags=re.IGNORECASE
        )

        # Remove email addresses
        text = re.sub(
            r"\S+@\S+",
            " ",
            text
        )

        # Remove academic metadata
        metadata_patterns = [
            r"RAJEEV\s+GANDHI\s+MEMORIAL",
            r"DEPARTMENT\s+OF\s+COMPUTER\s+SCIENCE",
            r"COMPUTER\s+SCIENCE\s+AND\s+ENGINEERING",
            r"RGMCET\s+CSE\s+DEPT",
            r"LECTURE\s+NOTES",
            r"III\s+B\.?\s*TECH\s*[-–]\s*II\s*SEM",
            r"II\s+SEM",
            r"AUTONOMOUS"
        ]

        for pattern in metadata_patterns:
            text = re.sub(
                pattern,
                " ",
                text,
                flags=re.IGNORECASE
            )

        # Remove code-like declarations
        code_patterns = [
            r"<\?xml.*?\?>",
            r"<!DOCTYPE.*?>",
            r"<!ATTLIST.*?>",
            r"</?[A-Za-z][^>]*>",
            r"<%.*?%>"
        ]

        for pattern in code_patterns:
            text = re.sub(
                pattern,
                " ",
                text,
                flags=re.IGNORECASE
            )

        # Normalize whitespace
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

    # =========================================================
    # CODE DETECTION
    # =========================================================

    @classmethod
    def is_code_like(cls, text):

        if not text:
            return True

        stripped = text.strip()

        code_patterns = [
            r"<\?xml",
            r"<!DOCTYPE",
            r"<!ATTLIST",
            r"</?[A-Za-z][^>]*>",
            r"<%.*?%>",

            r"\bpublic\s+(class|static|void)\b",
            r"\bprivate\s+(class|static|void)\b",
            r"\bprotected\s+(class|static|void)\b",

            r"\bfunction\s+\w+\s*\(",
            r"\bif\s*\(",
            r"\belse\s*(if)?\s*\{",
            r"\bfor\s*\(",
            r"\bwhile\s*\(",

            r"\w+\.\w+\s*\(",
            r"\borg\.[A-Za-z0-9_.]+",

            r"\bSELECT\b.+\bFROM\b",
            r"\bINSERT\b.+\bINTO\b",
            r"\bUPDATE\b.+\bSET\b",
            r"\bDELETE\b.+\bFROM\b"
        ]

        for pattern in code_patterns:
            if re.search(
                pattern,
                stripped,
                re.IGNORECASE
            ):
                return True

        symbols = len(
            re.findall(
                r"[{}[\]();=<>\"']",
                stripped
            )
        )

        words = max(
            len(stripped.split()),
            1
        )

        if symbols / words > 0.25:
            return True

        return False

    # =========================================================
    # SENTENCE SPLITTING
    # =========================================================

    @classmethod
    def split_sentences(cls, text):

        if not text:
            return []

        text = re.sub(
            r"\n+",
            " ",
            text
        )

        raw_sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        sentences = []

        for sentence in raw_sentences:

            sentence = sentence.strip()

            if len(sentence.split()) < 4:
                continue

            if cls.is_code_like(sentence):
                continue

            sentences.append(sentence)

        return sentences

    # =========================================================
    # NORMALIZE CONCEPT
    # =========================================================

    @classmethod
    def normalize_concept(
        cls,
        concept
    ):

        if not concept:
            return ""

        concept = re.sub(
            r"[^A-Za-z0-9\-\s]",
            " ",
            concept
        )

        concept = re.sub(
            r"\s+",
            " ",
            concept
        )

        return concept.strip()

    # =========================================================
    # VALID CONCEPT
    # =========================================================

    @classmethod
    def is_valid_concept(
        cls,
        concept
    ):

        if not concept:
            return False

        concept = cls.normalize_concept(
            concept
        )

        if not concept:
            return False

        lower = concept.lower()

        # Exact bad phrase
        if lower in cls.BAD_PHRASES:
            return False

        words = lower.split()

        # Length limits
        if len(words) > 4:
            return False

        if len(concept) < 3:
            return False

        # Repeated words
        if len(words) != len(set(words)):
            return False

        # Code fragment
        if cls.is_code_like(concept):
            return False

        # A phrase beginning/ending with fragment words is
        # usually not a useful study concept.
        if words and words[0] in cls.FRAGMENT_WORDS:
            return False

        if words and words[-1] in cls.FRAGMENT_WORDS:
            return False

        # Generic single word
        if len(words) == 1:

            if words[0] in cls.STOPWORDS:
                return False

            if words[0] in cls.GENERIC_WORDS:
                return False

        # Generic phrase ratio
        generic_count = sum(
            word in cls.STOPWORDS
            or word in cls.GENERIC_WORDS
            or word in cls.FRAGMENT_WORDS
            for word in words
        )

        if (
            generic_count / len(words)
        ) >= 0.50:
            return False

        return True

    # =========================================================
    # DEFINITION EXTRACTION
    # =========================================================

    @classmethod
    def extract_definition_concepts(
        cls,
        sentences
    ):

        results = []

        # -----------------------------------------------------
        # X stands for Y
        # -----------------------------------------------------

        stands_for_pattern = re.compile(
            r"^\s*"
            r"([A-Za-z][A-Za-z0-9\-\s]{0,60}?)"
            r"\s+stands\s+for\s+"
            r"(.+?)[.!?]?\s*$",
            re.IGNORECASE
        )

        # -----------------------------------------------------
        # Other useful definition patterns
        # -----------------------------------------------------

        patterns = [

            (
                re.compile(
                    r"^\s*"
                    r"([A-Za-z][A-Za-z0-9\-\s]{0,60}?)"
                    r"\s+is\s+(?:a|an|the)\s+(.+?)[.!?]?\s*$",
                    re.IGNORECASE
                ),
                "definition"
            ),

            (
                re.compile(
                    r"^\s*"
                    r"([A-Za-z][A-Za-z0-9\-\s]{0,60}?)"
                    r"\s+refers\s+to\s+(.+?)[.!?]?\s*$",
                    re.IGNORECASE
                ),
                "definition"
            ),

            (
                re.compile(
                    r"^\s*"
                    r"([A-Za-z][A-Za-z0-9\-\s]{0,60}?)"
                    r"\s+is\s+used\s+to\s+(.+?)[.!?]?\s*$",
                    re.IGNORECASE
                ),
                "usage"
            ),

            (
                re.compile(
                    r"^\s*"
                    r"([A-Za-z][A-Za-z0-9\-\s]{0,60}?)"
                    r"\s+is\s+used\s+for\s+(.+?)[.!?]?\s*$",
                    re.IGNORECASE
                ),
                "usage"
            )
        ]

        for sentence in sentences:

            # -------------------------------------------------
            # STANDS FOR
            # -------------------------------------------------

            match = stands_for_pattern.match(
                sentence
            )

            if match:

                left = cls.normalize_concept(
                    match.group(1)
                )

                right = cls.normalize_concept(
                    match.group(2)
                )

                # IMPORTANT:
                # Keep the acronym/name as the main concept.
                if cls.is_valid_concept(left):

                    results.append({
                        "concept": left,
                        "type": "definition",
                        "sentence": sentence,
                        "score": 10
                    })

                # Only keep expansion when it is a meaningful
                # multi-word technical term.
                if (
                    cls.is_valid_concept(right)
                    and len(right.split()) >= 2
                ):

                    # Avoid ordinary sentence fragments
                    right_words = right.lower().split()

                    if not any(
                        word in cls.FRAGMENT_WORDS
                        for word in right_words
                    ):

                        results.append({
                            "concept": right,
                            "type": "expansion",
                            "sentence": sentence,
                            "score": 5
                        })

                continue

            # -------------------------------------------------
            # OTHER DEFINITIONS
            # -------------------------------------------------

            for compiled, concept_type in patterns:

                match = compiled.match(
                    sentence
                )

                if not match:
                    continue

                concept = cls.normalize_concept(
                    match.group(1)
                )

                if cls.is_valid_concept(concept):

                    results.append({
                        "concept": concept,
                        "type": concept_type,
                        "sentence": sentence,
                        "score": 8
                    })

                break

        return results

    # =========================================================
    # TECHNICAL TERM EXTRACTION
    # =========================================================

    @classmethod
    def extract_technical_terms(
        cls,
        sentences
    ):

        results = []

        technical_patterns = [

            # Capitalized technologies / acronyms
            r"\b[A-Z]{2,}(?:\.[A-Z]{2,})*\b",

            # Terms with common technical endings
            r"\b[A-Za-z]+(?:Script|SQL|API|XML|HTML|HTTP|JSP|Java)\b",

            # Technical compound names
            r"\b(?:client-side|server-side|object-oriented|"
              r"machine-learning|deep-learning|"
              r"cloud-based|real-time)\b"
        ]

        for sentence in sentences:

            for pattern in technical_patterns:

                matches = re.findall(
                    pattern,
                    sentence
                )

                for match in matches:

                    concept = cls.normalize_concept(
                        match
                    )

                    if not cls.is_valid_concept(
                        concept
                    ):
                        continue

                    results.append({
                        "concept": concept,
                        "type": "technical",
                        "sentence": sentence,
                        "score": 6
                    })

        return results

    # =========================================================
    # MEANINGFUL COMPOUND TERM EXTRACTION
    # =========================================================

    @classmethod
    def extract_meaningful_terms(
        cls,
        sentences
    ):

        results = []

        # These words often indicate a meaningful technical
        # noun phrase after them.
        trigger_words = {
            "language",
            "protocol",
            "framework",
            "architecture",
            "technology",
            "database",
            "server",
            "client",
            "request",
            "response",
            "scripting",
            "markup",
            "stylesheet",
            "schema",
            "model",
            "algorithm",
            "interface",
            "component"
        }

        for sentence in sentences:

            words = re.findall(
                r"\b[A-Za-z][A-Za-z0-9-]*\b",
                sentence
            )

            for i, word in enumerate(words):

                if word.lower() not in trigger_words:
                    continue

                # Previous word + trigger
                if i > 0:

                    candidate = (
                        words[i - 1]
                        + " "
                        + word
                    )

                    candidate = cls.normalize_concept(
                        candidate
                    )

                    if cls.is_valid_concept(
                        candidate
                    ):

                        results.append({
                            "concept": candidate,
                            "type": "technical_phrase",
                            "sentence": sentence,
                            "score": 4
                        })

                # Previous 2 words + trigger
                if i > 1:

                    candidate = (
                        words[i - 2]
                        + " "
                        + words[i - 1]
                        + " "
                        + word
                    )

                    candidate = cls.normalize_concept(
                        candidate
                    )

                    if cls.is_valid_concept(
                        candidate
                    ):

                        results.append({
                            "concept": candidate,
                            "type": "technical_phrase",
                            "sentence": sentence,
                            "score": 3
                        })

        return results

    # =========================================================
    # MERGE VARIANTS
    # =========================================================

    @classmethod
    def merge_variants(
        cls,
        candidates
    ):

        groups = []

        for item in candidates:

            concept = item["concept"]

            concept_words = set(
                concept.lower().split()
            )

            merged = False

            for group in groups:

                existing_words = set(
                    group["concept"]
                    .lower()
                    .split()
                )

                if not concept_words:
                    continue

                if not existing_words:
                    continue

                # Exact match
                if (
                    concept.lower()
                    == group["concept"].lower()
                ):

                    group["score"] += (
                        item["score"]
                    )

                    merged = True
                    break

                # One concept contains another
                if (
                    concept_words.issubset(
                        existing_words
                    )
                    or
                    existing_words.issubset(
                        concept_words
                    )
                ):

                    # Prefer shorter concept
                    # when the longer one is simply
                    # a variation.
                    if (
                        len(concept_words)
                        < len(existing_words)
                    ):

                        group["concept"] = concept

                    group["score"] += (
                        item["score"]
                    )

                    merged = True
                    break

            if not merged:

                groups.append({
                    "concept": concept,
                    "score": item["score"],
                    "type": item["type"],
                    "sentence": item["sentence"]
                })

        return groups

    # =========================================================
    # FINAL SIMILARITY FILTER
    # =========================================================

    @classmethod
    def remove_similar(
        cls,
        items,
        threshold=0.60
    ):

        selected = []

        for item in items:

            concept = item["concept"]

            current_words = set(
                concept.lower().split()
            )

            duplicate = False

            for existing in selected:

                existing_words = set(
                    existing["concept"]
                    .lower()
                    .split()
                )

                if not current_words:
                    continue

                if not existing_words:
                    continue

                intersection = (
                    current_words
                    &
                    existing_words
                )

                union = (
                    current_words
                    |
                    existing_words
                )

                similarity = (
                    len(intersection)
                    /
                    len(union)
                )

                if similarity >= threshold:

                    duplicate = True

                    # Keep whichever has the
                    # higher score.
                    if (
                        item["score"]
                        >
                        existing["score"]
                    ):

                        selected.remove(
                            existing
                        )

                        selected.append(
                            item
                        )

                    break

            if not duplicate:
                selected.append(item)

        return selected

    # =========================================================
    # MAIN EXTRACTION
    # =========================================================

    @classmethod
    def extract_concepts(
        cls,
        text,
        top_k=20
    ):

        if not text or not text.strip():
            return []

        print("\n========================================")
        print("Starting key concept extraction...")
        print("========================================")

        cleaned = cls.clean_text(
            text
        )

        print(
            f"Cleaned text length: "
            f"{len(cleaned)} characters"
        )

        sentences = cls.split_sentences(
            cleaned
        )

        if not sentences:
            return []

        print(
            f"Meaningful sentences: "
            f"{len(sentences)}"
        )

        # -----------------------------------------------------
        # STRONG DEFINITION CONCEPTS
        # -----------------------------------------------------

        definitions = (
            cls.extract_definition_concepts(
                sentences
            )
        )

        # -----------------------------------------------------
        # TECHNICAL TERMS
        # -----------------------------------------------------

        technical_terms = (
            cls.extract_technical_terms(
                sentences
            )
        )

        # -----------------------------------------------------
        # MEANINGFUL TECHNICAL PHRASES
        # -----------------------------------------------------

        meaningful_terms = (
            cls.extract_meaningful_terms(
                sentences
            )
        )

        # -----------------------------------------------------
        # COMBINE
        # -----------------------------------------------------

        candidates = (
            definitions
            + technical_terms
            + meaningful_terms
        )

        print(
            f"Candidate concepts: "
            f"{len(candidates)}"
        )

        # -----------------------------------------------------
        # MERGE VARIANTS
        # -----------------------------------------------------

        merged = cls.merge_variants(
            candidates
        )

        # -----------------------------------------------------
        # FREQUENCY
        # -----------------------------------------------------

        frequency = Counter()

        for item in merged:

            concept = item[
                "concept"
            ].lower()

            for sentence in sentences:

                if concept in sentence.lower():

                    frequency[
                        concept
                    ] += 1

        # -----------------------------------------------------
        # FINAL SCORE
        # -----------------------------------------------------

        for item in merged:

            concept = item[
                "concept"
            ].lower()

            item["frequency"] = (
                frequency[
                    concept
                ]
            )

            # Frequency contributes
            # additional importance.
            item["score"] += (
                frequency[
                    concept
                ] * 2
            )

            # Definition concepts receive
            # an additional priority.
            if item["type"] == "definition":
                item["score"] += 5

            elif item["type"] == "technical":
                item["score"] += 2

        # -----------------------------------------------------
        # SORT
        # -----------------------------------------------------

        merged.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # -----------------------------------------------------
        # REMOVE SIMILAR CONCEPTS
        # -----------------------------------------------------

        selected = cls.remove_similar(
            merged,
            threshold=0.60
        )

        # -----------------------------------------------------
        # TOP K
        # -----------------------------------------------------

        selected = selected[:top_k]

        # -----------------------------------------------------
        # DISPLAY
        # -----------------------------------------------------

        print("\n========== FINAL KEY CONCEPTS ==========\n")

        if not selected:
            print("No suitable concepts found.")

        for index, item in enumerate(
            selected,
            start=1
        ):

            print(
                f"{index}. "
                f"{item['concept']}"
            )

            print(
                f"   Type: "
                f"{item['type']}"
            )

            print(
                f"   Frequency: "
                f"{item['frequency']}"
            )

            print(
                f"   Score: "
                f"{item['score']}"
            )

            print()

        print(
            "========================================"
        )

        return selected