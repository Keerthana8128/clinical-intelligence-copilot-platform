import re


MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def is_pdf_file(filename: str) -> bool:
    """
    Check whether the uploaded file is a PDF based on filename extension.
    """

    return filename.lower().endswith(".pdf")


def is_file_size_allowed(file_size_bytes: int) -> bool:
    """
    Check whether uploaded file size is within allowed limit.
    """

    return file_size_bytes <= MAX_FILE_SIZE_BYTES


def sanitize_filename(filename: str) -> str:
    """
    Create a safe filename by removing unsafe characters.
    """

    safe_filename = filename.strip().replace(" ", "_")
    safe_filename = re.sub(r"[^A-Za-z0-9_.-]", "", safe_filename)

    return safe_filename