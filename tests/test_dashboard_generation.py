"""
Test Suite for Dashboard Generation Advanced Features
Tests dashboard builder, chart editor, and export functionality
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock

# Import components to test
from src.dashboard_builder import (
    DashboardTheme, ChartType, ChartConfig, DashboardConfig,
    DashboardTemplate, ChartGenerator, InteractiveDashboardBuilder
)
from src.chart_editor import (
    ColorScheme, ChartAnimation, ChartStyling, InteractiveChartEditor
)
from src.dashboard_exporter import DashboardExporter, ExportFormat


class TestDashboardBuilder:
    """Test dashboard builder functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        np.random.seed(42)
        return pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=100, freq='D'),
            'sales': np.random.normal(1000, 200, 100),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
            'product': np.random.choice(['A', 'B', 'C'], 100),
            'revenue': np.random.normal(5000, 1000, 100),
            'cost': np.random.normal(3000, 500, 100),
            'profit': lambda x: x['revenue'] - x['cost']
        })
    
    def test_chart_config_creation(self):
        """Test ChartConfig creation and validation"""
        config = ChartConfig(
            chart_id="test_123",
            chart_type=ChartType.LINE,
            title="Test Chart",
            x_column="date",
            y_column="sales"
        )
        
        assert config.chart_id == "test_123"
        assert config.chart_type == ChartType.LINE
        assert config.title == "Test Chart"
        assert config.x_column == "date"
        assert config.y_column == "sales"
        assert config.position['width'] == 6  # Default width
        assert config.position['height'] == 4  # Default height
    
    def test_dashboard_config_creation(self):
        """Test DashboardConfig creation"""
        chart_config = ChartConfig(
            chart_id="chart_1",
            chart_type=ChartType.BAR,
            title="Test Bar Chart"
        )
        
        dashboard_config = DashboardConfig(
            dashboard_id="dash_123",
            title="Test Dashboard",
            description="Test description",
            theme=DashboardTheme.BUSINESS,
            layout={'type': 'grid'},
            charts=[chart_config],
            filters=[],
            kpis=[],
            text_blocks=[],
            created_at=datetime.now(),
            modified_at=datetime.now()
        )
        
        assert dashboard_config.dashboard_id == "dash_123"
        assert dashboard_config.title == "Test Dashboard"
        assert dashboard_config.theme == DashboardTheme.BUSINESS
        assert len(dashboard_config.charts) == 1
        assert dashboard_config.charts[0].chart_id == "chart_1"
    
    def test_dashboard_templates_available(self):
        """Test that dashboard templates are available"""
        templates = DashboardTemplate.get_available_templates()
        
        assert isinstance(templates, dict)
        assert len(templates) > 0
        assert "executive_summary" in templates
        assert "sales_analytics" in templates
        assert "financial_dashboard" in templates
        
        # Check template structure
        exec_template = templates["executive_summary"]
        assert "name" in exec_template
        assert "description" in exec_template
        assert "category" in exec_template
        assert "charts" in exec_template
    
    def test_chart_generator_initialization(self, sample_data):
        """Test ChartGenerator initialization"""
        generator = ChartGenerator(sample_data)
        
        assert generator.data is not None
        assert len(generator.numeric_columns) > 0
        assert len(generator.categorical_columns) > 0
        assert len(generator.datetime_columns) > 0
        assert 'sales' in generator.numeric_columns
        assert 'region' in generator.categorical_columns
        assert 'date' in generator.datetime_columns
    
    def test_template_dashboard_creation(self, sample_data):
        """Test creating dashboard from template"""
        dashboard_config = DashboardTemplate.create_dashboard_from_template(
            "executive_summary", 
            sample_data, 
            DashboardTheme.BUSINESS
        )
        
        assert isinstance(dashboard_config, DashboardConfig)
        assert dashboard_config.title == "Executive Summary"
        assert dashboard_config.theme == DashboardTheme.BUSINESS
        assert len(dashboard_config.charts) > 0
        
        # Check that charts have valid configurations
        for chart in dashboard_config.charts:
            assert isinstance(chart, ChartConfig)
            assert chart.chart_id is not None
            assert chart.title is not None
            assert isinstance(chart.chart_type, ChartType)
    
    def test_chart_generation_for_sales_template(self, sample_data):
        """Test chart generation for sales analytics template"""
        generator = ChartGenerator(sample_data)
        charts = generator._generate_sales_charts()
        
        assert len(charts) > 0
        
        # Check that we have different chart types
        chart_types = [chart.chart_type for chart in charts]
        assert ChartType.LINE in chart_types or ChartType.BAR in chart_types
        
        # Verify charts have proper configurations
        for chart in charts:
            assert chart.chart_id is not None
            assert chart.title is not None
    
    def test_kpi_generation(self, sample_data):
        """Test KPI generation"""
        generator = ChartGenerator(sample_data)
        kpis = generator.generate_kpis_for_template("executive_summary")
        
        assert isinstance(kpis, list)
        if kpis:  # May be empty if no suitable columns
            for kpi in kpis:
                assert 'id' in kpi
                assert 'title' in kpi
                assert 'value' in kpi
                assert 'format' in kpi
    
    @patch('streamlit.session_state', new_callable=dict)
    def test_interactive_dashboard_builder_initialization(self, mock_session_state, sample_data):
        """Test InteractiveDashboardBuilder initialization"""
        builder = InteractiveDashboardBuilder(sample_data)
        
        assert builder.data is not None
        assert builder.visualizer is not None
        assert builder.chart_generator is not None
        
        # Check session state initialization
        assert 'dashboard_builder_state' in mock_session_state


