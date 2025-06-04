"""Color recommendation service based on skin tone analysis."""

import numpy as np
from typing import Dict, List, Any, Tuple
import colorsys


class ColorRecommendationService:
    """Provides personalized color recommendations based on skin tone analysis."""
    
    def __init__(self):
        # Define color palettes for different skin tone categories and undertones
        self.color_palettes = {
            'very_light': {
                'cool': {
                    'best': ['#E6F3FF', '#B3D9FF', '#80BFFF', '#4D9FFF', '#1A7FFF', '#0066E6', '#004DB3', '#003380'],
                    'avoid': ['#FF6B35', '#FF8C42', '#FFA500', '#FFD700', '#FFFF00', '#ADFF2F', '#32CD32']
                },
                'warm': {
                    'best': ['#FFF8E1', '#FFECB3', '#FFE082', '#FFD54F', '#FFCA28', '#FFC107', '#FFB300', '#FFA000'],
                    'avoid': ['#8A2BE2', '#9932CC', '#BA55D3', '#DA70D6', '#EE82EE', '#DDA0DD', '#D8BFD8']
                },
                'neutral': {
                    'best': ['#F5F5F5', '#E0E0E0', '#BDBDBD', '#9E9E9E', '#757575', '#616161', '#424242', '#212121'],
                    'avoid': ['#FF1493', '#FF69B4', '#FFB6C1', '#FFC0CB', '#FFCCCB', '#F0E68C', '#BDB76B']
                }
            },
            'light': {
                'cool': {
                    'best': ['#E1F5FE', '#B3E5FC', '#81D4FA', '#4FC3F7', '#29B6F6', '#03A9F4', '#039BE5', '#0288D1'],
                    'avoid': ['#FF5722', '#FF7043', '#FF8A65', '#FFAB91', '#FFCCBC', '#FBE9E7', '#EFEBE9']
                },
                'warm': {
                    'best': ['#FFF3E0', '#FFE0B2', '#FFCC80', '#FFB74D', '#FFA726', '#FF9800', '#FB8C00', '#F57C00'],
                    'avoid': ['#3F51B5', '#5C6BC0', '#7986CB', '#9FA8DA', '#C5CAE9', '#E8EAF6', '#F3E5F5']
                },
                'neutral': {
                    'best': ['#FAFAFA', '#F5F5F5', '#EEEEEE', '#E0E0E0', '#BDBDBD', '#9E9E9E', '#757575', '#616161'],
                    'avoid': ['#E91E63', '#F06292', '#F48FB1', '#F8BBD9', '#FCE4EC', '#FFF0F5', '#FFFACD']
                }
            },
            'medium': {
                'cool': {
                    'best': ['#B39DDB', '#9575CD', '#7E57C2', '#673AB7', '#5E35B1', '#512DA8', '#4527A0', '#311B92'],
                    'avoid': ['#FF6F00', '#FF8F00', '#FFA000', '#FFB300', '#FFC107', '#FFD54F', '#FFE082']
                },
                'warm': {
                    'best': ['#FFAB91', '#FF8A65', '#FF7043', '#FF5722', '#F4511E', '#E64A19', '#D84315', '#BF360C'],
                    'avoid': ['#00BCD4', '#26C6DA', '#4DD0E1', '#80DEEA', '#B2EBF2', '#E0F2F1', '#F1F8E9']
                },
                'neutral': {
                    'best': ['#D7CCC8', '#BCAAA4', '#A1887F', '#8D6E63', '#795548', '#6D4C41', '#5D4037', '#4E342E'],
                    'avoid': ['#FF4081', '#FF80AB', '#FFAB91', '#FFCCBC', '#FBE9E7', '#EFEBE9', '#D7CCC8']
                }
            },
            'dark': {
                'cool': {
                    'best': ['#7B1FA2', '#8E24AA', '#9C27B0', '#AB47BC', '#BA68C8', '#CE93D8', '#E1BEE7', '#F3E5F5'],
                    'avoid': ['#FFEB3B', '#FFF176', '#FFF59D', '#FFF9C4', '#FFFDE7', '#F9FBE7', '#F1F8E9']
                },
                'warm': {
                    'best': ['#BF360C', '#D84315', '#E64A19', '#F4511E', '#FF5722', '#FF7043', '#FF8A65', '#FFAB91'],
                    'avoid': ['#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5', '#2196F3', '#1E88E5']
                },
                'neutral': {
                    'best': ['#3E2723', '#4E342E', '#5D4037', '#6D4C41', '#795548', '#8D6E63', '#A1887F', '#BCAAA4'],
                    'avoid': ['#FFCDD2', '#F8BBD9', '#E1BEE7', '#D1C4E9', '#C5CAE9', '#BBDEFB', '#B3E5FC']
                }
            }
        }
        
        # Define outfit combination rules
        self.outfit_combinations = {
            'professional': ['#2C3E50', '#34495E', '#95A5A6', '#BDC3C7'],
            'casual': ['#3498DB', '#E74C3C', '#F39C12', '#27AE60'],
            'formal': ['#000000', '#2C3E50', '#95A5A6', '#FFFFFF'],
            'trendy': ['#E91E63', '#9C27B0', '#673AB7', '#3F51B5']
        }
    
    def get_recommendations(self, skin_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive color recommendations based on skin tone analysis."""
        try:
            # Extract key information from skin analysis
            category = self._normalize_category(skin_analysis.get('category', 'medium'))
            undertone = self._normalize_undertone(skin_analysis.get('undertone', 'neutral'))
            lightness = skin_analysis.get('lightness', 50)
            
            # Get base color palette
            palette = self._get_base_palette(category, undertone)
            
            # Generate specific recommendations
            best_colors = self._generate_best_colors(palette, lightness)
            avoid_colors = self._generate_avoid_colors(palette, lightness)
            
            # Generate outfit combinations
            outfit_combinations = self._generate_outfit_combinations(best_colors, category, undertone)
            
            # Generate seasonal recommendations
            seasonal_colors = self._get_seasonal_recommendations(skin_analysis)
            
            # Generate makeup color suggestions
            makeup_colors = self._generate_makeup_recommendations(skin_analysis)
            
            # Generate hair color suggestions
            hair_colors = self._generate_hair_color_recommendations(skin_analysis)
            
            recommendations = {
                'best_colors': best_colors,
                'avoid_colors': avoid_colors,
                'outfit_combinations': outfit_combinations,
                'seasonal_colors': seasonal_colors,
                'makeup_colors': makeup_colors,
                'hair_colors': hair_colors,
                'color_theory': self._get_color_theory_explanation(undertone),
                'styling_tips': self._get_styling_tips(category, undertone)
            }
            
            return recommendations
            
        except Exception as e:
            raise ValueError(f"Color recommendation generation failed: {str(e)}")
    
    def _normalize_category(self, category: str) -> str:
        """Normalize skin tone category to match palette keys."""
        category_lower = category.lower().replace(' ', '_')
        
        if 'very_light' in category_lower or 'very light' in category_lower:
            return 'very_light'
        elif 'light' in category_lower and 'medium' not in category_lower:
            return 'light'
        elif 'dark' in category_lower and 'medium' not in category_lower:
            return 'dark'
        else:
            return 'medium'
    
    def _normalize_undertone(self, undertone: str) -> str:
        """Normalize undertone to match palette keys."""
        undertone_lower = undertone.lower()
        
        if 'cool' in undertone_lower:
            return 'cool'
        elif 'warm' in undertone_lower:
            return 'warm'
        else:
            return 'neutral'
    
    def _get_base_palette(self, category: str, undertone: str) -> Dict[str, List[str]]:
        """Get base color palette for the given category and undertone."""
        try:
            return self.color_palettes[category][undertone]
        except KeyError:
            # Fallback to medium neutral if specific combination not found
            return self.color_palettes['medium']['neutral']
    
    def _generate_best_colors(self, palette: Dict[str, List[str]], lightness: float) -> List[Dict[str, str]]:
        """Generate list of best colors with names and hex codes."""
        best_colors = []
        color_names = [
            'Navy Blue', 'Royal Blue', 'Sky Blue', 'Powder Blue',
            'Forest Green', 'Emerald', 'Sage Green', 'Mint Green',
            'Burgundy', 'Crimson', 'Rose', 'Blush Pink',
            'Charcoal', 'Slate Gray', 'Silver', 'Pearl White'
        ]
        
        for i, color_hex in enumerate(palette['best'][:8]):
            best_colors.append({
                'hex': color_hex,
                'name': color_names[i % len(color_names)],
                'category': 'best'
            })
        
        return best_colors
    
    def _generate_avoid_colors(self, palette: Dict[str, List[str]], lightness: float) -> List[Dict[str, str]]:
        """Generate list of colors to avoid with names and hex codes."""
        avoid_colors = []
        avoid_names = [
            'Bright Orange', 'Neon Yellow', 'Hot Pink', 'Electric Blue',
            'Lime Green', 'Purple', 'Magenta', 'Coral'
        ]
        
        for i, color_hex in enumerate(palette['avoid'][:8]):
            avoid_colors.append({
                'hex': color_hex,
                'name': avoid_names[i % len(avoid_names)],
                'category': 'avoid'
            })
        
        return avoid_colors
    
    def _generate_outfit_combinations(self, best_colors: List[Dict[str, str]], 
                                    category: str, undertone: str) -> List[List[str]]:
        """Generate outfit color combinations."""
        combinations = []
        
        # Professional combination
        if len(best_colors) >= 4:
            combinations.append([
                best_colors[0]['hex'],  # Dark base
                best_colors[1]['hex'],  # Medium accent
                best_colors[2]['hex'],  # Light accent
                '#FFFFFF'               # White
            ])
        
        # Casual combination
        if len(best_colors) >= 6:
            combinations.append([
                best_colors[2]['hex'],  # Medium base
                best_colors[4]['hex'],  # Accent 1
                best_colors[5]['hex'],  # Accent 2
                '#F5F5F5'               # Light neutral
            ])
        
        # Formal combination
        if len(best_colors) >= 3:
            combinations.append([
                '#000000',              # Black
                best_colors[0]['hex'],  # Dark accent
                best_colors[1]['hex'],  # Medium accent
                '#FFFFFF'               # White
            ])
        
        return combinations
    
    def _get_seasonal_recommendations(self, skin_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """Get seasonal color recommendations."""
        undertone = self._normalize_undertone(skin_analysis.get('undertone', 'neutral'))
        lightness = skin_analysis.get('lightness', 50)
        
        if undertone == 'cool':
            if lightness > 60:
                season = 'Summer'
                colors = ['#E6F3FF', '#B3D9FF', '#80BFFF', '#4D9FFF', '#E1BEE7', '#CE93D8']
            else:
                season = 'Winter'
                colors = ['#000000', '#FFFFFF', '#FF0000', '#0000FF', '#800080', '#008000']
        elif undertone == 'warm':
            if lightness > 60:
                season = 'Spring'
                colors = ['#FFE082', '#FFD54F', '#FFCA28', '#FFC107', '#FF8A65', '#FF7043']
            else:
                season = 'Autumn'
                colors = ['#8D6E63', '#795548', '#6D4C41', '#5D4037', '#FF5722', '#E64A19']
        else:
            season = 'Universal'
            colors = ['#9E9E9E', '#757575', '#616161', '#424242', '#BDBDBD', '#E0E0E0']
        
        return {
            'season': season,
            'colors': colors,
            'description': f'Your {season} palette complements your {undertone} undertone perfectly.'
        }
    
    def _generate_makeup_recommendations(self, skin_analysis: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Generate makeup color recommendations."""
        undertone = self._normalize_undertone(skin_analysis.get('undertone', 'neutral'))
        lightness = skin_analysis.get('lightness', 50)
        
        makeup_colors = {
            'lipstick': [],
            'eyeshadow': [],
            'blush': []
        }
        
        if undertone == 'cool':
            makeup_colors['lipstick'] = [
                {'hex': '#DC143C', 'name': 'Cherry Red'},
                {'hex': '#C71585', 'name': 'Deep Pink'},
                {'hex': '#8B008B', 'name': 'Berry'}
            ]
            makeup_colors['eyeshadow'] = [
                {'hex': '#4B0082', 'name': 'Indigo'},
                {'hex': '#483D8B', 'name': 'Slate Blue'},
                {'hex': '#708090', 'name': 'Slate Gray'}
            ]
            makeup_colors['blush'] = [
                {'hex': '#FFB6C1', 'name': 'Light Pink'},
                {'hex': '#FF69B4', 'name': 'Hot Pink'}
            ]
        elif undertone == 'warm':
            makeup_colors['lipstick'] = [
                {'hex': '#FF6347', 'name': 'Coral'},
                {'hex': '#FF4500', 'name': 'Orange Red'},
                {'hex': '#CD853F', 'name': 'Nude Brown'}
            ]
            makeup_colors['eyeshadow'] = [
                {'hex': '#D2691E', 'name': 'Chocolate'},
                {'hex': '#CD853F', 'name': 'Peru'},
                {'hex': '#F4A460', 'name': 'Sandy Brown'}
            ]
            makeup_colors['blush'] = [
                {'hex': '#FFA07A', 'name': 'Light Salmon'},
                {'hex': '#FA8072', 'name': 'Salmon'}
            ]
        else:  # neutral
            makeup_colors['lipstick'] = [
                {'hex': '#B22222', 'name': 'Fire Brick'},
                {'hex': '#A0522D', 'name': 'Sienna'},
                {'hex': '#CD5C5C', 'name': 'Indian Red'}
            ]
            makeup_colors['eyeshadow'] = [
                {'hex': '#696969', 'name': 'Dim Gray'},
                {'hex': '#A0522D', 'name': 'Sienna'},
                {'hex': '#D2B48C', 'name': 'Tan'}
            ]
            makeup_colors['blush'] = [
                {'hex': '#F0E68C', 'name': 'Khaki'},
                {'hex': '#DDA0DD', 'name': 'Plum'}
            ]
        
        return makeup_colors
    
    def _generate_hair_color_recommendations(self, skin_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate hair color recommendations."""
        undertone = self._normalize_undertone(skin_analysis.get('undertone', 'neutral'))
        lightness = skin_analysis.get('lightness', 50)
        
        hair_colors = []
        
        if undertone == 'cool':
            hair_colors = [
                {'hex': '#2F1B14', 'name': 'Ash Brown'},
                {'hex': '#4A4A4A', 'name': 'Ash Blonde'},
                {'hex': '#000000', 'name': 'Jet Black'},
                {'hex': '#8B7355', 'name': 'Ash Light Brown'}
            ]
        elif undertone == 'warm':
            hair_colors = [
                {'hex': '#8B4513', 'name': 'Chestnut Brown'},
                {'hex': '#DAA520', 'name': 'Golden Blonde'},
                {'hex': '#A0522D', 'name': 'Auburn'},
                {'hex': '#CD853F', 'name': 'Honey Blonde'}
            ]
        else:  # neutral
            hair_colors = [
                {'hex': '#654321', 'name': 'Medium Brown'},
                {'hex': '#8B7D6B', 'name': 'Light Brown'},
                {'hex': '#2F1B14', 'name': 'Dark Brown'},
                {'hex': '#F5DEB3', 'name': 'Wheat Blonde'}
            ]
        
        return hair_colors
    
    def _get_color_theory_explanation(self, undertone: str) -> Dict[str, str]:
        """Get color theory explanation for the undertone."""
        explanations = {
            'cool': {
                'theory': 'Cool undertones have blue, pink, or purple hues in the skin.',
                'best_colors': 'Colors with blue or purple bases complement cool undertones.',
                'avoid_colors': 'Warm colors with yellow or orange bases can clash with cool undertones.'
            },
            'warm': {
                'theory': 'Warm undertones have yellow, peach, or golden hues in the skin.',
                'best_colors': 'Colors with yellow or red bases enhance warm undertones.',
                'avoid_colors': 'Cool colors with blue bases can make warm undertones appear sallow.'
            },
            'neutral': {
                'theory': 'Neutral undertones have a balanced mix of warm and cool hues.',
                'best_colors': 'Most colors work well, with slight preference for balanced tones.',
                'avoid_colors': 'Extremely warm or cool colors may not be as flattering.'
            }
        }
        
        return explanations.get(undertone, explanations['neutral'])
    
    def _get_styling_tips(self, category: str, undertone: str) -> List[str]:
        """Get styling tips based on skin tone category and undertone."""
        tips = [
            f"Your {category} skin tone with {undertone} undertones works best with specific color families.",
            "When in doubt, choose colors that complement your undertone rather than your skin depth.",
            "Test colors near your face in natural lighting to see how they interact with your skin.",
            "Consider the occasion - professional settings may call for more muted tones.",
            "Don't be afraid to experiment with different shades within your recommended color family."
        ]
        
        if undertone == 'cool':
            tips.extend([
                "Silver jewelry typically complements cool undertones better than gold.",
                "Look for colors described as 'icy', 'ash', or 'platinum'.",
                "Blue-based reds and pinks are particularly flattering."
            ])
        elif undertone == 'warm':
            tips.extend([
                "Gold jewelry typically complements warm undertones better than silver.",
                "Look for colors described as 'golden', 'honey', or 'caramel'.",
                "Orange-based reds and corals are particularly flattering."
            ])
        else:  # neutral
            tips.extend([
                "Both gold and silver jewelry can work well with neutral undertones.",
                "You have the flexibility to wear both warm and cool colors.",
                "Focus on colors that enhance your natural skin depth."
            ])
        
        return tips