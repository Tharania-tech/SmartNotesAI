from services.learning_content_service import (
    LearningContentService
)


text = """
HTML stands for HyperText Markup Language.
HTML is used to create and structure web pages.
HTML uses tags and elements to define
the structure of web documents.

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
        "Testing Gemini LearningContentService"
    )

    print(
        "======================================\n"
    )

    keywords = (
        LearningContentService
        .generate_keywords(
            text,
            count=10
        )
    )

    print(
        "========== KEY CONCEPTS ==========\n"
    )

    for index, item in enumerate(
        keywords,
        start=1
    ):

        print(
            f"{index}. {item.get('keyword')}"
        )

        print(
            f"   {item.get('explanation')}\n"
        )

    print(
        "=================================="
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