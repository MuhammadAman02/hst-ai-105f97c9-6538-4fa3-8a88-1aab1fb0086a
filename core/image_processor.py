"""Image processing utilities for the skin tone analyzer."""

import os
import io
from typing import Optional, List, Tuple
import numpy as np
import cv2
from PIL import Image, ImageEnhance
from app.config import settings


class ImageProcessor:
    """Handles image loading, validation, and basic processing operations."""
    
    def __init__(self):
        self.max_size = (800, 800)  # Maximum image dimensions for processing
        self.allowed_formats = {'.jpg', '.jpeg', '.png', '.webp'}
    
    def validate_upload(self, content: io.BytesIO, filename: str) -> bool:
        """Validate uploaded image file."""
        try:
            # Check file extension
            file_ext = os.path.splitext(filename.lower())[1]
            if file_ext not in self.allowed_formats:
                return False
            
            # Check file size
            content.seek(0, 2)  # Seek to end
            size = content.tell()
            content.seek(0)  # Reset position
            
            if size > settings.max_image_size:
                return False
            
            # Try to open as image
            try:
                img = Image.open(content)
                img.verify()
                content.seek(0)  # Reset for actual use
                return True
            except Exception:
                return False
                
        except Exception:
            return False
    
    def load_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess image for analysis."""
        try:
            # Load image with PIL for better format support
            pil_image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Resize if too large
            if pil_image.size[0] > self.max_size[0] or pil_image.size[1] > self.max_size[1]:
                pil_image.thumbnail(self.max_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy array (RGB format)
            image_array = np.array(pil_image)
            
            return image_array
            
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")
    
    def save_image(self, image: np.ndarray, output_path: str, quality: int = 85) -> None:
        """Save processed image to file."""
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image.astype(np.uint8))
            
            # Save with appropriate format
            file_ext = os.path.splitext(output_path.lower())[1]
            if file_ext in ['.jpg', '.jpeg']:
                pil_image.save(output_path, 'JPEG', quality=quality, optimize=True)
            elif file_ext == '.png':
                pil_image.save(output_path, 'PNG', optimize=True)
            elif file_ext == '.webp':
                pil_image.save(output_path, 'WEBP', quality=quality, optimize=True)
            else:
                pil_image.save(output_path, 'JPEG', quality=quality, optimize=True)
                
        except Exception as e:
            raise ValueError(f"Failed to save image: {str(e)}")
    
    def resize_image(self, image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """Resize image while maintaining aspect ratio."""
        try:
            height, width = image.shape[:2]
            target_width, target_height = target_size
            
            # Calculate scaling factor
            scale = min(target_width / width, target_height / height)
            
            # Calculate new dimensions
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Resize image
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
            
            return resized
            
        except Exception as e:
            raise ValueError(f"Failed to resize image: {str(e)}")
    
    def enhance_image(self, image: np.ndarray, brightness: float = 1.0, 
                     contrast: float = 1.0, saturation: float = 1.0) -> np.ndarray:
        """Apply basic image enhancements."""
        try:
            # Convert to PIL for enhancement
            pil_image = Image.fromarray(image)
            
            # Apply brightness
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(pil_image)
                pil_image = enhancer.enhance(brightness)
            
            # Apply contrast
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(pil_image)
                pil_image = enhancer.enhance(contrast)
            
            # Apply saturation
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(pil_image)
                pil_image = enhancer.enhance(saturation)
            
            # Convert back to numpy array
            enhanced = np.array(pil_image)
            
            return enhanced
            
        except Exception as e:
            raise ValueError(f"Failed to enhance image: {str(e)}")
    
    def crop_face_region(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Detect and crop face region for better skin tone analysis."""
        try:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Load face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Use the largest face
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = largest_face
                
                # Add some padding around the face
                padding = int(min(w, h) * 0.2)
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(image.shape[1] - x, w + 2 * padding)
                h = min(image.shape[0] - y, h + 2 * padding)
                
                # Crop face region
                face_region = image[y:y+h, x:x+w]
                return face_region
            
            return None
            
        except Exception:
            # If face detection fails, return None
            return None
    
    def get_image_stats(self, image: np.ndarray) -> dict:
        """Get basic statistics about the image."""
        try:
            height, width, channels = image.shape
            
            stats = {
                'width': width,
                'height': height,
                'channels': channels,
                'total_pixels': width * height,
                'mean_brightness': np.mean(image),
                'std_brightness': np.std(image),
                'min_value': np.min(image),
                'max_value': np.max(image)
            }
            
            return stats
            
        except Exception as e:
            raise ValueError(f"Failed to get image statistics: {str(e)}")