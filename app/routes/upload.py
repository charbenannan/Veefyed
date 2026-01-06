from fastapi import APIRouter, UploadFile, File, Depends
from typing import Dict
from app.services.image_service import save_image
from app.utils.exceptions import InvalidFileTypeError, FileSizeExceededError


router = APIRouter()


@router.post("/upload", response_model=Dict)
async def upload_image(file: UploadFile = File(...)) -> Dict:
    """
    Upload an image for analysis.
    
    Args:
        file: Image file (JPEG or PNG, max 5MB)
        
    Returns:
        Dictionary containing image_id and metadata
        
    Raises:
        InvalidFileTypeError: If file type is not JPEG or PNG
        FileSizeExceededError: If file size exceeds 5MB
    """
    result = await save_image(file)
    
    return {
        "image_id": result["image_id"],
        "message": "Image uploaded successfully",
        "filename": result["filename"],
        "size_bytes": result["size_bytes"]
    }
