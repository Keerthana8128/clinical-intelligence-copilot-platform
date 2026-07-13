from pathlib import Path

import fitz


PROCESSED_DATA_DIR = Path("data/processed")


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    """

    extracted_pages = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text()

            extracted_pages.append(
                f"\n--- Page {page_number} ---\n{page_text}"
            )

    return "\n".join(extracted_pages)


def save_extracted_text(filename: str, text: str) -> Path:
    """
    Save extracted PDF text into data/processed folder.
    """

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_filename = filename.replace(".pdf", ".txt")
    output_path = PROCESSED_DATA_DIR / output_filename

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)

    return output_path