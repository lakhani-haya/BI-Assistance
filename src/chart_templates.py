"""
Chart templates and styling configurations for consistent visualizations
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from typing import Dict, List, Any, Optional
from src.config import Config


class ChartTemplates:
    """Pre-defined chart templates for common business scenarios"""
    
    @staticmethod
    def sales_dashboard_template(data_dict: Dict[str, Any]) -> go.Figure:
        """
        Create a comprehensive sales dashboard
        
        Args:
            data_dict (Dict): Dictionary containing:
                - 'revenue_over_time': DataFrame with date and revenue columns
                - 'sales_by_region': DataFrame with region and sales columns
                - 'product_performance': DataFrame with product and revenue columns
                - 'monthly_targets': DataFrame with month and target columns
        
        Returns:
            go.Figure: Complete sales dashboard
        """
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Revenue Trend Over Time',
                'Sales by Region', 
                'Top Product Performance',
                'Monthly Performance vs Target'
            ],
            specs=[
                [{"type": "scatter"}, {"type": "xy"}],
                [{"type": "xy"}, {"type": "scatter"}]
            ]
        )
        
        # Revenue over time (line chart)
        if 'revenue_over_time' in data_dict:
            df = data_dict['revenue_over_time']
            fig.add_trace(
                go.Scatter(
                    x=df['date'], y=df['revenue'],
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color=Config.COLOR_PALETTE[0], width=3)
                ),
                row=1, col=1
            )
        
        # Sales by region (bar chart)
        if 'sales_by_region' in data_dict:
            df = data_dict['sales_by_region']
            fig.add_trace(
                go.Bar(
                    x=df['region'], y=df['sales'],
                    name='Regional Sales',
                    marker_color=Config.COLOR_PALETTE[1]
                ),
                row=1, col=2
            )
        
        # Product performance (horizontal bar)
        if 'product_performance' in data_dict:
            df = data_dict['product_performance'].head(10)  # Top 10 products
            fig.add_trace(
                go.Bar(
                    x=df['revenue'], y=df['product'],
                    name='Product Revenue',
                    orientation='h',
                    marker_color=Config.COLOR_PALETTE[2]
                ),
                row=2, col=1
            )
        
        # Monthly targets vs actual
        if 'monthly_targets' in data_dict:
            df = data_dict['monthly_targets']
            fig.add_trace(
                go.Bar(
                    x=df['month'], y=df['actual'],
                    name='Actual',
                    marker_color=Config.COLOR_PALETTE[3]
                ),
                row=2, col=2
            )
            fig.add_trace(
                go.Scatter(
                    x=df['month'], y=df['target'],
                    mode='lines+markers',
                    name='Target',
                    line=dict(color='red', dash='dash')
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title="Sales Performance Dashboard",
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    @staticmethod
    def financial_overview_template(data_dict: Dict[str, Any]) -> go.Figure:
        """Create financial overview dashboard"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Revenue vs Expenses',
                'Profit Margin Trend',
                'Cost Breakdown',
                'Cash Flow Analysis'
            ]
        )
        
        # Revenue vs Expenses
        if 'revenue_expenses' in data_dict:
            df = data_dict['revenue_expenses']
            fig.add_trace(
                go.Bar(x=df['period'], y=df['revenue'], name='Revenue', 
                      marker_color=Config.COLOR_PALETTE[0]),
                row=1, col=1
            )
            fig.add_trace(
                go.Bar(x=df['period'], y=df['expenses'], name='Expenses',
                      marker_color=Config.COLOR_PALETTE[1]),
                row=1, col=1
            )
        
        # Profit margin trend
        if 'profit_margin' in data_dict:
            df = data_dict['profit_margin']
            fig.add_trace(
                go.Scatter(x=df['period'], y=df['margin'], 
                          mode='lines+markers', name='Profit Margin %',
                          line=dict(color=Config.COLOR_PALETTE[2])),
                row=1, col=2
            )
        
        # Cost breakdown (pie chart equivalent)
        if 'cost_breakdown' in data_dict:
            df = data_dict['cost_breakdown']
            fig.add_trace(
                go.Bar(x=df['category'], y=df['amount'],
                      name='Costs', marker_color=Config.COLOR_PALETTE[3:]),
                row=2, col=1
            )
        
        # Cash flow
        if 'cash_flow' in data_dict:
            df = data_dict['cash_flow']
            fig.add_trace(
                go.Waterfall(
                    x=df['category'], y=df['amount'],
                    name='Cash Flow'
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            title="Financial Overview Dashboard",
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    @staticmethod
    def operational_metrics_template(data_dict: Dict[str, Any]) -> go.Figure:
        """Create operational metrics dashboard"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Key Performance Indicators',
                'Process Efficiency Over Time',
                'Resource Utilization',
                'Quality Metrics'
            ]
        )
        
        # KPI gauge charts (simplified as bar charts)
        if 'kpis' in data_dict:
            df = data_dict['kpis']
            fig.add_trace(
                go.Bar(x=df['metric'], y=df['value'],
                      marker_color=Config.COLOR_PALETTE[0]),
                row=1, col=1
            )
        
        # Efficiency trend
        if 'efficiency' in data_dict:
            df = data_dict['efficiency']
            fig.add_trace(
                go.Scatter(x=df['date'], y=df['efficiency_score'],
                          mode='lines+markers', name='Efficiency',
                          line=dict(color=Config.COLOR_PALETTE[1])),
                row=1, col=2
            )
        
        # Resource utilization
        if 'resource_utilization' in data_dict:
            df = data_dict['resource_utilization']
            fig.add_trace(
                go.Bar(x=df['resource'], y=df['utilization_percent'],
                      marker_color=Config.COLOR_PALETTE[2]),
                row=2, col=1
            )
        
        # Quality metrics
        if 'quality_metrics' in data_dict:
            df = data_dict['quality_metrics']
            fig.add_trace(
                go.Scatter(x=df['date'], y=df['defect_rate'],
                          mode='lines+markers', name='Defect Rate',
                          line=dict(color='red')),
                row=2, col=2
            )
        
        fig.update_layout(
            title="Operational Metrics Dashboard",
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig


class ChartStyling:
    """Consistent styling configurations for charts"""
    
    BUSINESS_THEME = {
        'template': 'plotly_white',
        'color_palette': Config.COLOR_PALETTE,
        'font_family': 'Arial, sans-serif',
        'title_font_size': 18,
        'axis_font_size': 12,
        'legend_font_size': 10
    }
    
    EXECUTIVE_THEME = {
        'template': 'simple_white',
        'color_palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
        'font_family': 'Helvetica, Arial, sans-serif',
        'title_font_size': 20,
        'axis_font_size': 14,
        'legend_font_size': 12
    }
    
    PRESENTATION_THEME = {
        'template': 'plotly_dark',
        'color_palette': ['#636EFA', '#EF553B', '#00CC96', '#AB63FA'],
        'font_family': 'Calibri, Arial, sans-serif',
        'title_font_size': 24,
        'axis_font_size': 16,
        'legend_font_size': 14
    }
    
    @classmethod
    def apply_theme(cls, fig: go.Figure, theme_name: str = 'business') -> go.Figure:
        """Apply consistent theme to a figure"""
        
        themes = {
            'business': cls.BUSINESS_THEME,
            'executive': cls.EXECUTIVE_THEME,
            'presentation': cls.PRESENTATION_THEME
        }
        
        theme = themes.get(theme_name, cls.BUSINESS_THEME)
        
        fig.update_layout(
            template=theme['template'],
            font=dict(
                family=theme['font_family'],
                size=theme['axis_font_size']
            ),
            title=dict(
                font=dict(size=theme['title_font_size'])
            ),
            legend=dict(
                font=dict(size=theme['legend_font_size'])
            )
        )
        
        return fig
    
    @classmethod
    def get_color_sequence(cls, theme_name: str = 'business') -> List[str]:
        """Get color sequence for a theme"""
        themes = {
            'business': cls.BUSINESS_THEME,
            'executive': cls.EXECUTIVE_THEME,
            'presentation': cls.PRESENTATION_THEME
        }
        
        theme = themes.get(theme_name, cls.BUSINESS_THEME)
        return theme['color_palette']


class ChartAnnotations:
    """Helper class for adding annotations and insights to charts"""
    
    @staticmethod
    def add_trend_annotation(fig: go.Figure, x_pos: float, y_pos: float, 
                           trend_text: str, trend_type: str = 'positive') -> go.Figure:
        """Add trend annotation to chart"""
        
        colors = {
            'positive': 'green',
            'negative': 'red',
            'neutral': 'blue'
        }
        
        fig.add_annotation(
            x=x_pos, y=y_pos,
            text=trend_text,
            showarrow=True,
            arrowhead=2,
            arrowcolor=colors.get(trend_type, 'blue'),
            font=dict(color=colors.get(trend_type, 'blue'))
        )
        
        return fig
    
    @staticmethod
    def add_threshold_line(fig: go.Figure, threshold_value: float, 
                          line_name: str = 'Threshold', color: str = 'red') -> go.Figure:
        """Add horizontal threshold line to chart"""
        
        fig.add_hline(
            y=threshold_value,
            line_dash="dash",
            line_color=color,
            annotation_text=line_name
        )
        
        return fig
    
    @staticmethod
    def add_data_label(fig: go.Figure, x_pos: float, y_pos: float, 
                      label_text: str) -> go.Figure:
        """Add data label to specific point"""
        
        fig.add_annotation(
            x=x_pos, y=y_pos,
            text=label_text,
            showarrow=False,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        )
        
        return fig


class ResponsiveCharts:
    """Create responsive charts that adapt to different screen sizes"""
    
    @staticmethod
    def make_responsive(fig: go.Figure) -> go.Figure:
        """Make chart responsive for different devices"""
        
        fig.update_layout(
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50),
            # Responsive configuration
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar",
                            method="restyle"
                        )
                    ]),
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.01,
                    xanchor="left",
                    y=1.02,
                    yanchor="top"
                ),
            ]
        )
        
        return fig
    
    @staticmethod
    def mobile_optimized(fig: go.Figure) -> go.Figure:
        """Optimize chart for mobile display"""
        
        fig.update_layout(
            width=None,  # Let it be responsive
            height=400,  # Smaller height for mobile
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=10),  # Smaller font
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig


class InteractiveFeatures:
    """Add interactive features to charts"""
    
    @staticmethod
    def add_crossfilter(figures: List[go.Figure]) -> List[go.Figure]:
        """Add cross-filtering between multiple charts"""
        # This would typically involve JavaScript callbacks
        # For now, return charts with enhanced hover information
        
        for fig in figures:
            fig.update_traces(
                hovertemplate="<b>%{fullData.name}</b><br>" +
                             "Value: %{y}<br>" +
                             "Category: %{x}<br>" +
                             "<extra></extra>"
            )
        
        return figures
    
    @staticmethod
    def add_zoom_controls(fig: go.Figure) -> go.Figure:
        """Add zoom and pan controls"""
        
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        return fig
    
    @staticmethod
    def add_data_table(fig: go.Figure, data: dict) -> go.Figure:
        """Add data table below chart"""
        
        # This would be implemented in the dashboard layout
        # For now, add hover data
        fig.update_traces(
            hoverinfo="text",
            hovertext=[f"Value: {v}" for v in data.get('values', [])]
        )
        
        return fig


class ChartExporter:
    """Export charts in various formats"""
    
    @staticmethod
    def to_html_string(fig: go.Figure, include_plotlyjs: str = 'cdn') -> str:
        """Convert chart to HTML string"""
        return fig.to_html(include_plotlyjs=include_plotlyjs)
    
    @staticmethod
    def to_json(fig: go.Figure) -> str:
        """Convert chart to JSON string"""
        return fig.to_json()
    
    @staticmethod
    def to_image_bytes(fig: go.Figure, format: str = 'png') -> bytes:
        """Convert chart to image bytes"""
        return fig.to_image(format=format)
    
    @staticmethod
    def batch_export(figures: List[go.Figure], output_dir: str, 
                    formats: List[str] = ['html', 'png']) -> Dict[str, List[str]]:
        """Export multiple figures in multiple formats"""
        import os
        
        exported_files = {format: [] for format in formats}
        
        os.makedirs(output_dir, exist_ok=True)
        
        for i, fig in enumerate(figures):
            for format in formats:
                filename = f"chart_{i+1}.{format}"
                filepath = os.path.join(output_dir, filename)
                
                if format == 'html':
                    fig.write_html(filepath)
                elif format in ['png', 'jpg', 'pdf', 'svg']:
                    fig.write_image(filepath)
                
                exported_files[format].append(filepath)
        
        return exported_files
