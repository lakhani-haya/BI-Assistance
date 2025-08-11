"""
AI prompt templates for generating consistent and effective insights
"""

from typing import Dict, Any, List


class PromptTemplates:
    """Collection of prompt templates for different types of analysis"""
    
    @staticmethod
    def dataset_overview_prompt(context: str) -> str:
        """Template for dataset overview analysis"""
        return f"""
        You are a senior business intelligence analyst reviewing a new dataset. 
        Your audience consists of business executives who need actionable insights.
        
        Dataset Context:
        {context}
        
        Provide a comprehensive analysis with the following structure:
        
        ## Executive Summary
        (2-3 sentences describing what this dataset represents and its business value)
        
        ## Key Business Insights
        - [Insight 1: Focus on business impact]
        - [Insight 2: Highlight interesting patterns]
        - [Insight 3: Note any surprising findings]
        - [Insight 4: Identify opportunities or risks]
        - [Insight 5: Comment on data completeness/quality]
        
        ## Data Quality Assessment
        (Brief assessment of data reliability, completeness, and any concerns)
        
        ## Strategic Recommendations
        - [Recommendation 1: Immediate action item]
        - [Recommendation 2: Further analysis needed]
        - [Recommendation 3: Process improvement opportunity]
        
        Use specific numbers from the data when possible. Keep language business-friendly.
        Focus on what matters to decision-makers, not technical details.
        """
    
    @staticmethod
    def sales_analysis_prompt(context: str) -> str:
        """Specialized template for sales data analysis"""
        return f"""
        You are analyzing sales performance data for business stakeholders.
        
        Sales Data Context:
        {context}
        
        Provide insights focused on:
        
        ## Sales Performance Summary
        (Overall performance assessment with key metrics)
        
        ## Revenue Insights
        - Top performing products/categories
        - Revenue trends and growth patterns
        - Seasonal variations or cycles
        
        ## Customer Behavior Patterns
        - Purchase patterns and preferences
        - Customer segment performance
        - Geographic performance variations
        
        ## Business Opportunities
        - Growth opportunities identified
        - Underperforming areas needing attention
        - Cross-selling or upselling potential
        
        ## Action Items
        - Immediate tactical recommendations
        - Strategic initiatives to consider
        - Areas requiring further investigation
        
        Include specific numbers and percentages to support your insights.
        """
    
    @staticmethod
    def financial_analysis_prompt(context: str) -> str:
        """Template for financial data analysis"""
        return f"""
        You are analyzing financial data for executive leadership.
        
        Financial Data Context:
        {context}
        
        Provide analysis covering:
        
        ## Financial Health Overview
        (High-level assessment of financial performance)
        
        ## Revenue & Profitability Analysis
        - Revenue trends and drivers
        - Profit margin analysis
        - Cost structure insights
        
        ## Risk Assessment
        - Financial risks identified
        - Volatility patterns
        - Concentration risks
        
        ## Growth Opportunities
        - Areas of strong performance
        - Investment opportunities
        - Efficiency improvements
        
        ## Financial Recommendations
        - Budget allocation suggestions
        - Cost optimization opportunities
        - Revenue enhancement strategies
        
        Use financial terminology appropriately and focus on bottom-line impact.
        """
    
    @staticmethod
    def operational_analysis_prompt(context: str) -> str:
        """Template for operational data analysis"""
        return f"""
        You are analyzing operational performance data for management.
        
        Operational Data Context:
        {context}
        
        Focus your analysis on:
        
        ## Operational Efficiency Overview
        (Summary of operational performance and efficiency)
        
        ## Process Performance Insights
        - Key performance indicators analysis
        - Bottlenecks and constraints identified
        - Quality metrics assessment
        
        ## Resource Utilization
        - Resource allocation effectiveness
        - Capacity utilization patterns
        - Productivity trends
        
        ## Improvement Opportunities
        - Process optimization potential
        - Automation opportunities
        - Best practice implementations
        
        ## Operational Recommendations
        - Immediate process improvements
        - Long-term operational strategy
        - Technology enhancement suggestions
        
        Focus on operational excellence and continuous improvement opportunities.
        """
    
    @staticmethod
    def trend_analysis_prompt(context: str, time_period: str = "monthly") -> str:
        """Template for trend analysis"""
        return f"""
        You are conducting a comprehensive trend analysis for business planning.
        
        Trend Analysis Context:
        {context}
        Time Period: {time_period} analysis
        
        Provide detailed trend insights:
        
        ## Trend Overview
        (Summary of major trends observed in the data)
        
        ## Growth Patterns
        - Positive growth trends and drivers
        - Declining areas and causes
        - Cyclical patterns identified
        
        ## Seasonal Analysis
        - Seasonal variations observed
        - Peak and low periods
        - Seasonal adjustment recommendations
        
        ## Forecast Implications
        - What trends suggest for future performance
        - Potential trajectory changes
        - External factors to monitor
        
        ## Strategic Planning Insights
        - Resource allocation recommendations
        - Market timing considerations
        - Risk mitigation strategies
        
        Include growth rates, trend directions, and specific time periods in your analysis.
        """
    
    @staticmethod
    def comparative_analysis_prompt(context: str, comparison_type: str) -> str:
        """Template for comparative analysis"""
        return f"""
        You are conducting a {comparison_type} comparative analysis.
        
        Comparative Analysis Context:
        {context}
        
        Provide comprehensive comparison insights:
        
        ## Comparison Overview
        (High-level summary of key differences and similarities)
        
        ## Performance Comparison
        - Top performers and their characteristics
        - Underperformers and improvement areas
        - Performance gaps identified
        
        ## Pattern Differences
        - Unique patterns in each segment
        - Common trends across segments
        - Anomalies or outliers
        
        ## Competitive Insights
        - Competitive advantages identified
        - Areas needing improvement
        - Market positioning implications
        
        ## Strategic Recommendations
        - Best practices to replicate
        - Targeted improvement strategies
        - Resource reallocation suggestions
        
        Use specific metrics and percentages to quantify differences.
        """
    
    @staticmethod
    def anomaly_detection_prompt(context: str, anomalies: List[Dict]) -> str:
        """Template for anomaly analysis"""
        return f"""
        You are investigating data anomalies and unusual patterns.
        
        Data Context:
        {context}
        
        Detected Anomalies:
        {anomalies}
        
        Provide anomaly analysis:
        
        ## Anomaly Summary
        (Overview of unusual patterns detected)
        
        ## Potential Causes
        - Business reasons for anomalies
        - Data quality issues
        - External factor influences
        
        ## Business Impact Assessment
        - Revenue/cost implications
        - Operational impact
        - Customer experience effects
        
        ## Investigation Priorities
        - Critical anomalies requiring immediate attention
        - Moderate priority items
        - Monitoring recommendations
        
        ## Corrective Actions
        - Immediate response steps
        - Process improvements needed
        - Prevention strategies
        
        Focus on business impact and actionable responses to anomalies.
        """
    
    @staticmethod
    def chart_explanation_prompt(chart_type: str, chart_data: str, context: str) -> str:
        """Template for explaining specific charts"""
        return f"""
        You are explaining a data visualization to business stakeholders.
        
        Chart Type: {chart_type}
        Chart Data: {chart_data}
        Business Context: {context}
        
        Provide a clear, concise explanation (2-3 sentences) that covers:
        
        1. What the chart displays (the data story)
        2. The key insight or pattern shown
        3. Why this matters for business decisions
        
        Examples of good explanations:
        - "This bar chart shows monthly sales revenue, revealing a 23% increase in Q4 driven primarily by holiday promotions in December."
        - "The line graph displays customer acquisition trends, indicating steady 15% monthly growth with a notable acceleration in digital channels."
        - "This pie chart breaks down revenue by product category, showing that Electronics accounts for 45% of total sales, suggesting strong market position in this segment."
        
        Keep it business-focused, specific, and actionable.
        Avoid technical jargon and focus on business implications.
        """


