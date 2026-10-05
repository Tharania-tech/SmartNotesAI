from services.quiz_service import QuizService


text = """
HTML stands for HyperText Markup Language.
HTML is used to create and structure web pages.
HTML uses tags and elements to define web documents.

CSS is used to control the presentation and
appearance of web pages.

JavaScript is a client-side scripting language
used to create interactive web applications.

XML stands for Extensible Markup Language.
XML is used to represent and exchange structured data.
"""


quiz = QuizService.generate_quiz(
    text,
    number_of_questions=10
)


print("\n========== QUIZ ==========\n")

for index, item in enumerate(
    quiz,
    start=1
):

    print(
        f"{index}. {item['question']}"
    )

    for option, value in item[
        "options"
    ].items():

        print(
            f"   {option}. {value}"
        )

    print(
        f"   Correct: "
        f"{item['correct_answer']}"
    )

    print(
        f"   Explanation: "
        f"{item['explanation']}"
    )

    print(
        f"   Concept: "
        f"{item['concept']}"
    )

    print()

print(
    f"Generated: {len(quiz)} questions"
)