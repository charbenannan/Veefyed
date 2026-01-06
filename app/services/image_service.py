import uuid
from pathlib import Path
from typing import Dict
from fastapi import UploadFile
from app.config import UPLOAD_DIR
from app.utils.validators import validate_uploaded_file
from app.utils.exceptions import ImageNotFoundError


# In-memory storage for image metadata (would be a database in production)
image_store: Dict[str, Dict] = {}


async def save_image(file: UploadFile) -> Dict[str, str]:
    """
    Save uploaded image to local storage and return metadata.
    
    Args:
        file: Uploaded file from FastAPI
        
    Returns:
        Dictionary containing image_id, filename, and size
    """
    # Validate file
    content = await validate_uploaded_file(file)
    
    # Generate unique image ID
    image_id = str(uuid.uuid4())
    
    # Create unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{image_id}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file to disk
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Store metadata in memory
    image_store[image_id] = {
        "filename": file.filename,
        "stored_filename": unique_filename,
        "path": str(file_path),
        "size_bytes": len(content),
        "content_type": file.content_type
    }
    
    return {
        "image_id": image_id,
        "filename": file.filename,
        "size_bytes": len(content)
    }


def get_image_metadata(image_id: str) -> Dict:
    """
    Retrieve image metadata by ID.
    
    Args:
        image_id: Unique image identifier
        
    Returns:
        Image metadata dictionary
        
    Raises:
        ImageNotFoundError: If image_id doesn't exist
    """
    if image_id not in image_store:
        raise ImageNotFoundError(image_id)
    
    return image_store[image_id]


def get_image_path(image_id: str) -> Path:
    """
    Get the file path for an image.
    
    Args:
        image_id: Unique image identifier
        
    Returns:
        Path object to the image file
        
    Raises:
        ImageNotFoundError: If image_id doesn't exist
    """
    metadata = get_image_metadata(image_id)
    return Path(metadata["path"])
