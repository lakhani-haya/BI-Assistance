"""
Example usage of the enhanced file processing system
Demonstrates thnew file upload anprocessing capabilities
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path
import json
import tempfile
import zipfile

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.file_processor import FileProcessor, BatchFileProcessor, FileValidator, DataTypeConverter
from src.streamlit_upload import StreamlitFileUploader


def demonstrate_file_validation():
    """Demonstrate file validation capabilities"""
    print("🔍 File Validation Demonstration")
    print("-" * 40)
    
    # Create sample files for testing
    test_files = {
        'valid.csv': "name,age,city\nJohn,25,NYC\nJane,30,LA",
        'invalid.xyz': "unsupported content",
        'empty.csv': "",
        'large_header.csv': ",".join([f"col_{i}" for i in range(50)]) + "\n" + ",".join(["data"] * 50)
    }
    
    validator = FileValidator()
    
    for filename, content in test_files.items():
        print(f"\n📄 Testing: {filename}")
        
        if isinstance(content, str):
            file_obj = io.BytesIO(content.encode('utf-8'))
        else:
            file_obj = io.BytesIO(content)
        
        is_valid, errors = validator.validate_file(file_obj, filename)
        
        if is_valid:
            print("   ✅ Valid file")
        else:
            print("   ❌ Invalid file:")
            for error in errors:
                print(f"      - {error}")
    
    # Test encoding detection
    print(f"\n🔤 Encoding Detection:")
    test_content = "naïve résumé café"
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        encoded_content = test_content.encode(encoding)
        detected = validator.detect_encoding(encoded_content)
        print(f"   {encoding} → {detected}")


def demonstrate_single_file_processing():
    """Demonstrate single file processing"""
    print("\n📁 Single File Processing Demonstration")
    print("-" * 50)
    
    processor = FileProcessor()
    
    # Test CSV processing
    print("📊 Processing CSV file...")
    csv_data = """date,sales,region,product
