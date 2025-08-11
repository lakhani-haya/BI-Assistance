"""
Configuration settings for BI Assistant
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
    
    # Supported file formats
    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls']
    
    # Data processing settings
    MAX_ROWS_FOR_PREVIEW = 1000
    MAX_UNIQUE_VALUES_FOR_CATEGORICAL = 50
    
    # Visualization settings
    DEFAULT_CHART_WIDTH = 800
    DEFAULT_CHART_HEIGHT = 600
    COLOR_PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # AI Analysis settings
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        
        if cls.MAX_FILE_SIZE_MB <= 0:
            errors.append("MAX_FILE_SIZE_MB must be positive")
        
        return errors
