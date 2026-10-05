from services.learning_content_service import (
    LearningContentService
)


# =========================================================
# TEST CONTENT
# =========================================================

text = """
HTML stands for HyperText Markup Language.
It is used to create and structure web pages.
HTML uses tags and elements to define the
structure of a web document.

CSS is used to control the presentation and
appearance of web pages. CSS can be embedded
in an HTML page or placed in an external
style sheet.

JavaScript is a client-side scripting language
used to create interactive web applications.
JavaScript supports variables, functions,
events and form validation.

XML stands for Extensible Markup Language.
It is used to represent and exchange structured
information between applications.
"""


# =========================================================
# RUN TEST
# =========================================================

try:

    print(
        "\n======================================"
    )

    print(
        "Testing LearningContentService"
    )

    print(
        "======================================\n"
    )

    print(
        "Generating key concepts...\n"
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

        keyword = item.get(
            "keyword",
            ""
        )

        explanation = item.get(
            "explanation",
            ""
        )

        print(
            f"{index}. {keyword}"
        )

        print(
            f"   {explanation}\n"
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