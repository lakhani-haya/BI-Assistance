"""
Visualization with AI insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from src.visualizer import VisualizationEngine
from src.ai_analyzer import AIAnalyzer
from src.chart_templates import ChartTemplates, ChartStyling
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


class IntelligentVisualizationEngine:
    """Visualization engine with AI insights"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the intelligent visualization engine
        
        Args:
            openai_api_key (str, optional): OpenAI API key for AI-enhanced explanations
        """
        self.viz_engine = VisualizationEngine()
        self.ai_analyzer = AIAnalyzer(api_key=openai_api_key) if openai_api_key else None
        
        logger.info("Intelligent Visualization Engine initialized")
    
    def create_smart_dashboard(self, data: pd.DataFrame, 
                              business_category: str = 'general',
                              theme: str = 'business') -> Dict[str, Any]:
        """
        Create an intelligent dashboard with AI-generated insights
        
        Args:
            data (pd.DataFrame): Input data
            business_category (str): Business category for targeted analysis
            theme (str): Visual theme to apply
            
        Returns:
            Dict: Dashboard with charts and AI insights
        """
        try:
            logger.info(f"Creating smart dashboard for {business_category} category")
            
            # Generate visualizations
            viz_results = self.viz_engine.auto_visualize(data, max_charts=6)
            
            # Apply consistent theme to all charts
            themed_charts = []
            for chart_info in viz_results.get('interactive_charts', []):
                if chart_info.get('chart'):
                    themed_chart = ChartStyling.apply_theme(chart_info['chart'], theme)
                    chart_info['chart'] = themed_chart
                    themed_charts.append(chart_info)
            
            # Generate AI insights for each chart if AI is available
            enhanced_charts = []
            for chart_info in themed_charts:
                enhanced_chart = chart_info.copy()
                
                if self.ai_analyzer:
                    try:
                        # Generate AI explanation for the chart
                        chart_context = {
                            'chart_type': chart_info['type'],
                            'columns_used': chart_info['columns_used'],
                            'business_category': business_category
                        }
                        
                        ai_explanation = self.ai_analyzer.explain_chart_insights(
                            chart_info['type'], 
                            {'columns': chart_info['columns_used']}, 
                            chart_context
                        )
                        
                        enhanced_chart['ai_explanation'] = ai_explanation
                        
                    except Exception as e:
                        logger.warning(f"Failed to generate AI explanation: {str(e)}")
                        enhanced_chart['ai_explanation'] = chart_info.get('rationale', 'Standard chart explanation')
                else:
                    enhanced_chart['ai_explanation'] = chart_info.get('rationale', 'Standard chart explanation')
                
                enhanced_charts.append(enhanced_chart)
            
            # Create category-specific dashboard if supported
            specialized_dashboard = self._create_specialized_dashboard(data, business_category)
            
            # Generate overall dashboard insights
            dashboard_insights = {}
            if self.ai_analyzer:
                try:
                    dashboard_insights = self._generate_dashboard_insights(data, enhanced_charts, business_category)
                except Exception as e:
                    logger.warning(f"Failed to generate dashboard insights: {str(e)}")
            
            dashboard = {
                'charts': enhanced_charts,
                'specialized_dashboard': specialized_dashboard,
                'summary_dashboard': viz_results.get('summary_dashboard'),
                'statistical_summary': viz_results.get('statistical_summary'),
                'dashboard_insights': dashboard_insights,
                'theme_applied': theme,
                'business_category': business_category,
                'recommendations': viz_results.get('recommendations', []),
                'metadata': {
                    'total_charts': len(enhanced_charts),
                    'data_shape': data.shape,
                    'generated_at': pd.Timestamp.now().isoformat()
                }
            }
            
            logger.info(f"Smart dashboard created with {len(enhanced_charts)} charts")
            return dashboard
            
        except Exception as e:
            logger.error(f"Error creating smart dashboard: {str(e)}")
            return {
                'error': f"Dashboard creation failed: {str(e)}",
                'charts': [],
                'dashboard_insights': {}
            }
    
    def _create_specialized_dashboard(self, data: pd.DataFrame, 
                                    category: str) -> Optional[go.Figure]:
        """Create specialized dashboard based on business category"""
        try:
            if category == 'sales':
                return self._create_sales_dashboard(data)
            elif category == 'financial':
                return self._create_financial_dashboard(data)
            elif category == 'operational':
                return self._create_operational_dashboard(data)
            else:
                return None
                
        except Exception as e:
            logger.warning(f"Failed to create specialized {category} dashboard: {str(e)}")
            return None
    
    def _create_sales_dashboard(self, data: pd.DataFrame) -> Optional[go.Figure]:
        """Create sales-specific dashboard"""
        try:
            # Identify sales-related columns
            date_cols = data.select_dtypes(include=['datetime64']).columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            # Look for sales-related columns
            revenue_cols = [col for col in numeric_cols if any(term in col.lower() 
                           for term in ['sales', 'revenue', 'amount', 'total'])]
            region_cols = [col for col in data.columns if 'region' in col.lower()]
            product_cols = [col for col in data.columns if any(term in col.lower() 
                           for term in ['product', 'category', 'item'])]
            
            if not revenue_cols:
                return None
            
            # Prepare data for sales dashboard template
            data_dict = {}
            
            # Revenue over time
            if date_cols and revenue_cols:
                date_col = date_cols[0]
                revenue_col = revenue_cols[0]
                
                # Aggregate by date
                daily_revenue = data.groupby(data[date_col].dt.date)[revenue_col].sum().reset_index()
                daily_revenue.columns = ['date', 'revenue']
                data_dict['revenue_over_time'] = daily_revenue
            
            # Sales by region
            if region_cols and revenue_cols:
                region_col = region_cols[0]
                revenue_col = revenue_cols[0]
                
                regional_sales = data.groupby(region_col)[revenue_col].sum().reset_index()
                regional_sales.columns = ['region', 'sales']
                data_dict['sales_by_region'] = regional_sales
            
            # Product performance
            if product_cols and revenue_cols:
                product_col = product_cols[0]
                revenue_col = revenue_cols[0]
                
                product_performance = data.groupby(product_col)[revenue_col].sum().reset_index()
                product_performance.columns = ['product', 'revenue']
                product_performance = product_performance.sort_values('revenue', ascending=False)
                data_dict['product_performance'] = product_performance
            
            if data_dict:
                return ChartTemplates.sales_dashboard_template(data_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating sales dashboard: {str(e)}")
            return None
    
    def _create_financial_dashboard(self, data: pd.DataFrame) -> Optional[go.Figure]:
        """Create financial-specific dashboard"""
        try:
            # Look for financial columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            revenue_cols = [col for col in numeric_cols if any(term in col.lower() 
                           for term in ['revenue', 'income', 'sales'])]
            expense_cols = [col for col in numeric_cols if any(term in col.lower() 
                          for term in ['cost', 'expense', 'expenditure'])]
            profit_cols = [col for col in numeric_cols if any(term in col.lower() 
                          for term in ['profit', 'margin', 'net'])]
            
            if not revenue_cols and not expense_cols:
                return None
            
            # Prepare basic financial dashboard data
            data_dict = {}
            
            # If we have both revenue and expenses
            if revenue_cols and expense_cols:
                # Create period-based comparison (if date column exists)
                date_cols = data.select_dtypes(include=['datetime64']).columns
                if date_cols:
                    date_col = date_cols[0]
                    period_data = data.groupby(data[date_col].dt.to_period('M')).agg({
                        revenue_cols[0]: 'sum',
                        expense_cols[0]: 'sum'
                    }).reset_index()
                    period_data.columns = ['period', 'revenue', 'expenses']
                    data_dict['revenue_expenses'] = period_data
            
            if data_dict:
                return ChartTemplates.financial_overview_template(data_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating financial dashboard: {str(e)}")
            return None
    
    def _create_operational_dashboard(self, data: pd.DataFrame) -> Optional[go.Figure]:
        """Create operational-specific dashboard"""
        try:
            # Look for operational metrics
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            efficiency_cols = [col for col in numeric_cols if any(term in col.lower() 
                              for term in ['efficiency', 'utilization', 'performance'])]
            quality_cols = [col for col in numeric_cols if any(term in col.lower() 
                           for term in ['quality', 'defect', 'error', 'accuracy'])]
            
            if not efficiency_cols and not quality_cols:
                return None
            
            # Create basic operational dashboard
            data_dict = {}
            
            # KPIs (use first few numeric columns as sample KPIs)
            if len(numeric_cols) >= 3:
                kpi_data = pd.DataFrame({
                    'metric': numeric_cols[:3],
                    'value': [data[col].mean() for col in numeric_cols[:3]]
                })
                data_dict['kpis'] = kpi_data
            
            if data_dict:
                return ChartTemplates.operational_metrics_template(data_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating operational dashboard: {str(e)}")
            return None
    
    def _generate_dashboard_insights(self, data: pd.DataFrame, 
                                   charts: List[Dict[str, Any]], 
                                   category: str) -> Dict[str, Any]:
        """Generate AI insights about the overall dashboard"""
        try:
            # Prepare context about the dashboard
            context = f"""
            Dashboard Analysis for {category} data:
            
            Dataset: {len(data)} records, {len(data.columns)} columns
            Charts Generated: {len(charts)}
            
            Chart Summary:
            """
            
            for i, chart in enumerate(charts, 1):
                context += f"\n{i}. {chart['title']} ({chart['type']}) - {chart.get('rationale', 'N/A')}"
            
            # Sample of the data
            context += f"\n\nData Sample:\n{data.head(3).to_string()}"
            
            # Generate comprehensive dashboard insights
            prompt = f"""
            You are analyzing a business intelligence dashboard. Provide insights about:
            
            {context}
            
            Please provide:
            1. **Dashboard Overview** (what story does this dashboard tell?)
            2. **Key Patterns** (what patterns emerge across the visualizations?)
            3. **Business Implications** (what do these charts mean for business decisions?)
            4. **Recommended Actions** (what should stakeholders do based on this dashboard?)
            5. **Dashboard Effectiveness** (how well does this dashboard serve its purpose?)
            
            Keep insights business-focused and actionable.
            """
            
            response = self.ai_analyzer._call_openai_api(prompt)
            
            # Parse response into structured format
            insights = {
                'overview': 'Dashboard provides comprehensive view of business metrics.',
                'key_patterns': 'Multiple patterns identified across visualizations.',
                'business_implications': 'Several business implications identified.',
                'recommended_actions': 'Strategic actions recommended based on analysis.',
                'effectiveness_assessment': 'Dashboard effectively communicates key insights.',
                'full_analysis': response
            }
            
            # Simple parsing to extract sections
            lines = response.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if 'overview' in line.lower():
                    current_section = 'overview'
                elif 'patterns' in line.lower():
                    current_section = 'key_patterns'
                elif 'implications' in line.lower():
                    current_section = 'business_implications'
                elif 'actions' in line.lower() or 'recommended' in line.lower():
                    current_section = 'recommended_actions'
                elif 'effectiveness' in line.lower():
                    current_section = 'effectiveness_assessment'
                elif line and current_section and not line.startswith('#'):
                    insights[current_section] = line
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating dashboard insights: {str(e)}")
            return {
                'overview': 'Dashboard insights unavailable.',
                'error': str(e)
            }
    
    def export_dashboard(self, dashboard: Dict[str, Any], 
                        output_dir: str, format: str = 'html') -> List[str]:
        """
        Export complete dashboard to files
        
        Args:
            dashboard (Dict): Dashboard data
            output_dir (str): Output directory
            format (str): Export format
            
        Returns:
            List[str]: List of exported file paths
        """
        try:
            import os
            import json
            
            os.makedirs(output_dir, exist_ok=True)
            exported_files = []
            
            # Export individual charts
            charts = dashboard.get('charts', [])
            for i, chart_info in enumerate(charts):
                if chart_info.get('chart'):
                    filename = f"chart_{i+1}_{chart_info['type']}.{format}"
                    filepath = os.path.join(output_dir, filename)
                    
                    if format == 'html':
                        chart_info['chart'].write_html(filepath)
                    elif format == 'png':
                        chart_info['chart'].write_image(filepath)
                    
                    exported_files.append(filepath)
            
            # Export specialized dashboard
            if dashboard.get('specialized_dashboard'):
                filepath = os.path.join(output_dir, f"specialized_dashboard.{format}")
                if format == 'html':
                    dashboard['specialized_dashboard'].write_html(filepath)
                elif format == 'png':
                    dashboard['specialized_dashboard'].write_image(filepath)
                exported_files.append(filepath)
            
            # Export dashboard insights as JSON
            insights_file = os.path.join(output_dir, 'dashboard_insights.json')
            with open(insights_file, 'w') as f:
                json.dump({
                    'insights': dashboard.get('dashboard_insights', {}),
                    'metadata': dashboard.get('metadata', {}),
                    'recommendations': dashboard.get('recommendations', [])
                }, f, indent=2, default=str)
            exported_files.append(insights_file)
            
            logger.info(f"Dashboard exported to {output_dir} with {len(exported_files)} files")
            return exported_files
            
        except Exception as e:
            logger.error(f"Error exporting dashboard: {str(e)}")
            return []
    
    def get_chart_recommendations(self, data: pd.DataFrame, 
                                 user_preferences: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Get intelligent chart recommendations based on data and user preferences
        
        Args:
            data (pd.DataFrame): Input data
            user_preferences (Dict): User preferences for charts
            
        Returns:
            List[Dict]: Enhanced recommendations with explanations
        """
        # Get base recommendations
        recommendations = self.viz_engine.chart_recommender.recommend_charts(data)
        
        # Enhance with AI explanations if available
        if self.ai_analyzer:
            for rec in recommendations:
                try:
                    # Generate enhanced explanation
                    context = {
                        'data_shape': data.shape,
                        'columns': rec['columns'],
                        'chart_type': rec['chart_type']
                    }
                    
                    enhanced_rationale = self.ai_analyzer.explain_chart_insights(
                        rec['chart_type'], 
                        {'columns': rec['columns']}, 
                        context
                    )
                    
                    rec['enhanced_rationale'] = enhanced_rationale
                    
                except Exception as e:
                    logger.warning(f"Failed to enhance recommendation: {str(e)}")
                    rec['enhanced_rationale'] = rec['rationale']
        
        return recommendations
