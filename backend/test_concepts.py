from services.concept_service import ConceptService


text = """
HTML stands for HyperText Markup Language.
HTML is used to create and structure web pages.
HTML uses tags and elements to define the
structure of a web document.

CSS is used to control the presentation
and appearance of web pages.

JavaScript is a client-side scripting language
used to create interactive web applications.

XML stands for Extensible Markup Language.
XML is used to represent and exchange structured data.
"""


concepts = ConceptService.extract_concepts(
    text,
    top_k=15
)


print("\n========== CONCEPTS ==========\n")

for index, item in enumerate(
    concepts,
    start=1
):

    print(
        f"{index}. {item['concept']}"
    )

    print(
        f"   Type: {item['type']}"
    )

    print(
        f"   Frequency: {item['frequency']}"
    )

    print(
        f"   Score: {item['score']}"
    )

    print()