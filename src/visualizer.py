"""
Visualization Engine for BI


"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple, Union
import logging
from datetime import datetime
import base64
import io
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for matplotlib
plt.style.use('default')
sns.set_palette("husl")


class ChartRecommendationEngine:
    """
    Intelligent chart recommendation based on data characteristics
    """
    
    @staticmethod
    def recommend_charts(data: pd.DataFrame, target_column: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Recommend appropriate chart types based on data characteristics
        
        Args:
            data (pd.DataFrame): Input data
            target_column (str, optional): Specific column to focus on
            
        Returns:
            List[Dict]: Recommended charts with rationale
        """
        recommendations = []
        
        if target_column and target_column in data.columns:
            # Focus on specific column
            recommendations.extend(ChartRecommendationEngine._analyze_single_column(data, target_column))
        else:
            # Analyze entire dataset
            recommendations.extend(ChartRecommendationEngine._analyze_dataset(data))
        
        return recommendations
    
    @staticmethod
    def _analyze_single_column(data: pd.DataFrame, column: str) -> List[Dict[str, Any]]:
        """Analyze single column and recommend charts"""
        recommendations = []
        col_data = data[column]
        
        if pd.api.types.is_numeric_dtype(col_data):
            # Numeric column
            recommendations.append({
                'chart_type': 'histogram',
                'title': f'Distribution of {column}',
                'rationale': 'Shows the distribution pattern of numeric values',
                'priority': 'high',
                'columns': [column]
            })
            
            recommendations.append({
                'chart_type': 'box',
                'title': f'{column} Box Plot',
                'rationale': 'Identifies outliers and quartile distribution',
                'priority': 'medium',
                'columns': [column]
            })
            
        elif pd.api.types.is_categorical_dtype(col_data) or col_data.dtype == 'object':
            # Categorical column
            unique_count = col_data.nunique()
            
            if unique_count <= 10:
                recommendations.append({
                    'chart_type': 'pie',
                    'title': f'{column} Distribution',
                    'rationale': f'Shows proportion of {unique_count} categories',
                    'priority': 'high',
                    'columns': [column]
                })
                
                recommendations.append({
                    'chart_type': 'bar',
                    'title': f'{column} Count',
                    'rationale': 'Compares frequency across categories',
                    'priority': 'high',
                    'columns': [column]
                })
            else:
                recommendations.append({
                    'chart_type': 'bar',
                    'title': f'Top 10 {column} Values',
                    'rationale': f'Shows most frequent values from {unique_count} categories',
                    'priority': 'high',
                    'columns': [column]
                })
        
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            # DateTime column
            recommendations.append({
                'chart_type': 'timeline',
                'title': f'{column} Timeline',
                'rationale': 'Shows temporal distribution of dates',
                'priority': 'high',
                'columns': [column]
            })
        
        return recommendations
    
    @staticmethod
    def _analyze_dataset(data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze entire dataset and recommend charts"""
        recommendations = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = data.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Correlation heatmap for numeric data
        if len(numeric_cols) >= 2:
            recommendations.append({
                'chart_type': 'correlation_heatmap',
                'title': 'Correlation Analysis',
                'rationale': f'Shows relationships between {len(numeric_cols)} numeric variables',
                'priority': 'high',
                'columns': numeric_cols
            })
        
        # Time series analysis
        if datetime_cols and numeric_cols:
            for date_col in datetime_cols[:1]:  # Use first date column
                for num_col in numeric_cols[:2]:  # Use first 2 numeric columns
                    recommendations.append({
                        'chart_type': 'time_series',
                        'title': f'{num_col} Over Time',
                        'rationale': 'Reveals temporal trends and patterns',
                        'priority': 'high',
                        'columns': [date_col, num_col]
                    })
        
        # Scatter plots for numeric relationships
        if len(numeric_cols) >= 2:
            for i, col1 in enumerate(numeric_cols[:3]):
                for col2 in numeric_cols[i+1:4]:
                    recommendations.append({
                        'chart_type': 'scatter',
                        'title': f'{col1} vs {col2}',
                        'rationale': 'Explores potential relationships between variables',
                        'priority': 'medium',
                        'columns': [col1, col2]
                    })
        
        # Categorical analysis
        if categorical_cols and numeric_cols:
            for cat_col in categorical_cols[:2]:
                for num_col in numeric_cols[:2]:
                    if data[cat_col].nunique() <= 10:  # Reasonable number of categories
                        recommendations.append({
                            'chart_type': 'grouped_bar',
                            'title': f'{num_col} by {cat_col}',
                            'rationale': 'Compares numeric values across categories',
                            'priority': 'medium',
                            'columns': [cat_col, num_col]
                        })
        
        return recommendations[:8]  # Limit to top 8 recommendations


class PlotlyVisualizer:
    """
    Creates interactive visualizations using Plotly
    """
    
    def __init__(self):
        self.color_palette = Config.COLOR_PALETTE
        self.default_width = Config.DEFAULT_CHART_WIDTH
        self.default_height = Config.DEFAULT_CHART_HEIGHT
        
    def create_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: Optional[str] = None,
                        color_col: Optional[str] = None, title: str = "Bar Chart") -> go.Figure:
        """Create interactive bar chart"""
        try:
            if y_col is None:
                # Count chart
                value_counts = data[x_col].value_counts().head(10)
                fig = px.bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    title=title,
                    labels={'x': x_col, 'y': 'Count'},
                    color_discrete_sequence=self.color_palette
                )
            else:
                # Aggregated bar chart
                if color_col:
                    fig = px.bar(data, x=x_col, y=y_col, color=color_col, title=title)
                else:
                    fig = px.bar(data, x=x_col, y=y_col, title=title,
                                color_discrete_sequence=self.color_palette)
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height,
                showlegend=True if color_col else False
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {str(e)}")
            return self._create_error_chart(f"Error creating bar chart: {str(e)}")
    
    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_col: str,
                         color_col: Optional[str] = None, title: str = "Line Chart") -> go.Figure:
        """Create interactive line chart"""
        try:
            if color_col:
                fig = px.line(data, x=x_col, y=y_col, color=color_col, title=title)
            else:
                fig = px.line(data, x=x_col, y=y_col, title=title,
                             color_discrete_sequence=self.color_palette)
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height,
                xaxis_title=x_col,
                yaxis_title=y_col
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating line chart: {str(e)}")
            return self._create_error_chart(f"Error creating line chart: {str(e)}")
    
    def create_scatter_plot(self, data: pd.DataFrame, x_col: str, y_col: str,
                           color_col: Optional[str] = None, size_col: Optional[str] = None,
                           title: str = "Scatter Plot") -> go.Figure:
        """Create interactive scatter plot"""
        try:
            fig = px.scatter(
                data, x=x_col, y=y_col, color=color_col, size=size_col,
                title=title, color_discrete_sequence=self.color_palette
            )
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating scatter plot: {str(e)}")
            return self._create_error_chart(f"Error creating scatter plot: {str(e)}")
    
    def create_pie_chart(self, data: pd.DataFrame, column: str, title: str = "Pie Chart") -> go.Figure:
        """Create interactive pie chart"""
        try:
            value_counts = data[column].value_counts().head(10)
            
            fig = px.pie(
                values=value_counts.values,
                names=value_counts.index,
                title=title,
                color_discrete_sequence=self.color_palette
            )
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating pie chart: {str(e)}")
            return self._create_error_chart(f"Error creating pie chart: {str(e)}")
    
    def create_histogram(self, data: pd.DataFrame, column: str, bins: int = 30,
                        title: str = "Histogram") -> go.Figure:
        """Create interactive histogram"""
        try:
            fig = px.histogram(
                data, x=column, nbins=bins, title=title,
                color_discrete_sequence=self.color_palette
            )
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height,
                xaxis_title=column,
                yaxis_title='Frequency'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating histogram: {str(e)}")
            return self._create_error_chart(f"Error creating histogram: {str(e)}")
    
    def create_box_plot(self, data: pd.DataFrame, y_col: str, x_col: Optional[str] = None,
                       title: str = "Box Plot") -> go.Figure:
        """Create interactive box plot"""
        try:
            fig = px.box(
                data, y=y_col, x=x_col, title=title,
                color_discrete_sequence=self.color_palette
            )
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating box plot: {str(e)}")
            return self._create_error_chart(f"Error creating box plot: {str(e)}")
    
    def create_correlation_heatmap(self, data: pd.DataFrame, title: str = "Correlation Heatmap") -> go.Figure:
        """Create correlation heatmap"""
        try:
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                return self._create_error_chart("No numeric data available for correlation analysis")
            
            corr_matrix = numeric_data.corr()
            
            fig = px.imshow(
                corr_matrix,
                title=title,
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating correlation heatmap: {str(e)}")
            return self._create_error_chart(f"Error creating correlation heatmap: {str(e)}")
    
    def create_time_series(self, data: pd.DataFrame, date_col: str, value_col: str,
                          color_col: Optional[str] = None, title: str = "Time Series") -> go.Figure:
        """Create time series chart"""
        try:
            # Ensure date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
                data[date_col] = pd.to_datetime(data[date_col])
            
            # Sort by date
            data_sorted = data.sort_values(date_col)
            
            if color_col:
                fig = px.line(data_sorted, x=date_col, y=value_col, color=color_col, title=title)
            else:
                fig = px.line(data_sorted, x=date_col, y=value_col, title=title,
                             color_discrete_sequence=self.color_palette)
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height,
                xaxis_title=date_col,
                yaxis_title=value_col
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating time series: {str(e)}")
            return self._create_error_chart(f"Error creating time series: {str(e)}")
    
    def create_grouped_bar(self, data: pd.DataFrame, x_col: str, y_col: str, color_col: str,
                          title: str = "Grouped Bar Chart") -> go.Figure:
        """Create grouped bar chart"""
        try:
            fig = px.bar(
                data, x=x_col, y=y_col, color=color_col, title=title,
                barmode='group'
            )
            
            fig.update_layout(
                width=self.default_width,
                height=self.default_height
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating grouped bar chart: {str(e)}")
            return self._create_error_chart(f"Error creating grouped bar chart: {str(e)}")
    
    def create_dashboard_layout(self, figures: List[go.Figure], 
                               titles: List[str], rows: int = 2, cols: int = 2) -> go.Figure:
        """Create dashboard with multiple charts"""
        try:
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=titles,
                specs=[[{"type": "xy"}] * cols for _ in range(rows)]
            )
            
            for i, chart_fig in enumerate(figures):
                row = i // cols + 1
                col = i % cols + 1
                
                if row <= rows and col <= cols:
                    # Add traces from the chart to the subplot
                    for trace in chart_fig.data:
                        fig.add_trace(trace, row=row, col=col)
            
            fig.update_layout(
                height=600 * rows,
                showlegend=False,
                title_text="Dashboard Overview"
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {str(e)}")
            return self._create_error_chart(f"Error creating dashboard: {str(e)}")
    
    def _create_error_chart(self, error_message: str) -> go.Figure:
        """Create error chart when visualization fails"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"Visualization Error:<br>{error_message}",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Chart Error",
            width=self.default_width,
            height=self.default_height,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig


class MatplotlibVisualizer:
    """
    Creates static visualizations using Matplotlib/Seaborn
    """
    
    def __init__(self):
        self.color_palette = Config.COLOR_PALETTE
        self.figsize = (Config.DEFAULT_CHART_WIDTH/100, Config.DEFAULT_CHART_HEIGHT/100)
    
    def create_summary_dashboard(self, data: pd.DataFrame) -> str:
        """Create comprehensive summary dashboard"""
        try:
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Data Summary Dashboard', fontsize=16, fontweight='bold')
            
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns
            
            # 1. Correlation heatmap (if numeric data available)
            if len(numeric_cols) >= 2:
                corr_matrix = data[numeric_cols].corr()
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                           ax=axes[0, 0], cbar_kws={'shrink': 0.8})
                axes[0, 0].set_title('Correlation Matrix')
            else:
                axes[0, 0].text(0.5, 0.5, 'No numeric data\nfor correlation', 
                               ha='center', va='center', fontsize=12)
                axes[0, 0].set_title('Correlation Matrix')
            
            # 2. Distribution of first numeric column
            if len(numeric_cols) > 0:
                col = numeric_cols[0]
                axes[0, 1].hist(data[col].dropna(), bins=30, alpha=0.7, color=self.color_palette[0])
                axes[0, 1].set_title(f'Distribution of {col}')
                axes[0, 1].set_xlabel(col)
                axes[0, 1].set_ylabel('Frequency')
            else:
                axes[0, 1].text(0.5, 0.5, 'No numeric data\navailable', 
                               ha='center', va='center', fontsize=12)
                axes[0, 1].set_title('Distribution')
            
            # 3. Top categories in first categorical column
            if len(categorical_cols) > 0:
                col = categorical_cols[0]
                top_categories = data[col].value_counts().head(10)
                axes[1, 0].bar(range(len(top_categories)), top_categories.values, 
                              color=self.color_palette[:len(top_categories)])
                axes[1, 0].set_title(f'Top Categories in {col}')
                axes[1, 0].set_xlabel(col)
                axes[1, 0].set_ylabel('Count')
                axes[1, 0].set_xticks(range(len(top_categories)))
                axes[1, 0].set_xticklabels(top_categories.index, rotation=45, ha='right')
            else:
                axes[1, 0].text(0.5, 0.5, 'No categorical data\navailable', 
                               ha='center', va='center', fontsize=12)
                axes[1, 0].set_title('Category Distribution')
            
            # 4. Missing values analysis
            missing_data = data.isnull().sum()
            missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
            
            if len(missing_data) > 0:
                axes[1, 1].bar(range(len(missing_data)), missing_data.values, 
                              color='red', alpha=0.7)
                axes[1, 1].set_title('Missing Values by Column')
                axes[1, 1].set_xlabel('Columns')
                axes[1, 1].set_ylabel('Missing Count')
                axes[1, 1].set_xticks(range(len(missing_data)))
                axes[1, 1].set_xticklabels(missing_data.index, rotation=45, ha='right')
            else:
                axes[1, 1].text(0.5, 0.5, 'No missing values\ndetected', 
                               ha='center', va='center', fontsize=12, color='green')
                axes[1, 1].set_title('Missing Values Analysis')
            
            plt.tight_layout()
            
            # Convert to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return img_str
            
        except Exception as e:
            logger.error(f"Error creating matplotlib dashboard: {str(e)}")
            return None
    
    def create_statistical_summary(self, data: pd.DataFrame) -> str:
        """Create statistical summary visualization"""
        try:
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return None
            
            # Create box plots for numeric columns
            fig, ax = plt.subplots(figsize=self.figsize)
            
            # Limit to first 6 columns for readability
            cols_to_plot = numeric_cols[:6]
            data_to_plot = []
            labels = []
            
            for col in cols_to_plot:
                clean_data = data[col].dropna()
                if len(clean_data) > 0:
                    data_to_plot.append(clean_data)
                    labels.append(col)
            
            if data_to_plot:
                bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
                
                # Color the boxes
                for patch, color in zip(bp['boxes'], self.color_palette):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                
                ax.set_title('Statistical Summary - Box Plots', fontsize=14, fontweight='bold')
                ax.set_ylabel('Values')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                # Convert to base64
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                img_str = base64.b64encode(img_buffer.read()).decode()
                plt.close()
                
                return img_str
            
            plt.close()
            return None
            
        except Exception as e:
            logger.error(f"Error creating statistical summary: {str(e)}")
            return None


