"""
Configuration Management for Streamlit Dashboard
Handles Streamlit-specific settings and page configurations
"""

import streamlit as st
from typing import Dict, Any, Optional


class StreamlitConfig:
    """Configuration settings for Streamlit dashboard"""
    
    # Page configuration
    PAGE_CONFIG = {
        "page_title": "BI Assistant - Smart Data Analysis",
        "page_icon": "",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    # Theme settings
    THEMES = {
        "business": {
            "primary_color": "#1f77b4",
            "secondary_color": "#ff7f0e",
            "background_color": "#ffffff",
            "text_color": "#262730"
        },
        "executive": {
            "primary_color": "#2e4057",
            "secondary_color": "#048a81",
            "background_color": "#f8f9fa",
            "text_color": "#212529"
        },
        "presentation": {
            "primary_color": "#6c5ce7",
            "secondary_color": "#fd79a8",
            "background_color": "#dfe6e9",
            "text_color": "#2d3436"
        }
    }
    
    # Chart configuration
    CHART_CONFIG = {
        "responsive": True,
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            'pan2d', 'lasso2d', 'select2d', 'autoScale2d', 'hoverClosestCartesian',
            'hoverCompareCartesian', 'toggleSpikelines'
        ]
    }
    
    # Layout settings
    LAYOUT_SETTINGS = {
        "single_column_width": 800,
        "two_column_ratio": [1, 1],
        "three_column_ratio": [1, 1, 1],
        "sidebar_width": 300
    }
    
    # File upload settings
    UPLOAD_SETTINGS = {
        "max_file_size_mb": 200,  # Streamlit default
        "accepted_file_types": ['csv', 'xlsx', 'xls'],
        "encoding_options": ['utf-8', 'latin-1', 'iso-8859-1']
    }
    
    @staticmethod
    def get_custom_css(theme: str = "business") -> str:
        """Get custom CSS for the specified theme"""
        theme_colors = StreamlitConfig.THEMES.get(theme, StreamlitConfig.THEMES["business"])
        
        return f"""
        <style>
            /* Main theme colors */
            :root {{
                --primary-color: {theme_colors['primary_color']};
                --secondary-color: {theme_colors['secondary_color']};
                --background-color: {theme_colors['background_color']};
                --text-color: {theme_colors['text_color']};
            }}
            
            /* Header styles */
            .main-header {{
                font-size: 3rem;
                font-weight: bold;
                color: var(--primary-color);
                text-align: center;
                margin-bottom: 2rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }}
            
            .sub-header {{
                font-size: 1.8rem;
                color: var(--text-color);
                margin: 1.5rem 0;
                border-bottom: 2px solid var(--primary-color);
                padding-bottom: 0.5rem;
            }}
            
            /* Card styles */
            .metric-card {{
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border-left: 4px solid var(--primary-color);
                margin: 1rem 0;
                transition: transform 0.2s ease-in-out;
            }}
            
            .metric-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }}
            
            /* Insight boxes */
            .insight-box {{
                background: linear-gradient(135deg, #f0f2f6 0%, #e3e8f0 100%);
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 4px solid var(--primary-color);
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .insight-box h4 {{
                color: var(--primary-color);
                margin-top: 0;
            }}
            
            /* Status messages */
            .success-message {{
                background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                color: #155724;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #c3e6cb;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .warning-message {{
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                color: #856404;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #ffeaa7;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .error-message {{
                background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
                color: #721c24;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #f5c6cb;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .info-message {{
                background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                color: #0c5460;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #bee5eb;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            /* Sidebar enhancements */
            .sidebar-header {{
                background: var(--primary-color);
                color: white;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1rem;
                text-align: center;
                font-weight: bold;
            }}
            
            /* Button styles */
            .stButton > button {{
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            
            .stButton > button:hover {{
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }}
            
            /* Chart container */
            .chart-container {{
                background: white;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin: 1rem 0;
            }}
            
            /* Data table styling */
            .dataframe {{
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                overflow: hidden;
            }}
            
            /* Progress indicators */
            .progress-text {{
                font-weight: 600;
                color: var(--primary-color);
                margin: 0.5rem 0;
            }}
            
            /* Feature cards */
            .feature-card {{
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin: 1rem 0;
                border-top: 3px solid var(--primary-color);
            }}
            
            .feature-card h4 {{
                color: var(--primary-color);
                margin-top: 0;
            }}
            
            /* Navigation tabs */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                height: 50px;
                background-color: transparent;
                border-radius: 8px 8px 0 0;
                color: var(--text-color);
                font-weight: 600;
            }}
            
            .stTabs [aria-selected="true"] {{
                background-color: var(--primary-color);
                color: white;
            }}
            
            /* Footer */
            .footer {{
                text-align: center;
                padding: 2rem 0;
                color: #666;
                border-top: 1px solid #e0e0e0;
                margin-top: 3rem;
            }}
            
            /* Loading spinner customization */
            .stSpinner > div {{
                border-top-color: var(--primary-color) !important;
            }}
            
            /* Metric styling */
            [data-testid="metric-container"] {{
                background: white;
                border: 1px solid #e0e0e0;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }}
            
            /* Expander styling */
            .streamlit-expanderHeader {{
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }}
            
            /* File uploader */
            .stFileUploader > div {{
                border: 2px dashed var(--primary-color);
                border-radius: 10px;
                padding: 2rem;
                text-align: center;
                background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            }}
            
            /* Selectbox and other inputs */
            .stSelectbox > div > div {{
                border-radius: 8px;
                border: 1px solid #ced4da;
            }}
            
            .stTextInput > div > div {{
                border-radius: 8px;
                border: 1px solid #ced4da;
            }}
            
            /* Hide streamlit style */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
        </style>
        """
    
    @staticmethod
    def apply_page_config():
        """Apply page configuration to Streamlit"""
        st.set_page_config(**StreamlitConfig.PAGE_CONFIG)
    
    @staticmethod
    def apply_theme(theme: str = "business"):
        """Apply theme styling to the page"""
        css = StreamlitConfig.get_custom_css(theme)
        st.markdown(css, unsafe_allow_html=True)
    
    @staticmethod
    def get_chart_config(theme: str = "business") -> Dict[str, Any]:
        """Get chart configuration for Plotly"""
        theme_colors = StreamlitConfig.THEMES.get(theme, StreamlitConfig.THEMES["business"])
        
        config = StreamlitConfig.CHART_CONFIG.copy()
        config.update({
            "toImageButtonOptions": {
                "format": "png",
                "filename": "bi_assistant_chart",
                "height": 600,
                "width": 800,
                "scale": 2
            }
        })
        
        return config
    
    @staticmethod
    def get_plotly_theme(theme: str = "business") -> str:
        """Get Plotly theme name based on app theme"""
        theme_mapping = {
            "business": "plotly",
            "executive": "plotly_white",
            "presentation": "presentation"
        }
        
        return theme_mapping.get(theme, "plotly")