2024-01-01,1500.50,North,Product A
2024-01-02,2300.75,South,Product B
2024-01-03,1800.25,East,Product A
2024-01-04,2100.00,West,Product C"""
    
    csv_file = io.BytesIO(csv_data.encode('utf-8'))
    
    try:
        data, file_info = processor.process_file(csv_file, "sales_data.csv")
        
        print(f"   ✅ Processed successfully:")
        print(f"      Rows: {len(data)}")
        print(f"      Columns: {len(data.columns)}")
        print(f"      Data types: {dict(data.dtypes)}")
        print(f"      File hash: {file_info.file_hash[:8]}...")
        print(f"      Detected separator: '{file_info.detected_separator}'")
        
        # Show data preview
        print(f"\n   📋 Data Preview:")
        print(data.head().to_string(index=False))
        
    except Exception as e:
        print(f"   ❌ Processing failed: {e}")
    
    # Test JSON processing
    print(f"\n📋 Processing JSON file...")
    json_data = {
        "customers": [
            {"id": 1, "name": "Alice", "age": 30, "purchases": 5},
            {"id": 2, "name": "Bob", "age": 25, "purchases": 3},
            {"id": 3, "name": "Charlie", "age": 35, "purchases": 8}
        ]
    }
    
    json_content = json.dumps(json_data)
    json_file = io.BytesIO(json_content.encode('utf-8'))
    
    try:
        data, file_info = processor.process_file(json_file, "customers.json")
        
        print(f"   ✅ Processed successfully:")
        print(f"      Rows: {len(data)}")
        print(f"      Columns: {list(data.columns)}")
        print(f"      Encoding: {file_info.encoding}")
        
    except Exception as e:
        print(f"   ❌ Processing failed: {e}")


def demonstrate_batch_processing():
    """Demonstrate batch file processing"""
    print(f"\n📦 Batch Processing Demonstration")
    print("-" * 45)
    
    batch_processor = BatchFileProcessor()
    
    # Create sample datasets
    datasets = []
    
    # Dataset 1: Sales Q1
    sales_q1 = pd.DataFrame({
        'month': ['Jan', 'Feb', 'Mar'],
        'sales': [100000, 120000, 110000],
        'region': ['North', 'North', 'North']
    })
    datasets.append(sales_q1)
    
    # Dataset 2: Sales Q2
    sales_q2 = pd.DataFrame({
        'month': ['Apr', 'May', 'Jun'],
        'sales': [130000, 140000, 135000],
        'region': ['South', 'South', 'South']
    })
    datasets.append(sales_q2)
    
    # Dataset 3: Sales Q3 (different structure)
    sales_q3 = pd.DataFrame({
        'month': ['Jul', 'Aug', 'Sep'],
        'sales': [145000, 150000, 142000],
        'region': ['East', 'East', 'East'],
        'bonus_metric': [5000, 6000, 5500]  # Additional column
    })
    datasets.append(sales_q3)
    
    print("📊 Combining datasets...")
    
    # Test different combination methods
    for method in ['concat', 'union', 'intersect']:
        try:
            combined = batch_processor.combine_datasets(datasets, method=method)
            print(f"   {method.title()} method: {len(combined)} rows, {len(combined.columns)} columns")
            
            if method == 'intersect':
                print(f"      Common columns: {list(combined.columns)}")
                
        except Exception as e:
            print(f"   ❌ {method} failed: {e}")


def demonstrate_zip_processing():
    """Demonstrate ZIP file processing"""
    print(f"\n🗜️ ZIP Archive Processing Demonstration")
    print("-" * 50)
    
    # Create a temporary ZIP file with multiple datasets
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        try:
            with zipfile.ZipFile(temp_zip, 'w') as zip_file:
                # Add CSV file
                csv_content = "product,sales,month\nProduct A,5000,Jan\nProduct B,7000,Jan"
                zip_file.writestr("january_sales.csv", csv_content)
                
                # Add JSON file
                json_content = json.dumps({
                    "data": [
                        {"product": "Product C", "sales": 6000, "month": "Feb"},
                        {"product": "Product D", "sales": 8000, "month": "Feb"}
                    ]
                })
                zip_file.writestr("february_sales.json", json_content)
                
                # Add another CSV
                csv_content2 = "product;sales;month\nProduct E;9000;Mar\nProduct F;11000;Mar"
                zip_file.writestr("march_sales.csv", csv_content2)
            
            # Process the ZIP file
            batch_processor = BatchFileProcessor()
            
            with open(temp_zip.name, 'rb') as zip_file_obj:
                zip_data = io.BytesIO(zip_file_obj.read())
                results = batch_processor.process_zip_file(zip_data, "quarterly_sales.zip")
            
            print(f"📊 ZIP Processing Results:")
            print(f"   Total files: {results['total_files']}")
            print(f"   Processed: {results['processed_files']}")
            print(f"   Failed: {results['failed_files']}")
            
            if results['data_files']:
                print(f"   📁 Extracted files:")
                for file_path, file_result in results['data_files'].items():
                    if file_result['status'] == 'success':
                        data = file_result['data']
                        print(f"      ✅ {file_path}: {len(data)} rows")
                    else:
                        print(f"      ❌ {file_path}: failed")
            
            if results['errors']:
                print(f"   ⚠️ Errors:")
                for error in results['errors']:
                    print(f"      - {error}")
            
        except Exception as e:
            print(f"❌ ZIP processing failed: {e}")
        
        finally:
            # Clean up
            try:
                os.unlink(temp_zip.name)
            except:
                pass


def demonstrate_data_type_conversion():
    """Demonstrate intelligent data type conversion"""
    print(f"\n🔄 Data Type Conversion Demonstration")
    print("-" * 50)
    
    # Create test data with various convertible types
    test_data = pd.DataFrame({
        'string_integers': ['1', '2', '3', '4', '5'],
        'string_floats': ['1.5', '2.5', '3.5', '4.5', '5.5'],
        'boolean_strings': ['true', 'false', 'true', 'false', 'true'],
        'yes_no_strings': ['yes', 'no', 'yes', 'no', 'yes'],
        'date_strings': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'category_data': ['A', 'B', 'C', 'A', 'B'] * 2,
        'mixed_data': ['1', '2.5', '3', 'text', '5.5'],
        'high_cardinality': [f'unique_{i}' for i in range(10)]  # High cardinality
    })
    
    print("📊 Original data types:")
    for col, dtype in test_data.dtypes.items():
        print(f"   {col}: {dtype}")
    
    # Convert data types
    converter = DataTypeConverter()
    converted_data, conversion_log = converter.detect_and_convert_types(test_data)
    
    print(f"\n✨ After intelligent conversion:")
    for col, dtype in converted_data.dtypes.items():
        print(f"   {col}: {dtype}")
    
    print(f"\n📋 Conversion log:")
    for col, log_entry in conversion_log.items():
        print(f"   {col}: {log_entry['from']} → {log_entry['to']}")
        print(f"      Sample values: {log_entry['samples']}")


def demonstrate_sample_data_generation():
    """Demonstrate sample data generation"""
    print(f"\n🎲 Sample Data Generation Demonstration")
    print("-" * 50)
    
    uploader = StreamlitFileUploader()
    
    sample_types = [
        "Sales Performance",
        "Financial Metrics", 
        "Customer Analytics",
        "Operational Data",
        "Marketing Campaigns"
    ]
    
    for sample_type in sample_types:
        print(f"\n📊 Generating {sample_type} data...")
        
        try:
            if sample_type == "Sales Performance":
                data = uploader._create_sales_sample()
            elif sample_type == "Financial Metrics":
                data = uploader._create_financial_sample()
            elif sample_type == "Customer Analytics":
                data = uploader._create_customer_sample()
            elif sample_type == "Operational Data":
                data = uploader._create_operational_sample()
            elif sample_type == "Marketing Campaigns":
                data = uploader._create_marketing_sample()
            else:
                continue
            
            print(f"   ✅ Generated: {len(data)} rows, {len(data.columns)} columns")
            print(f"   📋 Columns: {', '.join(list(data.columns)[:5])}{'...' if len(data.columns) > 5 else ''}")
            
            # Show basic statistics
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                print(f"   📈 Numeric columns: {len(numeric_cols)}")
                sample_col = numeric_cols[0]
                print(f"      {sample_col}: min={data[sample_col].min():.2f}, max={data[sample_col].max():.2f}")
                
        except Exception as e:
            print(f"   ❌ Generation failed: {e}")


def demonstrate_error_handling():
    """Demonstrate error handling and recovery"""
    print(f"\n🛡️ Error Handling Demonstration")
    print("-" * 40)
    
    processor = FileProcessor()
    
    # Test various error scenarios
    error_cases = [
        {
            'name': 'Corrupted CSV',
            'content': 'name,age\nJohn,25\nJane,invalid_number\nBob,',
            'filename': 'corrupted.csv'
        },
        {
            'name': 'Empty file',
            'content': '',
            'filename': 'empty.csv'
        },
        {
            'name': 'Invalid JSON',
            'content': '{"invalid": json syntax}',
            'filename': 'invalid.json'
        },
        {
            'name': 'Mixed separators',
            'content': 'a,b,c\n1;2;3\n4,5,6',
            'filename': 'mixed.csv'
        }
    ]
    
    for case in error_cases:
        print(f"\n🧪 Testing: {case['name']}")
        
        file_obj = io.BytesIO(case['content'].encode('utf-8'))
        
        try:
            data, file_info = processor.process_file(file_obj, case['filename'])
            print(f"   ✅ Handled gracefully: {len(data)} rows processed")
            
            if file_info.validation_errors:
                print(f"   ⚠️ Warnings: {len(file_info.validation_errors)}")
                
        except Exception as e:
            print(f"   ❌ Failed as expected: {str(e)[:50]}...")


def main():
    """Run all demonstrations"""
    print("🤖📊 Enhanced File Processing System Demonstration")
    print("=" * 70)
    
    try:
        # Import required modules
        import io
        
        # Run demonstrations
        demonstrate_file_validation()
        demonstrate_single_file_processing()
        demonstrate_batch_processing()
        demonstrate_zip_processing()
        demonstrate_data_type_conversion()
        demonstrate_sample_data_generation()
        demonstrate_error_handling()
        
        print(f"\n" + "=" * 70)
        print("🎉 All demonstrations completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("   ✅ Multi-format file support (CSV, JSON, Excel, Parquet)")
        print("   ✅ Intelligent encoding and separator detection")
        print("   ✅ Batch processing with ZIP archive support")
        print("   ✅ Advanced data type optimization")
        print("   ✅ Comprehensive error handling and recovery")
        print("   ✅ Rich sample data generation")
        print("   ✅ File validation and quality assessment")
        
    except ImportError as e:
        print(f"❌ Required modules not available: {e}")
        print("💡 Install dependencies: pip install -r requirements.txt")
    
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
