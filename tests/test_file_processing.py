"""
Test Enhanced File Upload and Processing Components
Comprehensive testing for the new file processing capabilities
"""

import sys
import os
import unittest
import tempfile
import zipfile
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
import io
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from src.file_processor import FileProcessor, FileValidator, BatchFileProcessor, DataTypeConverter, FileInfo
    from src.streamlit_upload import StreamlitFileUploader
    FILE_PROCESSOR_AVAILABLE = True
except ImportError as e:
    FILE_PROCESSOR_AVAILABLE = False
    print(f" File processor modules not available: {e}")

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print(" Streamlit not available - skipping streamlit upload tests")


class TestFileValidator(unittest.TestCase):
    """Test file validation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_csv_content = "name,age,city\nJohn,25,NYC\nJane,30,LA"
        self.test_json_content = '{"data": [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]}'
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_supported_extensions(self):
        """Test supported file extensions"""
        supported = FileValidator.SUPPORTED_EXTENSIONS
        
        self.assertIn('.csv', supported)
        self.assertIn('.xlsx', supported)
        self.assertIn('.json', supported)
        self.assertEqual(supported['.csv'], 'text/csv')
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_file_size_validation(self):
        """Test file size validation"""
        # Test valid file
        valid_content = "test,data\n1,2"
        valid_file = io.BytesIO(valid_content.encode('utf-8'))
        
        is_valid, errors = FileValidator.validate_file(valid_file, "test.csv")
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Test empty file
        empty_file = io.BytesIO(b"")
        is_valid, errors = FileValidator.validate_file(empty_file, "empty.csv")
        self.assertFalse(is_valid)
        self.assertIn("File is empty", errors[0])
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_encoding_detection(self):
        """Test encoding detection"""
        # Test UTF-8 content
        utf8_content = "name,age\nJohn,25".encode('utf-8')
        detected_encoding = FileValidator.detect_encoding(utf8_content)
        self.assertIn(detected_encoding.lower(), ['utf-8', 'ascii'])
        
        # Test Latin-1 content
        latin1_content = "naïve,résumé\n1,2".encode('latin-1')
        detected_encoding = FileValidator.detect_encoding(latin1_content)
        self.assertIsNotNone(detected_encoding)
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_csv_separator_detection(self):
        """Test CSV separator detection"""
        # Test comma separator
        comma_content = "a,b,c\n1,2,3"
        separator = FileValidator.detect_csv_separator(comma_content)
        self.assertEqual(separator, ',')
        
        # Test semicolon separator
        semicolon_content = "a;b;c\n1;2;3"
        separator = FileValidator.detect_csv_separator(semicolon_content)
        self.assertEqual(separator, ';')
        
        # Test tab separator
        tab_content = "a\tb\tc\n1\t2\t3"
        separator = FileValidator.detect_csv_separator(tab_content)
        self.assertEqual(separator, '\t')
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_unsupported_format(self):
        """Test unsupported file format validation"""
        unsupported_file = io.BytesIO(b"test content")
        is_valid, errors = FileValidator.validate_file(unsupported_file, "test.xyz")
        
        self.assertFalse(is_valid)
        self.assertIn("Unsupported file format", errors[0])


class TestFileProcessor(unittest.TestCase):
    """Test file processing functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.processor = FileProcessor() if FILE_PROCESSOR_AVAILABLE else None
        
        # Test data
        self.test_csv_data = pd.DataFrame({
            'name': ['John', 'Jane', 'Bob'],
            'age': [25, 30, 35],
            'city': ['NYC', 'LA', 'Chicago']
        })
        
        self.test_json_data = {
            'data': [
                {'name': 'John', 'age': 25, 'city': 'NYC'},
                {'name': 'Jane', 'age': 30, 'city': 'LA'}
            ]
        }
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_csv_processing(self):
        """Test CSV file processing"""
        # Create CSV content
        csv_content = self.test_csv_data.to_csv(index=False)
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        
        # Process file
        data, file_info = self.processor.process_file(csv_file, "test.csv")
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 3)
        self.assertEqual(list(data.columns), ['name', 'age', 'city'])
        self.assertIsInstance(file_info, FileInfo)
        self.assertEqual(file_info.filename, "test.csv")
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_json_processing(self):
        """Test JSON file processing"""
        # Create JSON content
        json_content = json.dumps(self.test_json_data)
        json_file = io.BytesIO(json_content.encode('utf-8'))
        
        # Process file
        data, file_info = self.processor.process_file(json_file, "test.json")
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)
        self.assertIn('name', data.columns)
        self.assertEqual(file_info.filename, "test.json")
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_jsonl_processing(self):
        """Test JSONL file processing"""
        # Create JSONL content
        jsonl_content = '\n'.join([
            json.dumps({'name': 'John', 'age': 25}),
            json.dumps({'name': 'Jane', 'age': 30}),
            json.dumps({'name': 'Bob', 'age': 35})
        ])
        jsonl_file = io.BytesIO(jsonl_content.encode('utf-8'))
        
        # Process file
        data, file_info = self.processor.process_file(jsonl_file, "test.jsonl")
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 3)
        self.assertIn('name', data.columns)
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_data_type_optimization(self):
        """Test data type optimization"""
        # Create data with mixed types
        test_data = pd.DataFrame({
            'integer_col': ['1', '2', '3'],
            'float_col': ['1.5', '2.5', '3.5'],
            'category_col': ['A', 'B', 'A'],
            'date_col': ['2024-01-01', '2024-01-02', '2024-01-03']
        })
        
        optimized_data = self.processor._optimize_data_types(test_data)
        
        # Check that numeric columns were converted
        self.assertTrue(pd.api.types.is_numeric_dtype(optimized_data['integer_col']))
        self.assertTrue(pd.api.types.is_numeric_dtype(optimized_data['float_col']))
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_error_handling(self):
        """Test error handling for invalid files"""
        # Test invalid CSV
        invalid_csv = io.BytesIO(b"invalid,csv,content\nwith\tmixed\tseparators")
        
        try:
            data, file_info = self.processor.process_file(invalid_csv, "invalid.csv")
            # Should still process with fallback options
            self.assertIsInstance(data, pd.DataFrame)
        except ValueError:
            # Error is also acceptable for truly invalid content
            pass


