"""
Streamlit App Entry Point
Main entry 
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.dashboard import main

if __name__ == "__main__":
    main()
