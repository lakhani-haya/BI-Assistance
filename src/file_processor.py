"""
Advanced File Upload and Processing Module
Handles comprehensive file validation, preprocessing, and batch operations
"""

import os
import io
import mimetypes
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import chardet
import xlrd
import openpyxl
from dataclasses import dataclass
import hashlib
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """File information container"""
    filename: str
    size_bytes: int
    mime_type: str
    encoding: Optional[str] = None
    detected_separator: Optional[str] = None
    sheet_names: Optional[List[str]] = None
    preview_data: Optional[pd.DataFrame] = None
    validation_errors: List[str] = None
    file_hash: Optional[str] = None
    upload_timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []
        if self.upload_timestamp is None:
            self.upload_timestamp = datetime.now()


class FileValidator:
    """Comprehensive file validation"""
    
    # Supported file types
    SUPPORTED_EXTENSIONS = {
        '.csv': 'text/csv',
        '.txt': 'text/plain',
        '.tsv': 'text/tab-separated-values',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.json': 'application/json',
        '.jsonl': 'application/jsonlines',
        '.parquet': 'application/octet-stream'
    }
    
    # Size limits (in bytes)
    MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
    MAX_PREVIEW_SIZE = 5 * 1024 * 1024  # 5MB for preview
    
    # Content validation
    MIN_ROWS = 1
    MAX_COLUMNS = 1000
    MAX_ROWS_PREVIEW = 10000
    
    @classmethod
    def validate_file(cls, file_obj, filename: str) -> Tuple[bool, List[str]]:
        """Comprehensive file validation"""
        errors = []
        
        # File extension validation
        file_ext = Path(filename).suffix.lower()
        if file_ext not in cls.SUPPORTED_EXTENSIONS:
            errors.append(f"Unsupported file format: {file_ext}")
            return False, errors
        
        # File size validation
        file_obj.seek(0, 2)  # Seek to end
        file_size = file_obj.tell()
        file_obj.seek(0)  # Reset to beginning
        
        if file_size == 0:
            errors.append("File is empty")
            return False, errors
        
        if file_size > cls.MAX_FILE_SIZE:
            errors.append(f"File too large: {file_size / (1024*1024):.1f}MB (max: {cls.MAX_FILE_SIZE / (1024*1024):.0f}MB)")
            return False, errors
        
        # Content validation for text files
        if file_ext in ['.csv', '.txt', '.tsv']:
            try:
                # Read first chunk to validate encoding
                chunk = file_obj.read(min(file_size, 10240))  # Read first 10KB
                file_obj.seek(0)
                
                # Try to decode
                encoding = cls.detect_encoding(chunk)
                if not encoding:
                    errors.append("Could not detect file encoding")
                    return False, errors
                
                # Validate content structure
                try:
                    decoded_content = chunk.decode(encoding)
                    if not decoded_content.strip():
                        errors.append("File appears to be empty or contains only whitespace")
                        return False, errors
                        
                except UnicodeDecodeError:
                    errors.append(f"File encoding detection failed")
                    return False, errors
                    
            except Exception as e:
                errors.append(f"Content validation failed: {str(e)}")
                return False, errors
        
        return True, errors
    
    @staticmethod
    def detect_encoding(byte_content: bytes) -> Optional[str]:
        """Detect file encoding"""
        try:
            # Use chardet for detection
            result = chardet.detect(byte_content)
            if result and result['confidence'] > 0.7:
                return result['encoding']
            
            # Fallback encodings to try
            fallback_encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in fallback_encodings:
                try:
                    byte_content.decode(encoding)
                    return encoding
                except UnicodeDecodeError:
                    continue
            
            return None
            
        except Exception:
            return 'utf-8'  # Final fallback
    
    @staticmethod
    def detect_csv_separator(content: str, max_lines: int = 10) -> str:
        """Detect CSV separator"""
        lines = content.split('\n')[:max_lines]
        separators = [',', ';', '\t', '|']
        
        separator_counts = {}
        for sep in separators:
            counts = [line.count(sep) for line in lines if line.strip()]
            if counts and len(set(counts)) == 1 and counts[0] > 0:
                separator_counts[sep] = counts[0]
        
        if separator_counts:
            return max(separator_counts.items(), key=lambda x: x[1])[0]
        
        return ','  # Default fallback


