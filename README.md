# 🎨 Skin Tone Color Analyzer

A sophisticated AI-powered application that analyzes skin tones from uploaded photos and provides personalized color recommendations for clothing, makeup, and styling.

## ✨ Features

- **Smart Skin Tone Analysis**: Advanced computer vision algorithms detect and analyze skin tones
- **Personalized Color Recommendations**: Get custom color palettes based on your unique skin tone
- **Real-time Skin Tone Adjustment**: Interactive sliders to modify lightness, warmth, and saturation
- **Comprehensive Styling Guide**: Outfit combinations, makeup colors, and hair color suggestions
- **Professional Color Theory**: Based on established color analysis principles
- **Mobile-Friendly Interface**: Responsive design that works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd skin-tone-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8000`

## 🖼️ How to Use

1. **Upload Your Photo**: Click the upload area and select a clear photo of yourself
2. **View Analysis**: The app will automatically analyze your skin tone and display results
3. **Explore Recommendations**: Browse personalized color palettes and styling suggestions
4. **Adjust Skin Tone**: Use the interactive sliders to see how different adjustments affect your color recommendations
5. **Save Your Results**: Take screenshots or notes of your personalized color palette

## 🎯 Key Features Explained

### Skin Tone Analysis
- **Category Classification**: Very Light, Light, Medium, Dark
- **Undertone Detection**: Cool, Warm, or Neutral
- **Lightness Measurement**: Precise percentage-based assessment
- **Confidence Scoring**: Reliability indicator for analysis results

### Color Recommendations
- **Best Colors**: Curated palette of most flattering colors
- **Colors to Avoid**: Shades that may not complement your skin tone
- **Outfit Combinations**: Professional, casual, and formal color schemes
- **Seasonal Analysis**: Spring, Summer, Autumn, or Winter color palette

### Advanced Features
- **Makeup Color Suggestions**: Lipstick, eyeshadow, and blush recommendations
- **Hair Color Ideas**: Complementary hair colors for your skin tone
- **Color Theory Explanations**: Educational content about why certain colors work
- **Styling Tips**: Professional advice for making the most of your colors

## 🛠️ Technology Stack

- **Backend**: Python with NiceGUI framework
- **Computer Vision**: OpenCV, scikit-image
- **Image Processing**: Pillow (PIL), NumPy
- **Color Analysis**: Custom algorithms based on color theory
- **UI Framework**: NiceGUI with custom CSS
- **Deployment**: Docker, Fly.io ready

## 📁 Project Structure

```
skin-tone-analyzer/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── dockerfile             # Container configuration
├── fly.toml               # Deployment configuration
├── app/
│   ├── main.py            # Main UI and page definitions
│   └── config.py          # Application configuration
├── core/
│   ├── image_processor.py # Image loading and processing
│   ├── color_analyzer.py  # Skin tone analysis algorithms
│   └── skin_tone_modifier.py # Image adjustment utilities
├── services/
│   └── color_recommendations.py # Color recommendation engine
├── models/
│   └── schemas.py         # Data validation models
└── static/
    └── css/
        └── styles.css     # Custom styling
```

## 🔧 Configuration

The application can be configured through environment variables or the `.env` file:

```env
APP_NAME=Skin Tone Color Analyzer
DEBUG=True
HOST=0.0.0.0
PORT=8000
MAX_IMAGE_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
```

## 🚀 Deployment

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t skin-tone-analyzer .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 skin-tone-analyzer
   ```

### Fly.io Deployment

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy the application**
   ```bash
   fly deploy
   ```

## 🎨 Color Theory Background

This application is based on established color analysis principles:

- **Seasonal Color Analysis**: Categorizes individuals into seasonal types
- **Undertone Theory**: Identifies warm, cool, or neutral undertones
- **Color Harmony**: Uses complementary and analogous color relationships
- **Professional Standards**: Follows industry best practices for color consultation

## 🔒 Privacy & Security

- **Local Processing**: All image analysis happens on the server, not sent to third parties
- **Temporary Storage**: Uploaded images are processed and then deleted
- **No Data Collection**: No personal information is stored or tracked
- **Secure Upload**: File validation and size limits prevent malicious uploads

## 🐛 Troubleshooting

### Common Issues

1. **Image Upload Fails**
   - Check file format (JPG, PNG, WebP only)
   - Ensure file size is under 5MB
   - Try a different image with better lighting

2. **No Skin Detected**
   - Use a clear, well-lit photo
   - Ensure face is visible and unobstructed
   - Try a photo with more skin area visible

3. **Slow Processing**
   - Large images take longer to process
   - Ensure good internet connection
   - Try refreshing the page

### Performance Tips

- Use images with good lighting for better analysis
- Crop images to focus on face/skin areas
- Ensure stable internet connection for uploads

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on the repository.

---

**Made with ❤️ using Python and Computer Vision**