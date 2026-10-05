import re


class WeakTopicFlashcardService:

    VALID_TOPICS = {
        "html",
        "css",
        "javascript",
        "xml",
        "dhtml",
        "dom",
        "http",
        "https",
        "url",
        "uri",
        "api",
        "jdbc",
        "odbc",
        "jsp",
        "servlet",
        "servlets",
        "cgi",
        "rmi",
        "sax",
        "xsl",
        "xslt",
        "dtd",
        "xsd",
        "mvc",
        "mime",
        "ide",
        "jdk",
        "java"
    }

    @classmethod
    def is_valid_topic(cls, topic):

        if not topic:
            return False

        return topic.strip().lower() in cls.VALID_TOPICS

    @staticmethod
    def clean_text(text):

        if not text:
            return ""

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return text

    @classmethod
    def split_sentences(cls, text):

        text = cls.clean_text(text)

        if not text:
            return []

        return re.split(
            r"(?<=[.!?])\s+",
            text
        )

    @classmethod
    def generate_flashcards(
        cls,
        text,
        weak_topics,
        max_cards_per_topic=3
    ):

        if not text or not weak_topics:
            return []

        sentences = cls.split_sentences(text)

        flashcards = []

        for topic_item in weak_topics:

            # weak topic may be:
            # {"concept": "HTML", ...}
            # or {"topic": "HTML", ...}
            # or simply "HTML"

            if isinstance(topic_item, dict):

                topic = (
                    topic_item.get("concept")
                    or topic_item.get("topic")
                    or ""
                )

            else:

                topic = str(topic_item)

            topic = topic.strip()

            if not cls.is_valid_topic(topic):
                continue

            matched_sentences = []

            for sentence in sentences:

                sentence = cls.clean_text(
                    sentence
                )

                if not sentence:
                    continue

                if topic.lower() in sentence.lower():

                    # Avoid extremely small fragments
                    if len(sentence.split()) >= 6:

                        matched_sentences.append(
                            sentence
                        )

            # Remove duplicate sentences
            unique_sentences = []

            seen = set()

            for sentence in matched_sentences:

                key = sentence.lower()

                if key in seen:
                    continue

                seen.add(key)

                unique_sentences.append(
                    sentence
                )

            for sentence in unique_sentences[
                :max_cards_per_topic
            ]:

                flashcards.append({

                    "topic": topic,

                    "front": (
                        f"What is {topic}?"
                    ),

                    "back": sentence,

                    "explanation": (
                        f"This information is taken "
                        f"from the uploaded notes about "
                        f"{topic}."
                    )
                })

        return flashcards