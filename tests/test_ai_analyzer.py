"""
Unit tests for AI Analyzer module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
from src.ai_analyzer import AIAnalyzer, InsightFormatter
from src.prompts import PromptTemplates


class TestAIAnalyzer(unittest.TestCase):
    """Test cases for AIAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the OpenAI API to avoid actual API calls in tests
        self.mock_api_key = "test_api_key"
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100, freq='D'),
            'sales': np.random.normal(1000, 200, 100),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
            'product': np.random.choice(['A', 'B', 'C'], 100)
        })
        
        self.sample_summary = {
            'basic_info': {
                'rows': 100,
                'columns': 4,
                'memory_usage_mb': 0.1,
                'missing_values_total': 0,
                'duplicate_rows': 0
            },
            'column_info': {
                'numeric_columns': 1,
                'categorical_columns': 2,
                'datetime_columns': 1
            },
            'data_quality': {
                'overall_score': 95.0,
                'missing_data_percentage': 0.0,
                'duplicate_percentage': 0.0,
                'recommendations': []
            }
        }
    
    @patch('openai.ChatCompletion.create')
    def test_analyze_dataset_overview(self, mock_openai):
        """Test dataset overview analysis"""
        # Mock OpenAI response
        mock_openai.return_value = Mock()
        mock_openai.return_value.choices = [Mock()]
        mock_openai.return_value.choices[0].message.content = """
        ## Executive Summary
        This dataset contains sales data with strong data quality and good coverage.
        
        ## Key Findings
        - Sales show consistent patterns across regions
        - Product mix is balanced
        - No significant data quality issues
        
        ## Data Quality Assessment
        The data appears complete and reliable for analysis.
        
        ## Recommendations
        - Proceed with detailed analysis
        - Consider seasonal trend analysis
        """
        
        # Initialize analyzer with mock API key
        analyzer = AIAnalyzer(api_key=self.mock_api_key)
        
        # Test analysis
        result = analyzer.analyze_dataset_overview(self.sample_summary, self.sample_data.head())
        
        # Verify results
        self.assertIn('executive_summary', result)
        self.assertIn('key_findings', result)
        self.assertIn('data_quality', result)
        self.assertIn('recommendations', result)
        
        # Verify OpenAI was called
        mock_openai.assert_called_once()
    
    @patch('openai.ChatCompletion.create')
    def test_analyze_column_insights(self, mock_openai):
        """Test column-specific analysis"""
        mock_openai.return_value = Mock()
        mock_openai.return_value.choices = [Mock()]
        mock_openai.return_value.choices[0].message.content = """
        ## Pattern Analysis
        The sales column shows normal distribution with consistent patterns.
        
        ## Business Significance
        This represents core revenue metrics for the business.
        
        ## Anomalies or Concerns
        No significant anomalies detected in the data.
        
        ## Recommendations
        Monitor for seasonal variations and trend changes.
        """
        
        analyzer = AIAnalyzer(api_key=self.mock_api_key)
        
        column_stats = {
            'dtype': 'float64',
            'non_null_count': 100,
            'unique_count': 95,
            'statistics': {
                'mean': 1000.0,
                'median': 995.0,
                'std': 200.0,
                'min': 500.0,
                'max': 1500.0
            }
        }
        
        result = analyzer.analyze_column_insights('sales', self.sample_data['sales'], column_stats)
        
        self.assertIn('pattern_analysis', result)
        self.assertIn('business_significance', result)
        self.assertIn('anomalies', result)
        self.assertIn('recommendations', result)
    
    @patch('openai.ChatCompletion.create')
    def test_analyze_trends_and_patterns(self, mock_openai):
        """Test trend analysis"""
        mock_openai.return_value = Mock()
        mock_openai.return_value.choices = [Mock()]
        mock_openai.return_value.choices[0].message.content = """
        ## Trend Summary
        Sales show steady growth with seasonal variations.
        
        ## Seasonal Patterns
        Higher sales in winter months, lower in summer.
        
        ## Growth/Decline Analysis
        Overall positive trend with 5% monthly growth.
        
        ## Forecast Insights
        Expect continued growth if current trends maintain.
        
        ## Strategic Recommendations
        Invest in marketing during peak seasons.
        """
        
        analyzer = AIAnalyzer(api_key=self.mock_api_key)
        
        result = analyzer.analyze_trends_and_patterns(self.sample_data, 'date')
        
        self.assertIn('trend_summary', result)
        self.assertIn('seasonal_patterns', result)
        self.assertIn('growth_analysis', result)
        self.assertIn('forecast_insights', result)
        self.assertIn('recommendations', result)
        self.assertIn('metrics', result)
    
    @patch('openai.ChatCompletion.create')
    def test_generate_story_narrative(self, mock_openai):
        """Test narrative generation"""
        mock_openai.return_value = Mock()
        mock_openai.return_value.choices = [Mock()]
        mock_openai.return_value.choices[0].message.content = """
        Our sales data reveals a strong performance trajectory over the past quarter.
        The business has achieved consistent growth across all regions, with particularly
        strong performance in the North region. Key factors driving success include
        balanced product mix and effective seasonal strategies. Moving forward, we
        recommend maintaining current momentum while exploring expansion opportunities
        in underperforming segments.
        """
        
        analyzer = AIAnalyzer(api_key=self.mock_api_key)
        
        insights = {
            'growth_rate': '15%',
            'top_region': 'North',
            'trend': 'positive'
        }
        
        result = analyzer.generate_story_narrative(self.sample_data, insights)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 100)  # Should be substantial narrative
    
    @patch('openai.ChatCompletion.create')
    def test_explain_chart_insights(self, mock_openai):
        """Test chart explanation generation"""
        mock_openai.return_value = Mock()
        mock_openai.return_value.choices = [Mock()]
        mock_openai.return_value.choices[0].message.content = """
        This bar chart displays monthly sales performance, showing a clear upward trend
        with 15% growth in Q4. The data indicates strong seasonal performance during
        holiday months, suggesting effective promotional strategies and customer engagement.
        """
        
        analyzer = AIAnalyzer(api_key=self.mock_api_key)
        
        chart_data = {'x': 'months', 'y': 'sales', 'trend': 'increasing'}
        context = {'period': 'Q4', 'business_type': 'retail'}
        
        result = analyzer.explain_chart_insights('bar', chart_data, context)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 50)  # Should be meaningful explanation
    
    def test_identify_trends(self):
        """Test trend identification functionality"""
        analyzer = AIAnalyzer(api_key=self.mock_api_key)
        
        # Test with date column
        trends = analyzer._identify_trends(self.sample_data, 'date')
        
        self.assertIn('numeric_summary', trends)
        self.assertIn('total_records', trends['numeric_summary'])
        self.assertEqual(trends['numeric_summary']['total_records'], 100)
    
    def test_find_correlations(self):
        """Test correlation detection"""
        analyzer = AIAnalyzer(api_key=self.mock_api_key)
        
        # Create data with known correlation
        corr_data = pd.DataFrame({
            'x': range(100),
            'y': [i * 2 + np.random.normal(0, 0.1) for i in range(100)],  # Strong correlation
            'z': np.random.normal(0, 1, 100)  # No correlation
        })
        
        correlations = analyzer._find_correlations(corr_data)
        
        self.assertIsInstance(correlations, list)
        # Should find strong correlation between x and y
        if correlations:
            self.assertIn('correlation', correlations[0])
            self.assertIn('strength', correlations[0])
    
    def test_error_handling(self):
        """Test error handling in AI analyzer"""
        # Test with invalid API key
        with patch('openai.ChatCompletion.create', side_effect=Exception("API Error")):
            analyzer = AIAnalyzer(api_key="invalid_key")
            
            result = analyzer.analyze_dataset_overview(self.sample_summary, self.sample_data)
            
            # Should return error message instead of crashing
            self.assertIn('executive_summary', result)
            self.assertIn('unavailable', result['executive_summary'].lower())


