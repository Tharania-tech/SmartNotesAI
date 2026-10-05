import re


class TextChunkService:

    @staticmethod
    def clean_text(text):

        if not text:
            return ""

        text = text.replace(
            "\x00",
            " "
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    @classmethod
    def chunk_text(
        cls,
        text,
        max_words=700,
        overlap_words=100
    ):

        text = cls.clean_text(
            text
        )

        if not text:
            return []

        words = text.split()

        if len(words) <= max_words:
            return [text]

        chunks = []

        start = 0
        total_words = len(words)

        while start < total_words:

            end = min(
                start + max_words,
                total_words
            )

            chunk_words = words[
                start:end
            ]

            chunk = " ".join(
                chunk_words
            ).strip()

            if chunk:
                chunks.append(
                    chunk
                )

            if end >= total_words:
                break

            start = (
                end - overlap_words
            )

            if start < 0:
                start = 0

        return chunks