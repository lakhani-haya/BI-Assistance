"""
Simpllauncher for the BI Assistant dashboard
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit dashboard"""
    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Launch Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error launching application: {e}")

if __name__ == "__main__":
    main()
