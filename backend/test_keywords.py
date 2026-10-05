from services.keyword_service import KeywordService


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


keywords = KeywordService.extract_keywords(
    text,
    top_n=10
)


print("\n========== KEYWORDS ==========\n")

for index, keyword in enumerate(
    keywords,
    start=1
):
    print(f"{index}. {keyword}")