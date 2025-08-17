"""
Advanced Dashboard Generation System
Provides dynamic dashboard customization, interactive chart editing, and templating
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import uuid
from enum import Enum
import copy

# Import our components
from src.visualizer import PlotlyVisualizer, ChartRecommendationEngine
from src.intelligent_visualizer import IntelligentVisualizationEngine


class DashboardTheme(Enum):
    """Dashboard theme options"""
    BUSINESS = "business"
    EXECUTIVE = "executive"
    PRESENTATION = "presentation"
    DARK = "dark"
    LIGHT = "light"
    MODERN = "modern"
    CLASSIC = "classic"


class ChartType(Enum):
    """Available chart types"""
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    PIE = "pie"
    HISTOGRAM = "histogram"
    BOX = "box"
    HEATMAP = "heatmap"
    AREA = "area"
    VIOLIN = "violin"
    SUNBURST = "sunburst"
    TREEMAP = "treemap"
    WATERFALL = "waterfall"
    FUNNEL = "funnel"
    GAUGE = "gauge"
    RADAR = "radar"


@dataclass
class ChartConfig:
    """Configuration for individual charts"""
    chart_id: str
    chart_type: ChartType
    title: str
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    color_column: Optional[str] = None
    size_column: Optional[str] = None
    facet_column: Optional[str] = None
    aggregation: Optional[str] = None
    filter_conditions: Dict[str, Any] = None
    styling: Dict[str, Any] = None
    position: Dict[str, int] = None  # row, column, width, height
    custom_properties: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.filter_conditions is None:
            self.filter_conditions = {}
        if self.styling is None:
            self.styling = {}
        if self.position is None:
            self.position = {'row': 0, 'col': 0, 'width': 6, 'height': 4}
        if self.custom_properties is None:
            self.custom_properties = {}


@dataclass
class DashboardConfig:
    """Complete dashboard configuration"""
    dashboard_id: str
    title: str
    description: str
    theme: DashboardTheme
    layout: Dict[str, Any]  # Grid layout configuration
    charts: List[ChartConfig]
    filters: List[Dict[str, Any]]  # Global filters
    kpis: List[Dict[str, Any]]  # Key performance indicators
    text_blocks: List[Dict[str, Any]]  # Text/markdown blocks
    created_at: datetime
    modified_at: datetime
    
    def __post_init__(self):
        if not self.charts:
            self.charts = []
        if not self.filters:
            self.filters = []
        if not self.kpis:
            self.kpis = []
        if not self.text_blocks:
            self.text_blocks = []


class DashboardTemplate:
    """Pre-built dashboard templates"""
    
    @staticmethod
    def get_available_templates() -> Dict[str, Dict[str, Any]]:
        """Get all available dashboard templates"""
        return {
            "executive_summary": {
                "name": "Executive Summary",
                "description": "High-level KPIs and trends for executive reporting",
                "category": "business",
                "charts": ["kpi_cards", "trend_line", "top_categories", "performance_gauge"],
                "layout": "executive"
            },
            "sales_analytics": {
                "name": "Sales Analytics",
                "description": "Comprehensive sales performance analysis",
                "category": "sales",
                "charts": ["sales_trend", "regional_performance", "product_analysis", "sales_funnel"],
                "layout": "grid_4x2"
            },
            "financial_dashboard": {
                "name": "Financial Dashboard",
                "description": "Financial metrics and budget analysis",
                "category": "finance",
                "charts": ["revenue_chart", "expense_breakdown", "budget_variance", "profit_analysis"],
                "layout": "financial"
            },
            "operational_metrics": {
                "name": "Operational Metrics",
                "description": "Operational efficiency and performance tracking",
                "category": "operations",
                "charts": ["efficiency_trends", "resource_utilization", "quality_metrics", "capacity_analysis"],
                "layout": "operations"
            },
            "customer_insights": {
                "name": "Customer Insights",
                "description": "Customer behavior and satisfaction analysis",
                "category": "customer",
                "charts": ["customer_segments", "satisfaction_trends", "churn_analysis", "lifetime_value"],
                "layout": "customer"
            },
            "marketing_performance": {
                "name": "Marketing Performance",
                "description": "Marketing campaign effectiveness and ROI",
                "category": "marketing",
                "charts": ["campaign_roi", "channel_performance", "conversion_funnel", "audience_analysis"],
                "layout": "marketing"
            }
        }
    
    @staticmethod
    def create_dashboard_from_template(template_name: str, data: pd.DataFrame, 
                                     theme: DashboardTheme = DashboardTheme.BUSINESS) -> DashboardConfig:
        """Create a dashboard configuration from a template"""
        templates = DashboardTemplate.get_available_templates()
        
        if template_name not in templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = templates[template_name]
        dashboard_id = str(uuid.uuid4())
        
        # Create base dashboard config
        config = DashboardConfig(
            dashboard_id=dashboard_id,
            title=template["name"],
            description=template["description"],
            theme=theme,
            layout=DashboardTemplate._get_layout_config(template["layout"]),
            charts=[],
            filters=[],
            kpis=[],
            text_blocks=[],
            created_at=datetime.now(),
            modified_at=datetime.now()
        )
        
        # Generate charts based on template and data
        chart_generator = ChartGenerator(data)
        config.charts = chart_generator.generate_charts_for_template(template_name, template)
        
        # Add KPIs if applicable
        if template_name in ["executive_summary", "sales_analytics", "financial_dashboard"]:
            config.kpis = chart_generator.generate_kpis_for_template(template_name)
        
        return config


class ChartGenerator:
    """Intelligent chart generation based on data characteristics"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_columns = data.select_dtypes(include=['datetime64']).columns.tolist()
        self.recommendation_engine = ChartRecommendationEngine()
    
    def generate_charts_for_template(self, template_name: str, template: Dict[str, Any]) -> List[ChartConfig]:
        """Generate chart configurations for a specific template"""
        charts = []
        
        if template_name == "executive_summary":
            charts.extend(self._generate_executive_charts())
        elif template_name == "sales_analytics":
            charts.extend(self._generate_sales_charts())
        elif template_name == "financial_dashboard":
            charts.extend(self._generate_financial_charts())
        elif template_name == "operational_metrics":
            charts.extend(self._generate_operational_charts())
        elif template_name == "customer_insights":
            charts.extend(self._generate_customer_charts())
        elif template_name == "marketing_performance":
            charts.extend(self._generate_marketing_charts())
        
        return charts
    
    def generate_kpis_for_template(self, template_name: str) -> List[Dict[str, Any]]:
        """Generate KPI configurations for a template"""
        kpis = []
        
        if template_name == "executive_summary":
            kpis = self._generate_executive_kpis()
        elif template_name == "sales_analytics":
            kpis = self._generate_sales_kpis()
        elif template_name == "financial_dashboard":
            kpis = self._generate_financial_kpis()
        
        return kpis
    
    def _generate_executive_charts(self) -> List[ChartConfig]:
        """Generate charts for executive summary"""
        charts = []
        
        # Trend chart
        if self.datetime_columns and self.numeric_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.LINE,
                title="Key Metrics Trend",
                x_column=self.datetime_columns[0],
                y_column=self.numeric_columns[0],
                position={'row': 0, 'col': 0, 'width': 8, 'height': 4}
            ))
        
        # Performance gauge
        if self.numeric_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.GAUGE,
                title="Performance Score",
                y_column=self.numeric_columns[0],
                position={'row': 0, 'col': 8, 'width': 4, 'height': 4}
            ))
        
        # Top categories
        if self.categorical_columns and self.numeric_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.BAR,
                title="Top Categories",
                x_column=self.categorical_columns[0],
                y_column=self.numeric_columns[0],
                aggregation="sum",
                position={'row': 4, 'col': 0, 'width': 6, 'height': 4}
            ))
        
        return charts
    
    def _generate_sales_charts(self) -> List[ChartConfig]:
        """Generate charts for sales analytics"""
        charts = []
        
        # Sales trend over time
        if self.datetime_columns and self.numeric_columns:
            sales_col = self._find_column_by_keywords(['sales', 'revenue', 'amount'])
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.LINE,
                title="Sales Trend",
                x_column=self.datetime_columns[0],
                y_column=sales_col or self.numeric_columns[0],
                position={'row': 0, 'col': 0, 'width': 8, 'height': 4}
            ))
        
        # Regional performance
        if self.categorical_columns and self.numeric_columns:
            region_col = self._find_column_by_keywords(['region', 'territory', 'area', 'location'])
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.BAR,
                title="Regional Performance",
                x_column=region_col or self.categorical_columns[0],
                y_column=self.numeric_columns[0],
                aggregation="sum",
                position={'row': 0, 'col': 8, 'width': 4, 'height': 4}
            ))
        
        # Product analysis
        if len(self.categorical_columns) > 1 and self.numeric_columns:
            product_col = self._find_column_by_keywords(['product', 'item', 'category'])
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.PIE,
                title="Product Mix",
                color_column=product_col or self.categorical_columns[1],
                y_column=self.numeric_columns[0],
                aggregation="sum",
                position={'row': 4, 'col': 0, 'width': 6, 'height': 4}
            ))
        
        return charts
    
    def _generate_financial_charts(self) -> List[ChartConfig]:
        """Generate charts for financial dashboard"""
        charts = []
        
        # Revenue vs expenses
        revenue_col = self._find_column_by_keywords(['revenue', 'income', 'sales'])
        expense_col = self._find_column_by_keywords(['expense', 'cost', 'spending'])
        
        if revenue_col and expense_col and self.datetime_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.LINE,
                title="Revenue vs Expenses",
                x_column=self.datetime_columns[0],
                y_column=revenue_col,
                position={'row': 0, 'col': 0, 'width': 6, 'height': 4}
            ))
        
        # Budget variance
        if self.numeric_columns and len(self.numeric_columns) >= 2:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.WATERFALL,
                title="Budget Variance",
                x_column=self.categorical_columns[0] if self.categorical_columns else None,
                y_column=self.numeric_columns[1],
                position={'row': 0, 'col': 6, 'width': 6, 'height': 4}
            ))
        
        return charts
    
    def _generate_operational_charts(self) -> List[ChartConfig]:
        """Generate charts for operational metrics"""
        charts = []
        
        # Efficiency trends
        efficiency_col = self._find_column_by_keywords(['efficiency', 'productivity', 'performance'])
        if efficiency_col and self.datetime_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.AREA,
                title="Efficiency Trends",
                x_column=self.datetime_columns[0],
                y_column=efficiency_col,
                position={'row': 0, 'col': 0, 'width': 8, 'height': 4}
            ))
        
        # Resource utilization
        if self.categorical_columns and self.numeric_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.HEATMAP,
                title="Resource Utilization",
                x_column=self.categorical_columns[0],
                y_column=self.categorical_columns[1] if len(self.categorical_columns) > 1 else None,
                color_column=self.numeric_columns[0],
                position={'row': 0, 'col': 8, 'width': 4, 'height': 4}
            ))
        
        return charts
    
    def _generate_customer_charts(self) -> List[ChartConfig]:
        """Generate charts for customer insights"""
        charts = []
        
        # Customer segments
        if self.categorical_columns and self.numeric_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.SUNBURST,
                title="Customer Segments",
                color_column=self.categorical_columns[0],
                y_column=self.numeric_columns[0],
                position={'row': 0, 'col': 0, 'width': 6, 'height': 6}
            ))
        
        # Satisfaction trends
        satisfaction_col = self._find_column_by_keywords(['satisfaction', 'rating', 'score'])
        if satisfaction_col and self.datetime_columns:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.LINE,
                title="Customer Satisfaction",
                x_column=self.datetime_columns[0],
                y_column=satisfaction_col,
                position={'row': 0, 'col': 6, 'width': 6, 'height': 3}
            ))
        
        return charts
    
    def _generate_marketing_charts(self) -> List[ChartConfig]:
        """Generate charts for marketing performance"""
        charts = []
        
        # Campaign ROI
        roi_col = self._find_column_by_keywords(['roi', 'return', 'roas'])
        campaign_col = self._find_column_by_keywords(['campaign', 'channel', 'source'])
        
        if roi_col and campaign_col:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.BAR,
                title="Campaign ROI",
                x_column=campaign_col,
                y_column=roi_col,
                aggregation="mean",
                position={'row': 0, 'col': 0, 'width': 6, 'height': 4}
            ))
        
        # Conversion funnel
        if self.numeric_columns and len(self.numeric_columns) >= 3:
            charts.append(ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType.FUNNEL,
                title="Conversion Funnel",
                y_column=self.numeric_columns[0],
                position={'row': 0, 'col': 6, 'width': 6, 'height': 4}
            ))
        
        return charts
    
    def _generate_executive_kpis(self) -> List[Dict[str, Any]]:
        """Generate KPIs for executive summary"""
        kpis = []
        
        if self.numeric_columns:
            for i, col in enumerate(self.numeric_columns[:4]):
                kpis.append({
                    'id': str(uuid.uuid4()),
                    'title': col.replace('_', ' ').title(),
                    'value': float(self.data[col].sum()),
                    'format': 'number',
                    'trend': self._calculate_trend(col),
                    'position': {'row': 0, 'col': i * 3, 'width': 3, 'height': 2}
                })
        
        return kpis
    
    def _generate_sales_kpis(self) -> List[Dict[str, Any]]:
        """Generate KPIs for sales analytics"""
        kpis = []
        
        # Total revenue
        revenue_col = self._find_column_by_keywords(['revenue', 'sales', 'amount'])
        if revenue_col:
            kpis.append({
                'id': str(uuid.uuid4()),
                'title': 'Total Revenue',
                'value': float(self.data[revenue_col].sum()),
                'format': 'currency',
                'trend': self._calculate_trend(revenue_col),
                'position': {'row': 0, 'col': 0, 'width': 3, 'height': 2}
            })
        
        # Average order value
        if revenue_col:
            kpis.append({
                'id': str(uuid.uuid4()),
                'title': 'Avg Order Value',
                'value': float(self.data[revenue_col].mean()),
                'format': 'currency',
                'trend': 0,
                'position': {'row': 0, 'col': 3, 'width': 3, 'height': 2}
            })
        
        return kpis
    
    def _generate_financial_kpis(self) -> List[Dict[str, Any]]:
        """Generate KPIs for financial dashboard"""
        kpis = []
        
        # Profit margin
        revenue_col = self._find_column_by_keywords(['revenue', 'income'])
        expense_col = self._find_column_by_keywords(['expense', 'cost'])
        
        if revenue_col and expense_col:
            total_revenue = self.data[revenue_col].sum()
            total_expense = self.data[expense_col].sum()
            margin = ((total_revenue - total_expense) / total_revenue) * 100
            
            kpis.append({
                'id': str(uuid.uuid4()),
                'title': 'Profit Margin',
                'value': float(margin),
                'format': 'percentage',
                'trend': 0,
                'position': {'row': 0, 'col': 0, 'width': 4, 'height': 2}
            })
        
        return kpis
    
    def _find_column_by_keywords(self, keywords: List[str]) -> Optional[str]:
        """Find column that matches keywords"""
        all_columns = list(self.data.columns)
        
        for keyword in keywords:
            for col in all_columns:
                if keyword.lower() in col.lower():
                    return col
        
        return None
    
    def _calculate_trend(self, column: str) -> float:
        """Calculate trend for a numeric column"""
        try:
            if len(self.data) < 2:
                return 0
            
            recent_half = self.data[column].tail(len(self.data)//2).mean()
            earlier_half = self.data[column].head(len(self.data)//2).mean()
            
            if earlier_half == 0:
                return 0
            
            return ((recent_half - earlier_half) / earlier_half) * 100
        except:
            return 0
    
    @staticmethod
    def _get_layout_config(layout_name: str) -> Dict[str, Any]:
        """Get layout configuration by name"""
        layouts = {
            "executive": {
                "type": "grid",
                "rows": 8,
                "columns": 12,
                "spacing": 10,
                "responsive": True
            },
            "grid_4x2": {
                "type": "grid",
                "rows": 8,
                "columns": 12,
                "spacing": 15,
                "responsive": True
            },
            "financial": {
                "type": "grid",
                "rows": 10,
                "columns": 12,
                "spacing": 12,
                "responsive": True
            },
            "operations": {
                "type": "grid",
                "rows": 12,
                "columns": 12,
                "spacing": 8,
                "responsive": True
            },
            "customer": {
                "type": "grid",
                "rows": 10,
                "columns": 12,
                "spacing": 10,
                "responsive": True
            },
            "marketing": {
                "type": "grid",
                "rows": 8,
                "columns": 12,
                "spacing": 12,
                "responsive": True
            }
        }
        
        return layouts.get(layout_name, layouts["executive"])


class InteractiveDashboardBuilder:
    """Interactive dashboard builder with real-time editing"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.visualizer = PlotlyVisualizer()
        self.chart_generator = ChartGenerator(data)
        
        # Initialize session state for dashboard builder
        if 'dashboard_builder_state' not in st.session_state:
            st.session_state.dashboard_builder_state = {
                'current_dashboard': None,
                'selected_chart': None,
                'edit_mode': False,
                'preview_mode': False
            }
    
    def render_dashboard_builder(self) -> Optional[DashboardConfig]:
        """Render the interactive dashboard builder interface"""
        st.markdown("## 🎨 Dashboard Builder")
        
        # Builder mode selection
        builder_mode = st.radio(
            "Builder Mode:",
            ["Template", "Custom", "AI-Assisted"],
            horizontal=True,
            help="Choose how to create your dashboard"
        )
        
        if builder_mode == "Template":
            return self._render_template_builder()
        elif builder_mode == "Custom":
            return self._render_custom_builder()
        else:  # AI-Assisted
            return self._render_ai_assisted_builder()
    
    def _render_template_builder(self) -> Optional[DashboardConfig]:
        """Render template-based dashboard builder"""
        st.markdown("### 📋 Choose a Template")
        
        templates = DashboardTemplate.get_available_templates()
        
        # Template selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            template_options = {name: info["name"] for name, info in templates.items()}
            selected_template = st.selectbox(
                "Select Template:",
                list(template_options.keys()),
                format_func=lambda x: template_options[x]
            )
            
            if selected_template:
                template_info = templates[selected_template]
                st.info(f"📝 **Description:** {template_info['description']}")
                st.write(f"**Category:** {template_info['category'].title()}")
                st.write(f"**Charts:** {', '.join(template_info['charts'])}")
        
        with col2:
            theme = st.selectbox(
                "Dashboard Theme:",
                [theme.value for theme in DashboardTheme],
                index=0
            )
            
            if st.button("🚀 Create Dashboard", type="primary"):
                try:
                    dashboard_config = DashboardTemplate.create_dashboard_from_template(
                        selected_template, 
                        self.data, 
                        DashboardTheme(theme)
                    )
                    
                    st.session_state.dashboard_builder_state['current_dashboard'] = dashboard_config
                    st.success("✅ Dashboard created successfully!")
                    
                    return dashboard_config
                    
                except Exception as e:
                    st.error(f"❌ Failed to create dashboard: {str(e)}")
        
        return None
    
    def _render_custom_builder(self) -> Optional[DashboardConfig]:
        """Render custom dashboard builder"""
        st.markdown("### 🛠️ Custom Dashboard Builder")
        
        # Dashboard basic settings
        with st.expander("⚙️ Dashboard Settings", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                dashboard_title = st.text_input("Dashboard Title", "My Custom Dashboard")
                dashboard_description = st.text_area("Description", "Custom analytics dashboard")
            
            with col2:
                theme = st.selectbox("Theme:", [theme.value for theme in DashboardTheme])
                layout_type = st.selectbox("Layout:", ["grid", "flow", "fixed"])
        
        # Chart builder
        st.markdown("#### 📊 Add Charts")
        
        chart_tabs = st.tabs(["➕ Add Chart", "📝 Edit Charts", "👁️ Preview"])
        
        with chart_tabs[0]:
            self._render_chart_editor()
        
        with chart_tabs[1]:
            self._render_chart_list_editor()
        
        with chart_tabs[2]:
            self._render_dashboard_preview()
        
        return None
    
    def _render_ai_assisted_builder(self) -> Optional[DashboardConfig]:
        """Render AI-assisted dashboard builder"""
        st.markdown("### 🤖 AI-Assisted Dashboard Builder")
        
        # AI prompt interface
        with st.expander("💭 Describe Your Dashboard", expanded=True):
            dashboard_prompt = st.text_area(
                "What kind of dashboard do you want to create?",
                placeholder="I want to create a sales dashboard showing revenue trends, top products, and regional performance...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                focus_area = st.selectbox(
                    "Primary Focus:",
                    ["Sales", "Finance", "Operations", "Marketing", "Customer", "General"]
                )
            
            with col2:
                detail_level = st.selectbox(
                    "Detail Level:",
                    ["Executive Summary", "Detailed Analysis", "Operational View"]
                )
        
        if st.button("🧠 Generate AI Dashboard", type="primary"):
            with st.spinner("🤖 AI is analyzing your data and creating dashboard..."):
                try:
                    # Simulate AI dashboard generation
                    ai_dashboard = self._generate_ai_dashboard(dashboard_prompt, focus_area, detail_level)
                    
                    st.session_state.dashboard_builder_state['current_dashboard'] = ai_dashboard
                    st.success("✅ AI Dashboard generated successfully!")
                    
                    return ai_dashboard
                    
                except Exception as e:
                    st.error(f"❌ AI Dashboard generation failed: {str(e)}")
        
        return None
    
    def _render_chart_editor(self):
        """Render chart editor interface"""
        st.markdown("##### ➕ Add New Chart")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chart_type = st.selectbox(
                "Chart Type:",
                [chart_type.value for chart_type in ChartType]
            )
            
            chart_title = st.text_input("Chart Title", f"New {chart_type.title()} Chart")
        
        with col2:
            # Column selection based on chart type
            if chart_type in ['line', 'bar', 'scatter', 'area']:
                x_column = st.selectbox("X-Axis:", [''] + list(self.data.columns))
                y_column = st.selectbox("Y-Axis:", [''] + list(self.data.columns))
            elif chart_type in ['pie', 'sunburst', 'treemap']:
                color_column = st.selectbox("Category:", [''] + list(self.data.columns))
                y_column = st.selectbox("Values:", [''] + list(self.data.columns))
                x_column = None
            else:
                x_column = st.selectbox("X-Axis:", [''] + list(self.data.columns))
                y_column = st.selectbox("Y-Axis:", [''] + list(self.data.columns))
        
        with col3:
            # Optional columns
            color_column = st.selectbox("Color By:", [''] + list(self.data.columns), key="color_by")
            size_column = st.selectbox("Size By:", [''] + list(self.data.columns), key="size_by")
            
            # Aggregation for categorical x-axis
            if x_column and x_column in self.data.select_dtypes(include=['object', 'category']).columns:
                aggregation = st.selectbox("Aggregation:", ['sum', 'mean', 'count', 'max', 'min'])
            else:
                aggregation = None
        
        # Chart positioning
        with st.expander("📐 Chart Position & Size"):
            pos_col1, pos_col2 = st.columns(2)
            
            with pos_col1:
                row = st.number_input("Row", min_value=0, max_value=20, value=0)
                col = st.number_input("Column", min_value=0, max_value=12, value=0)
            
            with pos_col2:
                width = st.number_input("Width", min_value=1, max_value=12, value=6)
                height = st.number_input("Height", min_value=1, max_value=10, value=4)
        
        if st.button("➕ Add Chart"):
            # Create chart config
            chart_config = ChartConfig(
                chart_id=str(uuid.uuid4()),
                chart_type=ChartType(chart_type),
                title=chart_title,
                x_column=x_column if x_column else None,
                y_column=y_column if y_column else None,
                color_column=color_column if color_column else None,
                size_column=size_column if size_column else None,
                aggregation=aggregation,
                position={'row': row, 'col': col, 'width': width, 'height': height}
            )
            
            # Add to current dashboard or create new one
            if st.session_state.dashboard_builder_state['current_dashboard'] is None:
                # Create new dashboard
                dashboard_config = DashboardConfig(
                    dashboard_id=str(uuid.uuid4()),
                    title="Custom Dashboard",
                    description="Custom built dashboard",
                    theme=DashboardTheme.BUSINESS,
                    layout={'type': 'grid', 'rows': 12, 'columns': 12},
                    charts=[chart_config],
                    filters=[],
                    kpis=[],
                    text_blocks=[],
                    created_at=datetime.now(),
                    modified_at=datetime.now()
                )
                st.session_state.dashboard_builder_state['current_dashboard'] = dashboard_config
            else:
                # Add to existing dashboard
                st.session_state.dashboard_builder_state['current_dashboard'].charts.append(chart_config)
                st.session_state.dashboard_builder_state['current_dashboard'].modified_at = datetime.now()
            
            st.success(f"✅ Added {chart_title} to dashboard")
            st.rerun()
    
    def _render_chart_list_editor(self):
        """Render chart list with edit/delete options"""
        current_dashboard = st.session_state.dashboard_builder_state['current_dashboard']
        
        if not current_dashboard or not current_dashboard.charts:
            st.info("📝 No charts added yet. Use the 'Add Chart' tab to create your first chart.")
            return
        
        st.markdown("##### 📝 Manage Charts")
        
        for i, chart in enumerate(current_dashboard.charts):
            with st.expander(f"📊 {chart.title}", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Type:** {chart.chart_type.value}")
                    st.write(f"**Position:** Row {chart.position['row']}, Col {chart.position['col']}")
                    if chart.x_column:
                        st.write(f"**X-Axis:** {chart.x_column}")
                    if chart.y_column:
                        st.write(f"**Y-Axis:** {chart.y_column}")
                
                with col2:
                    if st.button(f"✏️ Edit", key=f"edit_{chart.chart_id}"):
                        st.session_state.dashboard_builder_state['selected_chart'] = chart.chart_id
                        st.session_state.dashboard_builder_state['edit_mode'] = True
                        st.rerun()
                
                with col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{chart.chart_id}"):
                        current_dashboard.charts.pop(i)
                        current_dashboard.modified_at = datetime.now()
                        st.success("Chart deleted")
                        st.rerun()
    
    def _render_dashboard_preview(self):
        """Render dashboard preview"""
        current_dashboard = st.session_state.dashboard_builder_state['current_dashboard']
        
        if not current_dashboard:
            st.info("📊 Create some charts first to see the dashboard preview.")
            return
        
        st.markdown("##### 👁️ Dashboard Preview")
        
        # Preview controls
        col1, col2, col3 = st.columns(3)
        with col1:
            show_grid = st.checkbox("Show Grid", value=True)
        with col2:
            interactive = st.checkbox("Interactive Mode", value=True)
        with col3:
            if st.button("🔄 Refresh Preview"):
                st.rerun()
        
        # Render dashboard
        self._render_dashboard_from_config(current_dashboard, show_grid=show_grid, interactive=interactive)
    
    def _render_dashboard_from_config(self, dashboard_config: DashboardConfig, 
                                    show_grid: bool = False, interactive: bool = True):
        """Render dashboard from configuration"""
        st.markdown(f"### {dashboard_config.title}")
        st.markdown(f"*{dashboard_config.description}*")
        
        if not dashboard_config.charts:
            st.warning("📊 No charts configured for this dashboard.")
            return
        
        # Create grid layout
        max_row = max(chart.position['row'] + chart.position['height'] for chart in dashboard_config.charts)
        
        # Render charts in grid
        current_row = 0
        while current_row <= max_row:
            # Find charts that start in this row
            row_charts = [chart for chart in dashboard_config.charts if chart.position['row'] == current_row]
            
            if row_charts:
                # Sort by column position
                row_charts.sort(key=lambda x: x.position['col'])
                
                # Create columns for this row
                col_widths = []
                charts_to_render = []
                
                for chart in row_charts:
                    col_widths.append(chart.position['width'])
                    charts_to_render.append(chart)
                
                # Ensure we don't exceed 12 columns
                total_width = sum(col_widths)
                if total_width > 12:
                    # Normalize widths
                    col_widths = [int(w * 12 / total_width) for w in col_widths]
                
                # Create columns and render charts
                if col_widths:
                    cols = st.columns(col_widths)
                    
                    for col, chart in zip(cols, charts_to_render):
                        with col:
                            self._render_single_chart_from_config(chart, interactive)
            
            current_row += 1
    
    def _render_single_chart_from_config(self, chart_config: ChartConfig, interactive: bool = True):
        """Render a single chart from configuration"""
        try:
            # Apply filters if any
            filtered_data = self._apply_chart_filters(self.data, chart_config.filter_conditions)
            
            # Create the chart based on configuration
            chart = self._create_chart_from_config(chart_config, filtered_data)
            
            if chart:
                st.plotly_chart(chart, use_container_width=True, key=chart_config.chart_id)
            else:
                st.error(f"Failed to create chart: {chart_config.title}")
                
        except Exception as e:
            st.error(f"Error rendering chart '{chart_config.title}': {str(e)}")
    
    def _create_chart_from_config(self, config: ChartConfig, data: pd.DataFrame) -> Optional[go.Figure]:
        """Create a Plotly chart from configuration"""
        try:
            chart_type = config.chart_type
            
            if chart_type == ChartType.LINE:
                return self.visualizer.create_line_chart(
                    data, config.x_column, config.y_column, 
                    color_column=config.color_column, title=config.title
                )
            elif chart_type == ChartType.BAR:
                return self.visualizer.create_bar_chart(
                    data, config.x_column, config.y_column,
                    color_column=config.color_column, title=config.title
                )
            elif chart_type == ChartType.SCATTER:
                return self.visualizer.create_scatter_plot(
                    data, config.x_column, config.y_column,
                    color_column=config.color_column, size_column=config.size_column,
                    title=config.title
                )
            elif chart_type == ChartType.PIE:
                return self.visualizer.create_pie_chart(
                    data, config.color_column, config.y_column, title=config.title
                )
            elif chart_type == ChartType.HISTOGRAM:
                return self.visualizer.create_histogram(
                    data, config.x_column, title=config.title
                )
            elif chart_type == ChartType.BOX:
                return self.visualizer.create_box_plot(
                    data, config.x_column, config.y_column, title=config.title
                )
            elif chart_type == ChartType.HEATMAP:
                return self.visualizer.create_correlation_heatmap(data, title=config.title)
            # Add more chart types as needed
            
            return None
            
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
            return None
    
    def _apply_chart_filters(self, data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to data for chart"""
        filtered_data = data.copy()
        
        if not filters:
            return filtered_data
        
        for column, filter_config in filters.items():
            if column not in filtered_data.columns:
                continue
            
            filter_type = filter_config.get('type', 'equals')
            filter_value = filter_config.get('value')
            
            if filter_type == 'equals':
                filtered_data = filtered_data[filtered_data[column] == filter_value]
            elif filter_type == 'range':
                min_val, max_val = filter_value
                filtered_data = filtered_data[
                    (filtered_data[column] >= min_val) & (filtered_data[column] <= max_val)
                ]
            elif filter_type == 'contains':
                filtered_data = filtered_data[filtered_data[column].str.contains(filter_value, na=False)]
        
        return filtered_data
    
    def _generate_ai_dashboard(self, prompt: str, focus_area: str, detail_level: str) -> DashboardConfig:
        """Generate dashboard using AI-like logic (simulated)"""
        # This is a simplified AI simulation - in practice, you'd use actual AI/LLM
        
        dashboard_id = str(uuid.uuid4())
        
        # Map focus area to template
        focus_template_map = {
            "Sales": "sales_analytics",
            "Finance": "financial_dashboard", 
            "Operations": "operational_metrics",
            "Marketing": "marketing_performance",
            "Customer": "customer_insights",
            "General": "executive_summary"
        }
        
        template_name = focus_template_map.get(focus_area, "executive_summary")
        
        # Create dashboard from template
        dashboard_config = DashboardTemplate.create_dashboard_from_template(
            template_name, self.data, DashboardTheme.MODERN
        )
        
        # Customize based on prompt (simplified logic)
        dashboard_config.title = f"AI-Generated {focus_area} Dashboard"
        dashboard_config.description = f"AI-generated dashboard based on: {prompt[:100]}..."
        
        return dashboard_config


# Export main classes
__all__ = [
    'DashboardTheme',
    'ChartType',
    'ChartConfig',
    'DashboardConfig',
    'DashboardTemplate',
    'ChartGenerator',
    'InteractiveDashboardBuilder'
]