class TestChartEditor:
    """Test chart editor functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        return pd.DataFrame({
            'x': range(10),
            'y': [i**2 for i in range(10)],
            'category': ['A', 'B'] * 5,
            'size': np.random.rand(10) * 100
        })
    
    @pytest.fixture
    def sample_chart_config(self):
        """Create sample chart config"""
        return ChartConfig(
            chart_id="test_chart",
            chart_type=ChartType.SCATTER,
            title="Test Scatter Plot",
            x_column="x",
            y_column="y",
            color_column="category",
            size_column="size"
        )
    
    def test_chart_styling_creation(self):
        """Test ChartStyling creation with defaults"""
        styling = ChartStyling()
        
        assert styling.color_scheme == ColorScheme.BUSINESS
        assert styling.background_color == "white"
        assert styling.title_font_size == 18
        assert styling.show_legend == True
        assert styling.animation == ChartAnimation.NONE
        assert isinstance(styling.custom_colors, list)
        assert isinstance(styling.annotations, list)
    
    def test_chart_styling_custom_creation(self):
        """Test ChartStyling creation with custom values"""
        styling = ChartStyling(
            color_scheme=ColorScheme.DARK,
            background_color="#2c3e50",
            title_font_size=24,
            show_legend=False,
            animation=ChartAnimation.FADE_IN
        )
        
        assert styling.color_scheme == ColorScheme.DARK
        assert styling.background_color == "#2c3e50"
        assert styling.title_font_size == 24
        assert styling.show_legend == False
        assert styling.animation == ChartAnimation.FADE_IN
    
    def test_interactive_chart_editor_initialization(self, sample_data):
        """Test InteractiveChartEditor initialization"""
        editor = InteractiveChartEditor(sample_data)
        
        assert editor.data is not None
        assert hasattr(editor, 'color_palettes')
        assert isinstance(editor.color_palettes, dict)
        assert len(editor.color_palettes) > 0
    
    def test_color_palette_retrieval(self, sample_data):
        """Test color palette functionality"""
        editor = InteractiveChartEditor(sample_data)
        
        # Test business colors
        business_colors = editor._get_colors_for_scheme(ColorScheme.BUSINESS, [])
        assert isinstance(business_colors, list)
        assert len(business_colors) > 0
        
        # Test custom colors
        custom_colors = ["#ff0000", "#00ff00", "#0000ff"]
        result_colors = editor._get_colors_for_scheme(ColorScheme.CUSTOM, custom_colors)
        assert result_colors == custom_colors
    
    def test_filter_application(self, sample_data):
        """Test data filter application"""
        editor = InteractiveChartEditor(sample_data)
        
        # Test range filter
        filters = {
            'x': {
                'type': 'range',
                'value': (2, 7)
            }
        }
        
        filtered_data = editor._apply_filters(sample_data, filters)
        assert len(filtered_data) < len(sample_data)
        assert filtered_data['x'].min() >= 2
        assert filtered_data['x'].max() <= 7
        
        # Test equals filter
        filters = {
            'category': {
                'type': 'in',
                'value': ['A']
            }
        }
        
        filtered_data = editor._apply_filters(sample_data, filters)
        assert all(filtered_data['category'] == 'A')
    
    def test_chart_creation_from_config(self, sample_data, sample_chart_config):
        """Test chart creation from configuration"""
        editor = InteractiveChartEditor(sample_data)
        
        chart = editor._create_base_chart(sample_chart_config, sample_data)
        
        assert chart is not None
        # Note: In real implementation, this would return a Plotly figure
        # For testing, we just ensure no exceptions are raised
    
    def test_styling_application(self, sample_data, sample_chart_config):
        """Test styling application to charts"""
        editor = InteractiveChartEditor(sample_data)
        styling = ChartStyling(
            color_scheme=ColorScheme.VIBRANT,
            title_font_size=20,
            show_grid=False
        )
        
        # Create a mock figure for testing
        mock_fig = Mock()
        mock_fig.update_layout = Mock()
        mock_fig.update_traces = Mock()
        mock_fig.update_xaxes = Mock()
        mock_fig.update_yaxes = Mock()
        
        styled_fig = editor._apply_styling(mock_fig, styling)
        
        # Verify styling methods were called
        mock_fig.update_layout.assert_called()
        mock_fig.update_xaxes.assert_called()
        mock_fig.update_yaxes.assert_called()


class TestDashboardExporter:
    """Test dashboard export functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        return pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=50),
            'value': np.random.randn(50),
            'category': np.random.choice(['A', 'B', 'C'], 50)
        })
    
    @pytest.fixture
    def sample_dashboard_config(self):
        """Create sample dashboard configuration"""
        chart = ChartConfig(
            chart_id="chart_1",
            chart_type=ChartType.LINE,
            title="Sample Chart",
            x_column="date",
            y_column="value"
        )
        
        return DashboardConfig(
            dashboard_id="dash_1",
            title="Sample Dashboard",
            description="Test dashboard for export",
            theme=DashboardTheme.BUSINESS,
            layout={'type': 'grid'},
            charts=[chart],
            filters=[],
            kpis=[],
            text_blocks=[],
            created_at=datetime.now(),
            modified_at=datetime.now()
        )
    
    def test_dashboard_exporter_initialization(self, sample_data):
        """Test DashboardExporter initialization"""
        exporter = DashboardExporter(sample_data)
        
        assert exporter.data is not None
        assert len(exporter.data) == len(sample_data)
    
    def test_html_dashboard_generation(self, sample_data, sample_dashboard_config):
        """Test HTML dashboard generation"""
        exporter = DashboardExporter(sample_data)
        
        html_content = exporter._generate_html_dashboard(
            sample_dashboard_config,
            {},
            include_interactive=True,
            include_filters=False,
            responsive_design=True,
            theme_style="Light",
            standalone_html=True
        )
        
        assert isinstance(html_content, str)
        assert "<!DOCTYPE html>" in html_content
        assert sample_dashboard_config.title in html_content
        assert "Sample Chart" in html_content
    
    def test_data_export_json(self, sample_data, sample_dashboard_config):
        """Test JSON data export"""
        exporter = DashboardExporter(sample_data)
        
        export_data = exporter._generate_data_export(
            sample_dashboard_config,
            "JSON",
            include_raw_data=True,
            include_processed_data=False,
            include_config=True,
            include_metadata=True,
            compress_output=False
        )
        
        assert export_data is not None
        
        # Parse the JSON to verify structure
        data_dict = json.loads(export_data.decode())
        assert 'data' in data_dict
        assert 'config' in data_dict
        assert 'metadata' in data_dict
    
    def test_data_export_csv(self, sample_data, sample_dashboard_config):
        """Test CSV data export"""
        exporter = DashboardExporter(sample_data)
        
        export_data = exporter._generate_data_export(
            sample_dashboard_config,
            "CSV",
            include_raw_data=True,
            include_processed_data=False,
            include_config=False,
            include_metadata=False,
            compress_output=False
        )
        
        assert export_data is not None
        
        # Verify CSV format
        csv_content = export_data.decode()
        lines = csv_content.strip().split('\n')
        assert len(lines) > 1  # Header + data
        assert 'date' in lines[0]  # Header contains column names
    
    def test_excel_export(self, sample_data, sample_dashboard_config):
        """Test Excel export functionality"""
        exporter = DashboardExporter(sample_data)
        
        export_data = exporter._generate_data_export(
            sample_dashboard_config,
            "Excel (XLSX)",
            include_raw_data=True,
            include_processed_data=False,
            include_config=True,
            include_metadata=False,
            compress_output=False
        )
        
        assert export_data is not None
        assert len(export_data) > 0
        
        # Verify it's valid Excel format (starts with ZIP signature)
        assert export_data.startswith(b'PK')
    
    def test_mime_type_detection(self, sample_data):
        """Test MIME type detection"""
        exporter = DashboardExporter(sample_data)
        
        assert exporter._get_mime_type('pdf') == 'application/pdf'
        assert exporter._get_mime_type('html') == 'text/html'
        assert exporter._get_mime_type('xlsx') == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert exporter._get_mime_type('csv') == 'text/csv'
        assert exporter._get_mime_type('json') == 'application/json'
        assert exporter._get_mime_type('zip') == 'application/zip'
        assert exporter._get_mime_type('unknown') == 'application/octet-stream'
    
    def test_executive_summary_generation(self, sample_data, sample_dashboard_config):
        """Test executive summary text generation"""
        exporter = DashboardExporter(sample_data)
        
        summary = exporter._generate_executive_summary(sample_dashboard_config)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert str(len(sample_dashboard_config.charts)) in summary
    
    def test_data_overview_generation(self, sample_data):
        """Test data overview text generation"""
        exporter = DashboardExporter(sample_data)
        
        overview = exporter._generate_data_overview_text()
        
        assert isinstance(overview, str)
        assert str(len(sample_data)) in overview
        assert str(len(sample_data.columns)) in overview
    
    @patch('tempfile.NamedTemporaryFile')
    @patch('os.unlink')
    def test_web_package_generation(self, mock_unlink, mock_tempfile, sample_data, sample_dashboard_config):
        """Test web package generation"""
        exporter = DashboardExporter(sample_data)
        
        package_data = exporter._generate_web_package(
            sample_dashboard_config,
            {},
            include_interactive=True,
            responsive_design=True
        )
        
        assert package_data is not None
        assert len(package_data) > 0
        
        # Verify it's a ZIP file (starts with ZIP signature)
        assert package_data.startswith(b'PK')


