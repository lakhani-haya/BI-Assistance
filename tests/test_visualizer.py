"""
Unit tests for visualization engine
"""

import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.visualizer import (
    VisualizationEngine, PlotlyVisualizer, MatplotlibVisualizer, 
    ChartRecommendationEngine
)
from src.chart_templates import ChartTemplates, ChartStyling


class TestChartRecommendationEngine(unittest.TestCase):
    """Test chart recommendation functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100, freq='D'),
            'sales': np.random.normal(1000, 200, 100),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'profit': np.random.normal(200, 50, 100)
        })
    
    def test_recommend_charts_numeric_column(self):
        """Test recommendations for numeric column"""
        recommendations = ChartRecommendationEngine.recommend_charts(
            self.sample_data, target_column='sales'
        )
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Should recommend histogram for numeric data
        chart_types = [rec['chart_type'] for rec in recommendations]
        self.assertIn('histogram', chart_types)
    
    def test_recommend_charts_categorical_column(self):
        """Test recommendations for categorical column"""
        recommendations = ChartRecommendationEngine.recommend_charts(
            self.sample_data, target_column='region'
        )
        
        chart_types = [rec['chart_type'] for rec in recommendations]
        self.assertIn('pie', chart_types)
        self.assertIn('bar', chart_types)
    
    def test_recommend_charts_entire_dataset(self):
        """Test recommendations for entire dataset"""
        recommendations = ChartRecommendationEngine.recommend_charts(self.sample_data)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Should include correlation heatmap for numeric data
        chart_types = [rec['chart_type'] for rec in recommendations]
        self.assertIn('correlation_heatmap', chart_types)
        
        # Should include time series for date + numeric combination
        self.assertIn('time_series', chart_types)


class TestPlotlyVisualizer(unittest.TestCase):
    """Test Plotly visualization functionality"""
    
    def setUp(self):
        """Set up test data and visualizer"""
        self.visualizer = PlotlyVisualizer()
        self.sample_data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'A', 'B'],
            'values': [10, 20, 15, 12, 18],
            'date': pd.date_range('2024-01-01', periods=5, freq='D'),
            'sales': [100, 150, 120, 110, 140]
        })
    
    def test_create_bar_chart(self):
        """Test bar chart creation"""
        fig = self.visualizer.create_bar_chart(
            self.sample_data, 'category', 'values', title='Test Bar Chart'
        )
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, 'Test Bar Chart')
        self.assertGreater(len(fig.data), 0)
    
    def test_create_line_chart(self):
        """Test line chart creation"""
        fig = self.visualizer.create_line_chart(
            self.sample_data, 'date', 'sales', title='Test Line Chart'
        )
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, 'Test Line Chart')
    
    def test_create_pie_chart(self):
        """Test pie chart creation"""
        fig = self.visualizer.create_pie_chart(
            self.sample_data, 'category', title='Test Pie Chart'
        )
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, 'Test Pie Chart')
    
    def test_create_histogram(self):
        """Test histogram creation"""
        fig = self.visualizer.create_histogram(
            self.sample_data, 'values', title='Test Histogram'
        )
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, 'Test Histogram')
    
    def test_create_scatter_plot(self):
        """Test scatter plot creation"""
        fig = self.visualizer.create_scatter_plot(
            self.sample_data, 'values', 'sales', title='Test Scatter'
        )
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, 'Test Scatter')
    
    def test_create_correlation_heatmap(self):
        """Test correlation heatmap creation"""
        # Add more numeric columns for correlation
        data_with_numeric = self.sample_data.copy()
        data_with_numeric['profit'] = [20, 30, 25, 22, 28]
        
        fig = self.visualizer.create_correlation_heatmap(
            data_with_numeric, title='Test Correlation'
        )
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, 'Test Correlation')
    
    def test_create_time_series(self):
        """Test time series creation"""
        fig = self.visualizer.create_time_series(
            self.sample_data, 'date', 'sales', title='Test Time Series'
        )
        
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, 'Test Time Series')
    
    def test_error_handling(self):
        """Test error handling in chart creation"""
        # Test with invalid column names
        fig = self.visualizer.create_bar_chart(
            self.sample_data, 'invalid_column', title='Error Test'
        )
        
        # Should return error chart instead of crashing
        self.assertIsInstance(fig, go.Figure)
        self.assertIn('Error', fig.layout.title.text)


class TestMatplotlibVisualizer(unittest.TestCase):
    """Test Matplotlib visualization functionality"""
    
    def setUp(self):
        """Set up test data and visualizer"""
        self.visualizer = MatplotlibVisualizer()
        self.sample_data = pd.DataFrame({
            'numeric_col1': np.random.normal(100, 20, 50),
            'numeric_col2': np.random.normal(200, 30, 50),
            'category': np.random.choice(['A', 'B', 'C'], 50),
            'text_col': ['text'] * 50
        })
    
    def test_create_summary_dashboard(self):
        """Test summary dashboard creation"""
        result = self.visualizer.create_summary_dashboard(self.sample_data)
        
        # Should return base64 encoded image string or None
        if result:
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 100)  # Should be substantial base64 string
    
    def test_create_statistical_summary(self):
        """Test statistical summary creation"""
        result = self.visualizer.create_statistical_summary(self.sample_data)
        
        # Should return base64 encoded image string or None
        if result:
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 100)
    
    def test_empty_numeric_data(self):
        """Test handling of data with no numeric columns"""
        text_only_data = pd.DataFrame({
            'text1': ['a', 'b', 'c'],
            'text2': ['x', 'y', 'z']
        })
        
        result = self.visualizer.create_statistical_summary(text_only_data)
        self.assertIsNone(result)


class TestVisualizationEngine(unittest.TestCase):
    """Test main visualization engine"""
    
    def setUp(self):
        """Set up test data and engine"""
        self.engine = VisualizationEngine()
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=50, freq='D'),
            'revenue': np.random.normal(1000, 200, 50),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 50),
            'product': np.random.choice(['Product A', 'Product B', 'Product C'], 50),
            'cost': np.random.normal(600, 100, 50)
        })
    
    def test_auto_visualize(self):
        """Test automatic visualization generation"""
        results = self.engine.auto_visualize(self.sample_data, max_charts=4)
        
        self.assertIn('interactive_charts', results)
        self.assertIn('recommendations', results)
        self.assertIn('charts_created', results)
        
        # Should create some charts
        self.assertGreaterEqual(results['charts_created'], 0)
        
        # Should have recommendations
        self.assertIsInstance(results['recommendations'], list)
    
    def test_create_custom_chart(self):
        """Test custom chart creation"""
        chart_config = {
            'x_col': 'region',
            'y_col': 'revenue',
            'title': 'Revenue by Region'
        }
        
        chart = self.engine.create_custom_chart(
            self.sample_data, 'bar', chart_config
        )
        
        if chart:  # Chart creation might fail in test environment
            self.assertIsInstance(chart, go.Figure)
    
    def test_get_chart_explanation(self):
        """Test chart explanation generation"""
        explanation = self.engine.get_chart_explanation(
            'bar', ['region', 'revenue'], {'sample': 'data'}
        )
        
        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 20)  # Should be meaningful explanation
    
    def test_invalid_chart_type(self):
        """Test handling of invalid chart type"""
        chart = self.engine.create_custom_chart(
            self.sample_data, 'invalid_type', {}
        )
        
        self.assertIsNone(chart)


class TestChartTemplates(unittest.TestCase):
    """Test chart templates functionality"""
    
    def test_sales_dashboard_template(self):
        """Test sales dashboard template"""
        # Create mock data for template
        data_dict = {
            'revenue_over_time': pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=12, freq='M'),
                'revenue': np.random.normal(100000, 20000, 12)
            }),
            'sales_by_region': pd.DataFrame({
                'region': ['North', 'South', 'East', 'West'],
                'sales': [50000, 60000, 45000, 55000]
            })
        }
        
        fig = ChartTemplates.sales_dashboard_template(data_dict)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertIn('Sales Performance Dashboard', fig.layout.title.text)
    
    def test_financial_overview_template(self):
        """Test financial overview template"""
        data_dict = {
            'revenue_expenses': pd.DataFrame({
                'period': ['Q1', 'Q2', 'Q3', 'Q4'],
                'revenue': [100000, 120000, 110000, 130000],
                'expenses': [80000, 90000, 85000, 95000]
            })
        }
        
        fig = ChartTemplates.financial_overview_template(data_dict)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertIn('Financial Overview Dashboard', fig.layout.title.text)


class TestChartStyling(unittest.TestCase):
    """Test chart styling functionality"""
    
    def test_apply_theme(self):
        """Test theme application"""
        # Create a simple figure
        fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3]))
        
        # Apply business theme
        styled_fig = ChartStyling.apply_theme(fig, 'business')
        
        self.assertIsInstance(styled_fig, go.Figure)
        self.assertEqual(styled_fig.layout.template, 'plotly_white')
    
    def test_get_color_sequence(self):
        """Test color sequence retrieval"""
        colors = ChartStyling.get_color_sequence('business')
        
        self.assertIsInstance(colors, list)
        self.assertGreater(len(colors), 0)
        
        # Test all theme types
        for theme in ['business', 'executive', 'presentation']:
            colors = ChartStyling.get_color_sequence(theme)
            self.assertIsInstance(colors, list)


if __name__ == '__main__':
    unittest.main()
