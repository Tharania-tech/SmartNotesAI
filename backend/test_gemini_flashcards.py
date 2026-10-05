from services.learning_content_service import (
    LearningContentService
)


text = """
HTML stands for HyperText Markup Language.
HTML is used to create and structure web pages.
HTML uses tags and elements to define the
structure of web documents.

CSS is used to control the presentation
and appearance of web pages.

JavaScript is a client-side scripting language
used to create interactive web applications.

XML stands for Extensible Markup Language.
XML is used to represent and exchange
structured data.
"""


try:

    print(
        "\n======================================"
    )

    print(
        "Testing Gemini Flashcards"
    )

    print(
        "======================================\n"
    )

    flashcards = (
        LearningContentService
        .generate_flashcards(
            text,
            count=10
        )
    )

    print(
        "========== FLASHCARDS ==========\n"
    )

    for index, card in enumerate(
        flashcards,
        start=1
    ):

        print(
            f"{index}. Concept: "
            f"{card['concept']}"
        )

        print(
            f"   Front: "
            f"{card['front']}"
        )

        print(
            f"   Back: "
            f"{card['back']}"
        )

        print()

    print(
        f"Generated: "
        f"{len(flashcards)} flashcards"
    )

except Exception as exc:

    print(
        "\n========== ERROR ==========\n"
    )

    print(
        type(exc).__name__
    )

    print(
        str(exc)
    )

    print(
        "\n============================"
    )