class TestIntegration:
    """Integration tests for dashboard generation features"""
    
    @pytest.fixture
    def comprehensive_data(self):
        """Create comprehensive test data"""
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=200, freq='D')
        
        return pd.DataFrame({
            'date': dates,
            'sales': np.random.normal(1000, 200, 200),
            'revenue': np.random.normal(5000, 1000, 200),
            'cost': np.random.normal(3000, 500, 200),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 200),
            'product': np.random.choice(['Product A', 'Product B', 'Product C'], 200),
            'channel': np.random.choice(['Online', 'Retail', 'Partner'], 200),
            'customer_satisfaction': np.random.uniform(1, 5, 200),
            'efficiency': np.random.uniform(0.7, 1.0, 200),
            'margin': lambda x: (x['revenue'] - x['cost']) / x['revenue']
        })
    
    def test_full_dashboard_creation_workflow(self, comprehensive_data):
        """Test complete dashboard creation workflow"""
        # Step 1: Create dashboard from template
        dashboard_config = DashboardTemplate.create_dashboard_from_template(
            "sales_analytics",
            comprehensive_data,
            DashboardTheme.MODERN
        )
        
        assert dashboard_config is not None
        assert len(dashboard_config.charts) > 0
        
        # Step 2: Create chart stylings
        chart_stylings = {}
        for chart in dashboard_config.charts:
            styling = ChartStyling(
                color_scheme=ColorScheme.VIBRANT,
                title_font_size=16,
                show_legend=True
            )
            chart_stylings[chart.chart_id] = styling
        
        # Step 3: Test export
        exporter = DashboardExporter(comprehensive_data)
        
        # Test HTML export
        html_export = exporter._generate_html_dashboard(
            dashboard_config,
            chart_stylings,
            include_interactive=True,
            include_filters=True,
            responsive_design=True,
            theme_style="Light",
            standalone_html=True
        )
        
        assert html_export is not None
        assert dashboard_config.title in html_export
        
        # Test data export
        json_export = exporter._generate_data_export(
            dashboard_config,
            "JSON",
            include_raw_data=True,
            include_processed_data=False,
            include_config=True,
            include_metadata=True,
            compress_output=False
        )
        
        assert json_export is not None
        
        # Verify JSON structure
        data_dict = json.loads(json_export.decode())
        assert 'data' in data_dict
        assert 'config' in data_dict
        assert len(data_dict['data']) == len(comprehensive_data)
    
    def test_chart_editor_workflow(self, comprehensive_data):
        """Test chart editor workflow"""
        # Create initial chart config
        chart_config = ChartConfig(
            chart_id="test_chart",
            chart_type=ChartType.LINE,
            title="Sales Trend",
            x_column="date",
            y_column="sales"
        )
        
        # Create editor
        editor = InteractiveChartEditor(comprehensive_data)
        
        # Test filter application
        filtered_data = editor._apply_filters(
            comprehensive_data,
            {
                'region': {'type': 'in', 'value': ['North', 'South']},
                'sales': {'type': 'range', 'value': (800, 1200)}
            }
        )
        
        assert len(filtered_data) < len(comprehensive_data)
        assert all(filtered_data['region'].isin(['North', 'South']))
        assert all((filtered_data['sales'] >= 800) & (filtered_data['sales'] <= 1200))
        
        # Test styling creation
        styling = ChartStyling(
            color_scheme=ColorScheme.OCEAN,
            background_color="#f8f9fa",
            title_font_size=20,
            show_grid=True,
            animation=ChartAnimation.FADE_IN
        )
        
        assert styling.color_scheme == ColorScheme.OCEAN
        assert styling.animation == ChartAnimation.FADE_IN
    
    def test_multiple_template_creation(self, comprehensive_data):
        """Test creating multiple dashboards from different templates"""
        templates = ["executive_summary", "sales_analytics", "financial_dashboard"]
        
        dashboards = []
        for template_name in templates:
            dashboard = DashboardTemplate.create_dashboard_from_template(
                template_name,
                comprehensive_data,
                DashboardTheme.BUSINESS
            )
            dashboards.append(dashboard)
        
        # Verify all dashboards were created
        assert len(dashboards) == 3
        
        # Verify each has different characteristics
        titles = [dash.title for dash in dashboards]
        assert len(set(titles)) == 3  # All unique titles
        
        # Verify charts were generated
        for dashboard in dashboards:
            assert len(dashboard.charts) > 0
            
            # Verify chart configurations are valid
            for chart in dashboard.charts:
                assert chart.chart_id is not None
                assert chart.title is not None
                assert isinstance(chart.chart_type, ChartType)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
