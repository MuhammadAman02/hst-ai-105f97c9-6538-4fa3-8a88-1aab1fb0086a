#!/usr/bin/env python3
"""
Skin Tone Color Analysis Application
Entry point for the application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import and run the application
if __name__ == "__main__":
    from app.main import main
    main()