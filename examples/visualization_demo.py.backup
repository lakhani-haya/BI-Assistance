"""
Example script demonstrating visualization capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from src.visualizer import VisualizationEngine
from src.intelligent_visualizer import IntelligentVisualizationEngine
from src.chart_templates import ChartTemplates, ChartStyling
from src.config import Config


def create_sample_sales_data():
    """Create comprehensive sample sales data"""
    np.random.seed(42)
    
    # Generate 1000 sales records
    n_records = 1000
    
    # Date range for the past year
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    
    data = []
    for i in range(n_records):
        date = np.random.choice(dates)
        
        # Seasonal effects
        month = date.month
        seasonal_multiplier = 1.0
        if month in [11, 12]:  # Holiday season
            seasonal_multiplier = 1.4
        elif month in [6, 7, 8]:  # Summer
            seasonal_multiplier = 0.8
        
        # Base sales amount with seasonality
        base_amount = np.random.normal(1000, 300) * seasonal_multiplier
        
        record = {
            'date': date,
            'sales_amount': max(100, base_amount),  # Minimum $100
            'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], 
                                     p=[0.25, 0.20, 0.20, 0.20, 0.15]),
            'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books'],
                                               p=[0.30, 0.25, 0.20, 0.15, 0.10]),
            'customer_type': np.random.choice(['New', 'Returning', 'VIP'], p=[0.30, 0.60, 0.10]),
            'sales_rep': f"Rep_{np.random.randint(1, 21)}",
            'discount_percent': np.random.uniform(0, 25),
            'profit_margin': np.random.normal(25, 8),  # Average 25% margin
            'units_sold': np.random.randint(1, 20),
            'customer_satisfaction': np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.10, 0.20, 0.35, 0.30])
        }
        
        # Calculate derived metrics
        record['profit_amount'] = record['sales_amount'] * (record['profit_margin'] / 100)
        record['unit_price'] = record['sales_amount'] / record['units_sold']
        
        data.append(record)
    
    return pd.DataFrame(data)


def demo_basic_visualization():
    """Demonstrate basic visualization capabilities"""
    print("=" * 60)
    print("📊 DEMO: Basic Visualization Engine")
    print("=" * 60)
    
    # Create sample data
    df = create_sample_sales_data()
    print(f"📈 Created sample dataset: {len(df)} records")
    
    # Initialize visualization engine
    viz_engine = VisualizationEngine()
    
    # Generate automatic visualizations
    print("\n🎨 Generating automatic visualizations...")
    results = viz_engine.auto_visualize(df, max_charts=5)
    
    print(f"✅ Generated {results['charts_created']} interactive charts")
    
    # Display chart information
    print("\n📋 Generated Charts:")
    for i, chart in enumerate(results.get('interactive_charts', []), 1):
        print(f"   {i}. {chart['title']} ({chart['type']})")
        print(f"      └─ {chart['rationale']}")
        print(f"      └─ Columns: {', '.join(chart['columns_used'])}")
    
    # Show recommendations
    print(f"\n💡 Total Recommendations: {len(results.get('recommendations', []))}")
    
    # Test custom chart creation
    print("\n🛠️  Testing Custom Chart Creation...")
    custom_chart = viz_engine.create_custom_chart(
        df, 'bar', {
            'x_col': 'region',
            'y_col': 'sales_amount',
            'title': 'Sales by Region'
        }
    )
    
    if custom_chart:
        print("✅ Custom bar chart created successfully")
    else:
        print("❌ Custom chart creation failed")
    
    return viz_engine, results


def demo_intelligent_visualization():
    """Demonstrate AI-enhanced visualization"""
    print("\n" + "=" * 60)
    print("🤖 DEMO: Intelligent Visualization Engine")
    print("=" * 60)
    
    # Check if API key is available
    api_key = Config.OPENAI_API_KEY
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API key not configured - using basic mode")
        intelligent_engine = IntelligentVisualizationEngine(openai_api_key=None)
    else:
        print("🧠 AI features enabled")
        intelligent_engine = IntelligentVisualizationEngine(openai_api_key=api_key)
    
    # Create sample data
    df = create_sample_sales_data()
    
    # Create smart dashboard
    print("\n🎛️  Creating smart dashboard...")
    dashboard = intelligent_engine.create_smart_dashboard(
        df, 
        business_category='sales',
        theme='business'
    )
    
    print(f"✅ Smart dashboard created with {dashboard['metadata']['total_charts']} charts")
    
    # Display dashboard information
    print("\n📊 Dashboard Components:")
    for i, chart in enumerate(dashboard.get('charts', []), 1):
        print(f"   {i}. {chart['title']}")
        print(f"      └─ Type: {chart['type']}")
        print(f"      └─ AI Explanation: {chart['ai_explanation'][:100]}...")
    
    # Show dashboard insights
    if dashboard.get('dashboard_insights'):
        insights = dashboard['dashboard_insights']
        print(f"\n🔍 Dashboard Insights:")
        print(f"   Overview: {insights.get('overview', 'N/A')[:100]}...")
        if 'recommended_actions' in insights:
            print(f"   Recommended Actions: {insights['recommended_actions'][:100]}...")
    
    # Test specialized dashboard
    if dashboard.get('specialized_dashboard'):
        print("\n🏢 Specialized Sales Dashboard: Created")
    else:
        print("\n🏢 Specialized Sales Dashboard: Not created (insufficient data patterns)")
    
    return intelligent_engine, dashboard


def demo_chart_templates():
    """Demonstrate chart templates"""
    print("\n" + "=" * 60)
    print("📋 DEMO: Chart Templates")
    print("=" * 60)
    
    # Create mock data for sales dashboard template
    print("🏪 Testing Sales Dashboard Template...")
    
    sample_revenue_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=12, freq='M'),
        'revenue': np.random.normal(100000, 20000, 12)
    })
    
    sample_regional_data = pd.DataFrame({
        'region': ['North', 'South', 'East', 'West'],
        'sales': [250000, 200000, 300000, 180000]
    })
    
    sample_product_data = pd.DataFrame({
        'product': ['Product A', 'Product B', 'Product C', 'Product D'],
        'revenue': [150000, 120000, 100000, 80000]
    })
    
    # Create template data
    template_data = {
        'revenue_over_time': sample_revenue_data,
        'sales_by_region': sample_regional_data,
        'product_performance': sample_product_data
    }
    
    # Generate dashboard template
    try:
        sales_dashboard = ChartTemplates.sales_dashboard_template(template_data)
        print("✅ Sales dashboard template created successfully")
        
        # Test theme application
        themed_dashboard = ChartStyling.apply_theme(sales_dashboard, 'business')
        print("✅ Business theme applied successfully")
        
    except Exception as e:
        print(f"❌ Template creation failed: {str(e)}")
    
    # Test color sequences
    print("\n🎨 Available Themes:")
    for theme in ['business', 'executive', 'presentation']:
        colors = ChartStyling.get_color_sequence(theme)
        print(f"   • {theme.title()}: {len(colors)} colors")


def demo_export_functionality():
    """Demonstrate export capabilities"""
    print("\n" + "=" * 60)
    print("💾 DEMO: Export Functionality")
    print("=" * 60)
    
    # Create sample data and basic dashboard
    df = create_sample_sales_data()
    viz_engine = VisualizationEngine()
    results = viz_engine.auto_visualize(df, max_charts=3)
    
    # Test export (simulated)
    print("📁 Export Options Available:")
    print("   • HTML (Interactive charts)")
    print("   • PNG (Static images)")
    print("   • PDF (Print-ready)")
    print("   • JSON (Chart configurations)")
    
    # Simulate export process
    charts = results.get('interactive_charts', [])
    if charts:
        print(f"\n💾 Ready to export {len(charts)} charts")
        print("   Example output structure:")
        print("   ├── chart_1_bar.html")
        print("   ├── chart_2_line.html")
        print("   ├── chart_3_pie.html")
        print("   └── dashboard_summary.json")
    else:
        print("\n⚠️  No charts available for export")


def main():
    """Run all visualization demos"""
    print("🚀 BI Assistant - Visualization Engine Demo")
    print("This demo showcases the visualization and charting capabilities")
    
    try:
        # Demo 1: Basic visualization
        viz_engine, basic_results = demo_basic_visualization()
        
        # Demo 2: Intelligent visualization
        intelligent_engine, dashboard = demo_intelligent_visualization()
        
        # Demo 3: Chart templates
        demo_chart_templates()
        
        # Demo 4: Export functionality
        demo_export_functionality()
        
        print("\n" + "=" * 60)
        print("✅ All visualization demos completed!")
        print("=" * 60)
        
        # Summary
        print("\n📊 Visualization Capabilities Summary:")
        print("   ✅ Automatic chart generation based on data types")
        print("   ✅ Interactive Plotly charts with hover effects")
        print("   ✅ Static matplotlib summaries and statistical views")
        print("   ✅ AI-enhanced chart explanations (with API key)")
        print("   ✅ Business-specific dashboard templates")
        print("   ✅ Consistent theming and styling")
        print("   ✅ Smart chart recommendations")
        print("   ✅ Export capabilities for multiple formats")
        
        print("\n🔗 Next Steps:")
        print("   • Set up OpenAI API key for AI-enhanced features")
        print("   • Try the web interface (coming next)")
        print("   • Upload your own datasets")
        print("   • Customize chart themes and templates")
        
        return {
            'basic_engine': viz_engine,
            'intelligent_engine': intelligent_engine,
            'dashboard': dashboard,
            'sample_data': create_sample_sales_data()
        }
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("This might be due to missing dependencies or configuration issues.")
        return None


if __name__ == "__main__":
    results = main()
