"""
Integration utilities for combining data processing with AI analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from src.data_processor import DataProcessor
from src.ai_analyzer import AIAnalyzer
from src.prompts import PromptTemplates, InsightCategories

logger = logging.getLogger(__name__)


class IntelligentDataAnalyzer:
    """Combines data processing with AI analysis"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the analyzer with optional OpenAI API key"""
        self.data_processor = DataProcessor()
        self.ai_analyzer = AIAnalyzer(api_key=openai_api_key) if openai_api_key else None
        self.analysis_results = {}
        
        logger.info("Intelligent Data Analyzer initialized")
    
    def analyze_file(self, file_path: str, 
                    clean_data: bool = True,
                    generate_insights: bool = True) -> Dict[str, Any]:
        """
        Complete analysis pipeline for a data file
        
        Args:
            file_path (str): Path to the data file
            clean_data (bool): Whether to clean the data
            generate_insights (bool): Whether to generate AI insights
            
        Returns:
            Dict: Complete analysis results
        """
        try:
            logger.info(f"Starting analysis for file: {file_path}")
            
            # Step 1: Load data
            if not self.data_processor.load_file(file_path):
                return {"error": "Failed to load data file"}
            
            # Step 2: Clean data if requested
            cleaning_summary = {}
            if clean_data:
                cleaning_summary = self.data_processor.clean_data()
                logger.info("Data cleaning completed")
            
            # Step 3: Generate data summary
            data_summary = self.data_processor.get_data_summary()
            
            # Step 4: Prepare results
            results = {
                "file_info": {
                    "file_path": file_path,
                    "processed_at": pd.Timestamp.now().isoformat(),
                    "cleaning_performed": clean_data
                },
                "data_summary": data_summary,
                "cleaning_summary": cleaning_summary,
                "sample_data": self.data_processor.data.head(10).to_dict('records'),
                "insights": {}
            }
            
            # Step 5: Generate AI insights if available and requested
            if generate_insights and self.ai_analyzer:
                insights = self._generate_comprehensive_insights()
                results["insights"] = insights
                logger.info("AI insights generated")
            
            # Store results for future reference
            self.analysis_results = results
            
            logger.info("Analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in file analysis: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def analyze_dataframe(self, df: pd.DataFrame, 
                         data_name: str = "dataset",
                         clean_data: bool = True,
                         generate_insights: bool = True) -> Dict[str, Any]:
        """
        Complete analysis pipeline for a DataFrame
        
        Args:
            df (pd.DataFrame): Input DataFrame
            data_name (str): Name for the dataset
            clean_data (bool): Whether to clean the data
            generate_insights (bool): Whether to generate AI insights
            
        Returns:
            Dict: Complete analysis results
        """
        try:
            logger.info(f"Starting analysis for DataFrame: {data_name}")
            
            # Step 1: Load DataFrame
            if not self.data_processor.load_dataframe(df):
                return {"error": "Failed to load DataFrame"}
            
            # Step 2: Clean data if requested
            cleaning_summary = {}
            if clean_data:
                cleaning_summary = self.data_processor.clean_data()
            
            # Step 3: Generate data summary
            data_summary = self.data_processor.get_data_summary()
            
            # Step 4: Prepare results
            results = {
                "file_info": {
                    "data_name": data_name,
                    "processed_at": pd.Timestamp.now().isoformat(),
                    "cleaning_performed": clean_data
                },
                "data_summary": data_summary,
                "cleaning_summary": cleaning_summary,
                "sample_data": self.data_processor.data.head(10).to_dict('records'),
                "insights": {}
            }
            
            # Step 5: Generate AI insights
            if generate_insights and self.ai_analyzer:
                insights = self._generate_comprehensive_insights()
                results["insights"] = insights
            
            self.analysis_results = results
            return results
            
        except Exception as e:
            logger.error(f"Error in DataFrame analysis: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _generate_comprehensive_insights(self) -> Dict[str, Any]:
        """Generate comprehensive AI insights about the current dataset"""
        if not self.ai_analyzer or self.data_processor.data is None:
            return {}
        
        insights = {}
        
        try:
            # 1. Dataset overview insights
            data_summary = self.data_processor.get_data_summary()
            sample_data = self.data_processor.data.head(10)
            
            overview_insights = self.ai_analyzer.analyze_dataset_overview(data_summary, sample_data)
            insights["overview"] = overview_insights
            
            # 2. Column-specific insights for key columns
            numeric_columns = data_summary['column_details']['numeric_columns'][:3]  # Top 3 numeric columns
            categorical_columns = data_summary['column_details']['categorical_columns'][:2]  # Top 2 categorical
            
            column_insights = {}
            
            # Analyze numeric columns
            for col in numeric_columns:
                if col in self.data_processor.data.columns:
                    col_analysis = self.data_processor.get_column_analysis(col)
                    col_insights = self.ai_analyzer.analyze_column_insights(
                        col, self.data_processor.data[col], col_analysis
                    )
                    column_insights[col] = col_insights
            
            # Analyze key categorical columns
            for col in categorical_columns:
                if col in self.data_processor.data.columns:
                    col_analysis = self.data_processor.get_column_analysis(col)
                    col_insights = self.ai_analyzer.analyze_column_insights(
                        col, self.data_processor.data[col], col_analysis
                    )
                    column_insights[col] = col_insights
            
            insights["columns"] = column_insights
            
            # 3. Trend analysis if date column is available
            date_columns = data_summary['column_details']['datetime_columns']
            if date_columns:
                date_col = date_columns[0]  # Use first date column
                trend_insights = self.ai_analyzer.analyze_trends_and_patterns(
                    self.data_processor.data, date_col
                )
                insights["trends"] = trend_insights
            
            # 4. Generate business narrative
            narrative = self.ai_analyzer.generate_story_narrative(
                self.data_processor.data, insights
            )
            insights["narrative"] = narrative
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            insights["error"] = f"Some insights could not be generated: {str(e)}"
        
        return insights
    
    def get_data_category_suggestions(self) -> List[str]:
        """
        Suggest data categories based on column names and content
        
        Returns:
            List[str]: Suggested categories for the dataset
        """
        if self.data_processor.data is None:
            return []
        
        columns = [col.lower() for col in self.data_processor.data.columns]
        suggestions = []
        
        # Sales-related patterns
        sales_patterns = ['sales', 'revenue', 'price', 'amount', 'order', 'customer', 'product']
        if any(pattern in ' '.join(columns) for pattern in sales_patterns):
            suggestions.append('sales')
        
        # Financial patterns
        financial_patterns = ['cost', 'profit', 'budget', 'expense', 'income', 'balance']
        if any(pattern in ' '.join(columns) for pattern in financial_patterns):
            suggestions.append('financial')
        
        # Operational patterns
        operational_patterns = ['time', 'duration', 'process', 'efficiency', 'capacity', 'performance']
        if any(pattern in ' '.join(columns) for pattern in operational_patterns):
            suggestions.append('operational')
        
        # Marketing patterns
        marketing_patterns = ['campaign', 'channel', 'conversion', 'click', 'impression', 'engagement']
        if any(pattern in ' '.join(columns) for pattern in marketing_patterns):
            suggestions.append('marketing')
        
        # HR patterns
        hr_patterns = ['employee', 'salary', 'department', 'performance', 'hire', 'tenure']
        if any(pattern in ' '.join(columns) for pattern in hr_patterns):
            suggestions.append('hr')
        
        return suggestions if suggestions else ['general']
    
    def generate_targeted_insights(self, category: str, 
                                 audience: str = 'general',
                                 urgency: str = 'MEDIUM') -> Dict[str, Any]:
        """
        Generate insights targeted for specific business category and audience
        
        Args:
            category (str): Business category (sales, financial, operational, etc.)
            audience (str): Target audience (executives, managers, analysts, general)
            urgency (str): Analysis urgency (HIGH, MEDIUM, LOW)
            
        Returns:
            Dict: Targeted insights
        """
        if not self.ai_analyzer or self.data_processor.data is None:
            return {"error": "No data loaded or AI analyzer not available"}
        
        try:
            # Get appropriate prompt template for category
            data_summary = self.data_processor.get_data_summary()
            sample_data = self.data_processor.data.head(10)
            
            # Prepare context based on category
            context = self._prepare_targeted_context(data_summary, sample_data, category)
            
            # Get category-specific prompt
            prompt_func = InsightCategories.get_category_prompt(category)
            prompt = prompt_func(context)
            
            # Enhance prompt for audience and urgency
            from src.prompts import PromptEnhancer
            prompt = PromptEnhancer.add_audience_context(prompt, audience)
            prompt = PromptEnhancer.add_urgency_context(prompt, urgency)
            
            # Generate insights
            response = self.ai_analyzer._call_openai_api(prompt)
            
            # Parse and structure response
            insights = {
                "category": category,
                "audience": audience,
                "urgency": urgency,
                "analysis": response,
                "generated_at": pd.Timestamp.now().isoformat()
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating targeted insights: {str(e)}")
            return {"error": f"Failed to generate targeted insights: {str(e)}"}
    
    def _prepare_targeted_context(self, data_summary: Dict[str, Any], 
                                sample_data: pd.DataFrame, 
                                category: str) -> str:
        """Prepare context string optimized for specific business category"""
        
        basic_info = data_summary.get('basic_info', {})
        
        # Base context
        context = f"""
        Dataset: {basic_info.get('rows', 'N/A'):,} records, {basic_info.get('columns', 'N/A')} fields
        Data Quality Score: {data_summary.get('data_quality', {}).get('overall_score', 'N/A')}/100
        """
        
        # Add category-specific details
        if category == 'sales':
            # Focus on sales-relevant columns
            sales_cols = [col for col in sample_data.columns 
                         if any(term in col.lower() for term in ['sales', 'revenue', 'price', 'amount', 'order'])]
            if sales_cols:
                context += f"\nSales Metrics Available: {sales_cols}"
        
        elif category == 'financial':
            # Focus on financial columns
            financial_cols = [col for col in sample_data.columns 
                            if any(term in col.lower() for term in ['cost', 'profit', 'budget', 'expense'])]
            if financial_cols:
                context += f"\nFinancial Metrics Available: {financial_cols}"
        
        # Add sample data
        context += f"\n\nSample Data Preview:\n{sample_data.head(3).to_string()}"
        
        return context
    
    def export_analysis_report(self, file_path: str, format: str = 'json') -> bool:
        """
        Export complete analysis results to file
        
        Args:
            file_path (str): Output file path
            format (str): Export format ('json', 'csv', 'excel')
            
        Returns:
            bool: True if successful
        """
        if not self.analysis_results:
            logger.error("No analysis results to export")
            return False
        
        try:
            if format.lower() == 'json':
                import json
                with open(file_path, 'w') as f:
                    json.dump(self.analysis_results, f, indent=2, default=str)
            
            elif format.lower() == 'csv':
                # Export data summary as CSV
                if 'sample_data' in self.analysis_results:
                    df = pd.DataFrame(self.analysis_results['sample_data'])
                    df.to_csv(file_path, index=False)
            
            elif format.lower() == 'excel':
                # Export multiple sheets to Excel
                with pd.ExcelWriter(file_path) as writer:
                    if 'sample_data' in self.analysis_results:
                        df = pd.DataFrame(self.analysis_results['sample_data'])
                        df.to_excel(writer, sheet_name='Sample_Data', index=False)
                    
                    # Export insights as text
                    if 'insights' in self.analysis_results:
                        insights_df = pd.DataFrame([self.analysis_results['insights']])
                        insights_df.to_excel(writer, sheet_name='Insights', index=False)
            
            logger.info(f"Analysis report exported to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting report: {str(e)}")
            return False
    
    def get_quick_summary(self) -> Dict[str, Any]:
        """
        Get a quick summary of the analysis results
        
        Returns:
            Dict: Quick summary with key metrics and insights
        """
        if not self.analysis_results:
            return {"error": "No analysis results available"}
        
        summary = {}
        
        # Basic metrics
        if 'data_summary' in self.analysis_results:
            basic_info = self.analysis_results['data_summary'].get('basic_info', {})
            summary['dataset_size'] = f"{basic_info.get('rows', 'N/A'):,} rows × {basic_info.get('columns', 'N/A')} columns"
            
            quality = self.analysis_results['data_summary'].get('data_quality', {})
            summary['data_quality'] = f"{quality.get('overall_score', 'N/A')}/100"
        
        # Key insights
        if 'insights' in self.analysis_results:
            insights = self.analysis_results['insights']
            
            if 'overview' in insights:
                overview = insights['overview']
                summary['executive_summary'] = overview.get('executive_summary', 'N/A')[:200] + "..."
                
                if 'key_findings' in overview and isinstance(overview['key_findings'], list):
                    summary['top_findings'] = overview['key_findings'][:3]
        
        # Processing info
        if 'file_info' in self.analysis_results:
            file_info = self.analysis_results['file_info']
            summary['processed_at'] = file_info.get('processed_at', 'N/A')
            summary['cleaning_performed'] = file_info.get('cleaning_performed', False)
        
        return summary
