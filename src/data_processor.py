"""
Data processing module for file handling and analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Data processing utilities"""
    
    def __init__(self):
        self.data = None
        self.original_data = None
        self.data_info = {}
        self.supported_formats = ['.csv', '.xlsx', '.xls']
        
    def load_file(self, file_path: str) -> bool:
        """
        Load data from CSV or Excel file
        
        Args:
            file_path (str): Path to the data file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            logger.info(f"Loading file: {file_path}")
            
            if file_extension == '.csv':
                # Try different encodings for CSV files
                encodings = ['utf-8', 'latin-1', 'cp1252']
                for encoding in encodings:
                    try:
                        self.data = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("Could not decode CSV file with any supported encoding")
                    
            elif file_extension in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            
            # Store original data for reference
            self.original_data = self.data.copy()
            logger.info(f"Successfully loaded {len(self.data)} rows and {len(self.data.columns)} columns")
            
            # Generate basic info about the dataset
            self._generate_data_info()
            return True
            
        except Exception as e:
            logger.error(f"Error loading file: {str(e)}")
            return False
    
    def load_dataframe(self, df: pd.DataFrame) -> bool:
        """
        Load data from a pandas DataFrame
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            bool: True if successful
        """
        try:
            self.data = df.copy()
            self.original_data = df.copy()
            self._generate_data_info()
            logger.info(f"Successfully loaded DataFrame with {len(self.data)} rows and {len(self.data.columns)} columns")
            return True
        except Exception as e:
            logger.error(f"Error loading DataFrame: {str(e)}")
            return False
    
    def _generate_data_info(self):
        """Generate comprehensive information about the dataset"""
        if self.data is None:
            return
        
        self.data_info = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'duplicate_rows': self.data.duplicated().sum(),
            'numeric_columns': list(self.data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(self.data.select_dtypes(include=['object', 'category']).columns),
            'datetime_columns': list(self.data.select_dtypes(include=['datetime64']).columns)
        }
        
        # Add statistical summary for numeric columns
        if self.data_info['numeric_columns']:
            self.data_info['numeric_summary'] = self.data[self.data_info['numeric_columns']].describe().to_dict()
        
        # Add value counts for categorical columns (top 10)
        categorical_summary = {}
        for col in self.data_info['categorical_columns']:
            if len(self.data[col].unique()) <= 50:  # Only for columns with reasonable number of unique values
                categorical_summary[col] = self.data[col].value_counts().head(10).to_dict()
        self.data_info['categorical_summary'] = categorical_summary
    
    def clean_data(self, 
                   drop_duplicates: bool = True,
                   handle_missing: str = 'auto',
                   convert_dtypes: bool = True) -> Dict[str, Any]:
        """
        Clean the loaded data
        
        Args:
            drop_duplicates (bool): Whether to drop duplicate rows
            handle_missing (str): How to handle missing values ('drop', 'fill', 'auto')
            convert_dtypes (bool): Whether to automatically convert data types
            
        Returns:
            Dict: Summary of cleaning operations performed
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        cleaning_summary = {
            'original_shape': self.data.shape,
            'operations_performed': []
        }
        
        # Drop duplicates
        if drop_duplicates:
            duplicates_before = self.data.duplicated().sum()
            self.data = self.data.drop_duplicates()
            duplicates_removed = duplicates_before - self.data.duplicated().sum()
            if duplicates_removed > 0:
                cleaning_summary['operations_performed'].append(f"Removed {duplicates_removed} duplicate rows")
        
        # Handle missing values
        if handle_missing != 'none':
            missing_before = self.data.isnull().sum().sum()
            
            if handle_missing == 'drop':
                self.data = self.data.dropna()
                cleaning_summary['operations_performed'].append("Dropped rows with missing values")
            
            elif handle_missing == 'fill':
                # Fill numeric columns with median, categorical with mode
                for col in self.data.columns:
                    if self.data[col].dtype in ['int64', 'float64']:
                        self.data[col].fillna(self.data[col].median(), inplace=True)
                    else:
                        mode_val = self.data[col].mode()
                        if len(mode_val) > 0:
                            self.data[col].fillna(mode_val[0], inplace=True)
                cleaning_summary['operations_performed'].append("Filled missing values (median for numeric, mode for categorical)")
            
            elif handle_missing == 'auto':
                # Smart handling based on missing percentage
                for col in self.data.columns:
                    missing_pct = self.data[col].isnull().sum() / len(self.data)
                    
                    if missing_pct > 0.5:  # If more than 50% missing, consider dropping column
                        cleaning_summary['operations_performed'].append(f"Column '{col}' has {missing_pct:.1%} missing values - consider review")
                    elif missing_pct > 0:
                        if self.data[col].dtype in ['int64', 'float64']:
                            self.data[col].fillna(self.data[col].median(), inplace=True)
                        else:
                            mode_val = self.data[col].mode()
                            if len(mode_val) > 0:
                                self.data[col].fillna(mode_val[0], inplace=True)
            
            missing_after = self.data.isnull().sum().sum()
            if missing_before > missing_after:
                cleaning_summary['operations_performed'].append(f"Handled {missing_before - missing_after} missing values")
        
        # Convert data types
        if convert_dtypes:
            conversions = []
            for col in self.data.columns:
                original_dtype = str(self.data[col].dtype)
                
                # Try to convert to datetime
                if self.data[col].dtype == 'object':
                    # Check if column might be datetime
                    sample_values = self.data[col].dropna().head(10)
                    datetime_indicators = ['date', 'time', 'created', 'updated', 'timestamp']
                    
                    if any(indicator in col.lower() for indicator in datetime_indicators):
                        try:
                            self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
                            if not self.data[col].isnull().all():
                                conversions.append(f"{col}: {original_dtype} → datetime64")
                        except:
                            pass
                    
                    # Try to convert to numeric
                    else:
                        try:
                            numeric_col = pd.to_numeric(self.data[col], errors='coerce')
                            # Only convert if we don't lose too much data
                            if numeric_col.notna().sum() / len(self.data[col]) > 0.8:
                                self.data[col] = numeric_col
                                conversions.append(f"{col}: {original_dtype} → numeric")
                        except:
                            pass
            
            if conversions:
                cleaning_summary['operations_performed'].extend(conversions)
        
        cleaning_summary['final_shape'] = self.data.shape
        
        # Update data info after cleaning
        self._generate_data_info()
        
        logger.info(f"Data cleaning completed. Shape: {cleaning_summary['original_shape']} → {cleaning_summary['final_shape']}")
        return cleaning_summary
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive summary of the current dataset
        
        Returns:
            Dict: Dataset summary including statistics and insights
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        summary = {
            "basic_info": {
                "rows": len(self.data),
                "columns": len(self.data.columns),
                "memory_usage_mb": round(self.data_info['memory_usage'] / (1024*1024), 2),
                "missing_values_total": sum(self.data_info['missing_values'].values()),
                "duplicate_rows": self.data_info['duplicate_rows']
            },
            "column_info": {
                "numeric_columns": len(self.data_info['numeric_columns']),
                "categorical_columns": len(self.data_info['categorical_columns']),
                "datetime_columns": len(self.data_info['datetime_columns'])
            },
            "data_quality": self._assess_data_quality(),
            "column_details": self.data_info
        }
        
        return summary
    
    def _assess_data_quality(self) -> Dict[str, Any]:
        """Assess the quality of the dataset"""
        if self.data is None:
            return {}
        
        total_cells = len(self.data) * len(self.data.columns)
        missing_cells = sum(self.data_info['missing_values'].values())
        
        quality_score = max(0, 100 - (missing_cells / total_cells * 100) - (self.data_info['duplicate_rows'] / len(self.data) * 10))
        
        quality_assessment = {
            "overall_score": round(quality_score, 1),
            "missing_data_percentage": round((missing_cells / total_cells) * 100, 2),
            "duplicate_percentage": round((self.data_info['duplicate_rows'] / len(self.data)) * 100, 2),
            "recommendations": []
        }
        
        # Generate recommendations
        if quality_assessment["missing_data_percentage"] > 10:
            quality_assessment["recommendations"].append("Consider handling missing values")
        
        if quality_assessment["duplicate_percentage"] > 5:
            quality_assessment["recommendations"].append("Consider removing duplicate rows")
        
        if len(self.data_info['numeric_columns']) == 0:
            quality_assessment["recommendations"].append("No numeric columns detected - check data types")
        
        return quality_assessment
    
    def get_column_analysis(self, column_name: str) -> Dict[str, Any]:
        """
        Get detailed analysis of a specific column
        
        Args:
            column_name (str): Name of the column to analyze
            
        Returns:
            Dict: Detailed column analysis
        """
        if self.data is None or column_name not in self.data.columns:
            return {"error": f"Column '{column_name}' not found"}
        
        col_data = self.data[column_name]
        analysis = {
            "name": column_name,
            "dtype": str(col_data.dtype),
            "non_null_count": col_data.count(),
            "null_count": col_data.isnull().sum(),
            "unique_count": col_data.nunique(),
            "memory_usage": col_data.memory_usage(deep=True)
        }
        
        if col_data.dtype in ['int64', 'float64']:
            analysis.update({
                "statistics": {
                    "mean": col_data.mean(),
                    "median": col_data.median(),
                    "std": col_data.std(),
                    "min": col_data.min(),
                    "max": col_data.max(),
                    "q25": col_data.quantile(0.25),
                    "q75": col_data.quantile(0.75)
                },
                "outliers": self._detect_outliers(col_data)
            })
        else:
            analysis.update({
                "value_counts": col_data.value_counts().head(10).to_dict(),
                "most_frequent": col_data.mode().iloc[0] if len(col_data.mode()) > 0 else None
            })
        
        return analysis
    
    def _detect_outliers(self, series: pd.Series) -> Dict[str, Any]:
        """Detect outliers using IQR method"""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        
        return {
            "count": len(outliers),
            "percentage": round((len(outliers) / len(series)) * 100, 2),
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        }
    
    def export_cleaned_data(self, file_path: str, format: str = 'csv') -> bool:
        """
        Export cleaned data to file
        
        Args:
            file_path (str): Output file path
            format (str): Output format ('csv' or 'excel')
            
        Returns:
            bool: True if successful
        """
        if self.data is None:
            logger.error("No data to export")
            return False
        
        try:
            if format.lower() == 'csv':
                self.data.to_csv(file_path, index=False)
            elif format.lower() == 'excel':
                self.data.to_excel(file_path, index=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Data exported successfully to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return False


# Utility functions
def validate_file_size(file_path: str, max_size_mb: int = 50) -> bool:
    """
    Validate if file size is within acceptable limits
    
    Args:
        file_path (str): Path to the file
        max_size_mb (int): Maximum allowed size in MB
        
    Returns:
        bool: True if file size is acceptable
    """
    try:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        return file_size_mb <= max_size_mb
    except Exception:
        return False


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get basic information about a file
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        Dict: File information
    """
    try:
        stat = os.stat(file_path)
        return {
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": os.path.splitext(file_path)[1].lower()
        }
    except Exception as e:
        return {"error": str(e)}