class SessionStateManager:
    """Manages Streamlit session state for the BI Assistant"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all required session state variables"""
        default_values = {
            'data_loaded': False,
            'current_data': None,
            'original_data': None,
            'analysis_results': None,
            'dashboard_results': None,
            'ai_enabled': False,
            'selected_theme': 'business',
            'processing_status': 'idle',
            'error_messages': [],
            'success_messages': [],
            'uploaded_filename': None,
            'analysis_history': [],
            'chart_export_format': 'png',
            'dashboard_layout': 'single_column',
            'show_advanced_options': False,
            'data_preview_rows': 10,
            'auto_refresh': False
        }
        
        for key, default_value in default_values.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def clear_analysis_state():
        """Clear analysis-related session state"""
        analysis_keys = [
            'analysis_results',
            'dashboard_results',
            'processing_status',
            'error_messages',
            'success_messages'
        ]
        
        for key in analysis_keys:
            if key in st.session_state:
                st.session_state[key] = None if key.endswith('_results') else []
    
    @staticmethod
    def add_message(message: str, message_type: str = 'info'):
        """Add a message to the appropriate message list"""
        if message_type == 'error':
            if 'error_messages' not in st.session_state:
                st.session_state.error_messages = []
            st.session_state.error_messages.append(message)
        elif message_type == 'success':
            if 'success_messages' not in st.session_state:
                st.session_state.success_messages = []
            st.session_state.success_messages.append(message)
    
    @staticmethod
    def clear_messages():
        """Clear all messages"""
        st.session_state.error_messages = []
        st.session_state.success_messages = []
    
    @staticmethod
    def update_processing_status(status: str):
        """Update processing status"""
        st.session_state.processing_status = status


