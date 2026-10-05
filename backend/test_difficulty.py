from services.difficulty_service import DifficultyService


text = """
HTML stands for HyperText Markup Language.
HTML is used to create and structure web pages.
CSS is used to control the presentation of web pages.
JavaScript is used to create interactive web applications.
XML is used to represent and exchange structured data.
"""


result = DifficultyService.analyze_note(text)

print("\n========== DIFFICULTY RESULT ==========\n")

for key, value in result.items():
    print(f"{key}: {value}")