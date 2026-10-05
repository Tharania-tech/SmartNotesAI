from services.handwriting.handwriting_service import (
    HandwritingService
)

file_path = "test_handwritten.pdf"

print("\nStarting handwriting OCR...\n")

try:

    text = HandwritingService.recognize_pdf(
        file_path
    )

    print(
        "\n========== EXTRACTED TEXT ==========\n"
    )

    print(text)

    print(
        "\n====================================\n"
    )

except Exception as e:

    print("\nOCR ERROR:")
    print(type(e).__name__, ":", str(e))