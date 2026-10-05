import os
import re
from io import BytesIO

import pymupdf
import torch

from PIL import Image, ImageOps

from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel
)


class HandwritingService:

    MODEL_NAME = "microsoft/trocr-base-handwritten"

    _processor = None
    _model = None

    # =========================================================
    # LOAD MODEL
    # =========================================================

    @classmethod
    def get_model(cls):

        if cls._processor is None or cls._model is None:

            print("Loading TrOCR handwriting model...")

            cls._processor = (
                TrOCRProcessor.from_pretrained(
                    cls.MODEL_NAME
                )
            )

            cls._model = (
                VisionEncoderDecoderModel.from_pretrained(
                    cls.MODEL_NAME
                )
            )

            cls._model.to("cpu")
            cls._model.eval()

            print(
                "TrOCR handwriting model loaded successfully."
            )

        return cls._processor, cls._model

    # =========================================================
    # IMAGE
    # =========================================================

    @classmethod
    def recognize(cls, file_path):

        if not file_path:
            raise ValueError(
                "File path is required."
            )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        processor, model = cls.get_model()

        with Image.open(file_path) as image:

            image = image.convert("RGB")

            return cls.recognize_page(
                image,
                processor,
                model
            )

    # =========================================================
    # PDF
    # =========================================================

    @classmethod
    def recognize_pdf(cls, file_path):

        if not file_path:
            raise ValueError(
                "PDF path is required."
            )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        return cls.run_pdf_ocr(
            file_path
        )

    # =========================================================
    # PDF → PAGES → LINES → TrOCR
    # =========================================================

    @classmethod
    def run_pdf_ocr(cls, file_path):

        processor, model = cls.get_model()

        document = pymupdf.open(
            file_path
        )

        all_pages = []

        try:

            total_pages = len(document)

            for page_number, page in enumerate(
                document,
                start=1
            ):

                print(
                    f"Processing page "
                    f"{page_number}/{total_pages}..."
                )

                # Render page directly into memory
                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(
                        2.0,
                        2.0
                    ),
                    alpha=False
                )

                image_bytes = pixmap.tobytes(
                    "png"
                )

                image = Image.open(
                    BytesIO(image_bytes)
                ).convert("RGB")

                page_text = cls.recognize_page(
                    image,
                    processor,
                    model
                )

                if page_text.strip():

                    all_pages.append(
                        page_text.strip()
                    )

                image.close()

                del image
                del image_bytes
                del pixmap

        finally:

            document.close()

        return cls.clean_text(
            "\n\n".join(all_pages)
        )

    # =========================================================
    # RECOGNIZE ONE PAGE
    # =========================================================

    @classmethod
    def recognize_page(
        cls,
        image,
        processor,
        model
    ):

        lines = cls.detect_text_lines(
            image
        )

        print(
            f"Detected {len(lines)} text lines."
        )

        if not lines:

            # Fallback: try full page
            text = cls.recognize_image(
                image,
                processor,
                model
            )

            return text

        recognized_lines = []

        for line_number, line_image in enumerate(
            lines,
            start=1
        ):

            print(
                f"  Recognizing line "
                f"{line_number}/{len(lines)}..."
            )

            text = cls.recognize_image(
                line_image,
                processor,
                model
            )

            if text.strip():

                recognized_lines.append(
                    text.strip()
                )

            line_image.close()

        return "\n".join(
            recognized_lines
        )

    # =========================================================
    # DETECT HANDWRITTEN TEXT LINES
    #
    # Uses PIL only.
    # No OpenCV.
    # No files are written to disk.
    # =========================================================

    @classmethod
    def detect_text_lines(
        cls,
        image
    ):

        # Convert to grayscale
        gray = ImageOps.grayscale(
            image
        )

        # Normalize contrast
        gray = ImageOps.autocontrast(
            gray
        )

        width, height = gray.size

        # Resize very large pages to make line detection faster.
        scale = 1.0

        if width > 1800:

            scale = 1800 / width

            gray = gray.resize(
                (
                    int(width * scale),
                    int(height * scale)
                )
            )

        width, height = gray.size

        # Convert to pixels
        pixels = gray.load()

        # -----------------------------------------------------
        # Horizontal dark-pixel projection
        # -----------------------------------------------------

        row_counts = []

        for y in range(height):

            dark_pixels = 0

            for x in range(
                width
            ):

                if pixels[x, y] < 180:
                    dark_pixels += 1

            row_counts.append(
                dark_pixels
            )

        # -----------------------------------------------------
        # Detect rows containing ink
        # -----------------------------------------------------

        threshold = max(
            2,
            int(width * 0.01)
        )

        active_rows = [
            count >= threshold
            for count in row_counts
        ]

        # -----------------------------------------------------
        # Group consecutive active rows
        # -----------------------------------------------------

        bands = []

        start = None

        for y, active in enumerate(
            active_rows
        ):

            if active and start is None:

                start = y

            elif not active and start is not None:

                end = y - 1

                if end - start >= 2:

                    bands.append(
                        (
                            start,
                            end
                        )
                    )

                start = None

        if start is not None:

            bands.append(
                (
                    start,
                    height - 1
                )
            )

        # -----------------------------------------------------
        # Merge lines separated by very small gaps
        # -----------------------------------------------------

        merged = []

        for start, end in bands:

            if not merged:

                merged.append(
                    [start, end]
                )
                continue

            previous = merged[-1]

            gap = start - previous[1]

            if gap <= 8:

                previous[1] = end

            else:

                merged.append(
                    [start, end]
                )

        # -----------------------------------------------------
        # Crop each line
        # -----------------------------------------------------

        line_images = []

        for start, end in merged:

            # Add vertical padding
            padding = 8

            top = max(
                0,
                start - padding
            )

            bottom = min(
                height,
                end + padding + 1
            )

            line = gray.crop(
                (
                    0,
                    top,
                    width,
                    bottom
                )
            )

            # Ignore extremely small regions
            if line.height < 10:
                line.close()
                continue

            # Convert back to RGB
            line = line.convert(
                "RGB"
            )

            # If page was resized, that's okay.
            # TrOCR handles the line image.

            line_images.append(
                line
            )

        return line_images

    # =========================================================
    # TROCR SINGLE LINE
    # =========================================================

    @classmethod
    def recognize_image(
        cls,
        image,
        processor,
        model
    ):

        inputs = processor(
            images=image,
            return_tensors="pt"
        )

        pixel_values = (
            inputs.pixel_values.to("cpu")
        )

        with torch.no_grad():

            generated_ids = model.generate(
                pixel_values,
                max_new_tokens=128,
                num_beams=4,
                early_stopping=True
            )

        text = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0]

        return text.strip()

    # =========================================================
    # CLEAN TEXT
    # =========================================================

    @classmethod
    def clean_text(cls, text):

        if not text:
            return ""

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()