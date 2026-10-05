from services.document.document_service import (
    DocumentService
)


file_path = r"D:\SmartNotesAI\test.pdf"


try:

    print(
        "\n================================"
    )

    print(
        "Testing DocumentService"
    )

    print(
        "================================\n"
    )

    text = DocumentService.extract_text(
        file_path
    )

    print(
        "\n========== EXTRACTED TEXT ==========\n"
    )

    print(text[:3000])

    print(
        "\n====================================="
    )

    print(
        "Extraction successful!"
    )

    print(
        "====================================="
    )

except Exception as e:

    print(
        "\nERROR:"
    )

    print(
        type(e).__name__,
        ":",
        str(e)
    )