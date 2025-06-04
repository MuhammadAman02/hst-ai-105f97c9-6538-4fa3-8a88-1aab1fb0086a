"""Color analysis utilities for skin tone detection and classification."""

import numpy as np
import cv2
from typing import Dict, List, Tuple, Any
from sklearn.cluster import KMeans
from skimage import color


class ColorAnalyzer:
    """Analyzes skin tones and classifies them according to color theory."""
    
    def __init__(self):
        # Define skin tone categories based on color theory
        self.skin_tone_categories = {
            'very_light': {'range': (0, 25), 'name': 'Very Light'},
            'light': {'range': (25, 40), 'name': 'Light'},
            'light_medium': {'range': (40, 55), 'name': 'Light Medium'},
            'medium': {'range': (55, 70), 'name': 'Medium'},
            'medium_dark': {'range': (70, 85), 'name': 'Medium Dark'},
            'dark': {'range': (85, 100), 'name': 'Dark'}
        }
        
        # Undertone classification thresholds
        self.undertone_thresholds = {
            'cool': {'blue_ratio': 0.4, 'red_ratio': 0.3},
            'warm': {'red_ratio': 0.4, 'blue_ratio': 0.3},
            'neutral': {'balance_threshold': 0.1}
        }
    
    def analyze_skin_tone(self, image: np.ndarray) -> Dict[str, Any]:
        """Comprehensive skin tone analysis."""
        try:
            # Detect skin regions
            skin_mask = self._detect_skin_regions(image)
            
            if np.sum(skin_mask) == 0:
                raise ValueError("No skin regions detected in the image")
            
            # Extract skin pixels
            skin_pixels = image[skin_mask > 0]
            
            # Analyze dominant colors
            dominant_colors = self._get_dominant_colors(skin_pixels, n_colors=5)
            
            # Calculate average skin color
            avg_skin_color = np.mean(skin_pixels, axis=0)
            
            # Determine lightness level
            lightness = self._calculate_lightness(avg_skin_color)
            
            # Classify skin tone category
            category = self._classify_skin_tone_category(lightness)
            
            # Determine undertone
            undertone = self._determine_undertone(avg_skin_color, skin_pixels)
            
            # Calculate color temperature
            temperature = self._calculate_color_temperature(avg_skin_color)
            
            # Get color harmony information
            harmony_info = self._get_color_harmony_info(avg_skin_color)
            
            analysis_result = {
                'category': category,
                'undertone': undertone,
                'lightness': lightness,
                'temperature': temperature,
                'dominant_colors': dominant_colors.tolist(),
                'average_color': avg_skin_color.tolist(),
                'harmony_info': harmony_info,
                'skin_pixel_count': len(skin_pixels),
                'confidence': self._calculate_confidence(skin_mask, image)
            }
            
            return analysis_result
            
        except Exception as e:
            raise ValueError(f"Skin tone analysis failed: {str(e)}")
    
    def _detect_skin_regions(self, image: np.ndarray) -> np.ndarray:
        """Detect skin regions using color-based segmentation."""
        try:
            # Convert to different color spaces for better skin detection
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
            
            # HSV-based skin detection
            lower_hsv = np.array([0, 20, 70], dtype=np.uint8)
            upper_hsv = np.array([20, 255, 255], dtype=np.uint8)
            mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)
            
            # YCrCb-based skin detection
            lower_ycrcb = np.array([0, 135, 85], dtype=np.uint8)
            upper_ycrcb = np.array([255, 180, 135], dtype=np.uint8)
            mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)
            
            # Combine masks
            skin_mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)
            
            # Apply morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
            
            # Apply Gaussian blur to smooth the mask
            skin_mask = cv2.GaussianBlur(skin_mask, (3, 3), 0)
            
            return skin_mask
            
        except Exception as e:
            raise ValueError(f"Skin detection failed: {str(e)}")
    
    def _get_dominant_colors(self, pixels: np.ndarray, n_colors: int = 5) -> np.ndarray:
        """Extract dominant colors using K-means clustering."""
        try:
            # Reshape pixels for clustering
            pixels_reshaped = pixels.reshape(-1, 3)
            
            # Apply K-means clustering
            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels_reshaped)
            
            # Get cluster centers (dominant colors)
            dominant_colors = kmeans.cluster_centers_
            
            # Sort by cluster size (most dominant first)
            labels = kmeans.labels_
            label_counts = np.bincount(labels)
            sorted_indices = np.argsort(label_counts)[::-1]
            
            dominant_colors = dominant_colors[sorted_indices]
            
            return dominant_colors.astype(np.uint8)
            
        except Exception as e:
            raise ValueError(f"Dominant color extraction failed: {str(e)}")
    
    def _calculate_lightness(self, rgb_color: np.ndarray) -> float:
        """Calculate lightness value (0-100) from RGB color."""
        try:
            # Convert RGB to LAB color space
            rgb_normalized = rgb_color.reshape(1, 1, 3) / 255.0
            lab = color.rgb2lab(rgb_normalized)
            
            # L* component represents lightness (0-100)
            lightness = lab[0, 0, 0]
            
            return max(0, min(100, lightness))
            
        except Exception as e:
            # Fallback to simple brightness calculation
            return np.mean(rgb_color) / 255.0 * 100
    
    def _classify_skin_tone_category(self, lightness: float) -> str:
        """Classify skin tone category based on lightness."""
        for category, info in self.skin_tone_categories.items():
            min_val, max_val = info['range']
            if min_val <= lightness < max_val:
                return info['name']
        
        # Fallback
        if lightness < 25:
            return 'Very Light'
        elif lightness >= 85:
            return 'Dark'
        else:
            return 'Medium'
    
    def _determine_undertone(self, avg_color: np.ndarray, skin_pixels: np.ndarray) -> str:
        """Determine skin undertone (cool, warm, or neutral)."""
        try:
            # Convert to different color spaces for undertone analysis
            rgb_normalized = avg_color / 255.0
            
            # Calculate color ratios
            red_ratio = rgb_normalized[0]
            green_ratio = rgb_normalized[1]
            blue_ratio = rgb_normalized[2]
            
            # Analyze undertone based on color balance
            red_blue_diff = red_ratio - blue_ratio
            
            if red_blue_diff > 0.05:  # More red than blue
                return 'Warm'
            elif red_blue_diff < -0.05:  # More blue than red
                return 'Cool'
            else:
                return 'Neutral'
                
        except Exception:
            return 'Neutral'
    
    def _calculate_color_temperature(self, rgb_color: np.ndarray) -> str:
        """Calculate color temperature classification."""
        try:
            r, g, b = rgb_color / 255.0
            
            # Simple color temperature estimation
            if r > b:
                if (r - b) > 0.1:
                    return 'Warm'
                else:
                    return 'Neutral-Warm'
            elif b > r:
                if (b - r) > 0.1:
                    return 'Cool'
                else:
                    return 'Neutral-Cool'
            else:
                return 'Neutral'
                
        except Exception:
            return 'Neutral'
    
    def _get_color_harmony_info(self, rgb_color: np.ndarray) -> Dict[str, Any]:
        """Get color harmony information for the skin tone."""
        try:
            # Convert to HSV for easier color harmony calculations
            rgb_normalized = rgb_color.reshape(1, 1, 3) / 255.0
            hsv = color.rgb2hsv(rgb_normalized)[0, 0]
            
            hue, saturation, value = hsv
            hue_degrees = hue * 360
            
            # Calculate complementary colors
            complementary_hue = (hue_degrees + 180) % 360
            
            # Calculate triadic colors
            triadic_hue1 = (hue_degrees + 120) % 360
            triadic_hue2 = (hue_degrees + 240) % 360
            
            # Calculate analogous colors
            analogous_hue1 = (hue_degrees + 30) % 360
            analogous_hue2 = (hue_degrees - 30) % 360
            
            harmony_info = {
                'base_hue': hue_degrees,
                'complementary': complementary_hue,
                'triadic': [triadic_hue1, triadic_hue2],
                'analogous': [analogous_hue1, analogous_hue2],
                'saturation': saturation,
                'value': value
            }
            
            return harmony_info
            
        except Exception:
            return {'base_hue': 0, 'complementary': 180, 'triadic': [120, 240], 'analogous': [30, 330]}
    
    def _calculate_confidence(self, skin_mask: np.ndarray, image: np.ndarray) -> float:
        """Calculate confidence score for the skin tone analysis."""
        try:
            total_pixels = image.shape[0] * image.shape[1]
            skin_pixels = np.sum(skin_mask > 0)
            
            # Base confidence on the proportion of detected skin
            skin_ratio = skin_pixels / total_pixels
            
            # Confidence is higher when we detect a reasonable amount of skin
            if skin_ratio < 0.05:  # Less than 5% skin
                confidence = 0.3
            elif skin_ratio < 0.15:  # 5-15% skin
                confidence = 0.6
            elif skin_ratio < 0.4:  # 15-40% skin
                confidence = 0.9
            else:  # More than 40% skin
                confidence = 0.8  # Might be too much, could include non-skin
            
            return min(1.0, max(0.0, confidence))
            
        except Exception:
            return 0.5
    
    def get_seasonal_color_palette(self, skin_analysis: Dict[str, Any]) -> str:
        """Determine seasonal color palette based on skin tone analysis."""
        try:
            lightness = skin_analysis['lightness']
            undertone = skin_analysis['undertone']
            
            # Seasonal color analysis
            if undertone == 'Cool':
                if lightness > 60:
                    return 'Summer'  # Cool and light
                else:
                    return 'Winter'  # Cool and dark
            elif undertone == 'Warm':
                if lightness > 60:
                    return 'Spring'  # Warm and light
                else:
                    return 'Autumn'  # Warm and dark
            else:  # Neutral
                if lightness > 60:
                    return 'Light Summer'  # Neutral and light
                else:
                    return 'Deep Autumn'  # Neutral and dark
                    
        except Exception:
            return 'Universal'