class InsightCategories:
    """Categories and types of insights that can be generated"""
    
    BUSINESS_CATEGORIES = {
        'sales': ['revenue_analysis', 'customer_behavior', 'product_performance', 'seasonal_trends'],
        'financial': ['profitability', 'cost_analysis', 'budget_variance', 'cash_flow'],
        'operational': ['efficiency', 'capacity_utilization', 'quality_metrics', 'process_optimization'],
        'marketing': ['campaign_performance', 'customer_acquisition', 'retention_analysis', 'channel_effectiveness'],
        'hr': ['employee_performance', 'retention_analysis', 'productivity_metrics', 'compensation_analysis']
    }
    
    INSIGHT_TYPES = {
        'descriptive': 'What happened?',
        'diagnostic': 'Why did it happen?',
        'predictive': 'What will happen?',
        'prescriptive': 'What should we do?'
    }
    
    @classmethod
    def get_category_prompt(cls, category: str) -> str:
        """Get specialized prompt based on data category"""
        prompts = {
            'sales': PromptTemplates.sales_analysis_prompt,
            'financial': PromptTemplates.financial_analysis_prompt,
            'operational': PromptTemplates.operational_analysis_prompt
        }
        
        return prompts.get(category, PromptTemplates.dataset_overview_prompt)


class PromptEnhancer:
    """Utility to enhance prompts with additional context"""
    
    @staticmethod
    def add_business_context(prompt: str, business_type: str, industry: str = None) -> str:
        """Add business context to improve relevance of insights"""
        context_addition = f"""
        
        Business Context:
        - Business Type: {business_type}
        - Industry: {industry or 'General'}
        
        Please tailor your analysis to be relevant for this type of business.
        Consider industry-specific metrics, challenges, and opportunities.
        """
        
        return prompt + context_addition
    
    @staticmethod
    def add_urgency_context(prompt: str, urgency_level: str) -> str:
        """Add urgency context to prioritize insights"""
        urgency_addition = f"""
        
        Analysis Priority: {urgency_level}
        
        {'Focus on immediate actionable insights and urgent issues.' if urgency_level == 'HIGH' else 
         'Provide balanced analysis with both immediate and strategic insights.' if urgency_level == 'MEDIUM' else
         'Focus on comprehensive strategic analysis and long-term trends.'}
        """
        
        return prompt + urgency_addition
    
    @staticmethod
    def add_audience_context(prompt: str, audience: str) -> str:
        """Tailor language and focus for specific audience"""
        audience_contexts = {
            'executives': 'Focus on high-level strategic insights, ROI implications, and key decisions needed.',
            'managers': 'Emphasize operational insights, team performance, and tactical recommendations.',
            'analysts': 'Include detailed statistical insights, methodology notes, and areas for deeper analysis.',
            'general': 'Use accessible language and focus on clear, actionable insights.'
        }
        
        context = audience_contexts.get(audience, audience_contexts['general'])
        
        return prompt + f"\n\nAudience: {audience.title()}\n{context}"
