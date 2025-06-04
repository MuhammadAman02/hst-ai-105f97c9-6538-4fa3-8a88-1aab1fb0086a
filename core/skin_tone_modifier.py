"""Skin tone modification utilities for adjusting skin appearance."""

import numpy as np
import cv2
from typing import Tuple
from skimage import color, exposure
from PIL import Image, ImageEnhance


class SkinToneModifier:
    """Modifies skin tone appearance in images while maintaining natural look."""
    
    def __init__(self):
        self.skin_detection_params = {
            'hsv_lower': np.array([0, 20, 70], dtype=np.uint8),
            'hsv_upper': np.array([20, 255, 255], dtype=np.uint8),
            'ycrcb_lower': np.array([0, 135, 85], dtype=np.uint8),
            'ycrcb_upper': np.array([255, 180, 135], dtype=np.uint8)
        }
    
    def adjust_lightness(self, image: np.ndarray, adjustment: float) -> np.ndarray:
        """
        Adjust the lightness of skin tones in the image.
        
        Args:
            image: Input image as numpy array (RGB)
            adjustment: Lightness adjustment (-50 to +50)
        
        Returns:
            Modified image with adjusted skin lightness
        """
        try:
            # Create a copy of the image
            result = image.copy()
            
            # Detect skin regions
            skin_mask = self._detect_skin_mask(image)
            
            if np.sum(skin_mask) == 0:
                return result
            
            # Convert to LAB color space for better lightness control
            lab = cv2.cvtColor(result, cv2.COLOR_RGB2LAB).astype(np.float32)
            
            # Adjust L channel (lightness) only in skin regions
            adjustment_factor = 1.0 + (adjustment / 100.0)
            lab[:, :, 0] = np.where(
                skin_mask > 0,
                np.clip(lab[:, :, 0] * adjustment_factor, 0, 100),
                lab[:, :, 0]
            )
            
            # Convert back to RGB
            lab = lab.astype(np.uint8)
            result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            
            return result
            
        except Exception as e:
            raise ValueError(f"Lightness adjustment failed: {str(e)}")
    
    def adjust_warmth(self, image: np.ndarray, adjustment: float) -> np.ndarray:
        """
        Adjust the warmth (color temperature) of skin tones.
        
        Args:
            image: Input image as numpy array (RGB)
            adjustment: Warmth adjustment (-50 to +50, negative = cooler, positive = warmer)
        
        Returns:
            Modified image with adjusted skin warmth
        """
        try:
            # Create a copy of the image
            result = image.copy().astype(np.float32)
            
            # Detect skin regions
            skin_mask = self._detect_skin_mask(image)
            
            if np.sum(skin_mask) == 0:
                return image
            
            # Calculate adjustment factors
            warmth_factor = adjustment / 100.0
            
            # Adjust red and blue channels to change warmth
            if warmth_factor > 0:  # Warmer (more red, less blue)
                red_adjustment = 1.0 + (warmth_factor * 0.3)
                blue_adjustment = 1.0 - (warmth_factor * 0.2)
            else:  # Cooler (less red, more blue)
                red_adjustment = 1.0 + (warmth_factor * 0.2)
                blue_adjustment = 1.0 - (warmth_factor * 0.3)
            
            # Apply adjustments only to skin regions
            result[:, :, 0] = np.where(
                skin_mask > 0,
                np.clip(result[:, :, 0] * red_adjustment, 0, 255),
                result[:, :, 0]
            )
            result[:, :, 2] = np.where(
                skin_mask > 0,
                np.clip(result[:, :, 2] * blue_adjustment, 0, 255),
                result[:, :, 2]
            )
            
            return result.astype(np.uint8)
            
        except Exception as e:
            raise ValueError(f"Warmth adjustment failed: {str(e)}")
    
    def adjust_saturation(self, image: np.ndarray, adjustment: float) -> np.ndarray:
        """
        Adjust the saturation of skin tones.
        
        Args:
            image: Input image as numpy array (RGB)
            adjustment: Saturation adjustment (-50 to +50)
        
        Returns:
            Modified image with adjusted skin saturation
        """
        try:
            # Create a copy of the image
            result = image.copy()
            
            # Detect skin regions
            skin_mask = self._detect_skin_mask(image)
            
            if np.sum(skin_mask) == 0:
                return result
            
            # Convert to HSV for saturation adjustment
            hsv = cv2.cvtColor(result, cv2.COLOR_RGB2HSV).astype(np.float32)
            
            # Calculate saturation adjustment factor
            saturation_factor = 1.0 + (adjustment / 100.0)
            
            # Adjust saturation only in skin regions
            hsv[:, :, 1] = np.where(
                skin_mask > 0,
                np.clip(hsv[:, :, 1] * saturation_factor, 0, 255),
                hsv[:, :, 1]
            )
            
            # Convert back to RGB
            hsv = hsv.astype(np.uint8)
            result = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            
            return result
            
        except Exception as e:
            raise ValueError(f"Saturation adjustment failed: {str(e)}")
    
    def change_skin_tone(self, image: np.ndarray, target_tone: str) -> np.ndarray:
        """
        Change skin tone to a predefined target tone.
        
        Args:
            image: Input image as numpy array (RGB)
            target_tone: Target skin tone ('lighter', 'darker', 'warmer', 'cooler')
        
        Returns:
            Modified image with changed skin tone
        """
        try:
            result = image.copy()
            
            # Define adjustment parameters for different target tones
            adjustments = {
                'lighter': {'lightness': 15, 'warmth': 0, 'saturation': -5},
                'darker': {'lightness': -15, 'warmth': 5, 'saturation': 5},
                'warmer': {'lightness': 0, 'warmth': 20, 'saturation': 10},
                'cooler': {'lightness': 0, 'warmth': -20, 'saturation': -5}
            }
            
            if target_tone not in adjustments:
                raise ValueError(f"Unknown target tone: {target_tone}")
            
            params = adjustments[target_tone]
            
            # Apply adjustments sequentially
            if params['lightness'] != 0:
                result = self.adjust_lightness(result, params['lightness'])
            
            if params['warmth'] != 0:
                result = self.adjust_warmth(result, params['warmth'])
            
            if params['saturation'] != 0:
                result = self.adjust_saturation(result, params['saturation'])
            
            return result
            
        except Exception as e:
            raise ValueError(f"Skin tone change failed: {str(e)}")
    
    def _detect_skin_mask(self, image: np.ndarray) -> np.ndarray:
        """Detect skin regions and return a binary mask."""
        try:
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
            
            # Create masks for skin detection
            mask_hsv = cv2.inRange(hsv, self.skin_detection_params['hsv_lower'], 
                                 self.skin_detection_params['hsv_upper'])
            mask_ycrcb = cv2.inRange(ycrcb, self.skin_detection_params['ycrcb_lower'], 
                                   self.skin_detection_params['ycrcb_upper'])
            
            # Combine masks
            skin_mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)
            
            # Apply morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
            
            # Apply Gaussian blur for smoother transitions
            skin_mask = cv2.GaussianBlur(skin_mask, (5, 5), 0)
            
            return skin_mask
            
        except Exception as e:
            raise ValueError(f"Skin mask detection failed: {str(e)}")
    
    def apply_gradual_adjustment(self, image: np.ndarray, adjustment_type: str, 
                               intensity: float, feather_radius: int = 10) -> np.ndarray:
        """
        Apply gradual skin tone adjustments with feathered edges.
        
        Args:
            image: Input image
            adjustment_type: Type of adjustment ('lightness', 'warmth', 'saturation')
            intensity: Adjustment intensity
            feather_radius: Radius for feathering effect
        
        Returns:
            Image with gradual adjustments applied
        """
        try:
            # Get skin mask
            skin_mask = self._detect_skin_mask(image)
            
            if np.sum(skin_mask) == 0:
                return image
            
            # Create feathered mask
            feathered_mask = cv2.GaussianBlur(skin_mask, (feather_radius * 2 + 1, feather_radius * 2 + 1), 0)
            feathered_mask = feathered_mask.astype(np.float32) / 255.0
            
            # Apply adjustment
            if adjustment_type == 'lightness':
                adjusted = self.adjust_lightness(image, intensity)
            elif adjustment_type == 'warmth':
                adjusted = self.adjust_warmth(image, intensity)
            elif adjustment_type == 'saturation':
                adjusted = self.adjust_saturation(image, intensity)
            else:
                return image
            
            # Blend original and adjusted images using feathered mask
            result = image.astype(np.float32)
            adjusted = adjusted.astype(np.float32)
            
            for channel in range(3):
                result[:, :, channel] = (
                    result[:, :, channel] * (1 - feathered_mask) +
                    adjusted[:, :, channel] * feathered_mask
                )
            
            return result.astype(np.uint8)
            
        except Exception as e:
            raise ValueError(f"Gradual adjustment failed: {str(e)}")
    
    def enhance_skin_texture(self, image: np.ndarray, smoothing: float = 0.3) -> np.ndarray:
        """
        Enhance skin texture while preserving natural appearance.
        
        Args:
            image: Input image
            smoothing: Smoothing intensity (0.0 to 1.0)
        
        Returns:
            Image with enhanced skin texture
        """
        try:
            # Detect skin regions
            skin_mask = self._detect_skin_mask(image)
            
            if np.sum(skin_mask) == 0:
                return image
            
            # Apply bilateral filter for skin smoothing
            smoothed = cv2.bilateralFilter(image, 15, 80, 80)
            
            # Blend original and smoothed based on skin mask and smoothing intensity
            skin_mask_norm = (skin_mask / 255.0 * smoothing).astype(np.float32)
            
            result = image.astype(np.float32)
            smoothed = smoothed.astype(np.float32)
            
            for channel in range(3):
                result[:, :, channel] = (
                    result[:, :, channel] * (1 - skin_mask_norm) +
                    smoothed[:, :, channel] * skin_mask_norm
                )
            
            return result.astype(np.uint8)
            
        except Exception as e:
            raise ValueError(f"Skin texture enhancement failed: {str(e)}")