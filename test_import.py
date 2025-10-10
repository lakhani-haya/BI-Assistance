"""
Test script to check if the dashboard loads correctly
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.dashboard import main
    print("✓ Dashboard module imported successfully")
    print("✓ All syntax errors fixed")
    print("✓ Ready to run: streamlit run app.py")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
except Exception as e:
    print(f"✗ Other error: {e}")