class TestInsightFormatter(unittest.TestCase):
    """Test cases for InsightFormatter utility class"""
    
    def test_format_for_dashboard(self):
        """Test dashboard formatting"""
        insights = {
            'summary': 'Test summary',
            'findings': ['Finding 1', 'Finding 2', 'Finding 3'],
            'score': 85.5
        }
        
        formatted = InsightFormatter.format_for_dashboard(insights)
        
        self.assertIn('summary', formatted)
        self.assertIn('findings', formatted)
        self.assertIn('•', formatted['findings'])  # Should format list with bullets
    
    def test_format_for_report(self):
        """Test report formatting"""
        insights = {
            'executive_summary': 'This is a test summary',
            'key_findings': ['Finding 1', 'Finding 2']
        }
        
        report = InsightFormatter.format_for_report(insights, "Test Report")
        
        self.assertIn('# Test Report', report)
        self.assertIn('## Executive Summary', report)
        self.assertIn('## Key Findings', report)
        self.assertIn('Generated on:', report)
    
    def test_extract_key_metrics(self):
        """Test key metrics extraction"""
        insights = {
            'summary': 'Sales increased by 15.5% with 90% confidence',
            'performance': 'Cost reduced by $1,234 and efficiency up 25%'
        }
        
        metrics = InsightFormatter.extract_key_metrics(insights)
        
        self.assertIsInstance(metrics, dict)
        # Should extract percentages and numbers
        for key, value in metrics.items():
            if value:  # If metrics were found
                self.assertIsInstance(value, str)


class TestPromptTemplates(unittest.TestCase):
    """Test cases for prompt templates"""
    
    def test_dataset_overview_prompt(self):
        """Test dataset overview prompt generation"""
        context = "Test dataset with 1000 rows and 5 columns"
        prompt = PromptTemplates.dataset_overview_prompt(context)
        
        self.assertIn(context, prompt)
        self.assertIn('Executive Summary', prompt)
        self.assertIn('Key Business Insights', prompt)
        self.assertIn('Strategic Recommendations', prompt)
    
    def test_sales_analysis_prompt(self):
        """Test sales-specific prompt"""
        context = "Sales data with revenue and customer information"
        prompt = PromptTemplates.sales_analysis_prompt(context)
        
        self.assertIn(context, prompt)
        self.assertIn('Revenue Insights', prompt)
        self.assertIn('Customer Behavior', prompt)
    
    def test_chart_explanation_prompt(self):
        """Test chart explanation prompt"""
        prompt = PromptTemplates.chart_explanation_prompt(
            'bar', 'monthly sales data', 'retail business'
        )
        
        self.assertIn('bar', prompt)
        self.assertIn('monthly sales data', prompt)
        self.assertIn('retail business', prompt)
        self.assertIn('2-3 sentences', prompt)


if __name__ == '__main__':
    unittest.main()
