"""Pydantic models for data validation and serialization."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class ColorInfo(BaseModel):
    """Model for color information."""
    hex: str = Field(..., description="Hex color code")
    name: str = Field(..., description="Color name")
    category: Optional[str] = Field(None, description="Color category")
    
    @validator('hex')
    def validate_hex_color(cls, v):
        """Validate hex color format."""
        if not v.startswith('#') or len(v) != 7:
            raise ValueError('Hex color must be in format #RRGGBB')
        try:
            int(v[1:], 16)
        except ValueError:
            raise ValueError('Invalid hex color format')
        return v.upper()


class SkinToneAnalysis(BaseModel):
    """Model for skin tone analysis results."""
    category: str = Field(..., description="Skin tone category")
    undertone: str = Field(..., description="Skin undertone")
    lightness: float = Field(..., ge=0, le=100, description="Lightness percentage")
    temperature: str = Field(..., description="Color temperature")
    dominant_colors: List[List[int]] = Field(..., description="Dominant colors as RGB values")
    average_color: List[float] = Field(..., description="Average skin color as RGB")
    harmony_info: Dict[str, Any] = Field(..., description="Color harmony information")
    skin_pixel_count: int = Field(..., ge=0, description="Number of skin pixels detected")
    confidence: float = Field(..., ge=0, le=1, description="Analysis confidence score")


class ColorRecommendations(BaseModel):
    """Model for color recommendations."""
    best_colors: List[ColorInfo] = Field(..., description="Recommended colors")
    avoid_colors: List[ColorInfo] = Field(..., description="Colors to avoid")
    outfit_combinations: List[List[str]] = Field(..., description="Outfit color combinations")
    seasonal_colors: Dict[str, Any] = Field(..., description="Seasonal color recommendations")
    makeup_colors: Dict[str, List[ColorInfo]] = Field(..., description="Makeup color suggestions")
    hair_colors: List[ColorInfo] = Field(..., description="Hair color suggestions")
    color_theory: Dict[str, str] = Field(..., description="Color theory explanation")
    styling_tips: List[str] = Field(..., description="Styling tips")


class ImageUploadRequest(BaseModel):
    """Model for image upload request."""
    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="MIME type of the image")
    size: int = Field(..., ge=0, description="File size in bytes")
    
    @validator('content_type')
    def validate_content_type(cls, v):
        """Validate image content type."""
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if v.lower() not in allowed_types:
            raise ValueError(f'Content type must be one of: {allowed_types}')
        return v.lower()


class SkinToneAdjustment(BaseModel):
    """Model for skin tone adjustment parameters."""
    adjustment_type: str = Field(..., description="Type of adjustment")
    value: float = Field(..., ge=-50, le=50, description="Adjustment value")
    
    @validator('adjustment_type')
    def validate_adjustment_type(cls, v):
        """Validate adjustment type."""
        allowed_types = ['lightness', 'warmth', 'saturation']
        if v.lower() not in allowed_types:
            raise ValueError(f'Adjustment type must be one of: {allowed_types}')
        return v.lower()


class AnalysisResponse(BaseModel):
    """Model for analysis response."""
    success: bool = Field(..., description="Whether the analysis was successful")
    message: str = Field(..., description="Response message")
    skin_analysis: Optional[SkinToneAnalysis] = Field(None, description="Skin tone analysis results")
    recommendations: Optional[ColorRecommendations] = Field(None, description="Color recommendations")
    error_details: Optional[str] = Field(None, description="Error details if analysis failed")


class HealthCheckResponse(BaseModel):
    """Model for health check response."""
    status: str = Field(..., description="Health status")
    app: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    timestamp: Optional[str] = Field(None, description="Response timestamp")


class AppSettings(BaseModel):
    """Model for application settings."""
    app_name: str = Field(..., description="Application name")
    app_version: str = Field(..., description="Application version")
    debug: bool = Field(False, description="Debug mode")
    host: str = Field("0.0.0.0", description="Host address")
    port: int = Field(8000, ge=1, le=65535, description="Port number")
    max_image_size: int = Field(5242880, ge=1, description="Maximum image size in bytes")
    allowed_extensions: List[str] = Field(["jpg", "jpeg", "png", "webp"], description="Allowed file extensions")
    temp_dir: str = Field("temp_images", description="Temporary directory for images")
    theme: str = Field("creative", description="UI theme")
    show_footer: bool = Field(True, description="Whether to show footer")