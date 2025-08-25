"""
 script to test the Streamlit dashboard locally
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path


def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'matplotlib',
        'seaborn',
        'numpy',
        'openai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("All required packages are installed")
    return True


def start_dashboard():
    """Start the Streamlit dashboard"""
    print("Starting BI Assistant Dashboard...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Get the project root directory
    project_root = Path(__file__).parent
    app_path = project_root / "app.py"
    
    if not app_path.exists():
        print(f"app.py not found at {app_path}")
        return
    
    # Start Streamlit
    try:
        print("Starting Streamlit server...")
        print("Dashboard will open in your default browser")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)]
        subprocess.run(cmd, cwd=project_root)
        
    except KeyboardInterrupt:
        print("\n\n Dashboard stopped by user")
    except Exception as e:
        print(f"Error starting dashboard: {e}")


def create_sample_env():
    """Create a sample .env file if it doesn't exist"""
    project_root = Path(__file__).parent
    env_path = project_root / ".env"
    
    if not env_path.exists():
        print("📝 Creating sample .env file...")
        
        env_content = """# BI Assistant Configuration
# Copy this file and add your actual API key

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Data Processing Settings
MAX_FILE_SIZE_MB=50
DEFAULT_ENCODING=utf-8
ENABLE_CACHING=true

# Visualization Settings
DEFAULT_CHART_THEME=business
ENABLE_PLOTLY_EXPORT=true

# Application Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
"""
        
        try:
            with open(env_path, 'w') as f:
                f.write(env_content)
            print(f"✅ Created {env_path}")
            print("💡 Edit this file to add your OpenAI API key for AI features")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")


def main():
    """Main function"""
    print("🤖📊 BI Assistant Dashboard Launcher")
    print("=" * 50)
    
    # Create sample .env if needed
    create_sample_env()
    
    # Start dashboard
    start_dashboard()


if __name__ == "__main__":
    main()
