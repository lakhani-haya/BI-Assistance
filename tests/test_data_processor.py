"""
Unit tests for data_processor module
"""

import unittest
import pandas as pd
import numpy as np
import tempfile
import os
from src.data_processor import DataProcessor, validate_file_size, get_file_info


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5, 1],  # Duplicate row
            'name': ['Alice', 'Bob', 'Charlie', None, 'Eve', 'Alice'],  # Missing value
            'age': [25, 30, 35, 40, 45, 25],
            'salary': [50000, 60000, 70000, 80000, 90000, 50000],
            'date_joined': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01', '2020-01-01']
        })
    
    def test_load_dataframe(self):
        """Test loading DataFrame"""
        result = self.processor.load_dataframe(self.sample_data)
        self.assertTrue(result)
        self.assertEqual(len(self.processor.data), 6)
        self.assertEqual(len(self.processor.data.columns), 5)
    
    def test_data_info_generation(self):
        """Test data info generation"""
        self.processor.load_dataframe(self.sample_data)
        
        self.assertEqual(self.processor.data_info['shape'], (6, 5))
        self.assertIn('id', self.processor.data_info['numeric_columns'])
        self.assertIn('name', self.processor.data_info['categorical_columns'])
        self.assertEqual(self.processor.data_info['duplicate_rows'], 1)
    
    def test_clean_data(self):
        """Test data cleaning functionality"""
        self.processor.load_dataframe(self.sample_data)
        
        # Test with default parameters
        summary = self.processor.clean_data()
        
        # Should remove duplicates
        self.assertEqual(len(self.processor.data), 5)
        self.assertIn('operations_performed', summary)
    
    def test_get_data_summary(self):
        """Test data summary generation"""
        self.processor.load_dataframe(self.sample_data)
        
        summary = self.processor.get_data_summary()
        
        self.assertIn('basic_info', summary)
        self.assertIn('column_info', summary)
        self.assertIn('data_quality', summary)
        self.assertEqual(summary['basic_info']['rows'], 6)
        self.assertEqual(summary['basic_info']['columns'], 5)
    
    def test_column_analysis(self):
        """Test individual column analysis"""
        self.processor.load_dataframe(self.sample_data)
        
        # Test numeric column
        age_analysis = self.processor.get_column_analysis('age')
        self.assertIn('statistics', age_analysis)
        self.assertIn('mean', age_analysis['statistics'])
        
        # Test categorical column
        name_analysis = self.processor.get_column_analysis('name')
        self.assertIn('value_counts', name_analysis)
        
        # Test non-existent column
        invalid_analysis = self.processor.get_column_analysis('invalid_col')
        self.assertIn('error', invalid_analysis)
    
    def test_outlier_detection(self):
        """Test outlier detection"""
        # Create data with outliers
        data_with_outliers = pd.DataFrame({
            'values': [1, 2, 3, 4, 5, 100]  # 100 is an outlier
        })
        
        self.processor.load_dataframe(data_with_outliers)
        outlier_info = self.processor._detect_outliers(self.processor.data['values'])
        
        self.assertGreater(outlier_info['count'], 0)
        self.assertIn('percentage', outlier_info)
    
    def test_export_functionality(self):
        """Test data export functionality"""
        self.processor.load_dataframe(self.sample_data)
        
        # Test CSV export
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            result = self.processor.export_cleaned_data(tmp.name, 'csv')
            self.assertTrue(result)
            self.assertTrue(os.path.exists(tmp.name))
            os.unlink(tmp.name)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_validate_file_size(self):
        """Test file size validation"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test data")
            tmp.flush()
            
            # Should pass for small file
            result = validate_file_size(tmp.name, max_size_mb=1)
            self.assertTrue(result)
            
            os.unlink(tmp.name)
    
    def test_get_file_info(self):
        """Test file info retrieval"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test data")
            tmp.flush()
            
            info = get_file_info(tmp.name)
            self.assertIn('size_mb', info)
            self.assertIn('modified', info)
            self.assertIn('extension', info)
            
            os.unlink(tmp.name)


if __name__ == '__main__':
    unittest.main()
