from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List
from app.services.analysis_service import analyze_image
from app.utils.exceptions import ImageNotFoundError


router = APIRouter()


class AnalyzeRequest(BaseModel):
    image_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "abc123def456"
            }
        }


class AnalyzeResponse(BaseModel):
    image_id: str
    skin_type: str
    issues: List[str]
    confidence: float
    analysis_timestamp: str
    recommendations: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "abc123def456",
                "skin_type": "Combination",
                "issues": ["Hyperpigmentation", "Fine Lines"],
                "confidence": 0.87,
                "analysis_timestamp": "2026-01-05T10:30:45.123456",
                "recommendations": [
                    "Use sunscreen daily to prevent further pigmentation",
                    "Consider retinol products for fine lines"
                ]
            }
        }


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> Dict:
    """
    Analyze a previously uploaded image.
    
    Args:
        request: Analysis request containing image_id
        
    Returns:
        Analysis results including skin type, issues, and recommendations
        
    Raises:
        ImageNotFoundError: If image_id doesn't exist
    """
    result = analyze_image(request.image_id)
    return result
