"""
Comprehensive Performance Optimizer for BI Assistant
Final performance tuning and optimization utilities
"""

import pandas as pd
import numpy as np
import streamlit as st
import time
import psutil
import gc
import warnings
from typing import Dict, List, Any, Optional, Tuple
from functools import wraps, lru_cache
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and optimize application performance"""
    
    def __init__(self):
        """Initialize performance monitoring"""
        self.metrics = {
            'function_times': {},
            'memory_usage': [],
            'cache_hits': 0,
            'cache_misses': 0,
            'data_processing_times': [],
            'visualization_times': [],
            'ai_response_times': []
        }
        self.start_time = time.time()
    
    def timing_decorator(self, category: str = 'general'):
        """Decorator to measure function execution time"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start
                    
                    # Record timing
                    if func.__name__ not in self.metrics['function_times']:
                        self.metrics['function_times'][func.__name__] = []
                    self.metrics['function_times'][func.__name__].append(duration)
                    
                    # Category-specific tracking
                    if category == 'data_processing':
                        self.metrics['data_processing_times'].append(duration)
                    elif category == 'visualization':
                        self.metrics['visualization_times'].append(duration)
                    elif category == 'ai':
                        self.metrics['ai_response_times'].append(duration)
                    
                    logger.info(f"{func.__name__} completed in {duration:.3f}s")
                    return result
                    
                except Exception as e:
                    duration = time.time() - start
                    logger.error(f"{func.__name__} failed after {duration:.3f}s: {str(e)}")
                    raise
                    
            return wrapper
        return decorator
    
    def memory_checkpoint(self, label: str = ""):
        """Record current memory usage"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        self.metrics['memory_usage'].append({
            'timestamp': datetime.now(),
            'label': label,
            'memory_mb': memory_mb,
            'cpu_percent': process.cpu_percent()
        })
        
        logger.info(f"Memory checkpoint '{label}': {memory_mb:.1f}MB")
        return memory_mb
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        current_time = time.time()
        uptime = current_time - self.start_time
        
        summary = {
            'uptime_seconds': uptime,
            'total_functions_called': sum(len(times) for times in self.metrics['function_times'].values()),
            'average_memory_mb': np.mean([m['memory_mb'] for m in self.metrics['memory_usage']]) if self.metrics['memory_usage'] else 0,
            'peak_memory_mb': max([m['memory_mb'] for m in self.metrics['memory_usage']]) if self.metrics['memory_usage'] else 0,
            'cache_hit_rate': self.metrics['cache_hits'] / (self.metrics['cache_hits'] + self.metrics['cache_misses']) if (self.metrics['cache_hits'] + self.metrics['cache_misses']) > 0 else 0,
        }
        
        # Function timing statistics
        if self.metrics['function_times']:
            summary['function_stats'] = {}
            for func_name, times in self.metrics['function_times'].items():
                summary['function_stats'][func_name] = {
                    'calls': len(times),
                    'total_time': sum(times),
                    'avg_time': np.mean(times),
                    'max_time': max(times),
                    'min_time': min(times)
                }
        
        # Category timing statistics
        for category in ['data_processing', 'visualization', 'ai_response']:
            times = self.metrics[f'{category}_times']
            if times:
                summary[f'{category}_stats'] = {
                    'calls': len(times),
                    'avg_time': np.mean(times),
                    'total_time': sum(times),
                    'percentile_95': np.percentile(times, 95)
                }
        
        return summary


class DataOptimizer:
    """Optimize data processing operations"""
    
    @staticmethod
    def optimize_dataframe(df: pd.DataFrame, memory_optimize: bool = True) -> pd.DataFrame:
        """Optimize DataFrame memory usage and performance"""
        
        if df.empty:
            return df
        
        optimized_df = df.copy()
        
        if memory_optimize:
            # Optimize numeric columns
            for col in optimized_df.select_dtypes(include=['int64']).columns:
                col_min = optimized_df[col].min()
                col_max = optimized_df[col].max()
                
                if col_min >= 0:  # Unsigned integers
                    if col_max < 255:
                        optimized_df[col] = optimized_df[col].astype('uint8')
                    elif col_max < 65535:
                        optimized_df[col] = optimized_df[col].astype('uint16')
                    elif col_max < 4294967295:
                        optimized_df[col] = optimized_df[col].astype('uint32')
                else:  # Signed integers
                    if col_min > -128 and col_max < 127:
                        optimized_df[col] = optimized_df[col].astype('int8')
                    elif col_min > -32768 and col_max < 32767:
                        optimized_df[col] = optimized_df[col].astype('int16')
                    elif col_min > -2147483648 and col_max < 2147483647:
                        optimized_df[col] = optimized_df[col].astype('int32')
            
            # Optimize float columns
            for col in optimized_df.select_dtypes(include=['float64']).columns:
                optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='float')
            
            # Optimize object columns to category where appropriate
            for col in optimized_df.select_dtypes(include=['object']).columns:
                if optimized_df[col].nunique() / len(optimized_df) < 0.5:  # Less than 50% unique values
                    try:
                        optimized_df[col] = optimized_df[col].astype('category')
                    except:
                        pass  # Keep as object if conversion fails
        
        return optimized_df
    
    @staticmethod
    @lru_cache(maxsize=128)
    def cached_data_summary(data_hash: str, shape: Tuple[int, int]) -> Dict[str, Any]:
        """Cached data summary computation"""
        # This would typically compute expensive summary statistics
        # For now, return basic info since we can't cache the actual DataFrame
        return {
            'cached_at': datetime.now().isoformat(),
            'shape': shape,
            'data_hash': data_hash
        }
    
    @staticmethod
    def sample_large_dataset(df: pd.DataFrame, max_rows: int = 10000, 
                           strategy: str = 'random') -> pd.DataFrame:
        """Intelligently sample large datasets for faster processing"""
        
        if len(df) <= max_rows:
            return df
        
        if strategy == 'random':
            return df.sample(n=max_rows, random_state=42)
        elif strategy == 'stratified':
            # Try to maintain proportions if categorical columns exist
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) > 0:
                # Use the first categorical column for stratification
                col = categorical_cols[0]
                return df.groupby(col, group_keys=False).apply(
                    lambda x: x.sample(min(len(x), max_rows // df[col].nunique()), random_state=42)
                )
            else:
                return df.sample(n=max_rows, random_state=42)
        elif strategy == 'time_based':
            # For time series data, take recent data
            date_cols = df.select_dtypes(include=['datetime64']).columns
            if len(date_cols) > 0:
                df_sorted = df.sort_values(date_cols[0], ascending=False)
                return df_sorted.head(max_rows)
            else:
                return df.tail(max_rows)  # Take last rows
        
        return df.sample(n=max_rows, random_state=42)


class CacheManager:
    """Manage application caching for better performance"""
    
    def __init__(self):
        """Initialize cache manager"""
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'cache_size': 0,
            'last_cleanup': datetime.now()
        }
    
    @staticmethod
    def setup_streamlit_cache():
        """Configure Streamlit caching for optimal performance"""
        
        # Clear cache if it gets too large
        if hasattr(st, 'cache_data'):
            try:
                cache_size = len(st.cache_data._cache_data_cache)
                if cache_size > 100:  # Arbitrary limit
                    st.cache_data.clear()
                    logger.info("Cleared Streamlit cache (size limit reached)")
            except:
                pass
    
    @staticmethod
    def memory_cleanup():
        """Perform memory cleanup operations"""
        
        # Suppress warnings during cleanup
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            # Force garbage collection
            collected = gc.collect()
            
            # Clear matplotlib figure cache
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass
            
            # Clear plotly cache if possible
            try:
                import plotly.io as pio
                pio.templates.default = "plotly"  # Reset to default
            except:
                pass
            
            logger.info(f"Memory cleanup completed, collected {collected} objects")
            return collected


class ApplicationOptimizer:
    """Main application optimizer"""
    
    def __init__(self):
        """Initialize application optimizer"""
        self.monitor = PerformanceMonitor()
        self.cache_manager = CacheManager()
        self.data_optimizer = DataOptimizer()
        
        # Setup optimizations
        self._setup_pandas_optimizations()
        self._setup_streamlit_optimizations()
    
    def _setup_pandas_optimizations(self):
        """Configure pandas for optimal performance"""
        
        # Set optimal pandas options
        pd.set_option('mode.chained_assignment', None)  # Disable SettingWithCopyWarning
        pd.set_option('display.max_columns', 20)  # Limit display columns
        pd.set_option('display.max_rows', 100)  # Limit display rows
        
        # Use faster engines where available
        pd.set_option('mode.copy_on_write', True)  # Enable copy-on-write
        
        logger.info("Pandas optimizations configured")
    
    def _setup_streamlit_optimizations(self):
        """Configure Streamlit for optimal performance"""
        
        # Setup caching
        self.cache_manager.setup_streamlit_cache()
        
        # Configure session state optimization
        if 'optimization_initialized' not in st.session_state:
            st.session_state.optimization_initialized = True
            st.session_state.performance_metrics = {}
            logger.info("Streamlit optimizations initialized")
    
    def optimize_for_production(self):
        """Apply production-ready optimizations"""
        
        # Suppress warnings in production
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=FutureWarning)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        
        # Setup logging for production
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        logging.getLogger('plotly').setLevel(logging.WARNING)
        logging.getLogger('streamlit').setLevel(logging.WARNING)
        
        # Memory management
        gc.set_threshold(700, 10, 10)  # More aggressive garbage collection
        
        logger.info("Production optimizations applied")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        
        process = psutil.Process()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'memory_available_gb': psutil.virtual_memory().available / (1024**3),
            'memory_percent': psutil.virtual_memory().percent,
            'process_memory_mb': process.memory_info().rss / (1024**2),
            'process_cpu_percent': process.cpu_percent(),
            'disk_usage_percent': psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else None,
            'python_version': f"{psutil.version_info if hasattr(psutil, 'version_info') else 'Unknown'}",
            'performance_summary': self.monitor.get_performance_summary()
        }
    
    def render_performance_dashboard(self):
        """Render performance monitoring dashboard in Streamlit"""
        
        st.markdown("## ⚡ Performance Monitor")
        
        # System metrics
        col1, col2, col3, col4 = st.columns(4)
        
        system_info = self.get_system_info()
        
        with col1:
            st.metric(
                "CPU Usage", 
                f"{system_info['cpu_percent']:.1f}%",
                delta=None
            )
        
        with col2:
            st.metric(
                "Memory Usage", 
                f"{system_info['memory_percent']:.1f}%",
                delta=None
            )
        
        with col3:
            st.metric(
                "Process Memory", 
                f"{system_info['process_memory_mb']:.1f}MB",
                delta=None
            )
        
        with col4:
            cache_hit_rate = system_info['performance_summary'].get('cache_hit_rate', 0)
            st.metric(
                "Cache Hit Rate", 
                f"{cache_hit_rate:.1%}",
                delta=None
            )
        
        # Performance summary
        perf_summary = system_info['performance_summary']
        
        if perf_summary.get('function_stats'):
            st.markdown("### Function Performance")
            
            func_data = []
            for func_name, stats in perf_summary['function_stats'].items():
                func_data.append({
                    'Function': func_name,
                    'Calls': stats['calls'],
                    'Avg Time (s)': round(stats['avg_time'], 3),
                    'Total Time (s)': round(stats['total_time'], 3),
                    'Max Time (s)': round(stats['max_time'], 3)
                })
            
            if func_data:
                df_funcs = pd.DataFrame(func_data)
                st.dataframe(df_funcs, use_container_width=True)
        
        # Memory cleanup
        st.markdown("### 🧹 Memory Management")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🧹 Clean Memory"):
                collected = self.cache_manager.memory_cleanup()
                st.success(f"Cleaned up {collected} objects")
        
        with col_b:
            if st.button("🗑️ Clear Cache"):
                if hasattr(st, 'cache_data'):
                    st.cache_data.clear()
                st.success("Cache cleared successfully")
        
        # System information
        with st.expander("🔧 System Information", expanded=False):
            st.json(system_info, expanded=False)


# Global optimizer instance
app_optimizer = ApplicationOptimizer()

# Export key components
__all__ = [
    'PerformanceMonitor',
    'DataOptimizer', 
    'CacheManager',
    'ApplicationOptimizer',
    'app_optimizer'
]
