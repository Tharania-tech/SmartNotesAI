import re


class QuizContentService:

    @staticmethod
    def clean_text(text):

        if not text:
            return ""

        lines = text.splitlines()

        cleaned = []
        seen = set()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Remove page numbers
            if re.fullmatch(
                r"page\s*\d+",
                line,
                flags=re.IGNORECASE
            ):
                continue

            if re.fullmatch(
                r"\d+",
                line
            ):
                continue

            # Remove URLs
            if re.search(
                r"https?://\S+|www\.\S+",
                line,
                flags=re.IGNORECASE
            ):
                continue

            # Remove email-only lines
            if re.fullmatch(
                r"[\w\.-]+@[\w\.-]+\.\w+",
                line
            ):
                continue

            # Remove repeated lines
            normalized = re.sub(
                r"\s+",
                " ",
                line.lower()
            )

            if normalized in seen:
                continue

            seen.add(normalized)

            cleaned.append(line)

        return "\n".join(cleaned)