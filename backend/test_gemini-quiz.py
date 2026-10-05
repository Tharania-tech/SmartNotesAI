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
        "Testing Gemini Quiz Generation"
    )

    print(
        "======================================\n"
    )

    quiz = (
        LearningContentService
        .generate_quiz(
            text,
            count=10
        )
    )

    print(
        "========== QUIZ ==========\n"
    )

    for index, item in enumerate(
        quiz,
        start=1
    ):

        print(
            f"{index}. {item['question']}"
        )

        print(
            f"A. {item['options']['A']}"
        )

        print(
            f"B. {item['options']['B']}"
        )

        print(
            f"C. {item['options']['C']}"
        )

        print(
            f"D. {item['options']['D']}"
        )

        print(
            f"Correct: {item['correct_answer']}"
        )

        print(
            f"Concept: {item['concept']}"
        )

        print(
            f"Explanation: {item['explanation']}"
        )

        print()

    print(
        f"Generated: {len(quiz)} questions"
    )

except Exception as e:

    print(
        "\n========== ERROR ==========\n"
    )

    print(
        type(e).__name__,
        ":",
        str(e)
    )

    print(
        "\n============================"
    )