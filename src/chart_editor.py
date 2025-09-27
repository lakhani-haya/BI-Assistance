"""
Advanced Chart Configuration and Styling System
Provides interactive chart editing, styling, and customization capabilities
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import json
import copy
from enum import Enum

# Import dashboard components
from src.dashboard_builder import ChartConfig, ChartType


class ColorScheme(Enum):
    """Predefined color schemes"""
    BUSINESS = "business"
    VIBRANT = "vibrant"
    PASTEL = "pastel"
    DARK = "dark"
    MONOCHROME = "monochrome"
    OCEAN = "ocean"
    SUNSET = "sunset"
    FOREST = "forest"
    CUSTOM = "custom"


class ChartAnimation(Enum):
    """Chart animation options"""
    NONE = "none"
    FADE_IN = "fade_in"
    SLIDE_UP = "slide_up"
    GROW = "grow"
    BOUNCE = "bounce"


@dataclass
class ChartStyling:
    """Complete chart styling configuration"""
    # Colors
    color_scheme: ColorScheme = ColorScheme.BUSINESS
    custom_colors: List[str] = None
    background_color: str = "white"
    plot_background_color: str = "white"
    
    # Typography
    title_font_size: int = 18
    title_font_family: str = "Arial"
    axis_font_size: int = 12
    axis_font_family: str = "Arial"
    legend_font_size: int = 10
    
    # Layout
    margin_top: int = 50
    margin_bottom: int = 50
    margin_left: int = 50
    margin_right: int = 50
    show_legend: bool = True
    legend_position: str = "right"
    
    # Grid and axes
    show_grid: bool = True
    grid_color: str = "#E0E0E0"
    grid_width: int = 1
    show_x_axis: bool = True
    show_y_axis: bool = True
    axis_line_color: str = "#000000"
    
    # Interactivity
    show_hover: bool = True
    hover_template: str = ""
    click_action: str = "none"
    zoom_enabled: bool = True
    pan_enabled: bool = True
    
    # Animation
    animation: ChartAnimation = ChartAnimation.NONE
    animation_duration: int = 750
    
    # Annotations
    annotations: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.custom_colors is None:
            self.custom_colors = []
        if self.annotations is None:
            self.annotations = []


class InteractiveChartEditor:
    """Interactive chart editor with real-time preview"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.color_palettes = self._get_color_palettes()
    
    def render_chart_editor(self, chart_config: ChartConfig) -> Tuple[ChartConfig, ChartStyling]:
        """Render interactive chart editor interface"""
        st.markdown("## 🎨 Chart Editor")
        
        # Create tabs for different editing aspects
        editor_tabs = st.tabs([
            "Data & Structure", 
            "🎨 Styling", 
            "📐 Layout", 
            "🔧 Advanced", 
            "👁️ Preview"
        ])
        
        # Initialize styling if not in session state
        styling_key = f"chart_styling_{chart_config.chart_id}"
        if styling_key not in st.session_state:
            st.session_state[styling_key] = ChartStyling()
        
        current_styling = st.session_state[styling_key]
        
        with editor_tabs[0]:
            updated_config = self._render_data_structure_editor(chart_config)
        
        with editor_tabs[1]:
            updated_styling = self._render_styling_editor(current_styling)
            st.session_state[styling_key] = updated_styling
        
        with editor_tabs[2]:
            updated_styling = self._render_layout_editor(st.session_state[styling_key])
            st.session_state[styling_key] = updated_styling
        
        with editor_tabs[3]:
            updated_styling = self._render_advanced_editor(st.session_state[styling_key])
            st.session_state[styling_key] = updated_styling
        
        with editor_tabs[4]:
            self._render_chart_preview(updated_config, st.session_state[styling_key])
        
        return updated_config, st.session_state[styling_key]
    
    def _render_data_structure_editor(self, chart_config: ChartConfig) -> ChartConfig:
        """Render data and structure editor"""
        st.markdown("### Data Configuration")
        
        # Create a copy to modify
        config = copy.deepcopy(chart_config)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic chart properties
            config.title = st.text_input("Chart Title", value=config.title)
            
            config.chart_type = ChartType(st.selectbox(
                "Chart Type",
                [ct.value for ct in ChartType],
                index=list(ChartType).index(config.chart_type)
            ))
        
        with col2:
            # Data columns
            all_columns = list(self.data.columns)
            
            if config.chart_type in [ChartType.LINE, ChartType.BAR, ChartType.SCATTER, ChartType.AREA]:
                config.x_column = st.selectbox(
                    "X-Axis Column",
                    [''] + all_columns,
                    index=all_columns.index(config.x_column) + 1 if config.x_column in all_columns else 0
                )
                
                config.y_column = st.selectbox(
                    "Y-Axis Column",
                    [''] + all_columns,
                    index=all_columns.index(config.y_column) + 1 if config.y_column in all_columns else 0
                )
            
            elif config.chart_type in [ChartType.PIE, ChartType.SUNBURST, ChartType.TREEMAP]:
                config.color_column = st.selectbox(
                    "Category Column",
                    [''] + all_columns,
                    index=all_columns.index(config.color_column) + 1 if config.color_column in all_columns else 0
                )
                
                config.y_column = st.selectbox(
                    "Value Column",
                    [''] + all_columns,
                    index=all_columns.index(config.y_column) + 1 if config.y_column in all_columns else 0
                )
        
        # Additional columns
        st.markdown("#### 🎨 Optional Styling Columns")
        col3, col4 = st.columns(2)
        
        with col3:
            config.color_column = st.selectbox(
                "Color By",
                [''] + all_columns,
                index=all_columns.index(config.color_column) + 1 if config.color_column and config.color_column in all_columns else 0,
                key="color_by_select"
            )
        
        with col4:
            if config.chart_type == ChartType.SCATTER:
                config.size_column = st.selectbox(
                    "Size By",
                    [''] + all_columns,
                    index=all_columns.index(config.size_column) + 1 if config.size_column and config.size_column in all_columns else 0
                )
        
        # Data filtering
        st.markdown("#### 🔍 Data Filters")
        with st.expander("Add Data Filters", expanded=False):
            self._render_filter_editor(config)
        
        # Aggregation settings
        if config.x_column and config.x_column in self.data.select_dtypes(include=['object', 'category']).columns:
            st.markdown("#### Aggregation")
            config.aggregation = st.selectbox(
                "Aggregation Method",
                ['sum', 'mean', 'count', 'max', 'min', 'median'],
                index=['sum', 'mean', 'count', 'max', 'min', 'median'].index(config.aggregation) if config.aggregation else 0
            )
        
        return config
    
    def _render_styling_editor(self, styling: ChartStyling) -> ChartStyling:
        """Render styling editor"""
        st.markdown("### 🎨 Chart Styling")
        
        # Color scheme
        col1, col2 = st.columns(2)
        
        with col1:
            styling.color_scheme = ColorScheme(st.selectbox(
                "Color Scheme",
                [cs.value for cs in ColorScheme],
                index=list(ColorScheme).index(styling.color_scheme)
            ))
            
            if styling.color_scheme == ColorScheme.CUSTOM:
                st.markdown("**Custom Colors:**")
                num_colors = st.number_input("Number of Colors", min_value=1, max_value=20, value=max(1, len(styling.custom_colors)))
                
                styling.custom_colors = []
                for i in range(int(num_colors)):
                    color = st.color_picker(f"Color {i+1}", value="#1f77b4" if i == 0 else "#ff7f0e")
                    styling.custom_colors.append(color)
        
        with col2:
            styling.background_color = st.color_picker("Background Color", value=styling.background_color)
            styling.plot_background_color = st.color_picker("Plot Background", value=styling.plot_background_color)
        
        # Typography
        st.markdown("#### 📝 Typography")
        col3, col4 = st.columns(2)
        
        with col3:
            styling.title_font_size = st.number_input("Title Font Size", min_value=8, max_value=48, value=styling.title_font_size)
            styling.title_font_family = st.selectbox(
                "Title Font",
                ["Arial", "Times New Roman", "Helvetica", "Georgia", "Verdana", "Courier New"],
                index=["Arial", "Times New Roman", "Helvetica", "Georgia", "Verdana", "Courier New"].index(styling.title_font_family)
            )
        
        with col4:
            styling.axis_font_size = st.number_input("Axis Font Size", min_value=6, max_value=24, value=styling.axis_font_size)
            styling.axis_font_family = st.selectbox(
                "Axis Font",
                ["Arial", "Times New Roman", "Helvetica", "Georgia", "Verdana", "Courier New"],
                index=["Arial", "Times New Roman", "Helvetica", "Georgia", "Verdana", "Courier New"].index(styling.axis_font_family)
            )
        
        # Grid and axes
        st.markdown("#### 📐 Grid & Axes")
        col5, col6 = st.columns(2)
        
        with col5:
            styling.show_grid = st.checkbox("Show Grid", value=styling.show_grid)
            if styling.show_grid:
                styling.grid_color = st.color_picker("Grid Color", value=styling.grid_color)
                styling.grid_width = st.number_input("Grid Width", min_value=1, max_value=5, value=styling.grid_width)
        
        with col6:
            styling.show_x_axis = st.checkbox("Show X-Axis", value=styling.show_x_axis)
            styling.show_y_axis = st.checkbox("Show Y-Axis", value=styling.show_y_axis)
            styling.axis_line_color = st.color_picker("Axis Line Color", value=styling.axis_line_color)
        
        return styling
    
    def _render_layout_editor(self, styling: ChartStyling) -> ChartStyling:
        """Render layout editor"""
        st.markdown("### 📐 Layout Configuration")
        
        # Margins
        st.markdown("#### 📏 Margins")
        col1, col2 = st.columns(2)
        
        with col1:
            styling.margin_top = st.number_input("Top Margin", min_value=0, max_value=200, value=styling.margin_top)
            styling.margin_bottom = st.number_input("Bottom Margin", min_value=0, max_value=200, value=styling.margin_bottom)
        
        with col2:
            styling.margin_left = st.number_input("Left Margin", min_value=0, max_value=200, value=styling.margin_left)
            styling.margin_right = st.number_input("Right Margin", min_value=0, max_value=200, value=styling.margin_right)
        
        # Legend
        st.markdown("#### 🏷️ Legend")
        col3, col4 = st.columns(2)
        
        with col3:
            styling.show_legend = st.checkbox("Show Legend", value=styling.show_legend)
        
        with col4:
            if styling.show_legend:
                styling.legend_position = st.selectbox(
                    "Legend Position",
                    ["right", "top", "bottom", "left"],
                    index=["right", "top", "bottom", "left"].index(styling.legend_position)
                )
                
                styling.legend_font_size = st.number_input(
                    "Legend Font Size", 
                    min_value=6, 
                    max_value=20, 
                    value=styling.legend_font_size
                )
        
        return styling
    
    def _render_advanced_editor(self, styling: ChartStyling) -> ChartStyling:
        """Render advanced editor"""
        st.markdown("### 🔧 Advanced Settings")
        
        # Interactivity
        st.markdown("#### 🖱️ Interactivity")
        col1, col2 = st.columns(2)
        
        with col1:
            styling.show_hover = st.checkbox("Show Hover Info", value=styling.show_hover)
            styling.zoom_enabled = st.checkbox("Enable Zoom", value=styling.zoom_enabled)
        
        with col2:
            styling.pan_enabled = st.checkbox("Enable Pan", value=styling.pan_enabled)
            styling.click_action = st.selectbox(
                "Click Action",
                ["none", "select", "filter", "drill_down"],
                index=["none", "select", "filter", "drill_down"].index(styling.click_action)
            )
        
        # Custom hover template
        if styling.show_hover:
            styling.hover_template = st.text_area(
                "Custom Hover Template",
                value=styling.hover_template,
                placeholder="<b>%{x}</b><br>Value: %{y}<extra></extra>",
                help="Use Plotly hover template syntax"
            )
        
        # Animation
        st.markdown("#### 🎬 Animation")
        col3, col4 = st.columns(2)
        
        with col3:
            styling.animation = ChartAnimation(st.selectbox(
                "Animation Type",
                [anim.value for anim in ChartAnimation],
                index=list(ChartAnimation).index(styling.animation)
            ))
        
        with col4:
            if styling.animation != ChartAnimation.NONE:
                styling.animation_duration = st.number_input(
                    "Animation Duration (ms)",
                    min_value=100,
                    max_value=5000,
                    value=styling.animation_duration
                )
        
        # Annotations
        st.markdown("#### 📝 Annotations")
        with st.expander("Add Annotations", expanded=False):
            self._render_annotation_editor(styling)
        
        return styling
    
    def _render_filter_editor(self, config: ChartConfig):
        """Render filter editor"""
        if config.filter_conditions is None:
            config.filter_conditions = {}
        
        st.markdown("Add filters to modify the data shown in this chart:")
        
        # Add new filter
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_column = st.selectbox(
                "Filter Column",
                [''] + list(self.data.columns),
                key=f"filter_col_{config.chart_id}"
            )
        
        if filter_column:
            with col2:
                if self.data[filter_column].dtype in ['object', 'category']:
                    unique_values = self.data[filter_column].unique()
                    filter_values = st.multiselect(
                        "Values",
                        unique_values,
                        key=f"filter_vals_{config.chart_id}"
                    )
                    
                    if filter_values:
                        config.filter_conditions[filter_column] = {
                            'type': 'in',
                            'value': filter_values
                        }
                
                else:  # Numeric column
                    min_val, max_val = float(self.data[filter_column].min()), float(self.data[filter_column].max())
                    filter_range = st.slider(
                        "Range",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        key=f"filter_range_{config.chart_id}"
                    )
                    
                    if filter_range != (min_val, max_val):
                        config.filter_conditions[filter_column] = {
                            'type': 'range',
                            'value': filter_range
                        }
            
            with col3:
                if st.button("Add Filter", key=f"add_filter_{config.chart_id}"):
                    st.success("Filter added!")
        
        # Display current filters
        if config.filter_conditions:
            st.markdown("**Active Filters:**")
            for column, filter_config in config.filter_conditions.items():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"• {column}: {filter_config['value']}")
                with col_b:
                    if st.button("Remove", key=f"remove_filter_{column}_{config.chart_id}"):
                        del config.filter_conditions[column]
                        st.rerun()
    
    def _render_annotation_editor(self, styling: ChartStyling):
        """Render annotation editor"""
        st.markdown("Add text annotations to your chart:")
        
        # Add new annotation
        col1, col2 = st.columns(2)
        
        with col1:
            ann_text = st.text_input("Annotation Text", key="ann_text")
            ann_x = st.number_input("X Position", value=0.5, key="ann_x")
            ann_y = st.number_input("Y Position", value=0.5, key="ann_y")
        
        with col2:
            ann_color = st.color_picker("Text Color", value="#000000", key="ann_color")
            ann_size = st.number_input("Font Size", min_value=8, max_value=32, value=12, key="ann_size")
            ann_arrow = st.checkbox("Show Arrow", key="ann_arrow")
        
        if st.button("Add Annotation") and ann_text:
            annotation = {
                'text': ann_text,
                'x': ann_x,
                'y': ann_y,
                'font': {'color': ann_color, 'size': ann_size},
                'showarrow': ann_arrow
            }
            styling.annotations.append(annotation)
            st.success("Annotation added!")
            st.rerun()
        
        # Display current annotations
        if styling.annotations:
            st.markdown("**Current Annotations:**")
            for i, ann in enumerate(styling.annotations):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"• {ann['text']} at ({ann['x']}, {ann['y']})")
                with col_b:
                    if st.button("Remove", key=f"remove_ann_{i}"):
                        styling.annotations.pop(i)
                        st.rerun()
    
    def _render_chart_preview(self, config: ChartConfig, styling: ChartStyling):
        """Render real-time chart preview"""
        st.markdown("### 👁️ Live Preview")
        
        preview_col1, preview_col2 = st.columns([3, 1])
        
        with preview_col2:
            if st.button("🔄 Refresh Preview"):
                st.rerun()
            
            show_code = st.checkbox("Show Code", value=False)
            
            if st.button("💾 Save Configuration"):
                config_data = {
                    'config': asdict(config),
                    'styling': asdict(styling)
                }
                
                st.download_button(
                    "📥 Download Config",
                    data=json.dumps(config_data, indent=2, default=str),
                    file_name=f"chart_config_{config.chart_id}.json",
                    mime="application/json"
                )
        
        with preview_col1:
            try:
                # Create chart with styling
                chart = self._create_styled_chart(config, styling)
                
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                    
                    if show_code:
                        st.markdown("#### 🔧 Generated Code")
                        st.code(self._generate_chart_code(config, styling), language="python")
                else:
                    st.error("Unable to create chart preview")
                    
            except Exception as e:
                st.error(f"Preview Error: {str(e)}")
                st.info("Check your data configuration and try again.")
    
    def _create_styled_chart(self, config: ChartConfig, styling: ChartStyling) -> go.Figure:
        """Create a styled chart from configuration"""
        # Apply filters to data
        filtered_data = self._apply_filters(self.data, config.filter_conditions)
        
        if filtered_data.empty:
            st.warning("No data available after applying filters.")
            return None
        
        # Create base chart
        fig = self._create_base_chart(config, filtered_data)
        
        if fig is None:
            return None
        
        # Apply styling
        fig = self._apply_styling(fig, styling)
        
        return fig
    
    def _create_base_chart(self, config: ChartConfig, data: pd.DataFrame) -> go.Figure:
        """Create base chart without styling"""
        chart_type = config.chart_type
        
        try:
            if chart_type == ChartType.LINE:
                fig = px.line(
                    data, 
                    x=config.x_column, 
                    y=config.y_column,
                    color=config.color_column,
                    title=config.title
                )
            
            elif chart_type == ChartType.BAR:
                if config.aggregation and config.x_column in data.select_dtypes(include=['object', 'category']).columns:
                    agg_data = data.groupby(config.x_column)[config.y_column].agg(config.aggregation).reset_index()
                    fig = px.bar(
                        agg_data,
                        x=config.x_column,
                        y=config.y_column,
                        color=config.color_column,
                        title=config.title
                    )
                else:
                    fig = px.bar(
                        data,
                        x=config.x_column,
                        y=config.y_column,
                        color=config.color_column,
                        title=config.title
                    )
            
            elif chart_type == ChartType.SCATTER:
                fig = px.scatter(
                    data,
                    x=config.x_column,
                    y=config.y_column,
                    color=config.color_column,
                    size=config.size_column,
                    title=config.title
                )
            
            elif chart_type == ChartType.PIE:
                if config.aggregation:
                    agg_data = data.groupby(config.color_column)[config.y_column].agg(config.aggregation).reset_index()
                    fig = px.pie(
                        agg_data,
                        names=config.color_column,
                        values=config.y_column,
                        title=config.title
                    )
                else:
                    fig = px.pie(
                        data,
                        names=config.color_column,
                        values=config.y_column,
                        title=config.title
                    )
            
            elif chart_type == ChartType.HISTOGRAM:
                fig = px.histogram(
                    data,
                    x=config.x_column,
                    title=config.title
                )
            
            elif chart_type == ChartType.BOX:
                fig = px.box(
                    data,
                    x=config.x_column,
                    y=config.y_column,
                    title=config.title
                )
            
            elif chart_type == ChartType.AREA:
                fig = px.area(
                    data,
                    x=config.x_column,
                    y=config.y_column,
                    color=config.color_column,
                    title=config.title
                )
            
            else:
                st.warning(f"Chart type {chart_type.value} not yet implemented in editor")
                return None
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
            return None
    
    def _apply_styling(self, fig: go.Figure, styling: ChartStyling) -> go.Figure:
        """Apply styling to chart"""
        # Get colors
        colors = self._get_colors_for_scheme(styling.color_scheme, styling.custom_colors)
        
        # Update layout
        fig.update_layout(
            title={
                'font': {
                    'size': styling.title_font_size,
                    'family': styling.title_font_family
                }
            },
            font={
                'size': styling.axis_font_size,
                'family': styling.axis_font_family
            },
            paper_bgcolor=styling.background_color,
            plot_bgcolor=styling.plot_background_color,
            margin=dict(
                t=styling.margin_top,
                b=styling.margin_bottom,
                l=styling.margin_left,
                r=styling.margin_right
            ),
            showlegend=styling.show_legend
        )
        
        # Legend positioning
        if styling.show_legend:
            legend_config = {'font': {'size': styling.legend_font_size}}
            
            if styling.legend_position == "top":
                legend_config.update({'orientation': 'h', 'y': 1.02, 'x': 0.5, 'xanchor': 'center'})
            elif styling.legend_position == "bottom":
                legend_config.update({'orientation': 'h', 'y': -0.2, 'x': 0.5, 'xanchor': 'center'})
            elif styling.legend_position == "left":
                legend_config.update({'x': -0.1, 'y': 0.5, 'yanchor': 'middle'})
            else:  # right
                legend_config.update({'x': 1.02, 'y': 0.5, 'yanchor': 'middle'})
            
            fig.update_layout(legend=legend_config)
        
        # Grid and axes
        fig.update_xaxes(
            visible=styling.show_x_axis,
            showgrid=styling.show_grid,
            gridcolor=styling.grid_color,
            gridwidth=styling.grid_width,
            linecolor=styling.axis_line_color
        )
        
        fig.update_yaxes(
            visible=styling.show_y_axis,
            showgrid=styling.show_grid,
            gridcolor=styling.grid_color,
            gridwidth=styling.grid_width,
            linecolor=styling.axis_line_color
        )
        
        # Colors
        if colors and len(colors) > 0:
            fig.update_traces(
                marker=dict(color=colors[0] if len(colors) == 1 else colors)
            )
        
        # Hover
        if styling.show_hover and styling.hover_template:
            fig.update_traces(hovertemplate=styling.hover_template)
        elif not styling.show_hover:
            fig.update_traces(hoverinfo="none")
        
        # Interactivity
        config_dict = {
            'scrollZoom': styling.zoom_enabled,
            'doubleClick': 'reset+autosize' if styling.zoom_enabled else False,
            'showTips': styling.show_hover,
            'displayModeBar': True
        }
        
        # Annotations
        if styling.annotations:
            fig.update_layout(annotations=styling.annotations)
        
        return fig
    
    def _apply_filters(self, data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to data"""
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
            elif filter_type == 'in':
                filtered_data = filtered_data[filtered_data[column].isin(filter_value)]
            elif filter_type == 'range':
                min_val, max_val = filter_value
                filtered_data = filtered_data[
                    (filtered_data[column] >= min_val) & (filtered_data[column] <= max_val)
                ]
            elif filter_type == 'contains':
                filtered_data = filtered_data[filtered_data[column].str.contains(filter_value, na=False)]
        
        return filtered_data
    
    def _get_colors_for_scheme(self, scheme: ColorScheme, custom_colors: List[str]) -> List[str]:
        """Get color palette for scheme"""
        if scheme == ColorScheme.CUSTOM and custom_colors:
            return custom_colors
        
        return self.color_palettes.get(scheme.value, self.color_palettes['business'])
    
    def _get_color_palettes(self) -> Dict[str, List[str]]:
        """Get predefined color palettes"""
        return {
            'business': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
            'vibrant': ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'],
            'pastel': ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc'],
            'dark': ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7', '#ecf0f1'],
            'monochrome': ['#2c3e50', '#34495e', '#5d6d7e', '#85929e', '#aeb6bf', '#d5dbdb'],
            'ocean': ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a'],
            'sunset': ['#ffd700', '#ffb347', '#ff6347', '#ff1493', '#8b008b', '#4b0082'],
            'forest': ['#228b22', '#32cd32', '#90ee90', '#98fb98', '#f0fff0', '#006400']
        }
    
    def _generate_chart_code(self, config: ChartConfig, styling: ChartStyling) -> str:
        """Generate Python code for the chart"""
        code = f"""
# Chart Configuration: {config.title}
import plotly.express as px
import plotly.graph_objects as go

# Create chart
fig = px.{config.chart_type.value}(
    data,
    x='{config.x_column}',
    y='{config.y_column}',
"""
        
        if config.color_column:
            code += f"    color='{config.color_column}',\n"
        
        if config.size_column:
            code += f"    size='{config.size_column}',\n"
        
        code += f"""    title='{config.title}'
)

# Apply styling
fig.update_layout(
    title_font_size={styling.title_font_size},
    font_size={styling.axis_font_size},
    paper_bgcolor='{styling.background_color}',
    plot_bgcolor='{styling.plot_background_color}',
    showlegend={styling.show_legend}
)

fig.show()
"""
        
        return code


# Export main classes
__all__ = [
    'ColorScheme',
    'ChartAnimation', 
    'ChartStyling',
    'InteractiveChartEditor'
]
