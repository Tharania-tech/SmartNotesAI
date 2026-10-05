import pymupdf

from services.handwriting.handwriting_service import HandwritingService


class DocumentService:

    @classmethod
    def extract_text(cls, file_path):

        if not file_path:
            raise ValueError(
                "File path is required."
            )

        extension = file_path.lower()

        # ==========================================
        # IMAGE FILE
        # ==========================================

        if extension.endswith(
            (".jpg", ".jpeg", ".png")
        ):

            return HandwritingService.recognize(
                file_path
            )

        # ==========================================
        # PDF FILE
        # ==========================================

        if extension.endswith(".pdf"):

            text = cls.extract_pdf_text(
                file_path
            )

            if text and len(text.strip()) > 50:

                print(
                    "Normal text PDF detected."
                )

                return text.strip()

            print(
                "No sufficient text found."
            )

            print(
                "PDF may be scanned/handwritten."
            )

            return HandwritingService.recognize_pdf(
                file_path
            )

        raise ValueError(
            "Unsupported file type. "
            "Supported formats: PDF, JPG, JPEG, PNG."
        )

    # ==========================================
    # NORMAL PDF TEXT EXTRACTION
    # ==========================================

    @classmethod
    def extract_pdf_text(cls, file_path):

        document = pymupdf.open(
            file_path
        )

        text_parts = []

        for page_number, page in enumerate(
            document,
            start=1
        ):

            page_text = page.get_text()

            if page_text:

                text_parts.append(
                    page_text
                )

            print(
                f"Processed PDF page {page_number}"
            )

        document.close()

        return "\n".join(
            text_parts
        )