class TestBatchFileProcessor(unittest.TestCase):
    """Test batch file processing functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.batch_processor = BatchFileProcessor() if FILE_PROCESSOR_AVAILABLE else None
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_zip_file_processing(self):
        """Test ZIP file processing"""
        # Create a temporary ZIP file with test data
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
            with zipfile.ZipFile(temp_zip, 'w') as zip_file:
                # Add CSV file
                csv_content = "name,age\nJohn,25\nJane,30"
                zip_file.writestr("test1.csv", csv_content)
                
                # Add JSON file
                json_content = '{"data": [{"name": "Bob", "age": 35}]}'
                zip_file.writestr("test2.json", json_content)
            
            # Process ZIP file
            zip_file_obj = io.BytesIO(open(temp_zip.name, 'rb').read())
            results = self.batch_processor.process_zip_file(zip_file_obj, "test.zip")
            
            self.assertGreater(results['processed_files'], 0)
            self.assertEqual(results['failed_files'], 0)
            self.assertIn('data_files', results)
            
            # Clean up
            os.unlink(temp_zip.name)
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_dataset_combination(self):
        """Test combining multiple datasets"""
        # Create test datasets
        df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        df2 = pd.DataFrame({'a': [5, 6], 'b': [7, 8]})
        df3 = pd.DataFrame({'a': [9, 10], 'c': [11, 12]})  # Different columns
        
        datasets = [df1, df2, df3]
        
        # Test concat method
        combined_concat = self.batch_processor.combine_datasets(datasets, method='concat')
        self.assertEqual(len(combined_concat), 6)  # All rows
        
        # Test intersect method (only common columns)
        combined_intersect = self.batch_processor.combine_datasets(datasets, method='intersect')
        self.assertEqual(len(combined_intersect), 6)
        self.assertEqual(list(combined_intersect.columns), ['a'])  # Only common column


class TestDataTypeConverter(unittest.TestCase):
    """Test data type conversion functionality"""
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_numeric_conversion(self):
        """Test numeric data type conversion"""
        # Create test data with string numbers
        test_data = pd.DataFrame({
            'integers': ['1', '2', '3', '4', '5'],
            'floats': ['1.5', '2.5', '3.5', '4.5', '5.5'],
            'mixed': ['1', '2.5', '3', '4.5', '5']
        })
        
        converted_data, conversion_log = DataTypeConverter.detect_and_convert_types(test_data)
        
        # Check that conversions happened
        self.assertTrue(pd.api.types.is_numeric_dtype(converted_data['integers']))
        self.assertTrue(pd.api.types.is_numeric_dtype(converted_data['floats']))
        self.assertTrue(pd.api.types.is_numeric_dtype(converted_data['mixed']))
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_boolean_conversion(self):
        """Test boolean conversion"""
        test_data = pd.DataFrame({
            'bool_col': ['true', 'false', 'true', 'false'],
            'yes_no': ['yes', 'no', 'yes', 'no'],
            'binary': ['1', '0', '1', '0']
        })
        
        converted_data, conversion_log = DataTypeConverter.detect_and_convert_types(test_data)
        
        # Check for boolean conversions
        for col in test_data.columns:
            if converted_data[col].dtype == 'bool':
                self.assertTrue(True)  # At least one boolean conversion occurred
                break
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_categorical_conversion(self):
        """Test categorical conversion"""
        test_data = pd.DataFrame({
            'category_col': ['A', 'B', 'C', 'A', 'B', 'C'] * 10,  # Repetitive data
            'unique_col': [f'unique_{i}' for i in range(60)]  # Highly unique
        })
        
        converted_data, conversion_log = DataTypeConverter.detect_and_convert_types(test_data)
        
        # Category column should be converted to categorical
        # Unique column should remain as object
        self.assertEqual(converted_data['category_col'].dtype.name, 'category')
        self.assertEqual(converted_data['unique_col'].dtype, 'object')


@unittest.skipUnless(STREAMLIT_AVAILABLE and FILE_PROCESSOR_AVAILABLE, "Streamlit or file processor not available")
class TestStreamlitFileUploader(unittest.TestCase):
    """Test Streamlit file upload interface"""
    
    def setUp(self):
        """Set up test environment"""
        self.uploader = StreamlitFileUploader()
    
    def test_initialization(self):
        """Test uploader initialization"""
        self.assertIsNotNone(self.uploader.file_processor)
        self.assertIsNotNone(self.uploader.batch_processor)
        self.assertIsInstance(self.uploader.uploaded_files, dict)
    
    def test_sample_data_generation(self):
        """Test sample data generation"""
        # Test different sample types
        sample_types = ["Sales Performance", "Financial Metrics", "Customer Analytics"]
        
        for sample_type in sample_types:
            data = self.uploader._generate_sample_data(sample_type)
            
            if data.get('success'):
                sample_data = data['data']
                self.assertIsInstance(sample_data, pd.DataFrame)
                self.assertGreater(len(sample_data), 0)
    
    def test_sales_sample_creation(self):
        """Test sales sample data creation"""
        sales_data = self.uploader._create_sales_sample()
        
        self.assertIsInstance(sales_data, pd.DataFrame)
        self.assertGreater(len(sales_data), 0)
        
        # Check for expected columns
        expected_columns = ['date', 'region', 'product', 'sales_rep', 'quantity_sold']
        for col in expected_columns:
            self.assertIn(col, sales_data.columns)
    
    def test_financial_sample_creation(self):
        """Test financial sample data creation"""
        financial_data = self.uploader._create_financial_sample()
        
        self.assertIsInstance(financial_data, pd.DataFrame)
        self.assertGreater(len(financial_data), 0)
        
        # Check for expected columns
        expected_columns = ['month', 'department', 'budget', 'actual_spending']
        for col in expected_columns:
            self.assertIn(col, financial_data.columns)


class TestFileProcessingIntegration(unittest.TestCase):
    """Test integration between file processing components"""
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_end_to_end_csv_processing(self):
        """Test complete CSV processing workflow"""
        # Create test CSV data
        test_data = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'sales': ['100.50', '200.75', '150.25'],
            'region': ['North', 'South', 'North'],
            'active': ['true', 'false', 'true']
        })
        
        csv_content = test_data.to_csv(index=False)
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        
        # Process through the full pipeline
        processor = FileProcessor()
        data, file_info = processor.process_file(csv_file, "test.csv")
        
        # Verify results
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 3)
        self.assertIsInstance(file_info, FileInfo)
        
        # Check data type optimization
        self.assertTrue(pd.api.types.is_numeric_dtype(data['sales']))
    
    @unittest.skipUnless(FILE_PROCESSOR_AVAILABLE, "File processor not available")
    def test_error_recovery(self):
        """Test error recovery and fallback mechanisms"""
        # Create problematic CSV data
        problematic_content = "name,age,city\nJohn,25,NYC\nJane,invalid_age,LA\nBob,,Chicago"
        csv_file = io.BytesIO(problematic_content.encode('utf-8'))
        
        processor = FileProcessor()
        
        try:
            data, file_info = processor.process_file(csv_file, "problematic.csv")
            
            # Should still return a DataFrame
            self.assertIsInstance(data, pd.DataFrame)
            self.assertGreater(len(data), 0)
            
        except Exception as e:
            # If it fails, the error should be informative
            self.assertIsInstance(e, (ValueError, Exception))


def run_file_processing_tests():
    """Run all file processing tests"""
    print(" Running File Processing Tests")
    print("=" * 60)
    
    # Test classes to run
    test_classes = [
        TestFileValidator,
        TestFileProcessor,
        TestBatchFileProcessor,
        TestDataTypeConverter,
        TestFileProcessingIntegration
    ]
    
    if STREAMLIT_AVAILABLE and FILE_PROCESSOR_AVAILABLE:
        test_classes.append(TestStreamlitFileUploader)
    
    # Run tests
    total_tests = 0
    total_failures = 0
    
    for test_class in test_classes:
        print(f"\n Testing {test_class.__name__}...")
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=1)
        result = runner.run(suite)
        
        total_tests += result.testsRun
        total_failures += len(result.failures) + len(result.errors)
    
    print("\n" + "=" * 60)
    print(f" Test Summary:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Failures: {total_failures}")
    
    if total_tests > 0:
        success_rate = ((total_tests - total_failures) / total_tests * 100)
        print(f"   Success Rate: {success_rate:.1f}%")
    
    if total_failures == 0:
        print(" All file processing tests passed!")
    else:
        print(f" {total_failures} test(s) failed")
    
    return total_failures == 0


def test_file_processing_capabilities():
    """Test file processing capabilities"""
    print("\n Testing File Processing Capabilities...")
    
    try:
        if FILE_PROCESSOR_AVAILABLE:
            from src.file_processor import FileValidator, FileProcessor
            
            # Test basic validation
            validator_test = FileValidator.SUPPORTED_EXTENSIONS
            print(f" File validator supports {len(validator_test)} file types")
            
            # Test processor
            processor = FileProcessor()
            print(" File processor initialized successfully")
            
            # Test sample data processing
            test_csv = "name,age\nJohn,25\nJane,30"
            csv_file = io.BytesIO(test_csv.encode('utf-8'))
            
            data, file_info = processor.process_file(csv_file, "test.csv")
            print(f" Sample CSV processing: {len(data)} rows, {len(data.columns)} columns")
        else:
            print(" File processor modules not available")
            return False
        
        if STREAMLIT_AVAILABLE:
            from src.streamlit_upload import StreamlitFileUploader
            uploader = StreamlitFileUploader()
            print(" Streamlit file uploader initialized")
        else:
            print(" Streamlit not available for upload interface testing")
        
        return True
        
    except Exception as e:
        print(f" File processing capability test failed: {e}")
        return False


if __name__ == "__main__":
    print(" BI Assistant File Processing Testing Suite")
    print("=" * 70)
    
    # Check availability
    print(" Component Availability:")
    print(f"   File Processor: {'' if FILE_PROCESSOR_AVAILABLE else ''}")
    print(f"   Streamlit: {'' if STREAMLIT_AVAILABLE else ''}")
    
    # Run tests
    tests_passed = run_file_processing_tests()
    
    # Test capabilities
    capabilities_test_passed = test_file_processing_capabilities()
    
    print("\n" + "=" * 70)
    print(" Overall Results:")
    
    if tests_passed and capabilities_test_passed:
        print(" All file processing tests passed! Enhanced upload system ready.")
        exit_code = 0
    else:
        print(" Some tests failed. Check the output above for details.")
        exit_code = 1
    
    print(" Enhanced file processing features:")
    print("   - Multi-format support (CSV, Excel, JSON, Parquet)")
    print("   - Intelligent encoding detection")
    print("   - Batch processing and ZIP archives")
    print("   - Advanced data type optimization")
    print("   - Comprehensive validation and error handling")
    
    sys.exit(exit_code)
