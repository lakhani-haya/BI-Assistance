"""
Streamlit App Entry Point

"""

import sys
import os

# Add here the src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.dashboard import main

if __name__ == "__main__":
    main()
