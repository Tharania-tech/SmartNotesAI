from services.ocr_service import OCRService


IMAGE_PATH = r"D:\SmartNotesAI\backend\test_images\test_note.png"


print("=" * 50)
print("SMARTNOTES AI - OCR TEST")
print("=" * 50)

print("\nTesting image:")
print(IMAGE_PATH)

try:

    extracted_text = OCRService.extract_text_from_image(
        IMAGE_PATH
    )

    print("\nOCR RESULT")
    print("-" * 50)

    if extracted_text:
        print(extracted_text)

        print("\n" + "=" * 50)
        print("OCR WORKING SUCCESSFULLY")
        print("=" * 50)

    else:
        print("No text was detected.")

        print("\n" + "=" * 50)
        print("OCR RAN BUT NO TEXT WAS FOUND")
        print("=" * 50)

except Exception as error:

    print("\n" + "=" * 50)
    print("OCR TEST FAILED")
    print("=" * 50)

    print("\nError:")
    print(error)