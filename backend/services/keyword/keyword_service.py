import json
import re
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM


class KeywordService:

    # ============================================================
    # MODEL CONFIGURATION
    # ============================================================

    MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

    tokenizer = None
    model = None

    # Maximum characters per chunk.
    # We deliberately use characters instead of sending the
    # entire PDF to the model at once.
    CHUNK_SIZE = 8000

    # Number of concepts finally returned
    MIN_CONCEPTS = 5
    MAX_CONCEPTS = 15

    # ============================================================
    # GENERIC / BAD TERMS
    # ============================================================

    GENERIC_TERMS = {
        "each client",
        "client",
        "source object",
        "object",
        "interface implemented",
        "implemented interface",
        "attributes tag",
        "attribute tag",
        "tag",
        "example",
        "examples",
        "output",
        "input",
        "page",
        "pages",
        "file",
        "files",
        "method",
        "methods",
        "function",
        "functions",
        "class",
        "classes",
        "process",
        "processing",
        "information",
        "data",
        "system",
        "application",
        "user",
        "users",
        "request",
        "response",
        "following",
        "above",
        "below",
        "given",
        "using",
    }

    # ============================================================
    # LOAD MODEL
    # ============================================================

    @classmethod
    def load_model(cls):

        if cls.model is not None and cls.tokenizer is not None:
            return

        print("\n========================================")
        print("Loading Qwen2.5-3B-Instruct...")
        print("========================================\n")

        # Tokenizer
        cls.tokenizer = AutoTokenizer.from_pretrained(
            cls.MODEL_NAME
        )

        # CPU configuration
        cls.model = AutoModelForCausalLM.from_pretrained(
            cls.MODEL_NAME,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

        cls.model.eval()

        print("\n========================================")
        print("Qwen model loaded successfully.")
        print("========================================\n")

    # ============================================================
    # CLEAN PDF TEXT
    # ============================================================

    @classmethod
    def clean_text(cls, text):

        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove common page-number/header patterns
        patterns = [
            r"\bWEB\s+TECHNOLOGIES\s+\d+\b",
            r"\bWEB TECHNOLOGY\s+\d+\b",
            r"\bPage\s+\d+\b",
            r"\bPAGE\s+\d+\b",
            r"\bPage:\s*\d+\b",
            r"\b\d+\s+of\s+\d+\b",
        ]

        for pattern in patterns:
            text = re.sub(
                pattern,
                " ",
                text,
                flags=re.IGNORECASE
            )

        # Remove repeated dots
        text = re.sub(r"\.{3,}", " ", text)

        # Remove repeated underscores
        text = re.sub(r"_{3,}", " ", text)

        # Remove excessive spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove empty lines
        lines = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            lines.append(line)

        text = "\n".join(lines)

        return text.strip()

    # ============================================================
    # SPLIT TEXT INTO CHUNKS
    # ============================================================

    @classmethod
    def chunk_text(cls, text):

        text = text.strip()

        if not text:
            return []

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = start + cls.CHUNK_SIZE

            if end >= text_length:

                chunk = text[start:]

                if chunk.strip():
                    chunks.append(chunk.strip())

                break

            # Try to break at a paragraph
            paragraph_break = text.rfind(
                "\n\n",
                start,
                end
            )

            if paragraph_break > start + 2000:

                end = paragraph_break

            else:

                # Try sentence boundary
                sentence_break = text.rfind(
                    ". ",
                    start,
                    end
                )

                if sentence_break > start + 2000:
                    end = sentence_break + 1

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end

        print(
            f"Text divided into {len(chunks)} chunk(s)."
        )

        return chunks

    # ============================================================
    # BUILD AI PROMPT
    # ============================================================

    @classmethod
    def build_prompt(cls, text):

        prompt = f"""
You are an expert educational content analyzer.

Your task is to extract the most important TECHNICAL CONCEPTS
from the educational text provided below.

IMPORTANT:
This text may come from a PDF and may contain:
- page numbers
- headers
- footers
- broken sentences
- examples
- repeated text
- formatting errors

Ignore all such noise.

STRICT RULES:

1. Extract only meaningful technical concepts.

2. A concept should represent an important topic, technology,
   protocol, programming language, API, architecture, framework,
   database concept, web technology, or technical terminology.

3. Do NOT extract ordinary English phrases.

4. Do NOT extract incomplete phrases.

5. Do NOT extract page numbers.

6. Do NOT extract headings that are not actual concepts.

7. Do NOT extract sentences.

8. Do NOT copy long text from the input.

9. Do NOT include duplicate concepts.

10. Do NOT include generic terms such as:
    "each client",
    "source object",
    "interface implemented",
    "attributes tag",
    "example",
    "page",
    "file",
    "method",
    "function",
    unless they are specifically part of a meaningful technical concept.

11. Normalize capitalization.
    For example:
    "Javascript" should become "JavaScript".
    "http request" should become "HTTP Request".

12. Explanations must be short.

13. Each explanation must contain only 1 or 2 sentences.

14. The explanation must explain the concept itself.

15. Do not copy unrelated surrounding PDF text into the explanation.

16. Extract between 5 and 15 concepts if enough concepts exist.

17. Return ONLY valid JSON.

18. Do not use Markdown.

19. Do not add ```json.

20. Use exactly this format:

[
  {{
    "keyword": "Concept Name",
    "explanation": "Short and accurate explanation."
  }}
]

TEXT:

{text}
"""

        return prompt

    # ============================================================
    # GENERATE AI RESPONSE
    # ============================================================

    @classmethod
    def generate_from_chunk(cls, text):

        cls.load_model()

        prompt = cls.build_prompt(text)

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        formatted_prompt = (
            cls.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
        )

        inputs = cls.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=12000
        )

        print("Generating concepts...")

        with torch.no_grad():

            outputs = cls.model.generate(
    **inputs,
    max_new_tokens=300,
    temperature=0.7
)

        # Remove input tokens from generated output
        generated_tokens = outputs[
            0
        ][
            inputs["input_ids"].shape[1]:
        ]

        result = cls.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return result.strip()

    # ============================================================
    # EXTRACT JSON ARRAY FROM AI RESPONSE
    # ============================================================

    @classmethod
    def parse_json_response(cls, response):

        if not response:
            return []

        response = response.strip()

        # Remove Markdown code fences if model produces them
        response = re.sub(
            r"```json",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r"```",
            "",
            response
        )

        response = response.strip()

        # Find JSON array
        start = response.find("[")

        end = response.rfind("]")

        if start == -1 or end == -1:
            print("No JSON array found in AI response.")
            return []

        json_text = response[start:end + 1]

        try:

            data = json.loads(json_text)

            if not isinstance(data, list):
                return []

            return data

        except json.JSONDecodeError as error:

            print(
                "JSON parsing error:",
                error
            )

            return []

    # ============================================================
    # NORMALIZE KEYWORD
    # ============================================================

    @classmethod
    def normalize_keyword(cls, keyword):

        if not keyword:
            return ""

        keyword = str(keyword).strip()

        # Remove quotes
        keyword = keyword.strip(
            "\"'`"
        )

        # Normalize spaces
        keyword = re.sub(
            r"\s+",
            " ",
            keyword
        )

        # Known capitalization corrections
        corrections = {
            "xml": "XML",
            "javascript": "JavaScript",
            "java script": "JavaScript",
            "http": "HTTP",
            "http request": "HTTP Request",
            "http response": "HTTP Response",
            "css": "CSS",
            "html": "HTML",
            "json": "JSON",
            "api": "API",
            "apis": "APIs",
            "jdbc": "JDBC",
            "servlet": "Servlet",
            "servlets": "Servlets",
            "rowset": "RowSet",
            "rowsets": "RowSets",
            "datasource": "DataSource",
            "data source": "DataSource",
            "connection pooling": "Connection Pooling",
        }

        lower = keyword.lower()

        if lower in corrections:
            return corrections[lower]

        # Title case for normal multi-word concepts
        if keyword.islower():
            keyword = keyword.title()

        return keyword

    # ============================================================
    # CHECK WHETHER KEYWORD IS VALID
    # ============================================================

    @classmethod
    def is_valid_keyword(cls, keyword):

        if not keyword:
            return False

        keyword = keyword.strip()

        lower = keyword.lower()

        # Generic term
        if lower in cls.GENERIC_TERMS:
            return False

        # Too short
        if len(keyword) < 2:
            return False

        # Too long
        words = keyword.split()

        if len(words) > 7:
            return False

        # Don't allow full sentences
        if keyword.endswith("."):
            return False

        # Don't allow very long keyword strings
        if len(keyword) > 80:
            return False

        # Must contain alphabetic characters
        if not re.search(
            r"[A-Za-z]",
            keyword
        ):
            return False

        return True

    # ============================================================
    # CLEAN EXPLANATION
    # ============================================================

    @classmethod
    def clean_explanation(
        cls,
        explanation,
        keyword
    ):

        if not explanation:
            return ""

        explanation = str(
            explanation
        ).strip()

        # Remove quotes
        explanation = explanation.strip(
            "\"'`"
        )

        # Remove newlines
        explanation = re.sub(
            r"\s+",
            " ",
            explanation
        ).strip()

        # Remove accidental JSON/markdown
        explanation = explanation.replace(
            "```",
            ""
        )

        # If explanation is extremely long,
        # keep only the first useful sentences.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            explanation
        )

        if len(sentences) > 2:

            explanation = " ".join(
                sentences[:2]
            )

        # Hard safety limit
        if len(explanation) > 400:

            explanation = (
                explanation[:400]
            )

            last_period = explanation.rfind(".")

            if last_period > 100:

                explanation = explanation[
                    :last_period + 1
                ]

        return explanation.strip()

    # ============================================================
    # REMOVE DUPLICATES
    # ============================================================

    @classmethod
    def remove_duplicates(cls, concepts):

        unique = []

        seen = set()

        for item in concepts:

            keyword = item.get(
                "keyword",
                ""
            )

            normalized = keyword.lower()

            # Remove punctuation for comparison
            normalized = re.sub(
                r"[^a-z0-9]+",
                " ",
                normalized
            ).strip()

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)

            unique.append(item)

        return unique

    # ============================================================
    # CLEAN AI CONCEPTS
    # ============================================================

    @classmethod
    def clean_concepts(cls, concepts):

        cleaned = []

        for item in concepts:

            if not isinstance(item, dict):
                continue

            keyword = item.get(
                "keyword",
                ""
            )

            explanation = item.get(
                "explanation",
                ""
            )

            keyword = cls.normalize_keyword(
                keyword
            )

            if not cls.is_valid_keyword(
                keyword
            ):
                continue

            explanation = cls.clean_explanation(
                explanation,
                keyword
            )

            if not explanation:
                continue

            cleaned.append(
                {
                    "keyword": keyword,
                    "explanation": explanation
                }
            )

        cleaned = cls.remove_duplicates(
            cleaned
        )

        return cleaned

    # ============================================================
    # MAIN FUNCTION
    # ============================================================

    @classmethod
    def extract_concepts(cls, text):

        if not text or not text.strip():

            return []

        print("\n========================================")
        print("Starting key concept extraction...")
        print("========================================")

        # --------------------------------------------------------
        # STEP 1: Clean text
        # --------------------------------------------------------

        cleaned_text = cls.clean_text(
            text
        )

        if not cleaned_text:

            print("No usable text found.")

            return []

        print(
            f"Cleaned text length: "
            f"{len(cleaned_text)} characters"
        )

        # --------------------------------------------------------
        # STEP 2: Split into chunks
        # --------------------------------------------------------

        chunks = cls.chunk_text(
            cleaned_text
        )

        if not chunks:
            return []

        # --------------------------------------------------------
        # STEP 3: AI extraction
        # --------------------------------------------------------

        all_concepts = []

        for index, chunk in enumerate(
            chunks,
            start=1
        ):

            print(
                f"\nProcessing chunk "
                f"{index}/{len(chunks)}..."
            )

            try:

                raw_response = (
                    cls.generate_from_chunk(
                        chunk
                    )
                )

                print(
                    "\nAI Response:"
                )

                print(raw_response)

                concepts = (
                    cls.parse_json_response(
                        raw_response
                    )
                )

                print(
                    f"Concepts found: "
                    f"{len(concepts)}"
                )

                all_concepts.extend(
                    concepts
                )

            except Exception as error:

                print(
                    f"Error processing chunk "
                    f"{index}: {error}"
                )

        # --------------------------------------------------------
        # STEP 4: Clean concepts
        # --------------------------------------------------------

        cleaned_concepts = (
            cls.clean_concepts(
                all_concepts
            )
        )

        # --------------------------------------------------------
        # STEP 5: Limit result
        # --------------------------------------------------------

        cleaned_concepts = (
            cleaned_concepts[
                :cls.MAX_CONCEPTS
            ]
        )

        print("\n========================================")
        print(
            f"Final concepts: "
            f"{len(cleaned_concepts)}"
        )
        print("========================================\n")

        return cleaned_concepts

    # ============================================================
    # ALIAS
    # ============================================================

    @classmethod
    def generate_keywords(cls, text):


        return cls.extract_concepts(
            text
        )