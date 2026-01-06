import random
from datetime import datetime
from typing import Dict, List
from app.services.image_service import get_image_metadata


# Mock data for skin analysis
SKIN_TYPES = ["Oily", "Dry", "Combination", "Normal", "Sensitive"]

SKIN_ISSUES = [
    "Hyperpigmentation",
    "Fine Lines",
    "Acne",
    "Dark Circles",
    "Uneven Texture",
    "Enlarged Pores",
    "Redness",
    "Dryness",
    "Excess Oil"
]

RECOMMENDATIONS = {
    "Hyperpigmentation": "Use sunscreen daily to prevent further pigmentation",
    "Fine Lines": "Consider retinol products for fine lines",
    "Acne": "Use gentle, non-comedogenic cleansers and consider salicylic acid",
    "Dark Circles": "Ensure adequate sleep and consider eye creams with caffeine",
    "Uneven Texture": "Regular exfoliation can help improve skin texture",
    "Enlarged Pores": "Use products with niacinamide to minimize pore appearance",
    "Redness": "Look for soothing ingredients like centella asiatica",
    "Dryness": "Use a rich moisturizer with hyaluronic acid",
    "Excess Oil": "Use oil-free, mattifying products and blotting papers"
}


def analyze_image(image_id: str) -> Dict:
    """
    Perform mock analysis on an uploaded image.
    
    This simulates AI-powered skin analysis. In production, this would:
    - Load the actual image file
    - Run it through a trained ML model
    - Return real detection results
    
    Args:
        image_id: Unique identifier for the uploaded image
        
    Returns:
        Dictionary containing analysis results
    """
    # Verify image exists (will raise ImageNotFoundError if not)
    get_image_metadata(image_id)
    
    # Mock analysis logic
    skin_type = random.choice(SKIN_TYPES)
    
    # Randomly select 1-3 issues
    num_issues = random.randint(1, 3)
    issues = random.sample(SKIN_ISSUES, num_issues)
    
    # Generate realistic confidence score
    confidence = round(random.uniform(0.70, 0.95), 2)
    
    # Generate recommendations based on detected issues
    recommendations = [RECOMMENDATIONS[issue] for issue in issues]
    
    return {
        "image_id": image_id,
        "skin_type": skin_type,
        "issues": issues,
        "confidence": confidence,
        "analysis_timestamp": datetime.now().isoformat(),
        "recommendations": recommendations
    }
