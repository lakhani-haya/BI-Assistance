"""
Enhanced Streamlit File Upload Interface
Advanced file upload components with validation, preview, and batch processing
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import zipfile
from typing import Dict, List, Any, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Import our file processing modules
from src.file_processor import FileProcessor, BatchFileProcessor, FileValidator, DataTypeConverter, FileInfo


class StreamlitFileUploader:
    """Enhanced file upload interface for Streamlit"""
    
    def __init__(self):
        self.file_processor = FileProcessor()
        self.batch_processor = BatchFileProcessor()
        self.uploaded_files = {}
    
    def render_file_upload_section(self) -> Dict[str, Any]:
        """Render comprehensive file upload interface"""
        st.markdown("### 📁 File Upload & Processing")
        
        # Upload mode selection
        upload_mode = st.radio(
            "Upload Mode:",
            ["Single File", "Multiple Files", "ZIP Archive", "Sample Data"],
            horizontal=True,
            help="Choose how you want to upload your data"
        )
        
        if upload_mode == "Single File":
            return self._render_single_file_upload()
        elif upload_mode == "Multiple Files":
            return self._render_multiple_file_upload()
        elif upload_mode == "ZIP Archive":
            return self._render_zip_upload()
        else:  # Sample Data
            return self._render_sample_data_selection()
    
    def _render_single_file_upload(self) -> Dict[str, Any]:
        """Render single file upload interface"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a data file",
                type=['csv', 'xlsx', 'xls', 'txt', 'tsv', 'json', 'jsonl', 'parquet'],
                help="Upload CSV, Excel, JSON, or Parquet files (max 200MB)",
                key="single_file_uploader"
            )
        
        with col2:
            if uploaded_file:
                self._display_file_info(uploaded_file)
        
        if uploaded_file is not None:
            return self._process_single_file(uploaded_file)
        
        return {}
    
    def _render_multiple_file_upload(self) -> Dict[str, Any]:
        """Render multiple file upload interface"""
        uploaded_files = st.file_uploader(
            "Choose multiple data files",
            type=['csv', 'xlsx', 'xls', 'txt', 'tsv', 'json', 'jsonl', 'parquet'],
            accept_multiple_files=True,
            help="Upload multiple files to process and combine",
            key="multiple_file_uploader"
        )
        
        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} files uploaded:**")
            
            # Display file list
            for i, file in enumerate(uploaded_files):
                with st.expander(f"📄 {file.name} ({file.size / 1024:.1f} KB)", expanded=False):
                    self._display_file_info(file)
            
            # Combination options
            st.markdown("#### 🔗 Combination Options")
            combination_method = st.selectbox(
                "How to combine files:",
                ["concat", "union", "intersect"],
                help="concat: stack files vertically, union: include all columns, intersect: only common columns"
            )
            
            if st.button("🚀 Process All Files", type="primary"):
                return self._process_multiple_files(uploaded_files, combination_method)
        
        return {}
    
    def _render_zip_upload(self) -> Dict[str, Any]:
        """Render ZIP file upload interface"""
        uploaded_zip = st.file_uploader(
            "Choose a ZIP archive",
            type=['zip'],
            help="Upload a ZIP file containing multiple data files",
            key="zip_file_uploader"
        )
        
        if uploaded_zip is not None:
            if st.button("📦 Extract and Process ZIP", type="primary"):
                return self._process_zip_file(uploaded_zip)
        
        return {}
    
    def _render_sample_data_selection(self) -> Dict[str, Any]:
        """Render sample data selection interface"""
        st.markdown("#### Sample Datasets")
        
        sample_options = {
            "Sales Performance": "Comprehensive sales data with regions, products, and time series",
            "Financial Metrics": "Company financial data with revenue, expenses, and KPIs",
            "Customer Analytics": "Customer behavior data with demographics and purchases",
            "Operational Data": "Business operations data with efficiency metrics",
            "Marketing Campaigns": "Marketing campaign performance with ROI metrics"
        }
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_sample = st.selectbox(
                "Choose sample dataset:",
                list(sample_options.keys()),
                help="Select a sample dataset to explore the platform features"
            )
            
            st.info(f"📝 **Description:** {sample_options[selected_sample]}")
        
        with col2:
            if st.button("📥 Load Sample Data", type="primary"):
                return self._generate_sample_data(selected_sample)
        
        return {}
    
    def _display_file_info(self, file):
        """Display file information in a compact format"""
        file_size_mb = file.size / (1024 * 1024)
        
        # Color code file size
        if file_size_mb > 50:
            size_color = "🔴"
        elif file_size_mb > 10:
            size_color = "🟡"
        else:
            size_color = "🟢"
        
        st.markdown(f"""
        **File Info:**
        - 📄 **Name:** {file.name}
        - {size_color} **Size:** {file_size_mb:.2f} MB
        - 🔖 **Type:** {file.type or 'Unknown'}
        """)
    
    def _process_single_file(self, uploaded_file) -> Dict[str, Any]:
        """Process single uploaded file"""
        try:
            with st.spinner("🔄 Processing file..."):
                # Get processing options
                processing_options = self._get_processing_options(uploaded_file)
                
                # Process file
                data, file_info = self.file_processor.process_file(
                    uploaded_file,
                    uploaded_file.name,
                    **processing_options
                )
                
                # Display results
                self._display_processing_results(data, file_info)
                
                return {
                    'data': data,
                    'file_info': file_info,
                    'processing_options': processing_options,
                    'success': True
                }
                
        except Exception as e:
            st.error(f"❌ Processing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _process_multiple_files(self, uploaded_files, combination_method: str) -> Dict[str, Any]:
        """Process multiple uploaded files"""
        try:
            with st.spinner("🔄 Processing multiple files..."):
                processed_datasets = []
                processing_results = []
                
                # Process each file
                progress_bar = st.progress(0)
                for i, file in enumerate(uploaded_files):
                    try:
                        # Get processing options for this file
                        processing_options = self._get_processing_options(file, show_ui=False)
                        
                        # Process file
                        data, file_info = self.file_processor.process_file(
                            file,
                            file.name,
                            **processing_options
                        )
                        
                        processed_datasets.append(data)
                        processing_results.append({
                            'filename': file.name,
                            'status': 'success',
                            'rows': len(data),
                            'columns': len(data.columns),
                            'file_info': file_info
                        })
                        
                    except Exception as e:
                        processing_results.append({
                            'filename': file.name,
                            'status': 'failed',
                            'error': str(e)
                        })
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                # Combine datasets if we have successful ones
                successful_datasets = [result for result in processing_results if result['status'] == 'success']
                
                if successful_datasets:
                    combined_data = self.batch_processor.combine_datasets(
                        processed_datasets,
                        method=combination_method
                    )
                    
                    # Display results
                    self._display_batch_processing_results(processing_results, combined_data)
                    
                    return {
                        'data': combined_data,
                        'processing_results': processing_results,
                        'combination_method': combination_method,
                        'success': True
                    }
                else:
                    st.error("❌ No files were processed successfully")
                    return {'success': False, 'processing_results': processing_results}
                
        except Exception as e:
            st.error(f"❌ Batch processing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _process_zip_file(self, uploaded_zip) -> Dict[str, Any]:
        """Process uploaded ZIP file"""
        try:
            with st.spinner("📦 Extracting and processing ZIP file..."):
                results = self.batch_processor.process_zip_file(uploaded_zip, uploaded_zip.name)
                
                if results['processed_files'] > 0:
                    # Get all processed datasets
                    datasets = [result['data'] for result in results['data_files'].values() 
                              if result['status'] == 'success']
                    
                    if datasets:
                        # Combine datasets
                        combined_data = self.batch_processor.combine_datasets(datasets, method='concat')
                        
                        # Display results
                        self._display_zip_processing_results(results, combined_data)
                        
                        return {
                            'data': combined_data,
                            'zip_results': results,
                            'success': True
                        }
                
                st.error("❌ No valid data files found in ZIP archive")
                return {'success': False, 'zip_results': results}
                
        except Exception as e:
            st.error(f"❌ ZIP processing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _generate_sample_data(self, sample_type: str) -> Dict[str, Any]:
        """Generate sample data based on type"""
        try:
            with st.spinner(f"🎲 Generating {sample_type} sample data..."):
                if sample_type == "Sales Performance":
                    data = self._create_sales_sample()
                elif sample_type == "Financial Metrics":
                    data = self._create_financial_sample()
                elif sample_type == "Customer Analytics":
                    data = self._create_customer_sample()
                elif sample_type == "Operational Data":
                    data = self._create_operational_sample()
                elif sample_type == "Marketing Campaigns":
                    data = self._create_marketing_sample()
                else:
                    data = self._create_sales_sample()  # Default fallback
                
                # Create mock file info
                file_info = FileInfo(
                    filename=f"{sample_type.lower().replace(' ', '_')}_sample.csv",
                    size_bytes=len(data) * 100,  # Rough estimate
                    mime_type="text/csv",
                    encoding="utf-8"
                )
                
                st.success(f"✅ Generated {sample_type} dataset with {len(data)} records")
                self._display_processing_results(data, file_info)
                
                return {
                    'data': data,
                    'file_info': file_info,
                    'sample_type': sample_type,
                    'success': True
                }
                
        except Exception as e:
            st.error(f"❌ Sample data generation failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _get_processing_options(self, file, show_ui: bool = True) -> Dict[str, Any]:
        """Get processing options from user interface"""
        options = {}
        
        if not show_ui:
            return options
        
        file_ext = file.name.split('.')[-1].lower()
        
        with st.expander("⚙️ Processing Options", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                if file_ext in ['csv', 'txt', 'tsv']:
                    encoding = st.selectbox(
                        "File Encoding:",
                        ["auto-detect", "utf-8", "latin-1", "cp1252", "iso-8859-1"],
                        help="Character encoding of the file"
                    )
                    if encoding != "auto-detect":
                        options['encoding'] = encoding
                    
                    if file_ext == 'csv':
                        separator = st.selectbox(
                            "CSV Separator:",
                            ["auto-detect", ",", ";", "\\t", "|"],
                            help="Character that separates columns"
                        )
                        if separator != "auto-detect":
                            if separator == "\\t":
                                separator = "\t"
                            options['separator'] = separator
            
            with col2:
                if file_ext in ['xlsx', 'xls']:
                    # For Excel files, we could add sheet selection here
                    # This would require reading the file first to get sheet names
                    st.info("💡 Excel files: First sheet will be used by default")
                
                # Data type optimization
                optimize_types = st.checkbox(
                    "Optimize Data Types",
                    value=True,
                    help="Automatically detect and convert to optimal data types"
                )
                options['optimize_types'] = optimize_types
        
        return options
    
    def _display_processing_results(self, data: pd.DataFrame, file_info: FileInfo):
        """Display processing results and data preview"""
        st.markdown("#### ✅ Processing Complete")
        
        # Success metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Rows", f"{len(data):,}")
        with col2:
            st.metric("📈 Columns", len(data.columns))
        with col3:
            memory_mb = data.memory_usage(deep=True).sum() / (1024 * 1024)
            st.metric("💾 Memory", f"{memory_mb:.1f} MB")
        with col4:
            missing_pct = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
            st.metric("❓ Missing", f"{missing_pct:.1f}%")
        
        # Data preview tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Preview", "📊 Summary", "🔍 Quality", "⚙️ Processing Info"])
        
        with tab1:
            st.markdown("**Data Preview (first 10 rows):**")
            st.dataframe(data.head(10), use_container_width=True)
        
        with tab2:
            self._display_data_summary(data)
        
        with tab3:
            self._display_data_quality(data)
        
        with tab4:
            self._display_file_processing_info(file_info)
    
    def _display_batch_processing_results(self, processing_results: List[Dict], combined_data: pd.DataFrame):
        """Display batch processing results"""
        st.markdown("#### 📦 Batch Processing Results")
        
        # Summary metrics
        successful = len([r for r in processing_results if r['status'] == 'success'])
        failed = len([r for r in processing_results if r['status'] == 'failed'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Successful", successful)
        with col2:
            st.metric("❌ Failed", failed)
        with col3:
            st.metric("📊 Combined Rows", f"{len(combined_data):,}")
        
        # Detailed results
        with st.expander("📄 File Processing Details"):
            for result in processing_results:
                if result['status'] == 'success':
                    st.success(f"✅ {result['filename']} - {result['rows']:,} rows, {result['columns']} columns")
                else:
                    st.error(f"❌ {result['filename']} - {result['error']}")
        
        # Combined data preview
        st.markdown("**Combined Dataset Preview:**")
        st.dataframe(combined_data.head(10), use_container_width=True)
    
    def _display_zip_processing_results(self, results: Dict, combined_data: pd.DataFrame):
        """Display ZIP processing results"""
        st.markdown("#### 📦 ZIP Archive Processing Results")
        
        # Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📁 Total Files", results['total_files'])
        with col2:
            st.metric("✅ Processed", results['processed_files'])
        with col3:
            st.metric("❌ Failed", results['failed_files'])
        with col4:
            st.metric("📊 Final Rows", f"{len(combined_data):,}")
        
        # File details
        if results['data_files']:
            with st.expander("📄 Extracted Files"):
                for file_path, file_result in results['data_files'].items():
                    if file_result['status'] == 'success':
                        data = file_result['data']
                        st.success(f"✅ {file_path} - {len(data):,} rows, {len(data.columns)} columns")
        
        # Error details
        if results['errors']:
            with st.expander("❌ Processing Errors"):
                for error in results['errors']:
                    st.error(error)
    
    def _display_data_summary(self, data: pd.DataFrame):
        """Display data summary statistics"""
        # Numeric columns summary
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.markdown("**Numeric Columns:**")
            st.dataframe(data[numeric_cols].describe(), use_container_width=True)
        
        # Categorical columns summary
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            st.markdown("**Categorical Columns:**")
            cat_summary = []
            for col in categorical_cols[:10]:  # Limit to first 10
                cat_summary.append({
                    'Column': col,
                    'Unique Values': data[col].nunique(),
                    'Most Common': str(data[col].mode().iloc[0] if len(data[col].mode()) > 0 else 'N/A'),
                    'Missing Count': data[col].isna().sum()
                })
            st.dataframe(pd.DataFrame(cat_summary), use_container_width=True)
    
    def _display_data_quality(self, data: pd.DataFrame):
        """Display data quality assessment"""
        # Missing data analysis
        missing_data = data.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if not missing_data.empty:
            st.markdown("**Missing Data by Column:**")
            
            # Create bar chart for missing data
            fig = px.bar(
                x=missing_data.values,
                y=missing_data.index,
                orientation='h',
                title="Missing Values by Column",
                labels={'x': 'Missing Count', 'y': 'Column'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("🎉 No missing data found!")
        
        # Data type distribution
        type_counts = data.dtypes.value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Types:**")
            for dtype, count in type_counts.items():
                st.write(f"- **{dtype}**: {count} columns")
        
        with col2:
            # Duplicate rows
            duplicate_count = data.duplicated().sum()
            st.metric("🔄 Duplicate Rows", duplicate_count)
            
            # Numeric ranges
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                outlier_count = 0
                for col in numeric_cols:
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
                    outlier_count += len(outliers)
                
                st.metric("📊 Potential Outliers", outlier_count)
    
    def _display_file_processing_info(self, file_info: FileInfo):
        """Display file processing information"""
        st.markdown("**File Information:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"- **Filename:** {file_info.filename}")
            st.write(f"- **Size:** {file_info.size_bytes / 1024:.1f} KB")
            st.write(f"- **MIME Type:** {file_info.mime_type}")
            if file_info.encoding:
                st.write(f"- **Encoding:** {file_info.encoding}")
        
        with col2:
            if file_info.detected_separator:
                st.write(f"- **Separator:** '{file_info.detected_separator}'")
            if file_info.sheet_names:
                st.write(f"- **Excel Sheets:** {', '.join(file_info.sheet_names)}")
            st.write(f"- **Processed:** {file_info.upload_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if file_info.validation_errors:
            st.markdown("**Validation Issues:**")
            for error in file_info.validation_errors:
                st.warning(f"⚠️ {error}")
    
    # Sample data generators
    def _create_sales_sample(self) -> pd.DataFrame:
        """Create sample sales data"""
        np.random.seed(42)
        n_records = 1000
        
        dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
        regions = ['North', 'South', 'East', 'West', 'Central']
        products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
        sales_reps = [f'Rep_{i:03d}' for i in range(1, 21)]
        
        data = []
        for _ in range(n_records):
            date = np.random.choice(dates)
            seasonal_factor = 1.2 if date.month in [11, 12] else 0.9 if date.month in [6, 7, 8] else 1.0
            
            record = {
                'date': date,
                'region': np.random.choice(regions),
                'product': np.random.choice(products),
                'sales_rep': np.random.choice(sales_reps),
                'quantity_sold': np.random.randint(1, 50),
                'unit_price': np.random.uniform(10, 500),
                'discount_percent': np.random.uniform(0, 25),
                'customer_satisfaction': np.random.uniform(3.0, 5.0),
                'seasonal_factor': seasonal_factor
            }
            
            record['gross_revenue'] = record['quantity_sold'] * record['unit_price']
            record['discount_amount'] = record['gross_revenue'] * (record['discount_percent'] / 100)
            record['net_revenue'] = record['gross_revenue'] - record['discount_amount']
            record['profit_margin'] = np.random.uniform(0.15, 0.45)
            record['profit'] = record['net_revenue'] * record['profit_margin']
            
            data.append(record)
        
        return pd.DataFrame(data)
    
    def _create_financial_sample(self) -> pd.DataFrame:
        """Create sample financial data"""
        np.random.seed(42)
        
        months = pd.date_range('2020-01-01', '2024-12-31', freq='MS')
        departments = ['Sales', 'Marketing', 'Operations', 'R&D', 'HR', 'Finance']
        
        data = []
        for month in months:
            for dept in departments:
                record = {
                    'month': month,
                    'department': dept,
                    'budget': np.random.uniform(50000, 500000),
                    'actual_spending': np.random.uniform(45000, 520000),
                    'revenue_generated': np.random.uniform(60000, 600000),
                    'headcount': np.random.randint(5, 50),
                    'projects_completed': np.random.randint(0, 10),
                    'efficiency_score': np.random.uniform(0.6, 1.0)
                }
                
                record['budget_variance'] = record['actual_spending'] - record['budget']
                record['budget_variance_percent'] = (record['budget_variance'] / record['budget']) * 100
                record['roi'] = (record['revenue_generated'] - record['actual_spending']) / record['actual_spending']
                record['cost_per_employee'] = record['actual_spending'] / record['headcount']
                
                data.append(record)
        
        return pd.DataFrame(data)
    
    def _create_customer_sample(self) -> pd.DataFrame:
        """Create sample customer analytics data"""
        np.random.seed(42)
        n_customers = 5000
        
        data = []
        for customer_id in range(1, n_customers + 1):
            age = np.random.randint(18, 80)
            income = np.random.normal(50000, 20000)
            
            record = {
                'customer_id': f'CUST_{customer_id:05d}',
                'age': age,
                'gender': np.random.choice(['Male', 'Female', 'Other'], p=[0.48, 0.48, 0.04]),
                'income': max(20000, income),
                'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], p=[0.3, 0.4, 0.25, 0.05]),
                'location': np.random.choice(['Urban', 'Suburban', 'Rural'], p=[0.5, 0.35, 0.15]),
                'acquisition_channel': np.random.choice(['Online', 'Referral', 'Advertisement', 'Store'], p=[0.4, 0.3, 0.2, 0.1]),
                'registration_date': pd.Timestamp('2020-01-01') + pd.Timedelta(days=np.random.randint(0, 1460)),
                'total_purchases': np.random.randint(1, 50),
                'total_spent': np.random.uniform(100, 10000),
                'last_purchase_date': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 365)),
                'customer_satisfaction': np.random.uniform(2.0, 5.0),
                'support_tickets': np.random.randint(0, 10)
            }
            
            record['average_order_value'] = record['total_spent'] / record['total_purchases']
            record['customer_lifetime_months'] = (pd.Timestamp('2024-12-31') - record['registration_date']).days / 30
            record['purchase_frequency'] = record['total_purchases'] / record['customer_lifetime_months']
            record['churn_risk'] = 1 if (pd.Timestamp('2024-12-31') - record['last_purchase_date']).days > 180 else 0
            
            data.append(record)
        
        return pd.DataFrame(data)
    
    def _create_operational_sample(self) -> pd.DataFrame:
        """Create sample operational data"""
        np.random.seed(42)
        
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        facilities = ['Facility_A', 'Facility_B', 'Facility_C', 'Facility_D']
        shifts = ['Morning', 'Afternoon', 'Night']
        
        data = []
        for date in dates:
            for facility in facilities:
                for shift in shifts:
                    record = {
                        'date': date,
                        'facility': facility,
                        'shift': shift,
                        'production_target': np.random.randint(800, 1200),
                        'actual_production': np.random.randint(750, 1250),
                        'downtime_minutes': np.random.randint(0, 120),
                        'quality_defects': np.random.randint(0, 50),
                        'energy_consumption_kwh': np.random.uniform(1000, 2000),
                        'staff_count': np.random.randint(8, 15),
                        'overtime_hours': np.random.uniform(0, 16),
                        'maintenance_cost': np.random.uniform(500, 5000)
                    }
                    
                    record['production_efficiency'] = record['actual_production'] / record['production_target']
                    record['quality_rate'] = 1 - (record['quality_defects'] / record['actual_production'])
                    record['energy_per_unit'] = record['energy_consumption_kwh'] / record['actual_production']
                    record['labor_productivity'] = record['actual_production'] / record['staff_count']
                    
                    data.append(record)
        
        return pd.DataFrame(data)
    
    def _create_marketing_sample(self) -> pd.DataFrame:
        """Create sample marketing campaign data"""
        np.random.seed(42)
        
        campaigns = [f'Campaign_{i:03d}' for i in range(1, 51)]
        channels = ['Email', 'Social Media', 'PPC', 'Display', 'Content Marketing', 'Influencer']
        audience_segments = ['Young Adults', 'Professionals', 'Families', 'Seniors', 'Students']
        
        data = []
        for campaign in campaigns:
            start_date = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 300))
            duration = np.random.randint(7, 90)
            
            record = {
                'campaign_id': campaign,
                'campaign_name': f'{np.random.choice(channels)} Campaign {campaign.split("_")[1]}',
                'channel': np.random.choice(channels),
                'audience_segment': np.random.choice(audience_segments),
                'start_date': start_date,
                'end_date': start_date + pd.Timedelta(days=duration),
                'budget': np.random.uniform(1000, 50000),
                'impressions': np.random.randint(10000, 1000000),
                'clicks': np.random.randint(100, 50000),
                'conversions': np.random.randint(10, 5000),
                'revenue': np.random.uniform(500, 75000),
                'cost_per_click': np.random.uniform(0.50, 5.00),
                'target_cpa': np.random.uniform(10, 100)
            }
            
            record['click_through_rate'] = record['clicks'] / record['impressions']
            record['conversion_rate'] = record['conversions'] / record['clicks']
            record['cost_per_acquisition'] = record['budget'] / record['conversions']
            record['return_on_ad_spend'] = record['revenue'] / record['budget']
            record['campaign_duration_days'] = duration
            
            data.append(record)
        
        return pd.DataFrame(data)


# Export main class
__all__ = ['StreamlitFileUploader']
