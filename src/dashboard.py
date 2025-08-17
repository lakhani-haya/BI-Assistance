"""
Main Streamlit Dashboard for BI Assistant
Provides user-friendly web interface for data analysis and visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import io
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.intelligent_analyzer import IntelligentDataAnalyzer
from src.intelligent_visualizer import IntelligentVisualizationEngine
from src.config import Config
from src.data_processor import DataProcessor, validate_file_size
from src.streamlit_upload import StreamlitFileUploader
from src.dashboard_builder import InteractiveDashboardBuilder, DashboardTemplate, DashboardTheme
from src.chart_editor import InteractiveChartEditor
from src.dashboard_exporter import DashboardExporter


# Page configuration
st.set_page_config(
    page_title="BI Assistant - Smart Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin: 1rem 0;
    }
    
    .insight-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #ffeaa7;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitDashboard:
    """Main dashboard class for Streamlit interface"""
    
    def __init__(self):
        """Initialize dashboard components"""
        self.initialize_session_state()
        self.file_uploader = StreamlitFileUploader()
        
        # Check configuration
        config_errors = Config.validate_config()
        if config_errors:
            st.warning("⚠️ Configuration Issues Detected:\n" + "\n".join(config_errors))
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        
        if 'current_data' not in st.session_state:
            st.session_state.current_data = None
        
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None
        
        if 'dashboard_results' not in st.session_state:
            st.session_state.dashboard_results = None
        
        if 'ai_enabled' not in st.session_state:
            st.session_state.ai_enabled = bool(Config.OPENAI_API_KEY and 
                                             Config.OPENAI_API_KEY != "your_openai_api_key_here")
    
    def render_header(self):
        """Render the main header"""
        st.markdown('<h1 class="main-header">🤖📊 BI Assistant</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Smart Business Intelligence with AI-Powered Insights</p>', unsafe_allow_html=True)
        
        # Display AI status
        if st.session_state.ai_enabled:
            st.success("🧠 AI Features Enabled - Full analytics available")
        else:
            st.info("📊 Basic Mode - Upload .env with OpenAI API key for AI features")
    
    def render_sidebar(self):
        """Render the sidebar with controls and options"""
        st.sidebar.header("🎛️ Control Panel")
        
        # Enhanced file upload section using new uploader
        st.sidebar.subheader("📁 Data Upload")
        
        # Use the enhanced file uploader
        upload_results = self.file_uploader.render_file_upload_section()
        
        if upload_results.get('success') and 'data' in upload_results:
            st.session_state.current_data = upload_results['data']
            st.session_state.data_loaded = True
            st.session_state.file_info = upload_results.get('file_info')
            st.sidebar.success("✅ Data loaded successfully!")
        
        # Analysis options
        if st.session_state.data_loaded:
            st.sidebar.subheader("⚙️ Analysis Options")
            
            # Data cleaning options
            clean_data = st.sidebar.checkbox("Clean Data Automatically", value=True,
                                           help="Remove duplicates and handle missing values")
            
            # AI analysis toggle
            if st.session_state.ai_enabled:
                use_ai = st.sidebar.checkbox("Generate AI Insights", value=True,
                                           help="Use AI to generate natural language insights")
            else:
                use_ai = False
                st.sidebar.info("💡 Add OpenAI API key to enable AI insights")
            
            # Business category selection
            business_category = st.sidebar.selectbox(
                "Business Category",
                ["auto-detect", "sales", "financial", "operational", "marketing", "general"],
                help="Select your business domain for targeted analysis"
            )
            
            # Visualization theme
            theme = st.sidebar.selectbox(
                "Dashboard Theme",
                ["business", "executive", "presentation"],
                help="Choose visual theme for charts and dashboards"
            )
            
            # Analysis button
            if st.sidebar.button("🚀 Run Analysis", type="primary"):
                self.run_comprehensive_analysis(clean_data, use_ai, business_category, theme)
        
        # Export options
        if st.session_state.analysis_results:
            st.sidebar.subheader("💾 Export")
            
            export_format = st.sidebar.selectbox(
                "Export Format",
                ["JSON Report", "CSV Data", "HTML Dashboard"],
                help="Choose export format"
            )
            
            if st.sidebar.button("Download Results"):
                self.export_results(export_format)
    
    def run_comprehensive_analysis(self, clean_data: bool, use_ai: bool, 
                                  business_category: str, theme: str):
        """Run comprehensive analysis on the current data"""
        if not st.session_state.data_loaded:
            st.error("❌ No data loaded")
            return
        
        with st.spinner("🔄 Running comprehensive analysis..."):
            try:
                # Initialize analyzer
                api_key = Config.OPENAI_API_KEY if use_ai else None
                analyzer = IntelligentDataAnalyzer(openai_api_key=api_key)
                
                # Run analysis
                analysis_results = analyzer.analyze_dataframe(
                    st.session_state.current_data,
                    data_name="User Upload",
                    clean_data=clean_data,
                    generate_insights=use_ai
                )
                
                # Initialize visualization engine
                viz_engine = IntelligentVisualizationEngine(openai_api_key=api_key)
                
                # Auto-detect category if needed
                if business_category == "auto-detect":
                    analyzer_for_category = IntelligentDataAnalyzer()
                    analyzer_for_category.analyze_dataframe(st.session_state.current_data, generate_insights=False)
                    suggestions = analyzer_for_category.get_data_category_suggestions()
                    business_category = suggestions[0] if suggestions else "general"
                
                # Create smart dashboard
                dashboard_results = viz_engine.create_smart_dashboard(
                    st.session_state.current_data,
                    business_category=business_category,
                    theme=theme
                )
                
                # Store results
                st.session_state.analysis_results = analysis_results
                st.session_state.dashboard_results = dashboard_results
                
                st.success("✅ Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
    
    def render_main_content(self):
        """Render the main content area with enhanced navigation"""
        if not st.session_state.data_loaded:
            self.render_welcome_screen()
        else:
            # Enhanced navigation for loaded data
            main_tabs = st.tabs([
                "📊 Overview",
                "🔍 Analysis", 
                "📈 Visualizations",
                "🎨 Dashboard Builder",
                "✏️ Chart Editor",
                "📤 Export"
            ])
            
            with main_tabs[0]:
                self.render_data_overview()
            
            with main_tabs[1]:
                if st.session_state.analysis_results:
                    self.render_analysis_results()
                else:
                    st.info("🔄 Run analysis to see detailed insights")
            
            with main_tabs[2]:
                if st.session_state.dashboard_results:
                    self.render_dashboard_results()
                else:
                    st.info("📊 Generate visualizations to see dashboard")
            
            with main_tabs[3]:
                self.render_dashboard_builder()
            
            with main_tabs[4]:
                self.render_chart_editor()
            
            with main_tabs[5]:
                self.render_export_interface()
    
    def render_welcome_screen(self):
        """Render welcome screen when no data is loaded"""
        st.markdown("## 👋 Welcome to BI Assistant")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### 🚀 Get Started
            
            **BI Assistant** is your intelligent data analysis companion that automatically:
            
            - 📊 **Analyzes your data** with smart insights
            - 🤖 **Generates AI explanations** in plain English  
            - 📈 **Creates beautiful visualizations** automatically
            - 💡 **Provides business recommendations** based on patterns
            - 🎯 **Tailors analysis** to your industry (sales, finance, operations)
            
            ### 📁 Upload Your Data
            
            Use the **sidebar** to:
            1. Upload a CSV or Excel file, OR
            2. Load sample data to try the features
            3. Configure analysis options
            4. Run comprehensive analysis
            
            ### ✨ Features Available
            """)
            
            # Feature cards
            feature_col1, feature_col2 = st.columns(2)
            
            with feature_col1:
                st.info("""
                **📊 Data Analysis**
                - Automatic data cleaning
                - Statistical summaries
                - Quality assessment
                - Missing value detection
                """)
                
                st.success("""
                **📈 Smart Visualizations**
                - 10+ chart types
                - Interactive dashboards
                - Business templates
                - Export capabilities
                """)
            
            with feature_col2:
                if st.session_state.ai_enabled:
                    st.success("""
                    **🤖 AI Insights (Enabled)**
                    - Natural language explanations
                    - Pattern recognition
                    - Business recommendations
                    - Trend analysis
                    """)
                else:
                    st.warning("""
                    **🤖 AI Insights (Disabled)**
                    - Add OpenAI API key to .env
                    - Unlock natural language insights
                    - Get business recommendations
                    - Advanced pattern recognition
                    """)
                
                st.info("""
                **🎯 Industry Focus**
                - Sales performance analysis
                - Financial health metrics
                - Operational efficiency
                - Marketing effectiveness
                """)
    
    def render_data_overview(self):
        """Render data overview section"""
        st.markdown("## 📋 Data Overview")
        
        data = st.session_state.current_data
        
        # Basic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Rows", f"{len(data):,}")
        
        with col2:
            st.metric("📈 Columns", len(data.columns))
        
        with col3:
            memory_mb = data.memory_usage(deep=True).sum() / (1024 * 1024)
            st.metric("💾 Memory Usage", f"{memory_mb:.1f} MB")
        
        with col4:
            missing_pct = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
            st.metric("❓ Missing Data", f"{missing_pct:.1f}%")
        
        # Enhanced data overview with file info
        if hasattr(st.session_state, 'file_info') and st.session_state.file_info:
            file_info = st.session_state.file_info
            
            with st.expander("📄 File Information", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**📁 Filename:** {file_info.filename}")
                    st.markdown(f"**📏 File Size:** {file_info.size_bytes / (1024*1024):.2f} MB")
                    st.markdown(f"**🔤 Encoding:** {file_info.encoding or 'Auto-detected'}")
                
                with col2:
                    st.markdown(f"**📋 MIME Type:** {file_info.mime_type}")
                    if file_info.detected_separator:
                        st.markdown(f"**🔗 Separator:** '{file_info.detected_separator}'")
                    if file_info.sheet_names:
                        st.markdown(f"**📊 Excel Sheets:** {', '.join(file_info.sheet_names)}")
        
        # Data preview
        with st.expander("🔍 Data Preview", expanded=True):
            st.dataframe(data.head(10), use_container_width=True)
        
        # Column information
        with st.expander("📊 Column Information"):
            col_info = []
            for col in data.columns:
                col_info.append({
                    'Column': col,
                    'Type': str(data[col].dtype),
                    'Non-Null Count': f"{data[col].count():,}",
                    'Unique Values': f"{data[col].nunique():,}",
                    'Missing': f"{data[col].isnull().sum():,}"
                })
            
            st.dataframe(pd.DataFrame(col_info), use_container_width=True)
    
    def render_analysis_results(self):
        """Render analysis results section"""
        st.markdown("## 🔍 Analysis Results")
        
        results = st.session_state.analysis_results
        
        # Data quality section
        if 'data_summary' in results:
            self.render_data_quality_section(results['data_summary'])
        
        # Data cleaning summary
        if 'cleaning_summary' in results and results['cleaning_summary'].get('operations_performed'):
            self.render_cleaning_summary(results['cleaning_summary'])
        
        # AI Insights section
        if 'insights' in results and results['insights']:
            self.render_ai_insights_section(results['insights'])
    
    def render_data_quality_section(self, data_summary: Dict[str, Any]):
        """Render data quality assessment"""
        st.markdown("### 📊 Data Quality Assessment")
        
        quality = data_summary.get('data_quality', {})
        
        # Quality score with color coding
        score = quality.get('overall_score', 0)
        if score >= 80:
            st.success(f"🟢 **Data Quality Score: {score}/100** - Excellent")
        elif score >= 60:
            st.warning(f"🟡 **Data Quality Score: {score}/100** - Good")
        else:
            st.error(f"🔴 **Data Quality Score: {score}/100** - Needs Attention")
        
        # Quality metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Missing Data %", f"{quality.get('missing_data_percentage', 0):.1f}%")
            st.metric("Duplicate Rows %", f"{quality.get('duplicate_percentage', 0):.1f}%")
        
        with col2:
            basic_info = data_summary.get('basic_info', {})
            st.metric("Total Records", f"{basic_info.get('rows', 0):,}")
            st.metric("Total Columns", basic_info.get('columns', 0))
        
        # Recommendations
        recommendations = quality.get('recommendations', [])
        if recommendations:
            st.markdown("**🎯 Recommendations:**")
            for rec in recommendations:
                st.markdown(f"- {rec}")
    
    def render_cleaning_summary(self, cleaning_summary: Dict[str, Any]):
        """Render data cleaning summary"""
        st.markdown("### 🧹 Data Cleaning Summary")
        
        operations = cleaning_summary.get('operations_performed', [])
        
        if operations:
            st.markdown("**✅ Cleaning Operations Performed:**")
            for operation in operations:
                st.markdown(f"- {operation}")
            
            # Before/after comparison
            original_shape = cleaning_summary.get('original_shape', (0, 0))
            final_shape = cleaning_summary.get('final_shape', (0, 0))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Original Size", f"{original_shape[0]:,} × {original_shape[1]}")
            with col2:
                st.metric("After Cleaning", f"{final_shape[0]:,} × {final_shape[1]}")
        else:
            st.info("✨ No cleaning operations were needed - your data is already in great shape!")
    
    def render_ai_insights_section(self, insights: Dict[str, Any]):
        """Render AI-generated insights"""
        st.markdown("### 🤖 AI-Generated Insights")
        
        # Overview insights
        if 'overview' in insights:
            overview = insights['overview']
            
            st.markdown("#### 📋 Executive Summary")
            if overview.get('executive_summary'):
                st.markdown(f'<div class="insight-box">{overview["executive_summary"]}</div>', 
                          unsafe_allow_html=True)
            
            # Key findings
            if overview.get('key_findings'):
                st.markdown("#### 🔍 Key Findings")
                findings = overview['key_findings']
                if isinstance(findings, list):
                    for finding in findings:
                        st.markdown(f"• {finding}")
                else:
                    st.markdown(findings)
            
            # Recommendations
            if overview.get('recommendations'):
                st.markdown("#### 💡 Recommendations")
                recommendations = overview['recommendations']
                if isinstance(recommendations, list):
                    for rec in recommendations:
                        st.markdown(f"• {rec}")
                else:
                    st.markdown(recommendations)
        
        # Business narrative
        if 'narrative' in insights:
            st.markdown("#### 📖 Business Story")
            st.markdown(f'<div class="insight-box">{insights["narrative"]}</div>', 
                       unsafe_allow_html=True)
        
        # Column insights
        if 'columns' in insights:
            with st.expander("📊 Column-Specific Insights"):
                for col_name, col_insights in insights['columns'].items():
                    st.markdown(f"**{col_name}:**")
                    if col_insights.get('business_significance'):
                        st.markdown(f"- *Significance:* {col_insights['business_significance']}")
                    if col_insights.get('pattern_analysis'):
                        st.markdown(f"- *Patterns:* {col_insights['pattern_analysis']}")
        
        # Trend insights
        if 'trends' in insights:
            with st.expander("📈 Trend Analysis"):
                trends = insights['trends']
                if trends.get('trend_summary'):
                    st.markdown(f"**Summary:** {trends['trend_summary']}")
                if trends.get('recommendations'):
                    st.markdown(f"**Recommendations:** {trends['recommendations']}")
    
    def render_dashboard_results(self):
        """Render dashboard and visualization results"""
        st.markdown("## 📊 Interactive Dashboard")
        
        dashboard = st.session_state.dashboard_results
        
        # Dashboard metadata
        metadata = dashboard.get('metadata', {})
        st.markdown(f"*Generated {metadata.get('total_charts', 0)} charts for {metadata.get('data_shape', ['N/A', 'N/A'])[0]:,} records*")
        
        # Dashboard insights
        if dashboard.get('dashboard_insights'):
            self.render_dashboard_insights(dashboard['dashboard_insights'])
        
        # Interactive charts
        charts = dashboard.get('charts', [])
        if charts:
            st.markdown("### 📈 Generated Visualizations")
            
            # Chart display options
            chart_layout = st.radio(
                "Display Layout:",
                ["Single Column", "Two Columns", "Grid View"],
                horizontal=True
            )
            
            self.display_charts(charts, chart_layout)
        
        # Specialized dashboard
        if dashboard.get('specialized_dashboard'):
            st.markdown("### 🏢 Business-Specific Dashboard")
            st.plotly_chart(dashboard['specialized_dashboard'], use_container_width=True)
        
        # Summary dashboards
        if dashboard.get('summary_dashboard'):
            st.markdown("### 📋 Statistical Summary")
            # Display matplotlib image
            img_data = base64.b64decode(dashboard['summary_dashboard'])
            st.image(img_data, caption="Comprehensive Data Summary", use_column_width=True)
        
        # Chart recommendations
        recommendations = dashboard.get('recommendations', [])
        if recommendations:
            with st.expander("💡 Additional Chart Recommendations"):
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"**{i}. {rec.get('title', 'Chart')}** ({rec.get('chart_type', 'Unknown')})")
                    st.markdown(f"   *Rationale:* {rec.get('rationale', 'N/A')}")
                    st.markdown(f"   *Priority:* {rec.get('priority', 'N/A').title()}")
    
    def render_dashboard_insights(self, insights: Dict[str, Any]):
        """Render dashboard-level insights"""
        st.markdown("### 🎯 Dashboard Insights")
        
        # Create tabs for different insight types
        tab1, tab2, tab3 = st.tabs(["📋 Overview", "🔍 Key Patterns", "💼 Business Impact"])
        
        with tab1:
            if insights.get('overview'):
                st.markdown(f'<div class="insight-box">{insights["overview"]}</div>', 
                          unsafe_allow_html=True)
        
        with tab2:
            if insights.get('key_patterns'):
                st.markdown(f'<div class="insight-box">{insights["key_patterns"]}</div>', 
                          unsafe_allow_html=True)
        
        with tab3:
            if insights.get('business_implications'):
                st.markdown(f'<div class="insight-box">{insights["business_implications"]}</div>', 
                          unsafe_allow_html=True)
            
            if insights.get('recommended_actions'):
                st.markdown("**🎯 Recommended Actions:**")
                st.markdown(f'<div class="insight-box">{insights["recommended_actions"]}</div>', 
                          unsafe_allow_html=True)
    
    def display_charts(self, charts: List[Dict[str, Any]], layout: str):
        """Display charts in the specified layout"""
        if layout == "Single Column":
            for chart_info in charts:
                self.render_single_chart(chart_info)
        
        elif layout == "Two Columns":
            for i in range(0, len(charts), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    if i < len(charts):
                        self.render_single_chart(charts[i])
                
                with col2:
                    if i + 1 < len(charts):
                        self.render_single_chart(charts[i + 1])
        
        elif layout == "Grid View":
            for i in range(0, len(charts), 3):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if i < len(charts):
                        self.render_single_chart(charts[i], compact=True)
                
                with col2:
                    if i + 1 < len(charts):
                        self.render_single_chart(charts[i + 1], compact=True)
                
                with col3:
                    if i + 2 < len(charts):
                        self.render_single_chart(charts[i + 2], compact=True)
    
    def render_single_chart(self, chart_info: Dict[str, Any], compact: bool = False):
        """Render a single chart with its information"""
        chart = chart_info.get('chart')
        if not chart:
            return
        
        # Chart title and info
        if not compact:
            st.markdown(f"#### {chart_info.get('title', 'Chart')}")
            
            # Chart metadata
            col1, col2 = st.columns([3, 1])
            with col2:
                st.caption(f"Type: {chart_info.get('type', 'Unknown')}")
                st.caption(f"Columns: {', '.join(chart_info.get('columns_used', []))}")
        
        # Display chart
        st.plotly_chart(chart, use_container_width=True)
        
        # AI explanation
        if not compact and chart_info.get('ai_explanation'):
            with st.expander("🤖 AI Explanation"):
                st.markdown(chart_info['ai_explanation'])
        
        # Chart rationale
        if not compact and chart_info.get('rationale'):
            st.caption(f"💡 {chart_info['rationale']}")
    
    def export_results(self, format: str):
        """Export analysis results in specified format"""
        try:
            if format == "JSON Report":
                # Combine all results
                export_data = {
                    'analysis_results': st.session_state.analysis_results,
                    'dashboard_metadata': st.session_state.dashboard_results.get('metadata', {}),
                    'dashboard_insights': st.session_state.dashboard_results.get('dashboard_insights', {}),
                    'export_timestamp': datetime.now().isoformat()
                }
                
                # Convert to JSON
                json_data = json.dumps(export_data, indent=2, default=str)
                
                st.download_button(
                    label="📥 Download JSON Report",
                    data=json_data,
                    file_name=f"bi_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            elif format == "CSV Data":
                # Export the cleaned data
                csv_data = st.session_state.current_data.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download CSV Data",
                    data=csv_data,
                    file_name=f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            elif format == "HTML Dashboard":
                st.info("🚧 HTML Dashboard export coming soon! Currently you can save individual charts by right-clicking them.")
        
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    def render_dashboard_builder(self):
        """Render dashboard builder interface"""
        if not st.session_state.data_loaded:
            st.warning("📊 Please upload data first to use the Dashboard Builder")
            return
        
        try:
            # Initialize dashboard builder
            if 'dashboard_builder' not in st.session_state:
                st.session_state.dashboard_builder = InteractiveDashboardBuilder(st.session_state.current_data)
            
            builder = st.session_state.dashboard_builder
            
            # Render builder interface
            dashboard_config = builder.render_dashboard_builder()
            
            if dashboard_config:
                st.success("✅ Dashboard created successfully!")
                
                # Store in session state for use in other tabs
                if 'custom_dashboards' not in st.session_state:
                    st.session_state.custom_dashboards = []
                
                st.session_state.custom_dashboards.append(dashboard_config)
                
                # Show quick preview
                with st.expander("👁️ Dashboard Preview", expanded=True):
                    builder._render_dashboard_from_config(dashboard_config)
        
        except Exception as e:
            st.error(f"❌ Dashboard Builder error: {str(e)}")
    
    def render_chart_editor(self):
        """Render chart editor interface"""
        if not st.session_state.data_loaded:
            st.warning("📊 Please upload data first to use the Chart Editor")
            return
        
        try:
            # Check if we have custom dashboards
            if 'custom_dashboards' not in st.session_state or not st.session_state.custom_dashboards:
                st.info("🎨 Create a dashboard first using the Dashboard Builder to edit charts")
                return
            
            # Select dashboard to edit
            dashboard_options = {f"Dashboard {i+1}: {dash.title}": i for i, dash in enumerate(st.session_state.custom_dashboards)}
            
            if dashboard_options:
                selected_dashboard_name = st.selectbox("Select Dashboard to Edit", list(dashboard_options.keys()))
                selected_index = dashboard_options[selected_dashboard_name]
                selected_dashboard = st.session_state.custom_dashboards[selected_index]
                
                if selected_dashboard.charts:
                    # Select chart to edit
                    chart_options = {f"{chart.title} ({chart.chart_type.value})": chart for chart in selected_dashboard.charts}
                    selected_chart_name = st.selectbox("Select Chart to Edit", list(chart_options.keys()))
                    selected_chart = chart_options[selected_chart_name]
                    
                    # Initialize chart editor
                    if 'chart_editor' not in st.session_state:
                        st.session_state.chart_editor = InteractiveChartEditor(st.session_state.current_data)
                    
                    editor = st.session_state.chart_editor
                    
                    # Render editor interface
                    updated_config, updated_styling = editor.render_chart_editor(selected_chart)
                    
                    # Update the chart in the dashboard
                    for i, chart in enumerate(selected_dashboard.charts):
                        if chart.chart_id == updated_config.chart_id:
                            selected_dashboard.charts[i] = updated_config
                            break
                
                else:
                    st.info("📊 The selected dashboard has no charts to edit")
            
        except Exception as e:
            st.error(f"❌ Chart Editor error: {str(e)}")
    
    def render_export_interface(self):
        """Render export interface"""
        if not st.session_state.data_loaded:
            st.warning("📊 Please upload data first to export")
            return
        
        try:
            # Initialize exporter
            if 'dashboard_exporter' not in st.session_state:
                st.session_state.dashboard_exporter = DashboardExporter(st.session_state.current_data)
            
            exporter = st.session_state.dashboard_exporter
            
            # Check if we have custom dashboards to export
            if 'custom_dashboards' in st.session_state and st.session_state.custom_dashboards:
                # Select dashboard to export
                dashboard_options = {f"Dashboard {i+1}: {dash.title}": dash for i, dash in enumerate(st.session_state.custom_dashboards)}
                
                selected_dashboard_name = st.selectbox("Select Dashboard to Export", list(dashboard_options.keys()))
                selected_dashboard = dashboard_options[selected_dashboard_name]
                
                # Get chart stylings (if available)
                chart_stylings = {}
                
                # Render export interface
                exporter.render_export_interface(selected_dashboard, chart_stylings)
            
            else:
                st.info("🎨 Create a dashboard first using the Dashboard Builder to export")
                
                # Still allow data export
                st.markdown("### 💾 Data Export")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Export as CSV"):
                        csv_data = st.session_state.current_data.to_csv(index=False)
                        st.download_button(
                            "📥 Download CSV",
                            data=csv_data,
                            file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("📊 Export as Excel"):
                        excel_buffer = io.BytesIO()
                        st.session_state.current_data.to_excel(excel_buffer, index=False)
                        excel_buffer.seek(0)
                        
                        st.download_button(
                            "📥 Download Excel",
                            data=excel_buffer.getvalue(),
                            file_name=f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
        
        except Exception as e:
            st.error(f"❌ Export interface error: {str(e)}")
    
    def run(self):
        """Main method to run the dashboard"""
        self.render_header()
        
        # Create layout
        self.render_sidebar()
        self.render_main_content()
        
        # Footer
        st.markdown("---")
        st.markdown("*Built with ❤️ using Streamlit, Plotly, and OpenAI*")


def main():
    """Main function to run the Streamlit app"""
    dashboard = StreamlitDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
