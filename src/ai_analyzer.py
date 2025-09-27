"""
AI analysis using OpenAI API
"""

import openai
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import json
import logging
from datetime import datetime
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAnalyzer:
    """
    AI-powered data analyzer that generates natural language insights
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Analyzer
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, uses config.
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
        logger.info(f"AI Analyzer initialized with model: {self.model}")
    
    def analyze_dataset_overview(self, data_summary: Dict[str, Any], sample_data: pd.DataFrame) -> Dict[str, str]:
        """
        Generate high-level insights about the dataset
        
        Args:
            data_summary (Dict): Summary statistics from DataProcessor
            sample_data (pd.DataFrame): Sample of the actual data
            
        Returns:
            Dict: AI-generated insights and analysis
        """
        try:
            # Prepare context for AI
            context = self._prepare_dataset_context(data_summary, sample_data)
            
            prompt = f"""
            You are a senior data analyst. Analyze this dataset and provide business insights.
            
            Dataset Information:
            {context}
            
            Please provide:
            1. **Executive Summary** (2-3 sentences about what this data represents)
            2. **Key Findings** (3-5 bullet points of interesting patterns or insights)
            3. **Data Quality Assessment** (brief comment on data completeness and reliability)
            4. **Business Recommendations** (2-3 actionable suggestions based on the data)
            
            Keep the language business-friendly and avoid technical jargon.
            Focus on actionable insights that would matter to stakeholders.
            """
            
            response = self._call_openai_api(prompt)
            
            # Parse the response into structured format
            insights = self._parse_overview_response(response)
            
            logger.info("Dataset overview analysis completed")
            return insights
            
        except Exception as e:
            logger.error(f"Error in dataset overview analysis: {str(e)}")
            return {
                "executive_summary": "Analysis unavailable due to technical error.",
                "key_findings": ["Unable to generate insights at this time."],
                "data_quality": "Assessment unavailable.",
                "recommendations": ["Please try again later."]
            }
    
    def analyze_column_insights(self, column_name: str, column_data: pd.Series, 
                              column_stats: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate insights about a specific column
        
        Args:
            column_name (str): Name of the column
            column_data (pd.Series): The actual column data
            column_stats (Dict): Statistical information about the column
            
        Returns:
            Dict: AI-generated column insights
        """
        try:
            # Prepare column context
            context = self._prepare_column_context(column_name, column_data, column_stats)
            
            prompt = f"""
            You are analyzing a specific data column. Provide insights about this column.
            
            Column Analysis:
            {context}
            
            Please provide:
            1. **Pattern Analysis** (what patterns do you see in this data?)
            2. **Business Significance** (why might this column be important?)
            3. **Anomalies or Concerns** (any unusual values or data quality issues?)
            4. **Recommendations** (suggestions for further analysis or action)
            
            Be specific and actionable in your analysis.
            """
            
            response = self._call_openai_api(prompt)
            insights = self._parse_column_response(response)
            
            logger.info(f"Column insights generated for: {column_name}")
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing column {column_name}: {str(e)}")
            return {
                "pattern_analysis": "Analysis unavailable.",
                "business_significance": "Unable to determine significance.",
                "anomalies": "No anomaly detection performed.",
                "recommendations": "Please try again later."
            }
    
    def analyze_trends_and_patterns(self, data: pd.DataFrame, 
                                   date_column: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze temporal trends and patterns in the data
        
        Args:
            data (pd.DataFrame): The dataset to analyze
            date_column (str, optional): Name of the date column for time series analysis
            
        Returns:
            Dict: Trend analysis and insights
        """
        try:
            # Identify trends and patterns
            trends = self._identify_trends(data, date_column)
            
            # Prepare context for AI analysis
            context = self._prepare_trends_context(trends, data)
            
            prompt = f"""
            You are analyzing trends and patterns in business data. 
            
            Trend Analysis:
            {context}
            
            Please provide:
            1. **Trend Summary** (describe the main trends you observe)
            2. **Seasonal Patterns** (any recurring patterns or seasonality?)
            3. **Growth/Decline Analysis** (areas of growth or concern)
            4. **Forecast Insights** (what might these trends suggest for the future?)
            5. **Strategic Recommendations** (how should the business respond?)
            
            Focus on business implications and actionable insights.
            """
            
            response = self._call_openai_api(prompt)
            insights = self._parse_trends_response(response)
            
            # Add quantitative metrics
            insights["metrics"] = trends
            
            logger.info("Trend analysis completed")
            return insights
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {str(e)}")
            return {
                "trend_summary": "Trend analysis unavailable.",
                "seasonal_patterns": "Unable to identify patterns.",
                "growth_analysis": "Analysis not performed.",
                "forecast_insights": "Forecasting unavailable.",
                "recommendations": "Please try again later.",
                "metrics": {}
            }
    
    def generate_story_narrative(self, data: pd.DataFrame, 
                                key_insights: Dict[str, Any]) -> str:
        """
        Generate a narrative story that explains the data in business terms
        
        Args:
            data (pd.DataFrame): The dataset
            key_insights (Dict): Previously generated insights
            
        Returns:
            str: A narrative explanation of the data
        """
        try:
            # Create context from insights and data
            context = self._prepare_narrative_context(data, key_insights)
            
            prompt = f"""
            You are a business analyst presenting findings to executives. 
            Create a compelling narrative that tells the story of this data.
            
            Data Context:
            {context}
            
            Write a clear, engaging narrative (300-500 words) that:
            1. Sets the business context
            2. Highlights the most important insights
            3. Explains what the data reveals about business performance
            4. Suggests strategic implications
            5. Ends with actionable next steps
            
            Use specific numbers and examples from the data.
            Write in a professional but accessible tone.
            Structure it like an executive briefing.
            """
            
            narrative = self._call_openai_api(prompt)
            
            logger.info("Business narrative generated")
            return narrative
            
        except Exception as e:
            logger.error(f"Error generating narrative: {str(e)}")
            return "Unable to generate business narrative at this time. Please try again later."
    
    def explain_chart_insights(self, chart_type: str, chart_data: Dict[str, Any], 
                              context: Dict[str, Any]) -> str:
        """
        Generate explanations for specific charts and visualizations
        
        Args:
            chart_type (str): Type of chart (bar, line, pie, etc.)
            chart_data (Dict): Data used in the chart
            context (Dict): Additional context about the data
            
        Returns:
            str: Natural language explanation of the chart
        """
        try:
            prompt = f"""
            You are explaining a data visualization to business stakeholders.
            
            Chart Type: {chart_type}
            Chart Data Summary: {json.dumps(chart_data, indent=2, default=str)}
            Context: {json.dumps(context, indent=2, default=str)}
            
            Provide a clear, 2-3 sentence explanation that:
            1. Describes what the chart shows
            2. Highlights the key insight or pattern
            3. Explains why this matters for the business
            
            Keep it concise and business-focused.
            """
            
            explanation = self._call_openai_api(prompt)
            
            logger.info(f"Chart explanation generated for {chart_type}")
            return explanation
            
        except Exception as e:
            logger.error(f"Error explaining chart: {str(e)}")
            return f"This {chart_type} chart displays the data patterns. Additional analysis is needed to provide detailed insights."
    
    def _call_openai_api(self, prompt: str) -> str:
        """Make API call to OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert business data analyst with years of experience in interpreting data and providing actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise
    
    def _prepare_dataset_context(self, data_summary: Dict[str, Any], 
                               sample_data: pd.DataFrame) -> str:
        """Prepare context string for dataset analysis"""
        basic_info = data_summary.get('basic_info', {})
        column_info = data_summary.get('column_info', {})
        data_quality = data_summary.get('data_quality', {})
        
        # Get sample of actual data
        sample_str = sample_data.head(3).to_string() if not sample_data.empty else "No sample data available"
        
        context = f"""
        Dataset Overview:
        - Rows: {basic_info.get('rows', 'N/A'):,}
        - Columns: {basic_info.get('columns', 'N/A')}
        - Memory Usage: {basic_info.get('memory_usage_mb', 'N/A')} MB
        - Missing Values: {basic_info.get('missing_values_total', 'N/A'):,}
        - Duplicate Rows: {basic_info.get('duplicate_rows', 'N/A'):,}
        
        Column Types:
        - Numeric: {column_info.get('numeric_columns', 'N/A')}
        - Categorical: {column_info.get('categorical_columns', 'N/A')}
        - DateTime: {column_info.get('datetime_columns', 'N/A')}
        
        Data Quality Score: {data_quality.get('overall_score', 'N/A')}/100
        
        Sample Data:
        {sample_str}
        """
        
        return context
    
    def _prepare_column_context(self, column_name: str, column_data: pd.Series, 
                              column_stats: Dict[str, Any]) -> str:
        """Prepare context for column analysis"""
        context = f"""
        Column: {column_name}
        Data Type: {column_stats.get('dtype', 'Unknown')}
        Non-null Count: {column_stats.get('non_null_count', 'N/A'):,}
        Unique Values: {column_stats.get('unique_count', 'N/A'):,}
        """
        
        if 'statistics' in column_stats:
            stats = column_stats['statistics']
            context += f"""
        Statistical Summary:
        - Mean: {stats.get('mean', 'N/A'):.2f}
        - Median: {stats.get('median', 'N/A'):.2f}
        - Std Dev: {stats.get('std', 'N/A'):.2f}
        - Min: {stats.get('min', 'N/A'):.2f}
        - Max: {stats.get('max', 'N/A'):.2f}
        """
        
        if 'outliers' in column_stats:
            outliers = column_stats['outliers']
            context += f"""
        Outliers: {outliers.get('count', 'N/A')} ({outliers.get('percentage', 'N/A'):.1f}%)
        """
        
        if 'value_counts' in column_stats:
            value_counts = column_stats['value_counts']
            context += f"""
        Top Values: {dict(list(value_counts.items())[:5])}
        """
        
        # Add sample values
        sample_values = column_data.dropna().head(5).tolist()
        context += f"""
        Sample Values: {sample_values}
        """
        
        return context
    
    def _identify_trends(self, data: pd.DataFrame, 
                        date_column: Optional[str] = None) -> Dict[str, Any]:
        """Identify quantitative trends in the data"""
        trends = {}
        
        # If date column is provided, analyze time series trends
        if date_column and date_column in data.columns:
            try:
                data[date_column] = pd.to_datetime(data[date_column])
                data_sorted = data.sort_values(date_column)
                
                # Calculate monthly/weekly trends for numeric columns
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                
                for col in numeric_cols:
                    if col != date_column:
                        # Group by month and calculate growth
                        monthly_data = data_sorted.groupby(data_sorted[date_column].dt.to_period('M'))[col].sum()
                        
                        if len(monthly_data) > 1:
                            growth_rate = ((monthly_data.iloc[-1] - monthly_data.iloc[0]) / monthly_data.iloc[0]) * 100
                            trends[f"{col}_monthly_growth"] = round(growth_rate, 2)
                        
                        # Recent vs previous period comparison
                        if len(monthly_data) >= 2:
                            recent_change = ((monthly_data.iloc[-1] - monthly_data.iloc[-2]) / monthly_data.iloc[-2]) * 100
                            trends[f"{col}_recent_change"] = round(recent_change, 2)
                
            except Exception as e:
                logger.warning(f"Error in time series analysis: {str(e)}")
        
        # General trends for numeric columns
        numeric_data = data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            trends['numeric_summary'] = {
                'total_records': len(data),
                'avg_values': numeric_data.mean().to_dict(),
                'correlation_insights': self._find_correlations(numeric_data)
            }
        
        return trends
    
    def _find_correlations(self, numeric_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Find interesting correlations in numeric data"""
        correlations = []
        
        if len(numeric_data.columns) >= 2:
            corr_matrix = numeric_data.corr()
            
            # Find strong correlations (> 0.7 or < -0.7)
            for i, col1 in enumerate(corr_matrix.columns):
                for j, col2 in enumerate(corr_matrix.columns):
                    if i < j:  # Avoid duplicates
                        corr_value = corr_matrix.loc[col1, col2]
                        if abs(corr_value) > 0.7:
                            correlations.append({
                                'column1': col1,
                                'column2': col2,
                                'correlation': round(corr_value, 3),
                                'strength': 'Strong' if abs(corr_value) > 0.8 else 'Moderate'
                            })
        
        return correlations[:5]  # Return top 5 correlations
    
    def _prepare_trends_context(self, trends: Dict[str, Any], 
                              data: pd.DataFrame) -> str:
        """Prepare context for trend analysis"""
        context = f"Dataset Size: {len(data):,} records\n"
        
        for key, value in trends.items():
            if isinstance(value, (int, float)):
                context += f"{key}: {value}\n"
            elif isinstance(value, dict) and key == 'numeric_summary':
                context += f"Average Values: {value.get('avg_values', {})}\n"
                context += f"Correlations Found: {len(value.get('correlation_insights', []))}\n"
        
        return context
    
    def _prepare_narrative_context(self, data: pd.DataFrame, 
                                 insights: Dict[str, Any]) -> str:
        """Prepare context for narrative generation"""
        context = f"""
        Dataset: {len(data):,} records across {len(data.columns)} dimensions
        
        Key Insights Summary:
        {json.dumps(insights, indent=2, default=str)[:1000]}...
        
        Column Names: {list(data.columns)[:10]}
        
        Sample Statistics:
        {data.describe().iloc[:3].to_string() if not data.empty else 'No statistics available'}
        """
        
        return context
    
    def _parse_overview_response(self, response: str) -> Dict[str, str]:
        """Parse AI response for dataset overview"""
        sections = {
            "executive_summary": "",
            "key_findings": [],
            "data_quality": "",
            "recommendations": []
        }
        
        # Simple parsing - in production, you might want more sophisticated parsing
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'executive summary' in line.lower() or 'summary' in line.lower():
                current_section = 'executive_summary'
            elif 'key finding' in line.lower() or 'findings' in line.lower():
                current_section = 'key_findings'
            elif 'data quality' in line.lower() or 'quality' in line.lower():
                current_section = 'data_quality'
            elif 'recommendation' in line.lower():
                current_section = 'recommendations'
            elif line and current_section:
                if current_section in ['key_findings', 'recommendations']:
                    if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                        sections[current_section].append(line[1:].strip())
                    elif line and not line.startswith('#'):
                        sections[current_section].append(line)
                else:
                    sections[current_section] += line + " "
        
        # Clean up
        for key, value in sections.items():
            if isinstance(value, str):
                sections[key] = value.strip()
        
        return sections
    
    def _parse_column_response(self, response: str) -> Dict[str, str]:
        """Parse AI response for column analysis"""
        sections = {
            "pattern_analysis": "",
            "business_significance": "",
            "anomalies": "",
            "recommendations": ""
        }
        
        # Simple parsing logic
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'pattern' in line.lower():
                current_section = 'pattern_analysis'
            elif 'significance' in line.lower() or 'business' in line.lower():
                current_section = 'business_significance'
            elif 'anomal' in line.lower() or 'concern' in line.lower():
                current_section = 'anomalies'
            elif 'recommendation' in line.lower():
                current_section = 'recommendations'
            elif line and current_section and not line.startswith('#'):
                sections[current_section] += line + " "
        
        # Clean up
        for key, value in sections.items():
            sections[key] = value.strip()
        
        return sections
    
    def _parse_trends_response(self, response: str) -> Dict[str, str]:
        """Parse AI response for trend analysis"""
        sections = {
            "trend_summary": "",
            "seasonal_patterns": "",
            "growth_analysis": "",
            "forecast_insights": "",
            "recommendations": ""
        }
        
        # Simple parsing logic
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'trend summary' in line.lower() or 'summary' in line.lower():
                current_section = 'trend_summary'
            elif 'seasonal' in line.lower() or 'pattern' in line.lower():
                current_section = 'seasonal_patterns'
            elif 'growth' in line.lower() or 'decline' in line.lower():
                current_section = 'growth_analysis'
            elif 'forecast' in line.lower() or 'future' in line.lower():
                current_section = 'forecast_insights'
            elif 'recommendation' in line.lower() or 'strategic' in line.lower():
                current_section = 'recommendations'
            elif line and current_section and not line.startswith('#'):
                sections[current_section] += line + " "
        
        # Clean up
        for key, value in sections.items():
            sections[key] = value.strip()
        
        return sections


class InsightFormatter:
    """
    Utility class for formatting AI insights for different outputs
    """
    
    @staticmethod
    def format_for_dashboard(insights: Dict[str, Any]) -> Dict[str, str]:
        """Format insights for dashboard display"""
        formatted = {}
        
        for key, value in insights.items():
            if isinstance(value, list):
                formatted[key] = "\n".join([f"• {item}" for item in value])
            elif isinstance(value, str):
                formatted[key] = value
            else:
                formatted[key] = str(value)
        
        return formatted
    
    @staticmethod
    def format_for_report(insights: Dict[str, Any], title: str = "Data Analysis Report") -> str:
        """Format insights as a structured report"""
        report = f"# {title}\n\n"
        report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for section, content in insights.items():
            section_title = section.replace('_', ' ').title()
            report += f"## {section_title}\n\n"
            
            if isinstance(content, list):
                for item in content:
                    report += f"- {item}\n"
            else:
                report += f"{content}\n"
            
            report += "\n"
        
        return report
    
    @staticmethod
    def extract_key_metrics(insights: Dict[str, Any]) -> Dict[str, str]:
        """Extract key metrics for quick display"""
        metrics = {}
        
        # Extract numbers and percentages from insights
        for section, content in insights.items():
            if isinstance(content, str):
                # Simple regex to find percentages and numbers
                import re
                numbers = re.findall(r'(\d+(?:\.\d+)?%?)', content)
                if numbers:
                    metrics[f"{section}_metrics"] = ", ".join(numbers[:3])
        
        return metrics
