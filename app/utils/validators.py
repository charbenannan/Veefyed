import os
from pathlib import Path
from fastapi import UploadFile
from app.config import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, MAX_FILE_SIZE
from app.utils.exceptions import InvalidFileTypeError, FileSizeExceededError


def validate_file_type(file: UploadFile) -> None:
    """Validate file type based on MIME type and extension."""
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise InvalidFileTypeError()
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise InvalidFileTypeError()


def validate_file_size(file_content: bytes) -> None:
    """Validate file size."""
    if len(file_content) > MAX_FILE_SIZE:
        raise FileSizeExceededError()


async def validate_uploaded_file(file: UploadFile) -> bytes:
    """Validate uploaded file and return content."""
    validate_file_type(file)
    
    content = await file.read()
    validate_file_size(content)
    
    # Reset file pointer for potential re-reading
    await file.seek(0)
    
    return content
