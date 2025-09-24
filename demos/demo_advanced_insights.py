"""
Demo script for Advanced Natural Language Insights
Demonstrates Step 8: Enhanced AI storytelling and Q&A capabilities
"""

import os
import sys
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.advanced_insights import AdvancedInsightsEngine, StorytellingMode
from src.interactive_storyteller import InteractiveStorytellerInterface


def create_demo_business_data():
    """Create comprehensive demo business data for storytelling"""
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', end='2024-01-31', freq='D')
    
    # Sales data with seasonal patterns and trends
    base_sales = 10000
    seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    trend_factor = 1 + 0.002 * np.arange(len(dates))  # 0.2% daily growth
    noise = np.random.normal(0, 0.1, len(dates))
    
    sales = base_sales * seasonal_factor * trend_factor * (1 + noise)
    
    # Create regional data
    regions = ['North', 'South', 'East', 'West', 'Central']
    region_weights = [0.25, 0.20, 0.22, 0.18, 0.15]
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
    category_weights = [0.35, 0.25, 0.20, 0.15, 0.05]
    
    # Customer segments
    segments = ['Enterprise', 'SMB', 'Individual']
    segment_weights = [0.45, 0.35, 0.20]
    
    # Create detailed dataset
    data_records = []
    
    for i, date in enumerate(dates):
        daily_sales = sales[i]
        
        # Distribute sales across regions, categories, and segments
        for region, reg_weight in zip(regions, region_weights):
            for category, cat_weight in zip(categories, category_weights):
                for segment, seg_weight in zip(segments, segment_weights):
                    
                    # Calculate record-level metrics
                    record_sales = daily_sales * reg_weight * cat_weight * seg_weight
                    record_sales *= np.random.uniform(0.7, 1.3)  # Add variation
                    
                    # Calculate related metrics
                    avg_order_value = np.random.uniform(80, 400)
                    orders = max(1, int(record_sales / avg_order_value))
                    
                    # Customer metrics
                    customers = max(1, int(orders * np.random.uniform(0.7, 1.0)))
                    
                    # Profit margin varies by category
                    margin_map = {
                        'Electronics': np.random.uniform(0.12, 0.18),
                        'Clothing': np.random.uniform(0.45, 0.65),
                        'Home & Garden': np.random.uniform(0.25, 0.35),
                        'Sports': np.random.uniform(0.30, 0.45),
                        'Books': np.random.uniform(0.35, 0.50)
                    }
                    profit_margin = margin_map[category]
                    profit = record_sales * profit_margin
                    
                    # Marketing spend (varies by segment and season)
                    marketing_spend = record_sales * np.random.uniform(0.05, 0.15)
                    if segment == 'Enterprise':
                        marketing_spend *= 0.7  # Lower marketing cost for enterprise
                    
                    # Customer satisfaction (varies by category and region)
                    base_satisfaction = 4.2
                    if category == 'Electronics':
                        base_satisfaction += 0.2
                    elif category == 'Books':
                        base_satisfaction += 0.3
                    
                    satisfaction = min(5.0, max(1.0, base_satisfaction + np.random.normal(0, 0.3)))
                    
                    data_records.append({
                        'Date': date,
                        'Region': region,
                        'Product_Category': category,
                        'Customer_Segment': segment,
                        'Revenue': round(record_sales, 2),
                        'Orders': orders,
                        'Customers': customers,
                        'Avg_Order_Value': round(avg_order_value, 2),
                        'Profit': round(profit, 2),
                        'Profit_Margin': round(profit_margin * 100, 1),
                        'Marketing_Spend': round(marketing_spend, 2),
                        'Customer_Satisfaction': round(satisfaction, 1),
                        'Quarter': f"Q{((date.month - 1) // 3) + 1}",
                        'Month': date.strftime('%B'),
                        'Weekday': date.strftime('%A'),
                        'Year': date.year
                    })
    
    return pd.DataFrame(data_records)


