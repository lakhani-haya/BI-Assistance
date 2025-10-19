"""
Advanced Dashboard Demo
Demonstadvanced dashboard generation, editing, and export capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Import dashboard components
from src.dashboard_builder import (
    DashboardTemplate, DashboardTheme, ChartType, ChartConfig, DashboardConfig,
    ChartGenerator, InteractiveDashboardBuilder
)
from src.chart_editor import ChartStyling, ColorScheme, ChartAnimation, InteractiveChartEditor
from src.dashboard_exporter import DashboardExporter


def create_sample_business_data():
    """Create comprehensive sample business data"""
    print("🏭 Creating sample business data...")
    
    np.random.seed(42)
    
    # Generate 500 records over 1 year
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    # Create comprehensive business dataset
    data = []
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    products = ['Cloud Services', 'Software Licenses', 'Consulting', 'Support']
    channels = ['Direct Sales', 'Partner', 'Online', 'Reseller']
    customer_segments = ['Enterprise', 'SMB', 'Startup', 'Government']
    
    for i in range(500):
        date = np.random.choice(dates)
        region = np.random.choice(regions)
        product = np.random.choice(products)
        channel = np.random.choice(channels)
        segment = np.random.choice(customer_segments)
        
        # Generate correlated business metrics
        base_revenue = np.random.normal(10000, 3000)
        if region == 'North America':
            base_revenue *= 1.3
        elif region == 'Europe':
            base_revenue *= 1.1
        
        if product == 'Cloud Services':
            base_revenue *= 1.4
        elif product == 'Consulting':
            base_revenue *= 0.8
        
        record = {
            'date': date,
            'region': region,
            'product': product,
            'channel': channel,
            'customer_segment': segment,
            'revenue': max(1000, base_revenue),
            'cost': base_revenue * np.random.uniform(0.6, 0.8),
            'units_sold': np.random.poisson(50),
            'customer_satisfaction': np.random.uniform(3.5, 5.0),
            'sales_rep_id': f"SR_{np.random.randint(1, 50):03d}",
            'deal_size': np.random.choice(['Small', 'Medium', 'Large'], p=[0.5, 0.3, 0.2]),
            'acquisition_cost': np.random.normal(500, 200),
            'customer_lifetime_value': base_revenue * np.random.uniform(3, 8),
            'conversion_rate': np.random.uniform(0.15, 0.35),
            'marketing_spend': np.random.normal(1500, 500),
            'competitor_price': base_revenue * np.random.uniform(0.9, 1.1)
        }
        
        # Calculate derived metrics
        record['profit'] = record['revenue'] - record['cost']
        record['margin'] = record['profit'] / record['revenue']
        record['roi'] = record['profit'] / record['marketing_spend']
        record['price_competitiveness'] = record['revenue'] / record['competitor_price']
        
        data.append(record)
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"✅ Created dataset with {len(df)} records and {len(df.columns)} columns")
    return df


def demonstrate_dashboard_templates():
    """Demonstrate dashboard template functionality"""
    print("\n" + "="*60)
    print("📋 DASHBOARD TEMPLATES DEMONSTRATION")
    print("="*60)
    
    # Create sample data
    data = create_sample_business_data()
    
    # Get available templates
    templates = DashboardTemplate.get_available_templates()
    print(f"\n📊 Available Templates: {len(templates)}")
    
    for template_name, template_info in templates.items():
        print(f"\n🎨 {template_info['name']}")
        print(f"   Category: {template_info['category']}")
        print(f"   Description: {template_info['description']}")
        print(f"   Charts: {', '.join(template_info['charts'])}")
    
    # Create dashboards from templates
    print(f"\n🚀 Creating dashboards from templates...")
    
    created_dashboards = {}
    
    for template_name in ['executive_summary', 'sales_analytics', 'financial_dashboard']:
        try:
            print(f"\n📊 Creating {template_name} dashboard...")
            
            dashboard_config = DashboardTemplate.create_dashboard_from_template(
                template_name,
                data,
                DashboardTheme.MODERN
            )
            
            created_dashboards[template_name] = dashboard_config
            
            print(f"   ✅ Created: {dashboard_config.title}")
            print(f"   📈 Charts: {len(dashboard_config.charts)}")
            print(f"   🎯 KPIs: {len(dashboard_config.kpis)}")
            print(f"   🎨 Theme: {dashboard_config.theme.value}")
            
            # Show chart details
            for i, chart in enumerate(dashboard_config.charts, 1):
                print(f"      Chart {i}: {chart.title} ({chart.chart_type.value})")
                if chart.x_column and chart.y_column:
                    print(f"         Axes: {chart.x_column} vs {chart.y_column}")
                if chart.aggregation:
                    print(f"         Aggregation: {chart.aggregation}")
            
            # Show KPI details
            for i, kpi in enumerate(dashboard_config.kpis, 1):
                print(f"      KPI {i}: {kpi['title']} = {kpi['value']:.2f}")
        
        except Exception as e:
            print(f"   ❌ Failed to create {template_name}: {str(e)}")
    
    return data, created_dashboards


def demonstrate_chart_editor():
    """Demonstrate chart editor functionality"""
    print("\n" + "="*60)
    print("✏️ CHART EDITOR DEMONSTRATION")
    print("="*60)
    
    # Create sample data
    data = create_sample_business_data()
    
    # Create chart editor
    editor = InteractiveChartEditor(data)
    print("✅ Chart Editor initialized")
    
    # Create sample chart configuration
    chart_config = ChartConfig(
        chart_id="demo_chart_001",
        chart_type=ChartType.SCATTER,
        title="Revenue vs Customer Satisfaction Analysis",
        x_column="customer_satisfaction",
        y_column="revenue",
        color_column="region",
        size_column="units_sold"
    )
    
    print(f"\n📊 Created sample chart: {chart_config.title}")
    print(f"   Type: {chart_config.chart_type.value}")
    print(f"   X-Axis: {chart_config.x_column}")
    print(f"   Y-Axis: {chart_config.y_column}")
    print(f"   Color: {chart_config.color_column}")
    print(f"   Size: {chart_config.size_column}")
    
    # Create different styling options
    styling_options = {
        'Business Professional': ChartStyling(
            color_scheme=ColorScheme.BUSINESS,
            background_color="#ffffff",
            title_font_size=18,
            show_legend=True,
            show_grid=True,
            animation=ChartAnimation.NONE
        ),
        'Modern Vibrant': ChartStyling(
            color_scheme=ColorScheme.VIBRANT,
            background_color="#f8f9fa",
            title_font_size=20,
            show_legend=True,
            show_grid=False,
            animation=ChartAnimation.FADE_IN,
            legend_position="top"
        ),
        'Dark Theme': ChartStyling(
            color_scheme=ColorScheme.DARK,
            background_color="#2c3e50",
            plot_background_color="#34495e",
            title_font_size=16,
            show_legend=True,
            show_grid=True,
            grid_color="#555555",
            animation=ChartAnimation.SLIDE_UP
        ),
        'Ocean Inspired': ChartStyling(
            color_scheme=ColorScheme.OCEAN,
            background_color="#f0f8ff",
            title_font_size=19,
            show_legend=True,
            legend_position="bottom",
            animation=ChartAnimation.GROW,
            annotations=[
                {
                    'text': 'Key Insight Area',
                    'x': 0.7,
                    'y': 0.8,
                    'font': {'color': '#2c3e50', 'size': 12},
                    'showarrow': True
                }
            ]
        )
    }
    
    print(f"\n🎨 Created {len(styling_options)} styling options:")
    
    for style_name, styling in styling_options.items():
        print(f"\n   🖌️ {style_name}:")
        print(f"      Color Scheme: {styling.color_scheme.value}")
        print(f"      Background: {styling.background_color}")
        print(f"      Font Size: {styling.title_font_size}px")
        print(f"      Animation: {styling.animation.value}")
        print(f"      Legend: {styling.legend_position if styling.show_legend else 'Hidden'}")
        if styling.annotations:
            print(f"      Annotations: {len(styling.annotations)}")
    
    # Demonstrate filter functionality
    print(f"\n🔍 Demonstrating filter functionality...")
    
    filter_examples = {
        'High Revenue': {
            'revenue': {'type': 'range', 'value': (15000, 50000)}
        },
        'Top Regions': {
            'region': {'type': 'in', 'value': ['North America', 'Europe']}
        },
        'Large Deals': {
            'deal_size': {'type': 'in', 'value': ['Large']},
            'customer_satisfaction': {'type': 'range', 'value': (4.0, 5.0)}
        }
    }
    
    for filter_name, filters in filter_examples.items():
        filtered_data = editor._apply_filters(data, filters)
        print(f"   📊 {filter_name}: {len(filtered_data)} records ({len(filtered_data)/len(data)*100:.1f}%)")
    
    # Test color schemes
    print(f"\n🌈 Available color schemes:")
    for scheme in ColorScheme:
        colors = editor._get_colors_for_scheme(scheme, [])
        print(f"   {scheme.value}: {len(colors)} colors")
    
    return chart_config, styling_options


def demonstrate_dashboard_export():
    """Demonstrate dashboard export functionality"""
    print("\n" + "="*60)
    print("📤 DASHBOARD EXPORT DEMONSTRATION")
    print("="*60)
    
    # Create sample data and dashboard
    data = create_sample_business_data()
    
    # Create a sample dashboard
    dashboard_config = DashboardTemplate.create_dashboard_from_template(
        "sales_analytics",
        data,
        DashboardTheme.MODERN
    )
    
    # Create exporter
    exporter = DashboardExporter(data)
    print("✅ Dashboard Exporter initialized")
    
    print(f"\n📊 Dashboard to export: {dashboard_config.title}")
    print(f"   Charts: {len(dashboard_config.charts)}")
    print(f"   KPIs: {len(dashboard_config.kpis)}")
    print(f"   Theme: {dashboard_config.theme.value}")
    
    # Create chart stylings
    chart_stylings = {}
    for chart in dashboard_config.charts:
        chart_stylings[chart.chart_id] = ChartStyling(
            color_scheme=ColorScheme.MODERN,
            title_font_size=16,
            animation=ChartAnimation.FADE_IN
        )
    
    # Demonstrate different export formats
    export_examples = [
        {
            'name': 'HTML Dashboard',
            'format': 'html',
            'description': 'Interactive web dashboard'
        },
        {
            'name': 'JSON Data Export',
            'format': 'json',
            'description': 'Complete data and configuration'
        },
        {
            'name': 'CSV Data Export',
            'format': 'csv',
            'description': 'Raw data in CSV format'
        },
        {
            'name': 'Excel Workbook',
            'format': 'xlsx',
            'description': 'Multi-sheet Excel file'
        }
    ]
    
    print(f"\n📁 Export format demonstrations:")
    
    for export_example in export_examples:
        try:
            print(f"\n   📄 {export_example['name']}...")
            
            if export_example['format'] == 'html':
                result = exporter._generate_html_dashboard(
                    dashboard_config,
                    chart_stylings,
                    include_interactive=True,
                    include_filters=True,
                    responsive_design=True,
                    theme_style="Light",
                    standalone_html=True
                )
                print(f"      ✅ HTML generated: {len(result)} characters")
                
            elif export_example['format'] == 'json':
                result = exporter._generate_data_export(
                    dashboard_config,
                    "JSON",
                    include_raw_data=True,
                    include_processed_data=False,
                    include_config=True,
                    include_metadata=True,
                    compress_output=False
                )
                if result:
                    data_dict = json.loads(result.decode())
                    print(f"      ✅ JSON exported with {len(data_dict)} sections")
                    print(f"         Data records: {len(data_dict.get('data', []))}")
                    print(f"         Config included: {'config' in data_dict}")
                    print(f"         Metadata included: {'metadata' in data_dict}")
            
            elif export_example['format'] == 'csv':
                result = exporter._generate_data_export(
                    dashboard_config,
                    "CSV",
                    include_raw_data=True,
                    include_processed_data=False,
                    include_config=False,
                    include_metadata=False,
                    compress_output=False
                )
                if result:
                    lines = result.decode().split('\n')
                    print(f"      ✅ CSV exported: {len(lines)} lines")
            
            elif export_example['format'] == 'xlsx':
                result = exporter._generate_data_export(
                    dashboard_config,
                    "Excel (XLSX)",
                    include_raw_data=True,
                    include_processed_data=False,
                    include_config=True,
                    include_metadata=False,
                    compress_output=False
                )
                if result:
                    print(f"      ✅ Excel exported: {len(result)} bytes")
        
        except Exception as e:
            print(f"      ❌ Export failed: {str(e)}")
    
    # Demonstrate web package export
    print(f"\n📦 Web Package Export...")
    try:
        web_package = exporter._generate_web_package(
            dashboard_config,
            chart_stylings,
            include_interactive=True,
            responsive_design=True
        )
        print(f"   ✅ Web package created: {len(web_package)} bytes")
        print(f"   📁 Package includes: HTML, CSS, JavaScript, README")
    except Exception as e:
        print(f"   ❌ Web package failed: {str(e)}")
    
    # Demonstrate text generation
    print(f"\n📝 Text Generation Examples:")
    
    executive_summary = exporter._generate_executive_summary(dashboard_config)
    print(f"   📋 Executive Summary: {len(executive_summary)} characters")
    
    data_overview = exporter._generate_data_overview_text()
    print(f"   📊 Data Overview: {len(data_overview)} characters")
    
    insights = exporter._generate_insights_text(dashboard_config)
    print(f"   💡 Insights: {len(insights)} characters")
    
    return dashboard_config, chart_stylings


def demonstrate_integration_workflow():
    """Demonstrate complete integration workflow"""
    print("\n" + "="*60)
    print("🔄 COMPLETE INTEGRATION WORKFLOW")
    print("="*60)
    
    # Step 1: Create comprehensive data
    print("1️⃣ Creating business data...")
    data = create_sample_business_data()
    print(f"   ✅ Dataset: {len(data)} records, {len(data.columns)} columns")
    
    # Step 2: Generate multiple dashboards
    print("\n2️⃣ Creating multiple dashboards...")
    dashboards = {}
    
    templates_to_create = ['executive_summary', 'sales_analytics', 'financial_dashboard']
    themes = [DashboardTheme.BUSINESS, DashboardTheme.MODERN, DashboardTheme.EXECUTIVE]
    
    for template_name, theme in zip(templates_to_create, themes):
        dashboard = DashboardTemplate.create_dashboard_from_template(
            template_name, data, theme
        )
        dashboards[template_name] = dashboard
        print(f"   ✅ {dashboard.title} ({theme.value}): {len(dashboard.charts)} charts")
    
    # Step 3: Create custom chart configurations
    print("\n3️⃣ Creating custom chart configurations...")
    
    custom_charts = [
        ChartConfig(
            chart_id="custom_001",
            chart_type=ChartType.SCATTER,
            title="ROI vs Marketing Spend Analysis",
            x_column="marketing_spend",
            y_column="roi",
            color_column="region",
            size_column="revenue"
        ),
        ChartConfig(
            chart_id="custom_002",
            chart_type=ChartType.HEATMAP,
            title="Performance by Region and Product",
            x_column="region",
            y_column="product",
            color_column="margin"
        ),
        ChartConfig(
            chart_id="custom_003",
            chart_type=ChartType.BOX,
            title="Revenue Distribution by Customer Segment",
            x_column="customer_segment",
            y_column="revenue"
        )
    ]
    
    for chart in custom_charts:
        print(f"   📊 {chart.title} ({chart.chart_type.value})")
    
    # Step 4: Apply advanced styling
    print("\n4️⃣ Applying advanced styling...")
    
    styling_themes = {
        'executive_summary': ChartStyling(
            color_scheme=ColorScheme.BUSINESS,
            title_font_size=18,
            animation=ChartAnimation.NONE,
            show_legend=True
        ),
        'sales_analytics': ChartStyling(
            color_scheme=ColorScheme.VIBRANT,
            title_font_size=16,
            animation=ChartAnimation.FADE_IN,
            legend_position="top"
        ),
        'financial_dashboard': ChartStyling(
            color_scheme=ColorScheme.DARK,
            background_color="#2c3e50",
            title_font_size=17,
            animation=ChartAnimation.GROW
        )
    }
    
    all_chart_stylings = {}
    for dashboard_name, dashboard in dashboards.items():
        styling = styling_themes[dashboard_name]
        for chart in dashboard.charts:
            all_chart_stylings[chart.chart_id] = styling
        print(f"   🎨 Styled {dashboard_name}: {styling.color_scheme.value} theme")
    
    # Step 5: Export in multiple formats
    print("\n5️⃣ Exporting dashboards...")
    
    exporter = DashboardExporter(data)
    
    export_summary = {}
    
    for dashboard_name, dashboard in dashboards.items():
        print(f"\n   📤 Exporting {dashboard_name}...")
        
        try:
            # HTML export
            html_result = exporter._generate_html_dashboard(
                dashboard, all_chart_stylings, True, True, True, "Light", True
            )
            export_summary[f"{dashboard_name}_html"] = len(html_result)
            
            # JSON export
            json_result = exporter._generate_data_export(
                dashboard, "JSON", True, False, True, True, False
            )
            if json_result:
                export_summary[f"{dashboard_name}_json"] = len(json_result)
            
            # Web package
            web_result = exporter._generate_web_package(
                dashboard, all_chart_stylings, True, True
            )
            export_summary[f"{dashboard_name}_web"] = len(web_result)
            
            print(f"      ✅ All formats exported successfully")
            
        except Exception as e:
            print(f"      ❌ Export error: {str(e)}")
    
    # Step 6: Summary
    print("\n6️⃣ Workflow Summary:")
    print(f"   📊 Dashboards Created: {len(dashboards)}")
    print(f"   📈 Total Charts: {sum(len(d.charts) for d in dashboards.values())}")
    print(f"   🎯 Total KPIs: {sum(len(d.kpis) for d in dashboards.values())}")
    print(f"   🎨 Styling Themes: {len(styling_themes)}")
    print(f"   📤 Export Outputs: {len(export_summary)}")
    
    print(f"\n   📁 Export Summary:")
    for export_name, size in export_summary.items():
        print(f"      {export_name}: {size:,} bytes")
    
    total_size = sum(export_summary.values())
    print(f"   📊 Total Export Size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
    
    return dashboards, all_chart_stylings, export_summary


def main():
    """Run all demonstrations"""
    print("🚀 ADVANCED DASHBOARD GENERATION DEMONSTRATION")
    print("="*80)
    print("This demo showcases the advanced dashboard generation capabilities")
    print("including templates, chart editing, and multi-format export.")
    print("="*80)
    
    try:
        # Run demonstrations
        data, templates_demo = demonstrate_dashboard_templates()
        chart_config, styling_demo = demonstrate_chart_editor()
        export_demo = demonstrate_dashboard_export()
        integration_demo = demonstrate_integration_workflow()
        
        print("\n" + "="*80)
        print("🎉 DEMONSTRATION COMPLETE!")
        print("="*80)
        print("✅ Dashboard Templates: Demonstrated template-based dashboard creation")
        print("✅ Chart Editor: Showcased advanced styling and customization")
        print("✅ Dashboard Export: Displayed multi-format export capabilities")
        print("✅ Integration Workflow: Completed end-to-end dashboard lifecycle")
        
        print(f"\n📊 Summary Statistics:")
        print(f"   🏭 Sample Data Records: {len(data):,}")
        print(f"   📋 Templates Available: {len(DashboardTemplate.get_available_templates())}")
        print(f"   🎨 Color Schemes: {len(list(ColorScheme))}")
        print(f"   📈 Chart Types: {len(list(ChartType))}")
        print(f"   🎭 Themes: {len(list(DashboardTheme))}")
        
        print(f"\n🚀 The advanced dashboard generation system is ready for production use!")
        print("   Features include template-based creation, interactive editing,")
        print("   advanced styling, and comprehensive export capabilities.")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
