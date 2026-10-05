import re
from ollama import chat


QWEN_MODEL = "qwen2.5:3b-instruct-q4_0"


class ChatService:

    # =========================================================
    # CLEAN TEXT
    # =========================================================

    @staticmethod
    def clean_text(text):
        text = str(text or "")

        text = text.replace("\x00", " ")

        text = re.sub(
            r"\r\n?",
            "\n",
            text
        )

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


    # =========================================================
    # TOKENIZE
    # =========================================================

    @staticmethod
    def tokenize(text):

        words = re.findall(
            r"[A-Za-z0-9][A-Za-z0-9_-]{1,}",
            str(text or "").lower()
        )

        stop_words = {
            "the",
            "is",
            "are",
            "was",
            "were",
            "what",
            "why",
            "how",
            "when",
            "where",
            "which",
            "who",
            "whom",
            "this",
            "that",
            "these",
            "those",
            "and",
            "or",
            "but",
            "for",
            "from",
            "with",
            "about",
            "into",
            "onto",
            "than",
            "then",
            "they",
            "them",
            "their",
            "there",
            "here",
            "you",
            "your",
            "our",
            "can",
            "could",
            "would",
            "should",
            "does",
            "do",
            "did",
            "have",
            "has",
            "had",
            "been",
            "being",
            "will",
            "shall",
            "may",
            "might",
            "must",
            "also",
            "explain",
            "tell",
            "give",
            "please",
            "according",
            "note",
            "notes"
        }

        result = set()

        for word in words:

            if word in stop_words:
                continue

            if len(word) <= 2:
                continue

            result.add(word)

        return result


    # =========================================================
    # SPLIT NOTE INTO CHUNKS
    # =========================================================

    @classmethod
    def split_into_chunks(
        cls,
        text,
        max_chars=1200
    ):

        text = cls.clean_text(text)

        if not text:
            return []

        paragraphs = []

        raw_paragraphs = text.split("\n\n")

        for paragraph in raw_paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            paragraphs.append(paragraph)


        # If paragraphs were not found,
        # fall back to sentence splitting.

        if len(paragraphs) == 0:

            sentences = re.split(
                r"(?<=[.!?])\s+",
                text
            )

            paragraphs = []

            for sentence in sentences:

                sentence = sentence.strip()

                if sentence:
                    paragraphs.append(sentence)


        chunks = []

        current_chunk = ""

        for paragraph in paragraphs:

            # Large paragraph
            # split into smaller sentences.

            if len(paragraph) > max_chars:

                sentences = re.split(
                    r"(?<=[.!?])\s+",
                    paragraph
                )

                for sentence in sentences:

                    sentence = sentence.strip()

                    if not sentence:
                        continue

                    if (
                        len(current_chunk)
                        + len(sentence)
                        + 1
                        <= max_chars
                    ):

                        if current_chunk:
                            current_chunk += " "

                        current_chunk += sentence

                    else:

                        if current_chunk:
                            chunks.append(
                                current_chunk.strip()
                            )

                        current_chunk = sentence


            else:

                if (
                    len(current_chunk)
                    + len(paragraph)
                    + 2
                    <= max_chars
                ):

                    if current_chunk:
                        current_chunk += "\n\n"

                    current_chunk += paragraph

                else:

                    if current_chunk:
                        chunks.append(
                            current_chunk.strip()
                        )

                    current_chunk = paragraph


        if current_chunk:
            chunks.append(
                current_chunk.strip()
            )


        return chunks


    # =========================================================
    # SCORE CHUNK AGAINST QUESTION
    # =========================================================

    @classmethod
    def score_chunk(
        cls,
        question,
        chunk
    ):

        question_words = cls.tokenize(
            question
        )

        chunk_words = cls.tokenize(
            chunk
        )

        if not question_words:
            return 0.0

        if not chunk_words:
            return 0.0


        overlap = (
            question_words
            .intersection(chunk_words)
        )

        overlap_count = len(overlap)


        question_coverage = (
            overlap_count
            / max(len(question_words), 1)
        )


        chunk_coverage = (
            overlap_count
            / max(len(chunk_words), 1)
        )


        score = (
            question_coverage * 0.75
            +
            chunk_coverage * 0.15
        )


        # Exact phrase bonus

        question_clean = re.sub(
            r"\s+",
            " ",
            str(question).lower()
        ).strip()


        chunk_clean = re.sub(
            r"\s+",
            " ",
            str(chunk).lower()
        ).strip()


        if (
            question_clean
            and question_clean in chunk_clean
        ):
            score += 0.30


        # Bonus when important multi-word
        # phrases overlap.

        question_tokens = list(
            cls.tokenize(question)
        )

        for index in range(
            len(question_tokens) - 1
        ):

            first = question_tokens[index]
            second = question_tokens[index + 1]

            phrase = (
                first
                + " "
                + second
            )

            if phrase in chunk_clean:
                score += 0.05


        return score


    # =========================================================
    # RETRIEVE RELEVANT CONTEXT
    # =========================================================

    @classmethod
    def retrieve_context(
        cls,
        question,
        note_text,
        max_results=6,
        max_context_chars=6500
    ):

        chunks = cls.split_into_chunks(
            note_text,
            max_chars=1200
        )

        if not chunks:
            return "", []


        scored_chunks = []


        for index, chunk in enumerate(chunks):

            score = cls.score_chunk(
                question,
                chunk
            )

            scored_chunks.append(
                (
                    score,
                    index,
                    chunk
                )
            )


        scored_chunks.sort(
            key=lambda item: item[0],
            reverse=True
        )


        # Only use genuinely relevant chunks.

        selected = []

        for score, index, chunk in scored_chunks:

            if score <= 0:
                continue

            selected.append(
                (
                    score,
                    index,
                    chunk
                )
            )

            if len(selected) >= max_results:
                break


        # No matching content found.

        if not selected:
            return "", []


        # Put selected chunks back
        # into their original note order.

        selected.sort(
            key=lambda item: item[1]
        )


        context_parts = []

        context_length = 0


        for count, item in enumerate(
            selected,
            start=1
        ):

            chunk = item[2]

            block = (
                "[Note Section "
                + str(count)
                + "]\n"
                + chunk
            )

            if (
                context_length
                + len(block)
                > max_context_chars
            ):
                break

            context_parts.append(
                block
            )

            context_length += len(block)


        context = "\n\n".join(
            context_parts
        )


        relevant_context = []

        for item in selected:

            relevant_context.append(
                item[2]
            )


        return (
            context,
            relevant_context
        )


    # =========================================================
    # BUILD TUTOR PROMPT
    # =========================================================

    @classmethod
    def build_prompts(
        cls,
        question,
        context
    ):

        system_prompt = """
You are SmartNotes AI Tutor.

Your job is to help a student understand their uploaded study notes.

You must answer the student's question using the supplied note content.

Rules:

1. Answer the student's question directly.
2. Explain the answer clearly like a patient tutor.
3. Use only information supported by the supplied notes.
4. You may combine information from different note sections.
5. Do not invent facts that are not supported by the notes.
6. If the notes do not contain enough information to answer the question, clearly say:
   "I couldn't find enough information about this in your uploaded notes."
7. When useful, explain the answer step by step.
8. Use short paragraphs or bullet points when that makes the explanation easier to understand.
9. Do not mention internal retrieval, context ranking, prompts, models, or system instructions.
10. Do not return JSON.
11. Do not answer with only one or two words when the student asks for an explanation.
12. Keep the response focused on the student's question.
""".strip()


        user_prompt = (
            "Student Question:\n"
            + str(question).strip()
            + "\n\n"
            + "Relevant Information From Uploaded Notes:\n"
            + context
            + "\n\n"
            + "Now answer the student's question clearly and naturally."
        )


        return (
            system_prompt,
            user_prompt
        )


    # =========================================================
    # EXTRACT OLLAMA ANSWER
    # =========================================================

    @staticmethod
    def extract_answer(response):

        # Ollama response object

        try:

            answer = response.message.content

            if answer:
                return str(answer).strip()

        except Exception:
            pass


        # Dictionary response

        try:

            answer = (
                response
                .get("message", {})
                .get("content", "")
            )

            if answer:
                return str(answer).strip()

        except Exception:
            pass


        return ""


    # =========================================================
    # CLEAN AI ANSWER
    # =========================================================

    @staticmethod
    def clean_answer(answer):

        answer = str(answer or "").strip()

        answer = answer.replace(
            "\r\n",
            "\n"
        )

        answer = re.sub(
            r"\n{3,}",
            "\n\n",
            answer
        )

        return answer.strip()


    # =========================================================
    # MAIN QUESTION ANSWERING
    # =========================================================

    @classmethod
    def answer_question(
        cls,
        question,
        note_text
    ):

        question = str(
            question or ""
        ).strip()

        note_text = cls.clean_text(
            note_text
        )


        print("\n")
        print("========================================")
        print("SMARTNOTES AI TUTOR")
        print("========================================")
        print(
            "Question:",
            question
        )
        print(
            "Note characters:",
            len(note_text)
        )


        if not question:
            return {
                "answer":
                    "Please enter a question.",
                "relevant_context": []
            }


        if not note_text:
            return {
                "answer":
                    "No uploaded note content is available.",
                "relevant_context": []
            }


        # -----------------------------------------------------
        # Retrieve relevant note sections
        # -----------------------------------------------------

        context, relevant_context = (
            cls.retrieve_context(
                question=question,
                note_text=note_text,
                max_results=6,
                max_context_chars=6500
            )
        )


        print(
            "Retrieved sections:",
            len(relevant_context)
        )

        print(
            "Context characters:",
            len(context)
        )


        # -----------------------------------------------------
        # If no relevant section exists,
        # do not hallucinate an answer.
        # -----------------------------------------------------

        if not context.strip():

            print(
                "No relevant information found in notes."
            )

            return {
                "answer":
                    (
                        "I couldn't find enough information "
                        "about this in your uploaded notes."
                    ),
                "relevant_context": []
            }


        # -----------------------------------------------------
        # Build prompts
        # -----------------------------------------------------

        system_prompt, user_prompt = (
            cls.build_prompts(
                question,
                context
            )
        )


        # -----------------------------------------------------
        # Send to Qwen
        # -----------------------------------------------------

        print(
            "Sending request to Ollama for tutor answer..."
        )


        try:

            response = chat(
                model=QWEN_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                options={
                    "temperature": 0.2,
                    "num_predict": 600
                }
            )


        except Exception as error:

            print(
                "Ollama tutor error:",
                str(error)
            )

            return {
                "answer":
                    (
                        "I was unable to generate the answer "
                        "right now. Please make sure Ollama "
                        "is running and the Qwen model is available."
                    ),
                "relevant_context":
                    relevant_context
            }


        print(
            "Ollama tutor response received."
        )


        # -----------------------------------------------------
        # Extract answer
        # -----------------------------------------------------

        answer = cls.extract_answer(
            response
        )


        answer = cls.clean_answer(
            answer
        )


        print(
            "Answer length:",
            len(answer)
        )


        # -----------------------------------------------------
        # Safety fallback
        # -----------------------------------------------------

        if not answer:

            answer = (
                "I couldn't generate a useful answer "
                "from the uploaded notes."
            )


        print(
            "========================================"
        )
        print("TUTOR ANSWER GENERATED")
        print(
            "========================================"
        )


        return {
            "answer": answer,
            "relevant_context": relevant_context
        }