class VisualizationEngine:
    """
    Main visualization engine that combines different visualization libraries
    """
    
    def __init__(self):
        self.plotly_viz = PlotlyVisualizer()
        self.matplotlib_viz = MatplotlibVisualizer()
        self.chart_recommender = ChartRecommendationEngine()
        
        logger.info("Visualization Engine initialized")
    
    def auto_visualize(self, data: pd.DataFrame, max_charts: int = 6) -> Dict[str, Any]:
        """
        Automatically create the best visualizations for the dataset
        
        Args:
            data (pd.DataFrame): Input data
            max_charts (int): Maximum number of charts to create
            
        Returns:
            Dict: Generated visualizations and recommendations
        """
        try:
            logger.info(f"Auto-generating visualizations for dataset with {len(data)} rows")
            
            # Get chart recommendations
            recommendations = self.chart_recommender.recommend_charts(data)
            
            # Sort by priority and limit
            high_priority = [r for r in recommendations if r['priority'] == 'high']
            medium_priority = [r for r in recommendations if r['priority'] == 'medium']
            
            selected_recommendations = (high_priority + medium_priority)[:max_charts]
            
            # Generate charts
            charts = []
            for rec in selected_recommendations:
                chart = self._create_chart_from_recommendation(data, rec)
                if chart:
                    charts.append({
                        'chart': chart,
                        'title': rec['title'],
                        'type': rec['chart_type'],
                        'rationale': rec['rationale'],
                        'columns_used': rec['columns']
                    })
            
            # Create summary dashboard with matplotlib
            summary_dashboard = self.matplotlib_viz.create_summary_dashboard(data)
            statistical_summary = self.matplotlib_viz.create_statistical_summary(data)
            
            results = {
                'interactive_charts': charts,
                'summary_dashboard': summary_dashboard,
                'statistical_summary': statistical_summary,
                'recommendations': recommendations,
                'charts_created': len(charts),
                'generated_at': datetime.now().isoformat()
            }
            
            logger.info(f"Generated {len(charts)} interactive charts and summary dashboards")
            return results
            
        except Exception as e:
            logger.error(f"Error in auto visualization: {str(e)}")
            return {
                'error': f"Visualization failed: {str(e)}",
                'interactive_charts': [],
                'recommendations': []
            }
    
    def create_custom_chart(self, data: pd.DataFrame, chart_type: str, 
                           chart_config: Dict[str, Any]) -> Optional[go.Figure]:
        """
        Create a custom chart based on user specifications
        
        Args:
            data (pd.DataFrame): Input data
            chart_type (str): Type of chart to create
            chart_config (Dict): Configuration for the chart
            
        Returns:
            Optional[go.Figure]: Generated chart or None if failed
        """
        try:
            chart_methods = {
                'bar': self.plotly_viz.create_bar_chart,
                'line': self.plotly_viz.create_line_chart,
                'scatter': self.plotly_viz.create_scatter_plot,
                'pie': self.plotly_viz.create_pie_chart,
                'histogram': self.plotly_viz.create_histogram,
                'box': self.plotly_viz.create_box_plot,
                'correlation_heatmap': self.plotly_viz.create_correlation_heatmap,
                'time_series': self.plotly_viz.create_time_series,
                'grouped_bar': self.plotly_viz.create_grouped_bar
            }
            
            method = chart_methods.get(chart_type)
            if not method:
                logger.warning(f"Unknown chart type: {chart_type}")
                return None
            
            # Call the appropriate method with configuration
            chart = method(data, **chart_config)
            
            logger.info(f"Created custom {chart_type} chart")
            return chart
            
        except Exception as e:
            logger.error(f"Error creating custom chart: {str(e)}")
            return None
    
    def _create_chart_from_recommendation(self, data: pd.DataFrame, 
                                         recommendation: Dict[str, Any]) -> Optional[go.Figure]:
        """Create chart based on recommendation"""
        try:
            chart_type = recommendation['chart_type']
            columns = recommendation['columns']
            title = recommendation['title']
            
            if chart_type == 'histogram' and len(columns) >= 1:
                return self.plotly_viz.create_histogram(data, columns[0], title=title)
            
            elif chart_type == 'box' and len(columns) >= 1:
                return self.plotly_viz.create_box_plot(data, columns[0], title=title)
            
            elif chart_type == 'pie' and len(columns) >= 1:
                return self.plotly_viz.create_pie_chart(data, columns[0], title=title)
            
            elif chart_type == 'bar' and len(columns) >= 1:
                return self.plotly_viz.create_bar_chart(data, columns[0], title=title)
            
            elif chart_type == 'correlation_heatmap':
                return self.plotly_viz.create_correlation_heatmap(data, title=title)
            
            elif chart_type == 'time_series' and len(columns) >= 2:
                return self.plotly_viz.create_time_series(data, columns[0], columns[1], title=title)
            
            elif chart_type == 'scatter' and len(columns) >= 2:
                return self.plotly_viz.create_scatter_plot(data, columns[0], columns[1], title=title)
            
            elif chart_type == 'grouped_bar' and len(columns) >= 3:
                return self.plotly_viz.create_grouped_bar(data, columns[0], columns[1], columns[2], title=title)
            
            else:
                logger.warning(f"Cannot create chart type {chart_type} with columns {columns}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating chart from recommendation: {str(e)}")
            return None
    
    def get_chart_explanation(self, chart_type: str, columns_used: List[str], 
                             data_sample: Dict[str, Any]) -> str:
        """
        Generate explanation for a chart (can be enhanced with AI integration)
        
        Args:
            chart_type (str): Type of chart
            columns_used (List[str]): Columns used in the chart
            data_sample (Dict): Sample data information
            
        Returns:
            str: Chart explanation
        """
        explanations = {
            'histogram': f"This histogram shows the distribution of values in {columns_used[0]}. It helps identify patterns like normal distribution, skewness, or multiple peaks in the data.",
            'box': f"This box plot displays the statistical summary of {columns_used[0]}, showing median, quartiles, and potential outliers.",
            'pie': f"This pie chart shows the proportion of different categories in {columns_used[0]}, making it easy to see which categories dominate.",
            'bar': f"This bar chart compares the frequency or values across different categories in {columns_used[0]}.",
            'correlation_heatmap': "This correlation heatmap reveals relationships between numeric variables. Strong correlations (near +1 or -1) indicate related variables.",
            'time_series': f"This time series chart shows how {columns_used[1]} changes over time ({columns_used[0]}), revealing trends and patterns.",
            'scatter': f"This scatter plot explores the relationship between {columns_used[0]} and {columns_used[1]}, helping identify correlations or clusters.",
            'grouped_bar': f"This grouped bar chart compares {columns_used[1]} across different {columns_used[0]} categories, grouped by {columns_used[2]}."
        }
        
        return explanations.get(chart_type, f"This {chart_type} chart visualizes the relationship between {', '.join(columns_used)}.")
    
    def export_charts(self, charts: List[go.Figure], output_dir: str, 
                     format: str = 'html') -> List[str]:
        """
        Export charts to files
        
        Args:
            charts (List[go.Figure]): Charts to export
            output_dir (str): Output directory
            format (str): Export format ('html', 'png', 'pdf')
            
        Returns:
            List[str]: List of created file paths
        """
        import os
        
        exported_files = []
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            for i, chart in enumerate(charts):
                filename = f"chart_{i+1}.{format}"
                filepath = os.path.join(output_dir, filename)
                
                if format == 'html':
                    chart.write_html(filepath)
                elif format == 'png':
                    chart.write_image(filepath)
                elif format == 'pdf':
                    chart.write_image(filepath)
                
                exported_files.append(filepath)
                
            logger.info(f"Exported {len(charts)} charts to {output_dir}")
            
        except Exception as e:
            logger.error(f"Error exporting charts: {str(e)}")
        
        return exported_files
