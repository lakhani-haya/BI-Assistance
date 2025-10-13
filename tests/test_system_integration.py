"""
Comprehensive Test Suite for Final System Integration
Tests all components working together for Step 9 
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def comprehensive_sample_data():
    """Create comprehensive sample data for integration testing"""
    np.random.seed(42)
    
    # Generate 6 months of daily business data
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    
    data = []
    for date in dates:
        for region in ['North', 'South', 'East', 'West']:
            for product in ['Product A', 'Product B', 'Product C']:
                data.append({
                    'Date': date,
                    'Region': region,
                    'Product': product,
                    'Revenue': np.random.uniform(1000, 10000),
                    'Units_Sold': np.random.randint(10, 100),
                    'Customer_Satisfaction': np.random.uniform(3.0, 5.0),
                    'Marketing_Spend': np.random.uniform(100, 1000),
                    'Support_Tickets': np.random.randint(0, 20)
                })
    
    return pd.DataFrame(data)


class TestSystemIntegration:
    """Test suite for complete system integration"""
    
    def test_data_processing_pipeline(self, comprehensive_sample_data):
        """Test complete data processing pipeline"""
        
        from src.data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # Test data validation
        validation_result = processor.validate_data(comprehensive_sample_data)
        assert validation_result['valid'] == True
        assert 'quality_score' in validation_result
        
        # Test data summary
        summary = processor.get_data_summary(comprehensive_sample_data)
        assert 'total_rows' in summary
        assert 'total_columns' in summary
        assert summary['total_rows'] > 0
        assert summary['total_columns'] > 0
    
    def test_ai_analysis_integration(self, comprehensive_sample_data):
        """Test AI analysis integration"""
        
        from src.intelligent_analyzer import IntelligentDataAnalyzer
        
        analyzer = IntelligentDataAnalyzer()
        
        # Test analysis with sample data
        result = analyzer.analyze_dataframe(
            comprehensive_sample_data.sample(100),  # Use subset for faster testing
            business_domain="retail",
            target_audience="executives"
        )
        
        assert isinstance(result, dict)
        assert 'summary_stats' in result
        assert 'insights' in result
        assert len(result['insights']) > 0
    
    def test_visualization_pipeline(self, comprehensive_sample_data):
        """Test visualization creation pipeline"""
        
        from src.intelligent_visualizer import IntelligentVisualizationEngine
        
        viz_engine = IntelligentVisualizationEngine()
        
        # Test dashboard creation
        dashboard_result = viz_engine.create_smart_dashboard(
            comprehensive_sample_data.sample(100),
            business_domain="retail",
            chart_theme="business"
        )
        
        assert isinstance(dashboard_result, dict)
        assert 'charts' in dashboard_result
        assert len(dashboard_result['charts']) > 0
        
        # Test individual chart creation
        for chart in dashboard_result['charts'][:3]:  # Test first 3 charts
            assert 'chart_type' in chart
            assert 'title' in chart
            assert 'data' in chart
    
    def test_advanced_insights_integration(self, comprehensive_sample_data):
        """Test advanced AI insights integration"""
        
        from src.advanced_insights import AdvancedInsightsEngine, StorytellingMode
        
        insights_engine = AdvancedInsightsEngine()
        
        # Test story generation
        story = insights_engine.create_data_story(
            comprehensive_sample_data.sample(50),
            mode=StorytellingMode.EXECUTIVE_BRIEF,
            target_audience="Business Executives"
        )
        
        assert story.title is not None
        assert len(story.key_findings) > 0
        assert story.executive_summary is not None
        
        # Test Q&A functionality
        answer = insights_engine.interactive_qa_session(
            comprehensive_sample_data.sample(50),
            "What are the main trends in revenue?"
        )
        
        assert isinstance(answer, dict)
        assert 'answer' in answer
        assert 'confidence' in answer
        assert len(answer['answer']) > 0
    
    def test_dashboard_builder_integration(self, comprehensive_sample_data):
        """Test dashboard builder integration"""
        
        from src.dashboard_builder import DashboardBuilder
        
        builder = DashboardBuilder()
        
        # Test template creation
        dashboard = builder.create_template_dashboard(
            comprehensive_sample_data.sample(50),
            template_name="sales_analytics"
        )
        
        assert dashboard is not None
        assert hasattr(dashboard, 'charts')
        assert len(dashboard.charts) > 0
        
        # Test each chart in dashboard
        for chart in dashboard.charts:
            assert hasattr(chart, 'chart_type')
            assert hasattr(chart, 'title')
            assert hasattr(chart, 'chart_data')
    
    def test_performance_optimization(self, comprehensive_sample_data):
        """Test performance optimization features"""
        
        from src.performance_optimizer import DataOptimizer, PerformanceMonitor
        
        # Test data optimization
        original_memory = comprehensive_sample_data.memory_usage(deep=True).sum()
        optimized_data = DataOptimizer.optimize_dataframe(comprehensive_sample_data)
        optimized_memory = optimized_data.memory_usage(deep=True).sum()
        
        # Should not increase memory usage
        assert optimized_memory <= original_memory
        
        # Data should be preserved
        assert len(optimized_data) == len(comprehensive_sample_data)
        assert optimized_data.columns.tolist() == comprehensive_sample_data.columns.tolist()
        
        # Test performance monitoring
        monitor = PerformanceMonitor()
        
        # Test timing decorator
        @monitor.timing_decorator('test')
        def test_function():
            return sum(range(1000))
        
        result = test_function()
        assert result == sum(range(1000))
        assert 'test_function' in monitor.metrics['function_times']
    
    def test_documentation_generation(self):
        """Test documentation generation"""
        
        from src.documentation_generator import DocumentationGenerator
        
        doc_generator = DocumentationGenerator()
        
        # Test documentation generation
        documentation = doc_generator.generate_complete_documentation()
        
        assert isinstance(documentation, dict)
        assert len(documentation) > 0
        
        # Check required sections
        required_sections = [
            'getting_started',
            'data_upload', 
            'analysis_features',
            'dashboard_creation',
            'ai_insights',
            'export_options',
            'troubleshooting'
        ]
        
        for section in required_sections:
            assert section in documentation
            assert len(documentation[section]) > 100  # Should have substantial content


class TestErrorHandling:
    """Test error handling across the system"""
    
    def test_empty_data_handling(self):
        """Test handling of empty datasets"""
        
        from src.data_processor import DataProcessor
        
        processor = DataProcessor()
        empty_df = pd.DataFrame()
        
        # Should handle empty data gracefully
        try:
            validation_result = processor.validate_data(empty_df)
            assert validation_result['valid'] == False
        except Exception as e:
            # If it raises an exception, it should be informative
            assert len(str(e)) > 0
    
    def test_invalid_data_handling(self):
        """Test handling of invalid data formats"""
        
        from src.data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # Test with all NaN data
        invalid_df = pd.DataFrame({
            'col1': [np.nan, np.nan, np.nan],
            'col2': [np.nan, np.nan, np.nan]
        })
        
        validation_result = processor.validate_data(invalid_df)
        assert validation_result['valid'] == False
        assert 'warnings' in validation_result or 'errors' in validation_result
    
    def test_large_data_handling(self):
        """Test handling of large datasets"""
        
        from src.performance_optimizer import DataOptimizer
        
        # Create large dataset
        large_data = pd.DataFrame({
            'id': range(50000),
            'value': np.random.randn(50000),
            'category': np.random.choice(['A', 'B', 'C'], 50000)
        })
        
        # Test sampling
        sampled_data = DataOptimizer.sample_large_dataset(large_data, max_rows=1000)
        
        assert len(sampled_data) <= 1000
        assert sampled_data.columns.tolist() == large_data.columns.tolist()


class TestExportFunctionality:
    """Test export functionality across the system"""
    
    def test_data_export_formats(self, comprehensive_sample_data):
        """Test various data export formats"""
        
        # Test CSV export
        csv_data = comprehensive_sample_data.to_csv(index=False)
        assert len(csv_data) > 0
        assert 'Date,Region,Product' in csv_data
        
        # Test JSON export
        json_data = comprehensive_sample_data.to_json()
        assert len(json_data) > 0
        
        # Test Excel export (if openpyxl available)
        try:
            import io
            excel_buffer = io.BytesIO()
            comprehensive_sample_data.to_excel(excel_buffer, index=False)
            excel_data = excel_buffer.getvalue()
            assert len(excel_data) > 0
        except ImportError:
            pass  # Skip if openpyxl not available


class TestScalabilityAndPerformance:
    """Test system scalability and performance"""
    
    def test_medium_dataset_performance(self):
        """Test performance with medium-sized datasets"""
        
        # Create medium dataset (10,000 rows)
        np.random.seed(42)
        medium_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10000, freq='H'),
            'value': np.random.randn(10000),
            'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 10000),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 10000)
        })
        
        from src.data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # Time the processing
        import time
        start_time = time.time()
        
        validation_result = processor.validate_data(medium_data)
        summary = processor.get_data_summary(medium_data)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within reasonable time (adjust threshold as needed)
        assert processing_time < 30  # 30 seconds max
        assert validation_result['valid'] == True
        assert summary['total_rows'] == 10000
    
    def test_memory_efficiency(self):
        """Test memory efficiency optimizations"""
        
        from src.performance_optimizer import DataOptimizer
        
        # Create data with inefficient types
        inefficient_data = pd.DataFrame({
            'small_int': np.random.randint(0, 100, 1000).astype('int64'),
            'category': ['Category_' + str(i % 5) for i in range(1000)],
            'float_data': np.random.randn(1000).astype('float64')
        })
        
        original_memory = inefficient_data.memory_usage(deep=True).sum()
        
        # Optimize data types
        optimized_data = DataOptimizer.optimize_dataframe(inefficient_data)
        optimized_memory = optimized_data.memory_usage(deep=True).sum()
        
        # Should reduce memory usage
        memory_reduction = (original_memory - optimized_memory) / original_memory
        assert memory_reduction >= 0  # At minimum, should not increase memory


def test_complete_workflow():
    """Test complete end-to-end workflow"""
    
    # This test simulates a complete user workflow
    
    # 1. Data Upload and Processing
    from src.data_processor import DataProcessor
    
    processor = DataProcessor()
    
    # Create sample data
    sample_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100, freq='D'),
        'revenue': np.random.uniform(1000, 5000, 100),
        'region': np.random.choice(['North', 'South'], 100),
        'product': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    # Validate data
    validation = processor.validate_data(sample_data)
    assert validation['valid'] == True
    
    # 2. Analysis
    from src.intelligent_analyzer import IntelligentDataAnalyzer
    
    analyzer = IntelligentDataAnalyzer()
    analysis_result = analyzer.analyze_dataframe(sample_data, "retail", "executives")
    assert len(analysis_result['insights']) > 0
    
    # 3. Visualization
    from src.intelligent_visualizer import IntelligentVisualizationEngine
    
    viz_engine = IntelligentVisualizationEngine()
    dashboard_result = viz_engine.create_smart_dashboard(sample_data, "retail", "business")
    assert len(dashboard_result['charts']) > 0
    
    # 4. AI Insights
    from src.advanced_insights import AdvancedInsightsEngine, StorytellingMode
    
    insights_engine = AdvancedInsightsEngine()
    story = insights_engine.create_data_story(sample_data, StorytellingMode.EXECUTIVE_BRIEF)
    assert story.title is not None
    
    # 5. Dashboard Building
    from src.dashboard_builder import DashboardBuilder
    
    builder = DashboardBuilder()
    dashboard = builder.create_template_dashboard(sample_data, "sales_analytics")
    assert len(dashboard.charts) > 0
    
    print("✅ Complete workflow test passed!")


if __name__ == "__main__":
    # Run specific tests
    pytest.main([__file__, "-v", "--tb=short"])
