from services.ocr_correction_service import (
    OCRCorrectionService
)


text = """
The human heart pumps blood through the body.
The heart contains four chambers.
Blood contains red blood cells and white blood cells.
Blood pressure is important for circulation.

The heank pumps bleod through the body.
The phessure of bleod is measured.
"""


corrected = OCRCorrectionService.correct_text(
    text
)

print("\n========== ORIGINAL ==========\n")
print(text)

print("\n========== CORRECTED ==========\n")
print(corrected)