class ComponentHelpers:
    """Helper functions for Streamlit components"""
    
    @staticmethod
    def render_status_messages():
        """Render status messages from session state"""
        # Error messages
        if st.session_state.get('error_messages'):
            for error in st.session_state.error_messages:
                st.error(f" {error}")
        
        # Success messages
        if st.session_state.get('success_messages'):
            for success in st.session_state.success_messages:
                st.success(f" {success}")
    
    @staticmethod
    def create_metric_card(title: str, value: str, delta: Optional[str] = None, 
                          help_text: Optional[str] = None):
        """Create a styled metric card"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if delta:
                st.metric(
                    label=title,
                    value=value,
                    delta=delta,
                    help=help_text
                )
            else:
                st.metric(
                    label=title,
                    value=value,
                    help=help_text
                )
    
    @staticmethod
    def create_info_box(content: str, box_type: str = "info", title: Optional[str] = None):
        """Create a styled information box"""
        css_class = f"{box_type}-message"
        
        if title:
            content = f"**{title}**\n\n{content}"
        
        st.markdown(f'<div class="{css_class}">{content}</div>', unsafe_allow_html=True)
    
    @staticmethod
    def create_progress_indicator(progress: float, text: str = ""):
        """Create a progress indicator with text"""
        progress_bar = st.progress(progress)
        if text:
            st.markdown(f'<p class="progress-text">{text}</p>', unsafe_allow_html=True)
        
        return progress_bar
    
    @staticmethod
    def create_feature_grid(features: Dict[str, Dict[str, str]], columns: int = 2):
        """Create a grid of feature cards"""
        feature_list = list(features.items())
        
        for i in range(0, len(feature_list), columns):
            cols = st.columns(columns)
            
            for j, col in enumerate(cols):
                if i + j < len(feature_list):
                    feature_name, feature_info = feature_list[i + j]
                    
                    with col:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h4>{feature_info.get('title', feature_name)}</h4>
                            <p>{feature_info.get('description', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_download_button(data, filename: str, mime_type: str, 
                             button_text: str = "Download"):
        """Create a styled download button"""
        return st.download_button(
            label=f"📥 {button_text}",
            data=data,
            file_name=filename,
            mime=mime_type,
            help=f"Download {filename}"
        )
    
    @staticmethod
    def render_data_quality_badge(score: float):
        """Render a data quality badge based on score"""
        if score >= 80:
            st.success(f"🟢 **Data Quality: {score}/100** - Excellent")
        elif score >= 60:
            st.warning(f"🟡 **Data Quality: {score}/100** - Good")
        else:
            st.error(f"🔴 **Data Quality: {score}/100** - Needs Attention")
    
    @staticmethod
    def create_expandable_section(title: str, content_func, expanded: bool = False, 
                                 help_text: Optional[str] = None):
        """Create an expandable section with custom content"""
        with st.expander(title, expanded=expanded, help=help_text):
            content_func()


# Export commonly used functions
__all__ = [
    'StreamlitConfig',
    'SessionStateManager', 
    'ComponentHelpers'
]
