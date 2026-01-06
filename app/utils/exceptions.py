from fastapi import HTTPException, status


class InvalidFileTypeError(HTTPException):
    def __init__(self, message: str = "Invalid file type. Only JPEG and PNG are allowed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class FileSizeExceededError(HTTPException):
    def __init__(self, message: str = "File size exceeds 5MB limit"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class ImageNotFoundError(HTTPException):
    def __init__(self, image_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image not found with id: {image_id}"
        )


class InvalidAPIKeyError(HTTPException):
    def __init__(self, message: str = "Invalid API key"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)
