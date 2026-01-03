"""
Example script demonstrati AI-powered data analysis
AI integration in action
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from src.intelligent_analyzer import IntelligentDataAnalyzer
from src.config import Config

def create_sample_sales_data():
    """Create sample sales data for demonstration"""
    np.random.seed(42)
    
    data = {
        'date': pd.date_range('2024-01-01', periods=365, freq='D'),
        'sales_amount': np.random.normal(1000, 200, 365) + np.sin(np.arange(365) * 2 * np.pi / 7) * 50,  # Weekly pattern
        'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], 365),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports'], 365),
        'customer_type': np.random.choice(['New', 'Returning', 'VIP'], 365, p=[0.3, 0.6, 0.1]),
        'sales_rep': np.random.choice([f'Rep_{i}' for i in range(1, 11)], 365),
        'discount_percent': np.random.uniform(0, 30, 365)
    }
    
    # Add some seasonality to sales
    for i, date in enumerate(data['date']):
        if date.month in [11, 12]:  # Holiday season
            data['sales_amount'][i] *= 1.3
        elif date.month in [6, 7, 8]:  # Summer slowdown
            data['sales_amount'][i] *= 0.9
    
    return pd.DataFrame(data)

def demo_basic_analysis():
    """Demonstrate basic analysis without AI"""
    print("=" * 60)
    print("🔍 DEMO: Basic Data Analysis (No AI Required)")
    print("=" * 60)
    
    # Create sample data
    df = create_sample_sales_data()
    print(f"📊 Created sample dataset: {len(df)} rows × {len(df.columns)} columns")
    
    # Initialize analyzer without AI
    analyzer = IntelligentDataAnalyzer(openai_api_key=None)
    
    # Run analysis without AI insights
    results = analyzer.analyze_dataframe(df, "Sample Sales Data", generate_insights=False)
    
    # Display basic results
    print("\n📈 Data Summary:")
    basic_info = results['data_summary']['basic_info']
    print(f"   • Rows: {basic_info['rows']:,}")
    print(f"   • Columns: {basic_info['columns']}")
    print(f"   • Data Quality Score: {results['data_summary']['data_quality']['overall_score']}/100")
    print(f"   • Missing Values: {basic_info['missing_values_total']}")
    
    print("\n🧹 Data Cleaning:")
    if results['cleaning_summary']['operations_performed']:
        for operation in results['cleaning_summary']['operations_performed']:
            print(f"   • {operation}")
    else:
        print("   • No cleaning operations needed")
    
    print("\n📋 Column Types:")
    column_info = results['data_summary']['column_info']
    print(f"   • Numeric: {column_info['numeric_columns']}")
    print(f"   • Categorical: {column_info['categorical_columns']}")
    print(f"   • DateTime: {column_info['datetime_columns']}")
    
    return analyzer, results

def demo_ai_analysis():
    """Demonstrate AI-powered analysis (requires API key)"""
    print("\n" + "=" * 60)
    print("🤖 DEMO: AI-Powered Analysis")
    print("=" * 60)
    
    # Check if API key is available
    api_key = Config.OPENAI_API_KEY
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API key not configured.")
        print("   To enable AI features:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OpenAI API key to the .env file")
        print("   3. Restart the application")
        return None
    
    try:
        # Create sample data
        df = create_sample_sales_data()
        
        # Initialize analyzer with AI
        analyzer = IntelligentDataAnalyzer(openai_api_key=api_key)
        
        print("🧠 Generating AI insights... (this may take a moment)")
        
        # Run full analysis with AI
        results = analyzer.analyze_dataframe(df, "Sample Sales Data", generate_insights=True)
        
        # Display AI insights
        if 'insights' in results and results['insights']:
            insights = results['insights']
            
            if 'overview' in insights:
                print("\n📝 Executive Summary:")
                print(f"   {insights['overview'].get('executive_summary', 'Not available')}")
                
                print("\n🔍 Key Findings:")
                findings = insights['overview'].get('key_findings', [])
                for i, finding in enumerate(findings[:3], 1):
                    print(f"   {i}. {finding}")
                
                print("\n💡 Recommendations:")
                recommendations = insights['overview'].get('recommendations', [])
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec}")
            
            if 'narrative' in insights:
                print("\n📖 Business Narrative:")
                narrative = insights['narrative'][:500] + "..." if len(insights['narrative']) > 500 else insights['narrative']
                print(f"   {narrative}")
        
        return analyzer, results
        
    except Exception as e:
        print(f"❌ Error in AI analysis: {str(e)}")
        print("   This might be due to:")
        print("   • Invalid API key")
        print("   • Network connectivity issues")
        print("   • API rate limits")
        return None

def demo_targeted_analysis():
    """Demonstrate targeted business analysis"""
    print("\n" + "=" * 60)
    print("🎯 DEMO: Targeted Business Analysis")
    print("=" * 60)
    
    # This demo shows how to use the intelligent analyzer
    # for different business scenarios
    
    df = create_sample_sales_data()
    analyzer = IntelligentDataAnalyzer()
    analyzer.analyze_dataframe(df, generate_insights=False)
    
    # Get category suggestions
    suggestions = analyzer.get_data_category_suggestions()
    print(f"📊 Detected data categories: {', '.join(suggestions)}")
    
    # Show what targeted analysis would look like
    print("\n🎯 Available Analysis Types:")
    print("   • Sales Performance Analysis")
    print("   • Financial Health Assessment") 
    print("   • Operational Efficiency Review")
    print("   • Customer Behavior Insights")
    print("   • Trend and Forecasting Analysis")
    
    print("\n👥 Audience-Specific Reports:")
    print("   • Executive Dashboard (High-level KPIs)")
    print("   • Manager Reports (Operational metrics)")
    print("   • Analyst Deep-Dive (Statistical insights)")
    
    return analyzer

def main():
    """Run all demonstrations"""
    print("🚀 BI Assistant - AI Integration Demo")
    print("This demo showcases the AI-powered analysis capabilities")
    
    # Demo 1: Basic analysis (always works)
    analyzer, basic_results = demo_basic_analysis()
    
    # Demo 2: AI analysis (requires API key)
    ai_results = demo_ai_analysis()
    
    # Demo 3: Targeted analysis concepts
    targeted_analyzer = demo_targeted_analysis()
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")
    print("=" * 60)
    
    # Show next steps
    print("\n🔗 Next Steps:")
    print("   • Set up OpenAI API key for full AI features")
    print("   • Try uploading your own data files")
    print("   • Explore the web interface (coming next)")
    print("   • Generate automated dashboards")
    
    return {
        'basic_analyzer': analyzer,
        'basic_results': basic_results,
        'ai_results': ai_results,
        'targeted_analyzer': targeted_analyzer
    }

if __name__ == "__main__":
    results = main()
