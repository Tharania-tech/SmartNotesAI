from services.flashcard_service import (
    FlashcardService
)


text = """
HTML stands for HyperText Markup Language.
HTML is used to create and structure web pages.
HTML uses tags and elements to define
the structure of a web document.

CSS is used to control the presentation
and appearance of web pages.

JavaScript is a client-side scripting language
used to create interactive web applications.

XML stands for Extensible Markup Language.
XML is used to represent and exchange
structured data.
"""


flashcards = FlashcardService.generate_flashcards(
    text,
    number_of_cards=10
)


print("\n========== FLASHCARDS ==========\n")

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
    f"Generated: {len(flashcards)} flashcards"
)