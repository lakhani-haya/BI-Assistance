"""
Test the Streamlit dashboard components
Run this script to validate all dashboard functionality
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import streamlit as st
    from src.dashboard import StreamlitDashboard
    from src.streamlit_config import StreamlitConfig, SessionStateManager, ComponentHelpers
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("⚠️ Streamlit not available - skipping dashboard tests")


class TestStreamlitConfig(unittest.TestCase):
    """Test Streamlit configuration"""
    
    def test_page_config(self):
        """Test page configuration settings"""
        config = StreamlitConfig.PAGE_CONFIG
        
        self.assertIn('page_title', config)
        self.assertIn('page_icon', config)
        self.assertIn('layout', config)
        self.assertEqual(config['layout'], 'wide')
    
    def test_themes(self):
        """Test theme configurations"""
        themes = StreamlitConfig.THEMES
        
        self.assertIn('business', themes)
        self.assertIn('executive', themes)
        self.assertIn('presentation', themes)
        
        # Check theme structure
        for theme_name, theme_config in themes.items():
            self.assertIn('primary_color', theme_config)
            self.assertIn('secondary_color', theme_config)
            self.assertIn('background_color', theme_config)
            self.assertIn('text_color', theme_config)
    
    def test_custom_css_generation(self):
        """Test custom CSS generation"""
        css = StreamlitConfig.get_custom_css('business')
        
        self.assertIsInstance(css, str)
        self.assertIn('<style>', css)
        self.assertIn('</style>', css)
        self.assertIn('.main-header', css)
        self.assertIn('--primary-color', css)
    
    def test_chart_config(self):
        """Test chart configuration"""
        config = StreamlitConfig.get_chart_config('business')
        
        self.assertIn('responsive', config)
        self.assertIn('displayModeBar', config)
        self.assertIn('toImageButtonOptions', config)
    
    def test_plotly_theme_mapping(self):
        """Test Plotly theme mapping"""
        self.assertEqual(StreamlitConfig.get_plotly_theme('business'), 'plotly')
        self.assertEqual(StreamlitConfig.get_plotly_theme('executive'), 'plotly_white')
        self.assertEqual(StreamlitConfig.get_plotly_theme('presentation'), 'presentation')
        self.assertEqual(StreamlitConfig.get_plotly_theme('unknown'), 'plotly')


class TestSessionStateManager(unittest.TestCase):
    """Test session state management"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_session_state = {}
    
    def test_session_state_initialization(self):
        """Test session state initialization"""
        # Mock st.session_state
        with patch('streamlit.session_state', self.mock_session_state):
            SessionStateManager.initialize_session_state()
            
            # Check required keys
            required_keys = [
                'data_loaded', 'current_data', 'analysis_results',
                'dashboard_results', 'ai_enabled'
            ]
            
            for key in required_keys:
                self.assertIn(key, self.mock_session_state)
    
    def test_message_management(self):
        """Test message management"""
        with patch('streamlit.session_state', self.mock_session_state):
            SessionStateManager.initialize_session_state()
            
            # Add messages
            SessionStateManager.add_message("Test error", "error")
            SessionStateManager.add_message("Test success", "success")
            
            self.assertIn("Test error", self.mock_session_state['error_messages'])
            self.assertIn("Test success", self.mock_session_state['success_messages'])
            
            # Clear messages
            SessionStateManager.clear_messages()
            self.assertEqual(len(self.mock_session_state['error_messages']), 0)
            self.assertEqual(len(self.mock_session_state['success_messages']), 0)
    
    def test_processing_status_update(self):
        """Test processing status updates"""
        with patch('streamlit.session_state', self.mock_session_state):
            SessionStateManager.initialize_session_state()
            
            SessionStateManager.update_processing_status("running")
            self.assertEqual(self.mock_session_state['processing_status'], "running")


@unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit not available")
class TestStreamlitDashboard(unittest.TestCase):
    """Test Streamlit dashboard functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_session_state = {
            'data_loaded': False,
            'current_data': None,
            'analysis_results': None,
            'dashboard_results': None,
            'ai_enabled': False
        }
    
    @patch('streamlit.session_state')
    @patch('src.config.Config')
    def test_dashboard_initialization(self, mock_config, mock_session_state):
        """Test dashboard initialization"""
        mock_session_state.__contains__ = lambda self, key: key in self.mock_session_state
        mock_session_state.__getitem__ = lambda self, key: self.mock_session_state[key]
        mock_session_state.__setitem__ = lambda self, key, value: self.mock_session_state.__setitem__(key, value)
        
        mock_config.validate_config.return_value = []
        mock_config.OPENAI_API_KEY = "test_key"
        
        dashboard = StreamlitDashboard()
        self.assertIsInstance(dashboard, StreamlitDashboard)
    
    def test_sample_data_creation(self):
        """Test sample data creation"""
        with patch('streamlit.session_state', self.mock_session_state):
            dashboard = StreamlitDashboard()
            sample_data = dashboard.create_sample_data()
            
            self.assertIsInstance(sample_data, pd.DataFrame)
            self.assertGreater(len(sample_data), 0)
            
            # Check required columns
            expected_columns = [
                'date', 'sales_amount', 'region', 'product_category',
                'customer_type', 'units_sold', 'discount_percent',
                'profit_margin_percent', 'profit_amount'
            ]
            
            for col in expected_columns:
                self.assertIn(col, sample_data.columns)
    
    @patch('pandas.read_csv')
    def test_file_processing(self, mock_read_csv):
        """Test file upload processing"""
        with patch('streamlit.session_state', self.mock_session_state):
            dashboard = StreamlitDashboard()
            
            # Mock uploaded file
            mock_file = Mock()
            mock_file.type = "text/csv"
            mock_file.size = 1024 * 1024  # 1MB
            
            # Mock successful data loading
            mock_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            mock_read_csv.return_value = mock_data
            
            result = dashboard.process_uploaded_file(mock_file)
            
            self.assertTrue(result)
            mock_read_csv.assert_called_once()


class TestComponentHelpers(unittest.TestCase):
    """Test component helper functions"""
    
    def test_metric_card_creation(self):
        """Test metric card creation"""
        # This would require mocking Streamlit components
        # For now, just test that the function exists and is callable
        self.assertTrue(callable(ComponentHelpers.create_metric_card))
    
    def test_info_box_creation(self):
        """Test info box creation"""
        self.assertTrue(callable(ComponentHelpers.create_info_box))
    
    def test_progress_indicator_creation(self):
        """Test progress indicator creation"""
        self.assertTrue(callable(ComponentHelpers.create_progress_indicator))


class TestDashboardIntegration(unittest.TestCase):
    """Test dashboard integration with other components"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'sales': np.random.randint(100, 1000, 100),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
            'product': np.random.choice(['A', 'B', 'C'], 100)
        })
    
    def test_data_processing_integration(self):
        """Test integration with data processing components"""
        try:
            from src.data_processor import DataProcessor
            
            processor = DataProcessor()
            result = processor.load_dataframe(self.sample_data, "test_data")
            
            self.assertTrue(result)
            self.assertIsNotNone(processor.data)
        except ImportError:
            self.skipTest("DataProcessor not available")
    
    def test_visualization_integration(self):
        """Test integration with visualization components"""
        try:
            from src.visualizer import PlotlyVisualizer
            
            visualizer = PlotlyVisualizer()
            
            # Test basic chart creation
            chart = visualizer.create_histogram(
                self.sample_data,
                'sales',
                title="Test Histogram"
            )
            
            self.assertIsNotNone(chart)
        except ImportError:
            self.skipTest("Visualizer not available")


def run_dashboard_tests():
    """Run all dashboard tests"""
    print("🧪 Running Dashboard Tests")
    print("=" * 50)
    
    # Create test suite
    test_classes = [
        TestStreamlitConfig,
        TestSessionStateManager,
        TestComponentHelpers,
        TestDashboardIntegration
    ]
    
    if STREAMLIT_AVAILABLE:
        test_classes.append(TestStreamlitDashboard)
    
    # Run tests
    total_tests = 0
    total_failures = 0
    
    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}...")
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=1)
        result = runner.run(suite)
        
        total_tests += result.testsRun
        total_failures += len(result.failures) + len(result.errors)
    
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Failures: {total_failures}")
    print(f"   Success Rate: {((total_tests - total_failures) / total_tests * 100):.1f}%")
    
    if total_failures == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {total_failures} test(s) failed")
    
    return total_failures == 0


def test_dashboard_launch():
    """Test dashboard launch capabilities"""
    print("\n🚀 Testing Dashboard Launch...")
    
    try:
        # Test imports
        if STREAMLIT_AVAILABLE:
            from src.dashboard import StreamlitDashboard
            print("✅ Dashboard module imports successfully")
        else:
            print("⚠️ Streamlit not available")
        
        # Test configuration
        from src.streamlit_config import StreamlitConfig
        config = StreamlitConfig.get_custom_css()
        print("✅ Configuration system working")
        
        # Test sample data generation
        if STREAMLIT_AVAILABLE:
            dashboard = StreamlitDashboard()
            sample_data = dashboard.create_sample_data()
            print(f"✅ Sample data generation working ({len(sample_data)} records)")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard launch test failed: {e}")
        return False


if __name__ == "__main__":
    print("🤖📊 BI Assistant Dashboard Testing Suite")
    print("=" * 60)
    
    # Run component tests
    tests_passed = run_dashboard_tests()
    
    # Test dashboard launch
    launch_test_passed = test_dashboard_launch()
    
    print("\n" + "=" * 60)
    print("🏁 Overall Results:")
    
    if tests_passed and launch_test_passed:
        print("✅ All dashboard tests passed! Ready for deployment.")
        exit_code = 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        exit_code = 1
    
    print("💡 To start the dashboard, run: python run_dashboard.py")
    sys.exit(exit_code)