class FileProcessor:
    """Advanced file processing and data extraction"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="bi_assistant_")
        self.processed_files = {}
    
    def process_file(self, file_obj, filename: str, 
                    encoding: Optional[str] = None,
                    separator: Optional[str] = None,
                    sheet_name: Optional[str] = None) -> Tuple[pd.DataFrame, FileInfo]:
        """Process uploaded file and extract data"""
        
        # Create file info
        file_info = self._create_file_info(file_obj, filename)
        
        # Validate file
        is_valid, errors = FileValidator.validate_file(file_obj, filename)
        if not is_valid:
            file_info.validation_errors = errors
            raise ValueError(f"File validation failed: {'; '.join(errors)}")
        
        # Extract data based on file type
        file_ext = Path(filename).suffix.lower()
        
        try:
            if file_ext == '.csv':
                data = self._process_csv(file_obj, file_info, encoding, separator)
            elif file_ext == '.txt':
                data = self._process_txt(file_obj, file_info, encoding, separator)
            elif file_ext == '.tsv':
                data = self._process_tsv(file_obj, file_info, encoding)
            elif file_ext in ['.xlsx', '.xls']:
                data = self._process_excel(file_obj, file_info, sheet_name)
            elif file_ext == '.json':
                data = self._process_json(file_obj, file_info)
            elif file_ext == '.jsonl':
                data = self._process_jsonl(file_obj, file_info)
            elif file_ext == '.parquet':
                data = self._process_parquet(file_obj, file_info)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            # Post-process data
            data = self._post_process_data(data, file_info)
            
            # Create preview
            file_info.preview_data = data.head(100).copy()
            
            # Store processed file info
            self.processed_files[file_info.file_hash] = file_info
            
            logger.info(f"Successfully processed {filename}: {len(data)} rows, {len(data.columns)} columns")
            
            return data, file_info
            
        except Exception as e:
            error_msg = f"Error processing {filename}: {str(e)}"
            file_info.validation_errors.append(error_msg)
            logger.error(error_msg)
            raise
    
    def _create_file_info(self, file_obj, filename: str) -> FileInfo:
        """Create file information object"""
        # Get file size
        file_obj.seek(0, 2)
        size_bytes = file_obj.tell()
        file_obj.seek(0)
        
        # Calculate file hash
        content = file_obj.read()
        file_hash = hashlib.md5(content).hexdigest()
        file_obj.seek(0)
        
        # Detect MIME type
        mime_type = mimetypes.guess_type(filename)[0]
        if not mime_type:
            file_ext = Path(filename).suffix.lower()
            mime_type = FileValidator.SUPPORTED_EXTENSIONS.get(file_ext, 'application/octet-stream')
        
        return FileInfo(
            filename=filename,
            size_bytes=size_bytes,
            mime_type=mime_type,
            file_hash=file_hash
        )
    
    def _process_csv(self, file_obj, file_info: FileInfo, 
                    encoding: Optional[str] = None,
                    separator: Optional[str] = None) -> pd.DataFrame:
        """Process CSV file"""
        # Detect encoding if not provided
        if not encoding:
            content_bytes = file_obj.read(10240)  # Read first 10KB
            file_obj.seek(0)
            encoding = FileValidator.detect_encoding(content_bytes)
            if not encoding:
                encoding = 'utf-8'
        
        file_info.encoding = encoding
        
        # Detect separator if not provided
        if not separator:
            try:
                content_sample = file_obj.read(10240).decode(encoding)
                file_obj.seek(0)
                separator = FileValidator.detect_csv_separator(content_sample)
            except:
                separator = ','
        
        file_info.detected_separator = separator
        
        # Read CSV with pandas
        try:
            data = pd.read_csv(
                file_obj,
                encoding=encoding,
                sep=separator,
                low_memory=False,
                encoding_errors='replace'
            )
            return data
        except Exception as e:
            # Try with different parameters
            file_obj.seek(0)
            try:
                data = pd.read_csv(
                    file_obj,
                    encoding=encoding,
                    sep=separator,
                    low_memory=False,
                    encoding_errors='replace',
                    error_bad_lines=False,
                    warn_bad_lines=True
                )
                return data
            except:
                # Final attempt with most permissive settings
                file_obj.seek(0)
                data = pd.read_csv(
                    file_obj,
                    encoding='utf-8',
                    sep=None,  # Let pandas detect
                    engine='python',
                    encoding_errors='replace',
                    on_bad_lines='skip'
                )
                return data
    
    def _process_txt(self, file_obj, file_info: FileInfo,
                    encoding: Optional[str] = None,
                    separator: Optional[str] = None) -> pd.DataFrame:
        """Process TXT file (assume CSV-like format)"""
        return self._process_csv(file_obj, file_info, encoding, separator)
    
    def _process_tsv(self, file_obj, file_info: FileInfo,
                    encoding: Optional[str] = None) -> pd.DataFrame:
        """Process TSV file"""
        return self._process_csv(file_obj, file_info, encoding, '\t')
    
    def _process_excel(self, file_obj, file_info: FileInfo,
                      sheet_name: Optional[str] = None) -> pd.DataFrame:
        """Process Excel file"""
        # Get sheet names
        try:
            if file_info.filename.endswith('.xlsx'):
                wb = openpyxl.load_workbook(file_obj, read_only=True)
                sheet_names = wb.sheetnames
                wb.close()
            else:  # .xls
                file_obj.seek(0)
                wb = xlrd.open_workbook(file_contents=file_obj.read())
                sheet_names = wb.sheet_names()
            
            file_info.sheet_names = sheet_names
            file_obj.seek(0)
            
        except Exception as e:
            logger.warning(f"Could not read sheet names: {e}")
            file_info.sheet_names = []
        
        # Read data
        try:
            if sheet_name and sheet_name in file_info.sheet_names:
                data = pd.read_excel(file_obj, sheet_name=sheet_name)
            elif file_info.sheet_names:
                data = pd.read_excel(file_obj, sheet_name=file_info.sheet_names[0])
            else:
                data = pd.read_excel(file_obj)
            
            return data
            
        except Exception as e:
            # Fallback to first sheet
            file_obj.seek(0)
            data = pd.read_excel(file_obj, sheet_name=0)
            return data
    
    def _process_json(self, file_obj, file_info: FileInfo) -> pd.DataFrame:
        """Process JSON file"""
        try:
            # Detect encoding
            content_bytes = file_obj.read()
            encoding = FileValidator.detect_encoding(content_bytes)
            if not encoding:
                encoding = 'utf-8'
            
            file_info.encoding = encoding
            
            # Parse JSON
            content = content_bytes.decode(encoding)
            json_data = json.loads(content)
            
            # Convert to DataFrame
            if isinstance(json_data, list):
                data = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                # Try to find the main data array
                for key, value in json_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        data = pd.DataFrame(value)
                        break
                else:
                    # Treat as single record
                    data = pd.DataFrame([json_data])
            else:
                raise ValueError("JSON format not supported for tabular data")
            
            return data
            
        except Exception as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
    
    def _process_jsonl(self, file_obj, file_info: FileInfo) -> pd.DataFrame:
        """Process JSONL (JSON Lines) file"""
        try:
            # Detect encoding
            content_bytes = file_obj.read()
            encoding = FileValidator.detect_encoding(content_bytes)
            if not encoding:
                encoding = 'utf-8'
            
            file_info.encoding = encoding
            
            # Parse JSONL
            content = content_bytes.decode(encoding)
            lines = content.strip().split('\n')
            
            records = []
            for line in lines:
                if line.strip():
                    try:
                        record = json.loads(line)
                        records.append(record)
                    except json.JSONDecodeError:
                        continue
            
            if not records:
                raise ValueError("No valid JSON records found")
            
            data = pd.DataFrame(records)
            return data
            
        except Exception as e:
            raise ValueError(f"Invalid JSONL format: {str(e)}")
    
    def _process_parquet(self, file_obj, file_info: FileInfo) -> pd.DataFrame:
        """Process Parquet file"""
        try:
            data = pd.read_parquet(file_obj)
            return data
        except Exception as e:
            raise ValueError(f"Invalid Parquet format: {str(e)}")
    
    def _post_process_data(self, data: pd.DataFrame, file_info: FileInfo) -> pd.DataFrame:
        """Post-process loaded data"""
        # Basic validation
        if data.empty:
            raise ValueError("File contains no data")
        
        if len(data.columns) > FileValidator.MAX_COLUMNS:
            raise ValueError(f"Too many columns: {len(data.columns)} (max: {FileValidator.MAX_COLUMNS})")
        
        # Clean column names
        data.columns = data.columns.astype(str)
        data.columns = [col.strip() for col in data.columns]
        
        # Handle duplicate column names
        cols = pd.Series(data.columns)
        for dup in cols[cols.duplicated()].unique():
            cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup 
                                                            for i in range(sum(cols == dup))]
        data.columns = cols
        
        # Remove completely empty rows and columns
        data = data.dropna(how='all').loc[:, data.notna().any()]
        
        # Data type optimization
        data = self._optimize_data_types(data)
        
        return data
    
    def _optimize_data_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """Optimize data types for memory efficiency"""
        optimized_data = data.copy()
        
        for col in optimized_data.columns:
            col_data = optimized_data[col]
            
            # Skip if all values are null
            if col_data.isna().all():
                continue
            
            # Try to convert to numeric
            if col_data.dtype == 'object':
                # Try to convert to numeric
                numeric_data = pd.to_numeric(col_data, errors='coerce')
                
                # If most values converted successfully, use numeric type
                conversion_rate = numeric_data.notna().sum() / len(col_data)
                if conversion_rate > 0.8:  # 80% conversion success
                    optimized_data[col] = numeric_data
                    continue
                
                # Try to convert to datetime
                if col_data.notna().sum() > 0:
                    try:
                        datetime_data = pd.to_datetime(col_data, errors='coerce', infer_datetime_format=True)
                        conversion_rate = datetime_data.notna().sum() / col_data.notna().sum()
                        if conversion_rate > 0.7:  # 70% conversion success
                            optimized_data[col] = datetime_data
                            continue
                    except:
                        pass
                
                # Check if it could be categorical
                unique_ratio = col_data.nunique() / len(col_data)
                if unique_ratio < 0.5 and col_data.nunique() < 1000:
                    optimized_data[col] = col_data.astype('category')
        
        return optimized_data


class BatchFileProcessor:
    """Process multiple files in batch"""
    
    def __init__(self):
        self.file_processor = FileProcessor()
        self.batch_results = {}
    
    def process_zip_file(self, zip_file_obj, filename: str) -> Dict[str, Any]:
        """Process ZIP file containing multiple data files"""
        results = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'data_files': {},
            'errors': []
        }
        
        try:
            with zipfile.ZipFile(zip_file_obj, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                results['total_files'] = len(file_list)
                
                for file_path in file_list:
                    if file_path.endswith('/'):  # Skip directories
                        continue
                    
                    file_ext = Path(file_path).suffix.lower()
                    if file_ext not in FileValidator.SUPPORTED_EXTENSIONS:
                        continue
                    
                    try:
                        # Extract and process file
                        with zip_ref.open(file_path) as extracted_file:
                            file_content = io.BytesIO(extracted_file.read())
                            
                            data, file_info = self.file_processor.process_file(
                                file_content, 
                                Path(file_path).name
                            )
                            
                            results['data_files'][file_path] = {
                                'data': data,
                                'info': file_info,
                                'status': 'success'
                            }
                            results['processed_files'] += 1
                            
                    except Exception as e:
                        error_msg = f"Failed to process {file_path}: {str(e)}"
                        results['errors'].append(error_msg)
                        results['failed_files'] += 1
                        logger.error(error_msg)
        
        except Exception as e:
            error_msg = f"Failed to process ZIP file {filename}: {str(e)}"
            results['errors'].append(error_msg)
            logger.error(error_msg)
        
        return results
    
    def combine_datasets(self, datasets: List[pd.DataFrame], 
                        method: str = 'concat') -> pd.DataFrame:
        """Combine multiple datasets"""
        if not datasets:
            raise ValueError("No datasets to combine")
        
        if len(datasets) == 1:
            return datasets[0]
        
        try:
            if method == 'concat':
                # Simple concatenation
                combined = pd.concat(datasets, ignore_index=True, sort=False)
            elif method == 'union':
                # Union of columns (outer join)
                combined = pd.concat(datasets, ignore_index=True, sort=False)
            elif method == 'intersect':
                # Intersection of columns (inner join)
                common_cols = set(datasets[0].columns)
                for df in datasets[1:]:
                    common_cols = common_cols.intersection(set(df.columns))
                
                filtered_datasets = [df[list(common_cols)] for df in datasets]
                combined = pd.concat(filtered_datasets, ignore_index=True)
            else:
                raise ValueError(f"Unknown combination method: {method}")
            
            return combined
            
        except Exception as e:
            raise ValueError(f"Failed to combine datasets: {str(e)}")


class DataTypeConverter:
    """Advanced data type detection and conversion"""
    
    @staticmethod
    def detect_and_convert_types(data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
        """Detect and convert data types intelligently"""
        converted_data = data.copy()
        conversion_log = {}
        
        for col in data.columns:
            original_type = str(data[col].dtype)
            converted_type = DataTypeConverter._convert_column(converted_data, col)
            
            if converted_type != original_type:
                conversion_log[col] = {
                    'from': original_type,
                    'to': converted_type,
                    'samples': converted_data[col].dropna().head(3).tolist()
                }
        
        return converted_data, conversion_log
    
    @staticmethod
    def _convert_column(data: pd.DataFrame, col: str) -> str:
        """Convert a single column to optimal data type"""
        series = data[col]
        
        # Skip if already optimal or mostly null
        if series.isna().sum() / len(series) > 0.9:
            return str(series.dtype)
        
        # Try numeric conversion
        if series.dtype == 'object':
            # Clean numeric strings
            cleaned_series = series.astype(str).str.replace(r'[^\d.-]', '', regex=True)
            numeric_series = pd.to_numeric(cleaned_series, errors='coerce')
            
            # Check conversion success rate
            success_rate = numeric_series.notna().sum() / series.notna().sum()
            if success_rate > 0.8:
                # Determine if integer or float
                if numeric_series.dropna().apply(lambda x: x.is_integer()).all():
                    # Check if it fits in smaller integer types
                    max_val = numeric_series.max()
                    min_val = numeric_series.min()
                    
                    if min_val >= 0 and max_val <= 255:
                        data[col] = numeric_series.astype('uint8')
                        return 'uint8'
                    elif min_val >= -128 and max_val <= 127:
                        data[col] = numeric_series.astype('int8')
                        return 'int8'
                    elif min_val >= 0 and max_val <= 65535:
                        data[col] = numeric_series.astype('uint16')
                        return 'uint16'
                    elif min_val >= -32768 and max_val <= 32767:
                        data[col] = numeric_series.astype('int16')
                        return 'int16'
                    elif min_val >= 0 and max_val <= 4294967295:
                        data[col] = numeric_series.astype('uint32')
                        return 'uint32'
                    elif min_val >= -2147483648 and max_val <= 2147483647:
                        data[col] = numeric_series.astype('int32')
                        return 'int32'
                    else:
                        data[col] = numeric_series.astype('int64')
                        return 'int64'
                else:
                    data[col] = numeric_series.astype('float32')
                    return 'float32'
            
            # Try datetime conversion
            try:
                datetime_series = pd.to_datetime(series, errors='coerce', infer_datetime_format=True)
                success_rate = datetime_series.notna().sum() / series.notna().sum()
                if success_rate > 0.7:
                    data[col] = datetime_series
                    return 'datetime64[ns]'
            except:
                pass
            
            # Try boolean conversion
            boolean_values = {'true', 'false', 'yes', 'no', '1', '0', 'y', 'n'}
            unique_values = set(series.dropna().astype(str).str.lower().unique())
            if unique_values.issubset(boolean_values) and len(unique_values) <= 2:
                bool_mapping = {
                    'true': True, 'false': False, 'yes': True, 'no': False,
                    '1': True, '0': False, 'y': True, 'n': False
                }
                data[col] = series.astype(str).str.lower().map(bool_mapping)
                return 'bool'
            
            # Consider categorical
            unique_ratio = series.nunique() / len(series)
            if unique_ratio < 0.5 and series.nunique() < 1000:
                data[col] = series.astype('category')
                return 'category'
        
        return str(series.dtype)


# Export main classes
__all__ = [
    'FileInfo',
    'FileValidator', 
    'FileProcessor',
    'BatchFileProcessor',
    'DataTypeConverter'
]
