import os
import pymupdf
from PIL import Image

from paddleocr import PaddleOCR


class OCRService:

    _ocr = None

    @staticmethod
    def get_ocr():
        if OCRService._ocr is None:
            OCRService._ocr = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                engine="paddle",
                enable_mkldnn=False
            )

        return OCRService._ocr

    @staticmethod
    def extract_text_from_image(image_path):

        ocr = OCRService.get_ocr()

        results = ocr.predict(image_path)

        text_parts = []

        for result in results:

            result_data = result.json

            if isinstance(result_data, str):
                continue

            if not isinstance(result_data, dict):
                continue

            res_data = result_data.get("res", {})

            rec_texts = res_data.get(
                "rec_texts",
                []
            )

            for text in rec_texts:

                if text:
                    text_parts.append(
                        str(text).strip()
                    )

        return "\n".join(text_parts)

    @staticmethod
    def extract_text_from_pdf(pdf_path):

        document = pymupdf.open(pdf_path)

        all_text = []

        try:

            for page_number in range(
                len(document)
            ):

                page = document[
                    page_number
                ]

                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(
                        2,
                        2
                    )
                )

                image_path = (
                    "uploads"
                    + os.sep
                    + "ocr_page_"
                    + str(page_number + 1)
                    + ".png"
                )

                pixmap.save(
                    image_path
                )

                page_text = (
                    OCRService
                    .extract_text_from_image(
                        image_path
                    )
                )

                if page_text.strip():

                    all_text.append(
                        page_text
                    )

                if os.path.exists(
                    image_path
                ):
                    os.remove(
                        image_path
                    )

        finally:

            document.close()

        return "\n\n".join(
            all_text
        )