def demo_ai_storytelling():
    """Demonstrate AI storytelling capabilities"""
    
    print(" Advanced AI Storytelling Demo")
    print("=" * 50)
    
    # Create demo data
    print(" Creating comprehensive business demo data...")
    data = create_demo_business_data()
    
    print(f" Generated dataset with {len(data)} records")
    print(f" Date range: {data['Date'].min()} to {data['Date'].max()}")
    print(f" Total revenue: ${data['Revenue'].sum():,.2f}")
    
    # Initialize insights engine
    print("\n Initializing Advanced Insights Engine...")
    insights_engine = AdvancedInsightsEngine()
    
    # Demo 1: Executive Brief Story
    print("\n Demo 1: Executive Brief Story")
    print("-" * 30)
    
    executive_story = insights_engine.create_data_story(
        data,
        mode=StorytellingMode.EXECUTIVE_BRIEF,
        target_audience="C-Suite Executives",
        business_context="Multi-regional retail business with diverse product portfolio"
    )
    
    print(f" Title: {executive_story.title}")
    print(f" Target: {executive_story.target_audience}")
    print(f" Executive Summary: {executive_story.executive_summary[:200]}...")
    print(f" Key Findings: {len(executive_story.key_findings)} insights")
    
    # Demo 2: Interactive Q&A Session
    print("\n Demo 2: Interactive Q&A Session")
    print("-" * 30)
    
    sample_questions = [
        "What are the main revenue trends across regions?",
        "Which product category has the highest profit margin?",
        "How does customer satisfaction correlate with revenue?",
        "What seasonal patterns can you identify in the sales data?"
    ]
    
    for question in sample_questions:
        print(f"\n Question: {question}")
        
        answer = insights_engine.interactive_qa_session(data, question)
        print(f" Answer: {answer['answer'][:150]}...")
        print(f" Confidence: {answer.get('confidence', 0)}%")
        
        if answer.get('follow_up_questions'):
            print(f" Follow-up: {answer['follow_up_questions'][0]}")
    
    # Demo 3: Opportunity Mining
    print("\n Demo 3: Business Opportunity Mining")
    print("-" * 30)
    
    opportunities = insights_engine.mine_opportunities(
        data,
        industry_context="Multi-channel retail with focus on customer experience and operational efficiency",
        current_metrics={
            'revenue_growth': 15.2,
            'customer_acquisition_cost': 45.0,
            'retention_rate': 78.5,
            'profit_margin': 32.1
        }
    )
    
    print(f" Identified {len(opportunities)} business opportunities:")
    for i, opp in enumerate(opportunities[:3], 1):
        print(f"\n{i}. {opp['title']}")
        print(f"    {opp['description'][:100]}...")
        print(f"    Impact: {opp['potential_impact']}")
        print(f"    Timeline: {opp['time_to_value']}")
    
    # Demo 4: Performance Diagnosis
    print("\n Demo 4: Performance Diagnosis")
    print("-" * 30)
    
    diagnosis = insights_engine.diagnose_performance(
        data,
        time_column='Date',
        performance_metrics=['Revenue', 'Profit', 'Customer_Satisfaction']
    )
    
    print(f" Overall Assessment: {diagnosis['overall_assessment']}")
    print(f" Strengths: {len(diagnosis.get('strengths', []))} identified")
    print(f" Improvement Areas: {len(diagnosis.get('areas_for_improvement', []))}")
    print(f" Recommendations: {len(diagnosis.get('recommendations', []))}")
    
    # Demo 5: Enhanced Insights Generation
    print("\n Demo 5: Enhanced Insights Generation")
    print("-" * 30)
    
    enhanced_insights = insights_engine.generate_enhanced_insights(
        data,
        business_context="Retail analytics focusing on growth and optimization",
        focus_areas=['trends', 'correlations', 'opportunities', 'performance']
    )
    
    print(f" Generated {len(enhanced_insights)} enhanced insights:")
    for insight in enhanced_insights[:3]:
        print(f"\n {insight.title}")
        print(f"    Type: {insight.insight_type.value}")
        print(f"    Priority: {insight.priority}")
        print(f"    Confidence: {insight.confidence_score}%")
        print(f"    Summary: {insight.summary[:100]}...")
        print(f"    Actions: {len(insight.recommended_actions)} recommended")
    
    return data, insights_engine


def demo_streamlit_interface():
    """Demonstrate Streamlit interface integration"""
    
    print("\n Streamlit Interface Demo")
    print("=" * 50)
    
    # This would be run in a Streamlit app
    data = create_demo_business_data()
    
    # Initialize the interactive storyteller interface
    storyteller = InteractiveStorytellerInterface(data)
    
    print(" Interactive Storyteller Interface initialized")
    print(" Ready for Streamlit integration")
    print("\nFeatures available:")
    print("-  Story Generation with 6 modes")
    print("-  Interactive Q&A with follow-ups")
    print("-  Deep AI insights generation")
    print("-  Business opportunity mining")
    print("-  Performance diagnosis")
    print("-  Visualization suggestions")
    print("-  Export capabilities")
    
    return storyteller


def main():
    """Main demo function"""
    
    print(" Step 8: Natural Language Insights Enhancement Demo")
    print("=" * 60)
    print("This demo showcases advanced AI-powered data storytelling")
    print("and interactive Q&A capabilities for business intelligence.")
    print()
    
    try:
        # Run core AI storytelling demo
        data, insights_engine = demo_ai_storytelling()
        
        # Demo Streamlit interface
        storyteller = demo_streamlit_interface()
        
        print("\n Demo Complete!")
        print("=" * 50)
        print(" All Step 8 features demonstrated successfully")
        print(" Ready for Streamlit web interface")
        print("\n Next Steps:")
        print("1. Run `streamlit run src/dashboard.py` to test web interface")
        print("2. Navigate to ' AI Insights' tab")
        print("3. Explore all storytelling features")
        print("4. Test Q&A with your own questions")
        print("5. Export generated stories and insights")
        
        print(f"\n Demo Data Summary:")
        print(f"   Records: {len(data):,}")
        print(f"   Columns: {len(data.columns)}")
        print(f"   Date Range: {data['Date'].min()} to {data['Date'].max()}")
        print(f"   Total Revenue: ${data['Revenue'].sum():,.2f}")
        print(f"   Avg Daily Revenue: ${data.groupby('Date')['Revenue'].sum().mean():,.2f}")
        
    except Exception as e:
        print(f" Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
