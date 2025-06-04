"""Main application UI and page definitions."""

import asyncio
import os
import tempfile
from typing import Optional, Dict, Any
from pathlib import Path

from nicegui import ui, app, events
import numpy as np
from PIL import Image

from app.config import settings
from core.image_processor import ImageProcessor
from core.color_analyzer import ColorAnalyzer
from core.skin_tone_modifier import SkinToneModifier
from services.color_recommendations import ColorRecommendationService


class SkinToneAnalyzerApp:
    """Main application class for the Skin Tone Color Analyzer."""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.color_analyzer = ColorAnalyzer()
        self.skin_tone_modifier = SkinToneModifier()
        self.recommendation_service = ColorRecommendationService()
        
        # Application state
        self.current_image: Optional[np.ndarray] = None
        self.original_image: Optional[np.ndarray] = None
        self.current_image_path: Optional[str] = None
        self.skin_tone_analysis: Optional[Dict[str, Any]] = None
        self.color_recommendations: Optional[Dict[str, Any]] = None
        
        # UI components
        self.image_display = None
        self.analysis_container = None
        self.recommendations_container = None
        self.skin_tone_controls = None

    async def handle_image_upload(self, e: events.UploadEventArguments) -> None:
        """Handle image upload and initial processing."""
        try:
            # Validate file
            if not self.image_processor.validate_upload(e.content, e.name):
                ui.notify("Invalid image file. Please upload JPG, PNG, or WebP.", type="negative")
                return
            
            # Save uploaded file
            temp_path = os.path.join(settings.temp_dir, f"upload_{e.name}")
            with open(temp_path, "wb") as f:
                f.write(e.content.read())
            
            # Process image
            self.original_image = self.image_processor.load_image(temp_path)
            self.current_image = self.original_image.copy()
            self.current_image_path = temp_path
            
            # Analyze skin tone
            await self.analyze_skin_tone()
            
            # Update UI
            await self.update_image_display()
            await self.update_analysis_display()
            await self.generate_recommendations()
            
            ui.notify("Image uploaded and analyzed successfully!", type="positive")
            
        except Exception as e:
            ui.notify(f"Error processing image: {str(e)}", type="negative")

    async def analyze_skin_tone(self) -> None:
        """Analyze skin tone from the current image."""
        if self.current_image is None:
            return
        
        try:
            self.skin_tone_analysis = await asyncio.to_thread(
                self.color_analyzer.analyze_skin_tone, self.current_image
            )
        except Exception as e:
            ui.notify(f"Error analyzing skin tone: {str(e)}", type="negative")

    async def update_image_display(self) -> None:
        """Update the image display with the current image."""
        if self.current_image is None or self.image_display is None:
            return
        
        try:
            # Save current image to temporary file for display
            temp_display_path = os.path.join(settings.temp_dir, "current_display.jpg")
            display_image = Image.fromarray(self.current_image)
            display_image.save(temp_display_path, "JPEG", quality=85)
            
            # Update image source
            self.image_display.set_source(temp_display_path)
            
        except Exception as e:
            ui.notify(f"Error updating image display: {str(e)}", type="negative")

    async def update_analysis_display(self) -> None:
        """Update the skin tone analysis display."""
        if self.analysis_container is None or self.skin_tone_analysis is None:
            return
        
        self.analysis_container.clear()
        
        with self.analysis_container:
            ui.label("Skin Tone Analysis").classes("text-h6 text-primary mb-4")
            
            analysis = self.skin_tone_analysis
            
            with ui.card().classes("w-full"):
                with ui.card_section():
                    ui.label(f"Skin Tone Category: {analysis['category']}").classes("text-subtitle1 font-medium")
                    ui.label(f"Undertone: {analysis['undertone']}").classes("text-body1")
                    ui.label(f"Lightness Level: {analysis['lightness']:.1f}%").classes("text-body1")
                
                with ui.card_section():
                    ui.label("Dominant Colors:").classes("text-subtitle2 mb-2")
                    with ui.row().classes("gap-2"):
                        for color in analysis['dominant_colors'][:5]:
                            color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                            ui.html(f'<div style="width: 40px; height: 40px; background-color: {color_hex}; border: 1px solid #ccc; border-radius: 4px;"></div>')

    async def generate_recommendations(self) -> None:
        """Generate color recommendations based on skin tone analysis."""
        if self.skin_tone_analysis is None or self.recommendations_container is None:
            return
        
        try:
            self.color_recommendations = await asyncio.to_thread(
                self.recommendation_service.get_recommendations, self.skin_tone_analysis
            )
            
            await self.update_recommendations_display()
            
        except Exception as e:
            ui.notify(f"Error generating recommendations: {str(e)}", type="negative")

    async def update_recommendations_display(self) -> None:
        """Update the color recommendations display."""
        if self.recommendations_container is None or self.color_recommendations is None:
            return
        
        self.recommendations_container.clear()
        
        with self.recommendations_container:
            ui.label("Color Recommendations").classes("text-h6 text-primary mb-4")
            
            recommendations = self.color_recommendations
            
            # Best colors
            with ui.card().classes("w-full mb-4"):
                with ui.card_section():
                    ui.label("Best Colors for You").classes("text-subtitle1 font-medium mb-2")
                    with ui.grid(columns=6).classes("gap-2"):
                        for color_info in recommendations['best_colors']:
                            color_hex = color_info['hex']
                            with ui.column().classes("items-center"):
                                ui.html(f'<div style="width: 50px; height: 50px; background-color: {color_hex}; border: 1px solid #ccc; border-radius: 8px;"></div>')
                                ui.label(color_info['name']).classes("text-caption text-center")
            
            # Colors to avoid
            with ui.card().classes("w-full mb-4"):
                with ui.card_section():
                    ui.label("Colors to Avoid").classes("text-subtitle1 font-medium mb-2")
                    with ui.grid(columns=6).classes("gap-2"):
                        for color_info in recommendations['avoid_colors']:
                            color_hex = color_info['hex']
                            with ui.column().classes("items-center"):
                                ui.html(f'<div style="width: 50px; height: 50px; background-color: {color_hex}; border: 1px solid #ccc; border-radius: 8px; opacity: 0.6;"></div>')
                                ui.label(color_info['name']).classes("text-caption text-center")
            
            # Outfit combinations
            with ui.card().classes("w-full"):
                with ui.card_section():
                    ui.label("Suggested Outfit Combinations").classes("text-subtitle1 font-medium mb-2")
                    for i, combo in enumerate(recommendations['outfit_combinations'][:3]):
                        with ui.row().classes("items-center gap-4 mb-2"):
                            ui.label(f"Combo {i+1}:").classes("font-medium")
                            for color_hex in combo:
                                ui.html(f'<div style="width: 30px; height: 30px; background-color: {color_hex}; border: 1px solid #ccc; border-radius: 4px;"></div>')

    async def adjust_skin_tone(self, adjustment_type: str, value: float) -> None:
        """Adjust skin tone based on user input."""
        if self.original_image is None:
            return
        
        try:
            if adjustment_type == "lightness":
                self.current_image = await asyncio.to_thread(
                    self.skin_tone_modifier.adjust_lightness, self.original_image, value
                )
            elif adjustment_type == "warmth":
                self.current_image = await asyncio.to_thread(
                    self.skin_tone_modifier.adjust_warmth, self.original_image, value
                )
            elif adjustment_type == "saturation":
                self.current_image = await asyncio.to_thread(
                    self.skin_tone_modifier.adjust_saturation, self.original_image, value
                )
            
            # Re-analyze with modified image
            await self.analyze_skin_tone()
            await self.update_image_display()
            await self.update_analysis_display()
            await self.generate_recommendations()
            
        except Exception as e:
            ui.notify(f"Error adjusting skin tone: {str(e)}", type="negative")

    async def reset_image(self) -> None:
        """Reset image to original state."""
        if self.original_image is None:
            return
        
        self.current_image = self.original_image.copy()
        await self.analyze_skin_tone()
        await self.update_image_display()
        await self.update_analysis_display()
        await self.generate_recommendations()
        
        ui.notify("Image reset to original", type="info")

    def create_ui(self) -> None:
        """Create the main user interface."""
        # Header
        with ui.header().classes("bg-primary text-white"):
            with ui.row().classes("w-full items-center"):
                ui.label("🎨 Skin Tone Color Analyzer").classes("text-h5 font-bold")
                ui.space()
                ui.label("Discover Your Perfect Colors").classes("text-subtitle1")

        # Main content
        with ui.column().classes("w-full max-w-6xl mx-auto p-4 gap-6"):
            
            # Upload section
            with ui.card().classes("w-full"):
                with ui.card_section():
                    ui.label("Upload Your Photo").classes("text-h6 mb-4")
                    ui.label("Upload a clear photo of yourself to get personalized color recommendations").classes("text-body2 mb-4")
                    
                    ui.upload(
                        on_upload=self.handle_image_upload,
                        max_file_size=settings.max_image_size,
                        max_files=1
                    ).classes("w-full").props("accept=image/*")

            # Main content area
            with ui.row().classes("w-full gap-6"):
                
                # Left column - Image and controls
                with ui.column().classes("flex-1"):
                    
                    # Image display
                    with ui.card().classes("w-full"):
                        with ui.card_section():
                            ui.label("Your Photo").classes("text-h6 mb-4")
                            self.image_display = ui.image().classes("w-full max-w-md mx-auto rounded-lg")
                    
                    # Skin tone adjustment controls
                    with ui.card().classes("w-full"):
                        with ui.card_section():
                            ui.label("Adjust Skin Tone").classes("text-h6 mb-4")
                            
                            ui.label("Lightness").classes("text-subtitle2 mb-2")
                            lightness_slider = ui.slider(
                                min=-50, max=50, value=0, step=1
                            ).classes("w-full mb-4")
                            lightness_slider.on_value_change(
                                lambda e: asyncio.create_task(self.adjust_skin_tone("lightness", e.value))
                            )
                            
                            ui.label("Warmth").classes("text-subtitle2 mb-2")
                            warmth_slider = ui.slider(
                                min=-50, max=50, value=0, step=1
                            ).classes("w-full mb-4")
                            warmth_slider.on_value_change(
                                lambda e: asyncio.create_task(self.adjust_skin_tone("warmth", e.value))
                            )
                            
                            ui.label("Saturation").classes("text-subtitle2 mb-2")
                            saturation_slider = ui.slider(
                                min=-50, max=50, value=0, step=1
                            ).classes("w-full mb-4")
                            saturation_slider.on_value_change(
                                lambda e: asyncio.create_task(self.adjust_skin_tone("saturation", e.value))
                            )
                            
                            ui.button("Reset to Original", on_click=self.reset_image).classes("w-full")

                # Right column - Analysis and recommendations
                with ui.column().classes("flex-1"):
                    
                    # Analysis results
                    self.analysis_container = ui.column().classes("w-full")
                    
                    # Color recommendations
                    self.recommendations_container = ui.column().classes("w-full")

        # Footer
        if settings.show_footer:
            with ui.footer().classes("bg-grey-8 text-white"):
                with ui.row().classes("w-full items-center justify-center"):
                    ui.label(f"{settings.app_name} v{settings.app_version}").classes("text-caption")


# Global app instance
skin_tone_app = SkinToneAnalyzerApp()


@ui.page("/")
async def index():
    """Main page route."""
    skin_tone_app.create_ui()


@ui.page("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.app_name, "version": settings.app_version}


def main():
    """Main application entry point."""
    # Add custom CSS
    ui.add_head_html("""
    <style>
        .q-page-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .q-card {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .text-primary {
            color: #6b46c1 !important;
        }
        .bg-primary {
            background-color: #6b46c1 !important;
        }
    </style>
    """)
    
    # Configure and run the application
    ui.run(
        host=settings.host,
        port=settings.port,
        title=settings.app_name,
        favicon="🎨",
        dark=False,
        show=settings.debug,
        reload=settings.debug
    )


if __name__ == "__main__":
    main()