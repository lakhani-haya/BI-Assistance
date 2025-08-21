"""
User Guide and Documentation Generator
Creates comprehensive documentation for the BI Assistant
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import streamlit as st


class DocumentationGenerator:
    """Generate comprehensive user documentation"""
    
    def __init__(self):
        """Initialize documentation generator"""
        self.docs_sections = {
            'getting_started': self._generate_getting_started,
            'data_upload': self._generate_data_upload_guide,
            'analysis_features': self._generate_analysis_guide,
            'dashboard_creation': self._generate_dashboard_guide,
            'ai_insights': self._generate_ai_insights_guide,
            'export_options': self._generate_export_guide,
            'troubleshooting': self._generate_troubleshooting,
            'api_reference': self._generate_api_reference
        }
    
    def _generate_getting_started(self) -> str:
        """Generate getting started guide"""
        return """
# 🚀 Getting Started with BI Assistant

## What is BI Assistant?

BI Assistant is an intelligent data analysis tool that transforms raw data into actionable business insights using AI-powered analytics, automated visualizations, and natural language explanations.

## Key Features

### 📊 **Automated Data Analysis**
- Upload CSV/Excel files and get instant statistical analysis
- Automatic data quality assessment and cleaning suggestions
- Smart column type detection and handling of missing values

### 🤖 **AI-Powered Insights**
- Natural language explanations of data patterns and trends
- Interactive Q&A - ask questions about your data in plain English
- Business opportunity identification and performance diagnosis
- 6 different storytelling modes for various audiences

### 📈 **Interactive Visualizations**
- 15+ chart types with automatic recommendations
- Professional dashboard templates for different business domains
- Interactive chart editor with advanced customization options
- Real-time data filtering and dynamic updates

### 🎨 **Professional Dashboards**
- Template-based dashboard creation (Sales, Finance, Operations, Marketing, etc.)
- Drag-and-drop interface for custom dashboard building
- Export to PDF, PowerPoint, HTML, and image formats
- Mobile-responsive design for any device

## Quick Start (5 Minutes)

### Step 1: Launch the Application
```bash
# Option 1: Use the launcher script
python run_dashboard.py

# Option 2: Direct Streamlit command  
streamlit run src/dashboard.py
```

### Step 2: Upload Your Data
1. Use the **sidebar** to upload a CSV or Excel file
2. Or click **"Load Sample Data"** to try with demo datasets
3. Configure analysis options (business domain, theme, etc.)

### Step 3: Run Analysis
1. Click **"🚀 Run Analysis"** 
2. Wait for automated processing (usually 10-30 seconds)
3. Review data quality assessment and statistics

### Step 4: Explore Results
- **📊 Overview**: Data summary and quality metrics
- **🔍 Analysis**: Detailed statistical insights and AI explanations  
- **📈 Visualizations**: Interactive charts and graphs
- **🎨 Dashboard Builder**: Create professional dashboards
- **🤖 AI Insights**: Natural language Q&A and storytelling
- **📤 Export**: Download results in various formats

## First Analysis Checklist

- [ ] Data uploaded successfully (green checkmark in sidebar)
- [ ] Business domain selected (Sales, Finance, Operations, etc.)
- [ ] Analysis completed without errors
- [ ] Key insights make sense for your business context
- [ ] Visualizations are relevant and accurate
- [ ] AI insights provide valuable business recommendations

## Need Help?

- Check the **Troubleshooting** section for common issues
- Use the **🤖 AI Insights** tab to ask specific questions about your data
- Review sample datasets to understand expected data formats
- Contact support for technical assistance

---
*Ready to transform your data into insights? Let's get started!* 🎯
"""
    
    def _generate_data_upload_guide(self) -> str:
        """Generate data upload guide"""
        return """
# 📁 Data Upload Guide

## Supported File Formats

### ✅ **Recommended Formats**
- **CSV (.csv)**: Comma-separated values - most reliable
- **Excel (.xlsx)**: Modern Excel format with multiple sheets
- **Excel (.xls)**: Legacy Excel format

### 📊 **Data Requirements**

#### **Structure Guidelines**
- **Headers Required**: First row should contain column names
- **Consistent Data Types**: Each column should have consistent data (all numbers, all dates, etc.)
- **No Merged Cells**: Avoid merged cells in Excel files
- **No Empty Rows**: Remove empty rows between data

#### **Size Limits**
- **Maximum File Size**: 50MB (configurable)
- **Recommended Rows**: Up to 100,000 rows for optimal performance
- **Columns**: Up to 50 columns for best visualization experience

## Step-by-Step Upload Process

### Step 1: Prepare Your Data
```
✅ Good Example:
Date,Product,Sales,Region,Customer_Satisfaction
2024-01-01,Widget A,1500,North,4.2
2024-01-02,Widget B,2300,South,4.8
2024-01-03,Widget A,1800,East,4.1

❌ Avoid:
- Missing headers
- Inconsistent date formats
- Mixed data types in columns
- Special characters in column names
```

### Step 2: Upload File
1. **Locate Upload Section**: Look for "📁 Upload Data" in the sidebar
2. **Choose File**: Click "Browse files" or drag and drop
3. **Wait for Processing**: File will be validated and processed
4. **Confirm Success**: Green checkmark indicates successful upload

### Step 3: Review Data Preview
- **Data Types**: Check that columns are correctly identified
- **Missing Values**: Review any missing data highlighted
- **Sample Rows**: Verify data looks correct in preview
- **Column Statistics**: Review basic statistics for each column

## Data Types and Handling

### 📅 **Date Columns**
- **Supported Formats**: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY
- **Automatic Detection**: System will try to auto-detect date columns
- **Time Series Analysis**: Date columns enable time-based insights

### 🔢 **Numeric Columns**
- **Integers**: Whole numbers (sales quantities, counts)
- **Floats**: Decimal numbers (prices, ratings, percentages)
- **Currency**: Will be treated as numeric (remove currency symbols)

### 📝 **Text/Categorical Columns**
- **Categories**: Product names, regions, customer segments
- **IDs**: Customer IDs, order numbers (treated as categories)
- **Descriptions**: Free text fields (limited analysis available)

### ✅ **Boolean Columns**
- **True/False**: Binary indicators
- **Yes/No**: Converted to boolean
- **1/0**: Numeric boolean representation

## Common Data Issues and Solutions

### 🔧 **Missing Values**
- **Detection**: Automatically identified and highlighted
- **Options**: Exclude, fill with average, fill with most common value
- **Recommendation**: Review missing data patterns before analysis

### 🔧 **Inconsistent Formats**
- **Dates**: Standardize date format across all rows
- **Numbers**: Remove commas, currency symbols, percentage signs
- **Text**: Consistent capitalization and spelling

### 🔧 **Large Files**
- **Sampling**: System may sample large datasets for performance
- **Optimization**: Remove unnecessary columns before upload
- **Chunking**: Consider splitting very large files

## Sample Datasets

Try these sample datasets to explore features:

### 🛒 **Sales Data Sample**
- Monthly sales by product and region
- Includes customer satisfaction scores
- Perfect for revenue analysis and forecasting

### 💰 **Financial Data Sample**  
- Quarterly financial metrics
- Budget vs actual comparisons
- Ideal for financial performance analysis

### 👥 **Customer Data Sample**
- Customer demographics and behavior
- Purchase history and preferences
- Great for customer segmentation analysis

### 📈 **Marketing Data Sample**
- Campaign performance metrics
- Multi-channel attribution data
- Excellent for marketing ROI analysis

## Advanced Upload Options

### ⚙️ **File Processing Settings**
- **Encoding**: UTF-8 (default), Windows-1252, ISO-8859-1
- **Delimiter**: Comma (default), semicolon, tab
- **Quote Character**: Double quote (default), single quote
- **Skip Rows**: Skip header rows if needed

### 🔍 **Data Validation**
- **Automatic Validation**: File structure and format checks
- **Quality Assessment**: Data completeness and consistency scores
- **Recommendations**: Suggestions for improving data quality

## Best Practices

### ✅ **Do's**
- Use descriptive column names (Sales_Amount vs Col1)
- Maintain consistent data formats within columns
- Include date columns for time-based analysis
- Remove or document any unusual values or outliers
- Test with a small sample file first

### ❌ **Don'ts**
- Don't include totals or summary rows in the data
- Avoid special characters in column names (use underscores)
- Don't mix different units in the same column
- Avoid empty columns or rows
- Don't include sensitive personal information

---
*Need help with your specific data format? Use the 🤖 AI Insights feature to ask questions!*
"""
    
    def _generate_analysis_guide(self) -> str:
        """Generate analysis features guide"""
        return """
# 🔍 Analysis Features Guide

## Automated Statistical Analysis

### 📊 **Descriptive Statistics**
The system automatically calculates comprehensive statistics for all numeric columns:

- **Central Tendency**: Mean, median, mode
- **Variability**: Standard deviation, variance, range
- **Distribution Shape**: Skewness, kurtosis, percentiles
- **Data Quality**: Missing values, outliers, duplicates

### 📈 **Trend Analysis**
For time-series data, automatic trend detection includes:

- **Growth Rates**: Period-over-period changes
- **Seasonality**: Recurring patterns and cycles
- **Trend Direction**: Increasing, decreasing, or stable trends
- **Anomaly Detection**: Unusual spikes or drops in data

### 🔗 **Correlation Analysis**
Identifies relationships between variables:

- **Correlation Matrix**: Strength of relationships between all numeric variables
- **Key Insights**: Strongest positive and negative correlations
- **Business Implications**: What correlations mean for your business
- **Visualization**: Correlation heatmaps and scatter plots

## Business Domain Intelligence

### 🛒 **Sales Analytics**
Specialized analysis for sales data:

- **Revenue Trends**: Sales performance over time
- **Product Performance**: Top and bottom performing products
- **Regional Analysis**: Geographic sales distribution
- **Customer Segmentation**: High, medium, and low value customers
- **Forecasting**: Predictive sales projections

### 💰 **Financial Analytics**
Financial performance insights:

- **Profitability Analysis**: Margins and cost analysis
- **Budget Variance**: Actual vs planned performance
- **Cash Flow Patterns**: Revenue and expense trends
- **Financial Ratios**: Key performance indicators
- **Risk Assessment**: Financial health indicators

### ⚙️ **Operations Analytics**
Operational efficiency analysis:

- **Process Performance**: Efficiency metrics and bottlenecks
- **Quality Metrics**: Error rates and quality scores
- **Resource Utilization**: Capacity and utilization analysis
- **Productivity Trends**: Output and efficiency over time
- **Cost Optimization**: Cost reduction opportunities

### 📢 **Marketing Analytics**
Marketing campaign effectiveness:

- **Campaign ROI**: Return on marketing investment
- **Channel Performance**: Multi-channel attribution analysis
- **Customer Acquisition**: Cost and conversion metrics
- **Engagement Analysis**: Customer interaction patterns
- **A/B Testing**: Comparative campaign performance

## AI-Powered Insights

### 🤖 **Natural Language Explanations**
AI generates business-friendly explanations:

- **Pattern Recognition**: What trends and patterns exist in your data
- **Business Context**: Why these patterns matter for your business
- **Action Items**: Specific recommendations based on findings
- **Risk Alerts**: Potential issues or concerns identified
- **Opportunity Identification**: Areas for improvement or growth

### 💬 **Interactive Q&A**
Ask questions about your data in plain English:

```
Example Questions:
• "What are the main drivers of customer satisfaction?"
• "Which products have the highest profit margins?"
• "How has performance changed over the last quarter?"
• "What factors correlate with high sales?"
• "Are there any seasonal patterns in the data?"
```

### 📖 **Data Storytelling**
AI creates comprehensive narratives:

- **Executive Summary**: High-level insights for leadership
- **Detailed Analysis**: Comprehensive findings for analysts
- **Problem-Solution**: Issue identification and recommendations
- **Opportunity Focus**: Growth and optimization opportunities

## Advanced Analysis Features

### 🔍 **Outlier Detection**
Identifies unusual data points:

- **Statistical Outliers**: Values outside normal ranges
- **Business Context**: Why outliers might occur
- **Impact Assessment**: How outliers affect overall analysis
- **Recommendations**: Whether to investigate or exclude outliers

### 📊 **Segmentation Analysis**
Automatic grouping and classification:

- **Customer Segments**: Based on behavior and characteristics
- **Product Categories**: Performance-based groupings
- **Geographic Regions**: Location-based analysis
- **Time Periods**: Comparative analysis across different periods

### 🎯 **Performance Benchmarking**
Compare against standards:

- **Industry Benchmarks**: How you compare to industry standards
- **Historical Performance**: Trends compared to past performance
- **Goal Achievement**: Progress toward targets and objectives
- **Peer Comparison**: Performance relative to similar organizations

## Quality Assessment

### ✅ **Data Quality Metrics**
Comprehensive data quality evaluation:

- **Completeness**: Percentage of missing values
- **Consistency**: Uniform formatting and standards
- **Accuracy**: Reasonable values and ranges
- **Uniqueness**: Duplicate record identification
- **Validity**: Data conforms to expected formats

### 🔧 **Data Cleaning Recommendations**
Automated suggestions for data improvement:

- **Missing Value Treatment**: Fill, interpolate, or exclude options
- **Outlier Handling**: Investigation or exclusion recommendations
- **Format Standardization**: Consistent date, number, and text formats
- **Duplicate Resolution**: Merge or remove duplicate records

## Customization Options

### ⚙️ **Analysis Configuration**
Customize analysis parameters:

- **Confidence Levels**: Statistical significance thresholds
- **Time Periods**: Focus on specific date ranges
- **Filters**: Include/exclude specific data segments
- **Aggregation**: Daily, weekly, monthly, or custom groupings

### 🎨 **Visualization Preferences**
Control chart generation:

- **Chart Types**: Preferred visualization styles
- **Color Schemes**: Corporate branding or accessibility themes
- **Layout Options**: Single charts or dashboard layouts
- **Export Formats**: Image, PDF, or interactive options

## Performance Optimization

### ⚡ **Large Dataset Handling**
Efficient processing for big data:

- **Intelligent Sampling**: Representative data samples for faster analysis
- **Chunked Processing**: Memory-efficient handling of large files
- **Progressive Analysis**: Incremental results as processing continues
- **Performance Monitoring**: Real-time processing status and metrics

---
*The analysis engine continuously learns and improves. Your feedback helps make insights more accurate and relevant!*
"""
    
    def _generate_dashboard_guide(self) -> str:
        """Generate dashboard creation guide"""
        return """
# 🎨 Dashboard Creation Guide

## Dashboard Builder Overview

The Dashboard Builder provides professional-grade dashboard creation with templates, custom layouts, and interactive features.

## Quick Dashboard Creation

### 🚀 **Template-Based Dashboards (5 minutes)**

#### Step 1: Choose a Template
Select from 6 professional templates:

- **📊 Sales Analytics**: Revenue trends, product performance, regional analysis
- **💰 Financial Overview**: P&L visualization, budget tracking, financial KPIs
- **⚙️ Operations Dashboard**: Process metrics, efficiency tracking, quality indicators
- **📢 Marketing Performance**: Campaign ROI, channel analysis, conversion funnels
- **👥 Customer Analytics**: Segmentation, satisfaction, retention metrics
- **📋 Executive Summary**: High-level KPIs for leadership overview

#### Step 2: Customize Content
- **Auto-Population**: Template automatically maps your data to relevant charts
- **Chart Selection**: Modify which charts to include
- **Data Mapping**: Adjust which columns feed into each visualization
- **Filters**: Add interactive filtering options

#### Step 3: Style and Export
- **Theme Selection**: Choose from professional color schemes
- **Layout Adjustment**: Modify chart sizes and positions
- **Export Options**: PDF, PowerPoint, HTML, or image formats

### 🛠️ **Custom Dashboard Creation (15 minutes)**

#### Step 1: Start from Scratch
1. Select **"Custom Dashboard"** option
2. Choose base layout (2x2, 3x2, 4x3, or flexible grid)
3. Name your dashboard and set description

#### Step 2: Add Charts
1. **Chart Type Selection**: Choose from 15+ visualization types
2. **Data Mapping**: Select columns for X-axis, Y-axis, grouping, etc.
3. **Chart Configuration**: Set titles, labels, and basic styling
4. **Position Placement**: Drag and drop to desired location

#### Step 3: Advanced Customization
1. **Interactive Features**: Enable filtering, zooming, hover details
2. **Advanced Styling**: Custom colors, fonts, and branding
3. **Responsive Design**: Ensure mobile compatibility
4. **Performance Optimization**: Optimize for large datasets

## Chart Types and Best Uses

### 📈 **Time Series Charts**
**Best for**: Trends over time, forecasting, seasonal analysis

- **Line Charts**: Continuous trends and patterns
- **Area Charts**: Volume and accumulation over time  
- **Bar Charts (Time)**: Discrete time periods and comparisons
- **Candlestick**: Financial data with OHLC values

**Data Requirements**:
- Date/time column
- One or more numeric metrics
- Consistent time intervals

### 📊 **Comparison Charts**
**Best for**: Category comparisons, ranking, performance gaps

- **Bar Charts**: Category comparisons and rankings
- **Column Charts**: Vertical comparisons with many categories
- **Horizontal Bar**: Long category names or narrow layouts
- **Grouped Bar**: Multiple metrics per category

**Data Requirements**:
- Categorical column (products, regions, etc.)
- One or more numeric metrics
- Clear category distinctions

### 🥧 **Composition Charts**
**Best for**: Parts of a whole, market share, budget allocation

- **Pie Charts**: Simple proportions (max 5-7 categories)
- **Donut Charts**: Proportions with central metric display
- **Stacked Bar**: Composition over categories or time
- **Treemap**: Hierarchical proportions and nested categories

**Data Requirements**:
- Categorical grouping column
- Numeric values that sum to meaningful total
- Limited number of categories for clarity

### 🔗 **Relationship Charts**
**Best for**: Correlations, clustering, outlier detection

- **Scatter Plots**: Two-variable relationships and correlations
- **Bubble Charts**: Three-variable relationships with size encoding
- **Correlation Matrix**: Multiple variable relationships
- **Heatmaps**: Intensity mapping across two dimensions

**Data Requirements**:
- Two or more numeric columns
- Sufficient data points for pattern recognition
- Meaningful relationships between variables

### 📍 **Geographic Charts**
**Best for**: Location-based analysis, regional performance

- **Choropleth Maps**: Regional performance with color intensity
- **Scatter Maps**: Point locations with metric sizing
- **Flow Maps**: Movement and connections between locations

**Data Requirements**:
- Geographic identifiers (country, state, city, coordinates)
- Numeric metrics for visualization
- Proper geographic data format

## Dashboard Layout Best Practices

### 📐 **Visual Hierarchy**
- **Top-Left Priority**: Place most important metrics top-left
- **F-Pattern Layout**: Follow natural reading patterns
- **Size Indicates Importance**: Larger charts for key metrics
- **Grouping**: Related charts near each other

### 🎨 **Design Principles**
- **Consistent Styling**: Same fonts, colors, and spacing throughout
- **White Space**: Don't overcrowd; allow breathing room
- **Color Consistency**: Use color to group related information
- **Accessibility**: Ensure color-blind friendly palettes

### 📱 **Responsive Design**
- **Mobile First**: Ensure readability on small screens
- **Flexible Layouts**: Charts that adapt to screen size
- **Touch Friendly**: Interactive elements sized for fingers
- **Performance**: Optimize for various connection speeds

## Interactive Features

### 🔍 **Filtering and Drilling**
- **Global Filters**: Apply filters across entire dashboard
- **Chart-Specific Filters**: Individual chart filtering options
- **Drill-Down**: Click to explore deeper levels of detail
- **Cross-Filtering**: Selecting in one chart filters others

### 📊 **Dynamic Updates**
- **Real-Time Data**: Automatic refresh capabilities
- **Parameter Controls**: Sliders, dropdowns for user interaction
- **Time Range Selection**: Dynamic time period adjustment
- **Conditional Formatting**: Visual alerts based on thresholds

### 💫 **Animation and Transitions**
- **Smooth Transitions**: Animated changes between states
- **Loading Indicators**: Progress feedback during updates
- **Hover Effects**: Interactive feedback on mouse hover
- **Zoom and Pan**: Detailed exploration of chart areas

## Export and Sharing Options

### 📄 **Static Exports**
- **PDF Reports**: Multi-page professional documents
- **PowerPoint**: Business presentation ready slides
- **High-Res Images**: PNG/SVG for publications and reports
- **Print Optimization**: Layouts optimized for printing

### 🌐 **Interactive Exports**
- **HTML Dashboards**: Fully interactive web pages
- **Embedded Widgets**: Individual charts for websites
- **Shareable Links**: Secure sharing with access controls
- **Mobile Apps**: Responsive web apps for mobile access

### 📊 **Data Exports**
- **CSV Downloads**: Raw data behind visualizations
- **Excel Workbooks**: Formatted data with calculations
- **JSON Data**: Structured data for developers
- **API Endpoints**: Real-time data access for integrations

## Advanced Dashboard Features

### 🤖 **AI-Assisted Creation**
- **Smart Recommendations**: AI suggests optimal chart types
- **Auto-Layout**: Intelligent arrangement of dashboard elements
- **Content Generation**: Automatic titles, labels, and descriptions
- **Performance Optimization**: AI optimizes for speed and clarity

### 🔧 **Custom Components**
- **Text Boxes**: Narrative explanations and context
- **Image Embedding**: Logos, photos, and branded elements
- **Custom Calculations**: Derived metrics and KPIs
- **Third-Party Integrations**: External data sources and widgets

### 📈 **Advanced Analytics**
- **Statistical Overlays**: Trend lines, confidence intervals
- **Forecasting**: Predictive analytics and projections
- **Anomaly Highlighting**: Automatic outlier identification
- **Comparative Analysis**: Year-over-year, period comparisons

---
*Pro Tip: Start with templates to learn best practices, then create custom dashboards as you become more comfortable with the tools!*
"""
    
    def _generate_ai_insights_guide(self) -> str:
        """Generate AI insights guide"""
        return """
# 🤖 AI Insights Guide

## Overview of AI Capabilities

The AI Insights feature transforms your data into natural language explanations, interactive conversations, and actionable business recommendations using advanced machine learning.

## Data Storytelling

### 📖 **Storytelling Modes**

#### **Executive Brief**
Perfect for leadership presentations and high-level overviews:
- **Duration**: 5-10 minutes to read
- **Focus**: Key findings, business impact, strategic recommendations
- **Audience**: C-Suite, board members, senior management
- **Format**: Executive summary + 3-5 key insights + action items

#### **Detailed Analysis**
Comprehensive analysis for analysts and decision-makers:
- **Duration**: 15-30 minutes to read
- **Focus**: Statistical analysis, methodology, detailed findings
- **Audience**: Data analysts, researchers, department heads
- **Format**: Full methodology + detailed findings + supporting data

#### **Narrative Story**
Engaging story format that guides readers through discoveries:
- **Duration**: 10-20 minutes to read
- **Focus**: Storytelling approach with clear beginning, middle, end
- **Audience**: General business audience, stakeholders
- **Format**: Story arc + key revelations + conclusions

#### **Problem-Solution**
Structured approach for addressing specific business challenges:
- **Duration**: 10-15 minutes to read
- **Focus**: Issue identification, root cause analysis, solutions
- **Audience**: Operations teams, project managers
- **Format**: Problem statement + analysis + recommended solutions

#### **Opportunity Focus**
Emphasis on growth potential and business opportunities:
- **Duration**: 10-15 minutes to read
- **Focus**: Market opportunities, optimization potential, growth areas
- **Audience**: Business development, strategy teams
- **Format**: Current state + opportunities + implementation roadmap

#### **Comparative Study**
Analysis comparing different segments, periods, or scenarios:
- **Duration**: 15-25 minutes to read
- **Focus**: Comparative analysis, benchmarking, relative performance
- **Audience**: Competitive analysis teams, strategy groups
- **Format**: Comparison framework + findings + strategic implications

### 🎯 **Audience Targeting**

#### **Business Executives**
- **Language**: High-level, strategic terminology
- **Focus**: Revenue impact, competitive advantage, ROI
- **Metrics**: Executive KPIs, strategic objectives
- **Recommendations**: Strategic initiatives, resource allocation

#### **Technical Teams**
- **Language**: Technical accuracy, statistical precision
- **Focus**: Methodology, data quality, technical implementation
- **Metrics**: Technical performance indicators, accuracy measures
- **Recommendations**: Technical improvements, system optimizations

#### **Operations Managers**
- **Language**: Process-focused, efficiency-oriented
- **Focus**: Operational efficiency, cost reduction, quality improvement
- **Metrics**: Operational KPIs, process metrics
- **Recommendations**: Process improvements, workflow optimizations

#### **Marketing Teams**
- **Language**: Customer-centric, campaign-focused
- **Focus**: Customer behavior, campaign performance, market trends
- **Metrics**: Marketing ROI, conversion rates, customer metrics
- **Recommendations**: Campaign optimizations, targeting improvements

## Interactive Q&A System

### 💬 **How to Ask Effective Questions**

#### **Trend Analysis Questions**
```
Good Examples:
• "What are the main trends in sales over the last year?"
• "How has customer satisfaction changed by quarter?"
• "What seasonal patterns exist in our revenue data?"
• "Which product categories show growth vs decline?"

Tips:
- Specify time periods for clarity
- Ask about specific metrics or categories
- Request comparison across dimensions
```

#### **Performance Questions**
```
Good Examples:
• "Which regions have the highest profit margins?"
• "What factors correlate with customer retention?"
• "How do our top performers differ from average?"
• "What drives the highest customer satisfaction scores?"

Tips:
- Focus on specific performance metrics
- Ask about relationships between variables
- Request benchmarking and comparisons
```

#### **Diagnostic Questions**
```
Good Examples:
• "Why did sales drop in Q3?"
• "What's causing the increase in customer complaints?"
• "Which factors contribute to higher costs?"
• "What explains the regional performance differences?"

Tips:
- Ask "why" and "what causes" questions
- Focus on specific issues or anomalies
- Request root cause analysis
```

#### **Predictive Questions**
```
Good Examples:
• "What can we expect for next quarter's sales?"
• "Which customers are at risk of churning?"
• "How might seasonal trends affect our projections?"
• "What would happen if we increased marketing spend?"

Tips:
- Use future-oriented language
- Ask about scenarios and projections
- Request risk assessments
```

### 🎭 **Question Suggestions**

The AI automatically suggests relevant questions based on your data:

#### **Data-Driven Suggestions**
- **Correlation Questions**: Based on strong relationships found
- **Trend Questions**: Based on time-series patterns identified
- **Anomaly Questions**: Based on outliers or unusual patterns
- **Comparison Questions**: Based on categorical data available

#### **Industry-Specific Suggestions**
- **Sales Data**: Revenue trends, product performance, customer analysis
- **Financial Data**: Profitability, cost analysis, budget variance
- **Marketing Data**: Campaign ROI, channel effectiveness, conversion rates
- **Operations Data**: Efficiency metrics, quality indicators, process analysis

### 🔍 **Follow-Up Conversations**

The AI maintains context across questions:

- **Related Questions**: Suggestions based on previous answers
- **Deeper Analysis**: Drill-down into specific findings
- **Cross-Reference**: Questions connecting different insights
- **Validation**: Questions to verify or challenge findings

## Advanced Insight Generation

### 🧠 **Deep Pattern Analysis**

#### **Trend Detection**
- **Growth Patterns**: Exponential, linear, or cyclical growth
- **Seasonality**: Recurring patterns by time period
- **Trend Changes**: Acceleration, deceleration, or reversals
- **Correlation Trends**: How relationships change over time

#### **Anomaly Identification**
- **Statistical Outliers**: Values outside normal distributions
- **Temporal Anomalies**: Unusual patterns in time series
- **Categorical Anomalies**: Unusual performance by group
- **Correlation Anomalies**: Unexpected relationship changes

#### **Segmentation Analysis**
- **Customer Segments**: Behavior-based groupings
- **Product Categories**: Performance-based classifications
- **Geographic Regions**: Location-based patterns
- **Time Segments**: Period-based analysis

### 🎯 **Business Opportunity Mining**

#### **Growth Opportunities**
- **Market Expansion**: Underperforming regions or segments
- **Product Development**: Gaps in current offerings
- **Customer Growth**: Upselling and cross-selling potential
- **Operational Scaling**: Efficiency improvement opportunities

#### **Optimization Opportunities**
- **Cost Reduction**: Inefficient processes or overspending
- **Quality Improvement**: Areas with quality issues
- **Process Enhancement**: Workflow optimization potential
- **Resource Allocation**: Better distribution of resources

#### **Risk Mitigation**
- **Performance Risks**: Declining trends or metrics
- **Operational Risks**: Process failures or bottlenecks
- **Customer Risks**: Satisfaction or retention issues
- **Financial Risks**: Profitability or cash flow concerns

### 🩺 **Performance Diagnosis**

#### **Health Assessment**
- **Overall Performance**: Comprehensive business health score
- **Trend Analysis**: Direction and momentum of key metrics
- **Comparative Performance**: Benchmarking against standards
- **Risk Indicators**: Early warning signs of potential issues

#### **Root Cause Analysis**
- **Primary Drivers**: Main factors influencing performance
- **Contributing Factors**: Secondary influences and correlations
- **External Factors**: Market or environmental influences
- **Internal Factors**: Operational or strategic influences

#### **Improvement Roadmap**
- **Quick Wins**: Immediate improvement opportunities
- **Strategic Initiatives**: Long-term improvement projects
- **Resource Requirements**: Investments needed for improvements
- **Success Metrics**: KPIs to track improvement progress

## AI Configuration and Customization

### ⚙️ **Analysis Settings**

#### **Industry Context**
- **Retail**: Focus on sales, inventory, customer behavior
- **Finance**: Emphasis on profitability, risk, compliance
- **Manufacturing**: Operations efficiency, quality, supply chain
- **Healthcare**: Patient outcomes, operational efficiency, compliance
- **Technology**: User engagement, performance metrics, growth

#### **Analysis Depth**
- **Quick Overview**: High-level insights in 30 seconds
- **Standard Analysis**: Comprehensive analysis in 2-3 minutes
- **Deep Dive**: Extensive analysis with detailed exploration

#### **Focus Areas**
- **Trends**: Pattern identification and forecasting
- **Correlations**: Relationship analysis between variables
- **Anomalies**: Outlier detection and investigation
- **Opportunities**: Growth and optimization identification
- **Performance**: Health assessment and benchmarking

### 🎨 **Output Customization**

#### **Report Style**
- **Professional**: Formal business language and structure
- **Conversational**: Casual, easy-to-understand explanations
- **Technical**: Detailed methodology and statistical terminology
- **Executive**: High-level strategic focus

#### **Detail Level**
- **Summary**: Key points and main findings only
- **Standard**: Balanced detail with supporting information
- **Comprehensive**: Full analysis with extensive detail
- **Custom**: User-defined level of detail

## Best Practices for AI Insights

### ✅ **Getting Better Results**

#### **Data Preparation**
- **Clean Data**: Remove obvious errors and inconsistencies
- **Clear Naming**: Use descriptive column names
- **Context Information**: Provide business context in settings
- **Relevant Timeframes**: Focus on meaningful time periods

#### **Question Formulation**
- **Be Specific**: Ask about particular metrics or dimensions
- **Provide Context**: Include business situation in questions
- **Use Business Language**: Ask in terms relevant to your industry
- **Build on Answers**: Use follow-up questions for deeper insights

#### **Result Interpretation**
- **Validate Findings**: Cross-check insights with domain knowledge
- **Consider Context**: Interpret results within business context
- **Action Orientation**: Focus on actionable recommendations
- **Continuous Learning**: Use feedback to improve future analysis

### ⚠️ **Important Limitations**

#### **Data Quality Dependency**
- AI insights are only as good as the underlying data
- Poor data quality leads to unreliable insights
- Always validate findings against business knowledge

#### **Context Requirements**
- AI may miss important business context not in the data
- Industry-specific nuances require human interpretation
- External factors may not be captured in the analysis

#### **Confidence Levels**
- AI provides confidence scores for transparency
- Lower confidence insights should be validated carefully
- Use insights as starting points for further investigation

---
*The AI learns from your interactions. The more you use it and provide feedback, the better it becomes at understanding your business needs!*
"""
    
    def _generate_export_guide(self) -> str:
        """Generate export options guide"""
        return """
# 📤 Export Guide

## Export Options Overview

The BI Assistant provides comprehensive export capabilities to share insights, integrate with other tools, and create professional presentations.

## Quick Export Actions

### 🚀 **One-Click Exports**
- **PDF Report**: Complete analysis with charts and insights
- **PowerPoint Deck**: Presentation-ready slides with key findings
- **Excel Workbook**: Data and charts for further analysis
- **Image Gallery**: High-resolution chart images

### 📊 **Dashboard Exports**
- **Interactive HTML**: Fully functional web dashboard
- **Static PDF**: Print-ready dashboard layout
- **Image Sets**: Individual chart images in various formats
- **Data Files**: Underlying data in CSV or Excel format

## Detailed Export Options

### 📄 **PDF Reports**

#### **Professional Business Reports**
- **Executive Summary**: Key findings and recommendations
- **Detailed Analysis**: Comprehensive statistical analysis
- **Visualizations**: High-quality charts and graphs
- **Appendices**: Supporting data and methodology

#### **Customization Options**
- **Company Branding**: Logo, colors, and corporate styling
- **Report Sections**: Choose which sections to include
- **Chart Selection**: Pick specific visualizations
- **Detail Level**: Summary, standard, or comprehensive

#### **Layout Options**
- **Portrait/Landscape**: Optimal orientation for content
- **Page Size**: A4, Letter, or custom dimensions
- **Margins**: Professional or compact layouts
- **Font Selection**: Corporate or accessibility fonts

### 📽️ **PowerPoint Presentations**

#### **Presentation Formats**
- **Executive Briefing**: 5-10 slides for leadership
- **Detailed Analysis**: 15-25 slides for stakeholders
- **Dashboard Summary**: Visual overview of key metrics
- **Custom Selection**: Choose specific insights and charts

#### **Slide Templates**
- **Title Slides**: Professional headers with key messages
- **Chart Slides**: Full-screen visualizations with insights
- **Data Tables**: Formatted tables with key statistics
- **Summary Slides**: Conclusions and recommendations

#### **PowerPoint Features**
- **Editable Charts**: Native PowerPoint chart objects
- **Speaker Notes**: Detailed explanations for presenters
- **Animation Ready**: Slides optimized for presentation flow
- **Brand Consistency**: Corporate colors and styling

### 🌐 **Interactive HTML Dashboards**

#### **Web Dashboard Features**
- **Full Interactivity**: Filtering, zooming, hover details
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-Time Data**: Option for live data connections
- **Embedded Analytics**: Can be embedded in websites

#### **Sharing Options**
- **Standalone Files**: Self-contained HTML files
- **Web Hosting**: Direct upload to web servers
- **Email Sharing**: Compressed files for email distribution
- **Cloud Integration**: Direct sharing via cloud platforms

#### **Security Features**
- **Password Protection**: Secure access to sensitive data
- **Access Controls**: User-based permissions
- **Data Encryption**: Secure data transmission
- **Audit Trails**: Track access and usage

### 📊 **Data Exports**

#### **CSV Files**
- **Raw Data**: Original uploaded data with any cleaning applied
- **Processed Data**: Data after transformations and calculations
- **Summary Statistics**: Key metrics and calculations
- **Custom Selections**: Filtered or segmented data exports

#### **Excel Workbooks**
- **Multiple Worksheets**: Organized data by category or time period
- **Formatted Tables**: Professional styling with headers and formatting
- **Charts and Graphs**: Native Excel charts for further customization
- **Formulas and Calculations**: Preserves calculated fields and formulas

#### **JSON Data**
- **Structured Data**: Machine-readable format for developers
- **API Integration**: Data formatted for system integrations
- **Configuration Files**: Dashboard and analysis settings
- **Metadata**: Information about data sources and transformations

### 🖼️ **Image Exports**

#### **Chart Images**
- **PNG Format**: High-quality raster images (recommended)
- **SVG Format**: Vector graphics for scalability
- **JPEG Format**: Compressed images for web use
- **PDF Format**: Vector format for professional printing

#### **Resolution Options**
- **Screen Resolution**: 96 DPI for digital display
- **Print Resolution**: 300 DPI for professional printing
- **High Resolution**: 600 DPI for publication quality
- **Custom DPI**: User-defined resolution settings

#### **Size Options**
- **Standard Sizes**: 1920x1080, 1280x720, 800x600
- **Presentation Sizes**: 16:9, 4:3 aspect ratios
- **Custom Dimensions**: User-defined width and height
- **Print Sizes**: A4, Letter, poster dimensions

## Advanced Export Features

### 🤖 **AI-Enhanced Exports**

#### **Smart Summaries**
- **Auto-Generated Insights**: AI writes executive summaries
- **Key Finding Highlights**: Automatic identification of important insights
- **Recommendation Lists**: Action-oriented next steps
- **Risk Assessments**: Potential issues and mitigation strategies

#### **Contextual Explanations**
- **Chart Descriptions**: AI explains what each visualization shows
- **Business Implications**: What the data means for your business
- **Technical Notes**: Methodology and analysis approach
- **Confidence Indicators**: Reliability of findings and recommendations

### 📈 **Dynamic Content**

#### **Real-Time Updates**
- **Live Data Connections**: Exports that update with new data
- **Scheduled Refreshes**: Automatic report generation and distribution
- **Version Control**: Track changes and maintain report history
- **Notification Systems**: Alerts when new versions are available

#### **Parameterized Reports**
- **Variable Inputs**: Reports that adapt to different parameters
- **Scenario Analysis**: Multiple versions with different assumptions
- **Comparative Reports**: Side-by-side analysis of different periods
- **What-If Analysis**: Impact of different business scenarios

### 🔄 **Batch Export Operations**

#### **Multiple Format Export**
- **Single Click**: Export to PDF, PowerPoint, and Excel simultaneously
- **Bulk Processing**: Process multiple dashboards or analyses at once
- **Automated Workflow**: Scheduled exports with automatic distribution
- **Quality Assurance**: Validation checks before export completion

#### **Template-Based Export**
- **Report Templates**: Consistent formatting across all exports
- **Corporate Standards**: Automatic application of brand guidelines
- **Regulatory Compliance**: Templates that meet industry requirements
- **Custom Workflows**: User-defined export processes

## Integration and Automation

### 🔗 **System Integrations**

#### **Email Integration**
- **Direct Email**: Send reports directly from the application
- **Distribution Lists**: Automated sending to stakeholder groups
- **Scheduling**: Regular report distribution on defined schedules
- **Attachment Optimization**: Compressed files for email size limits

#### **Cloud Storage**
- **Google Drive**: Direct upload to Google Drive folders
- **Dropbox**: Automatic sync with Dropbox accounts
- **OneDrive**: Integration with Microsoft OneDrive
- **Custom APIs**: Integration with enterprise storage systems

#### **Business Applications**
- **CRM Integration**: Export customer insights to CRM systems
- **ERP Systems**: Financial and operational data integration
- **BI Platforms**: Export to Tableau, Power BI, or other BI tools
- **Collaboration Tools**: Integration with Slack, Teams, or similar

### 🤖 **Automation Features**

#### **Scheduled Exports**
- **Daily Reports**: Automated daily performance summaries
- **Weekly Dashboards**: Regular business review materials
- **Monthly Analysis**: Comprehensive monthly business reports
- **Custom Schedules**: User-defined timing and frequency

#### **Triggered Exports**
- **Data Updates**: Automatic export when new data is available
- **Threshold Alerts**: Reports generated when KPIs hit thresholds
- **Anomaly Detection**: Automatic reports when anomalies are detected
- **Custom Triggers**: User-defined conditions for export generation

## Best Practices for Exports

### ✅ **Professional Presentation**

#### **Report Design**
- **Consistent Branding**: Use corporate colors, fonts, and logos
- **Clear Hierarchy**: Organize content with clear headings and sections
- **White Space**: Don't overcrowd pages; allow breathing room
- **Quality Charts**: Use high-resolution images and clear labeling

#### **Content Organization**
- **Executive Summary First**: Lead with key findings and recommendations
- **Logical Flow**: Organize content in a logical, story-like progression
- **Supporting Detail**: Provide detailed analysis after high-level insights
- **Action Items**: End with clear, actionable next steps

### 📊 **Data Integrity**

#### **Accuracy Checks**
- **Data Validation**: Verify exported data matches source data
- **Chart Accuracy**: Ensure visualizations correctly represent data
- **Calculation Verification**: Double-check any calculated fields
- **Timestamp Accuracy**: Verify all dates and times are correct

#### **Version Control**
- **File Naming**: Use consistent, descriptive file names with dates
- **Version Numbers**: Track different versions of reports
- **Change Documentation**: Record what changed between versions
- **Archive Management**: Maintain historical versions for reference

### 🔒 **Security and Compliance**

#### **Data Protection**
- **Sensitive Data**: Remove or mask sensitive information before sharing
- **Access Controls**: Ensure exports only go to authorized recipients
- **Encryption**: Use password protection for sensitive reports
- **Audit Trails**: Track who exported what data and when

#### **Compliance Requirements**
- **Regulatory Standards**: Ensure exports meet industry regulations
- **Data Retention**: Follow company policies for data retention
- **Privacy Protection**: Comply with GDPR, CCPA, and other privacy laws
- **Documentation**: Maintain records of what was shared and with whom

---
*Pro Tip: Set up templates and automation for regular reports, but always review exports before distribution to ensure accuracy and relevance!*
"""
    
    def _generate_troubleshooting(self) -> str:
        """Generate troubleshooting guide"""
        return """
# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 📁 Data Upload Problems

#### **File Upload Failures**
```
Problem: "Upload failed" or "File not supported"

Solutions:
✅ Check file format (CSV, XLSX, XLS only)
✅ Verify file size is under 50MB limit
✅ Ensure file isn't corrupted or password-protected
✅ Try saving Excel files as CSV format
✅ Remove special characters from filename

Technical Fix:
- Clear browser cache and cookies
- Try different browser (Chrome, Firefox, Edge)
- Disable browser extensions temporarily
- Check internet connection stability
```

#### **Data Not Loading Correctly**
```
Problem: Data appears blank or columns misaligned

Solutions:
✅ Check that first row contains column headers
✅ Verify consistent data formatting within columns
✅ Remove empty rows and columns
✅ Ensure date formats are consistent (YYYY-MM-DD recommended)
✅ Check for hidden characters or encoding issues

Data Format Fix:
- Save file with UTF-8 encoding
- Remove merged cells in Excel
- Standardize decimal separators (use . not ,)
- Remove currency symbols and percentages
```

#### **Large File Performance Issues**
```
Problem: Upload slow or system freezing with large files

Solutions:
✅ Reduce file size by removing unnecessary columns
✅ Filter data to relevant time periods only
✅ Sample your data (take every nth row)
✅ Split large files into smaller chunks
✅ Use CSV format instead of Excel for better performance

Optimization Tips:
- Remove calculated columns (recreate in analysis)
- Use integer data types where possible
- Compress repetitive text data
- Consider monthly vs daily granularity
```

### 🔍 Analysis Issues

#### **No Analysis Results Generated**
```
Problem: Analysis runs but no insights or charts appear

Solutions:
✅ Verify data has numeric columns for analysis
✅ Check that data isn't all missing values
✅ Ensure date columns are properly formatted
✅ Try with sample data to test system functionality
✅ Check business domain selection matches your data

Debugging Steps:
1. Review data preview for obvious issues
2. Check data quality assessment scores
3. Try analysis with different business domains
4. Reduce analysis scope to specific columns
5. Contact support with error details
```

#### **Incorrect or Strange Insights**
```
Problem: AI insights don't make business sense

Solutions:
✅ Review data quality - garbage in, garbage out
✅ Provide more business context in settings
✅ Check for data entry errors or outliers
✅ Verify column names are descriptive
✅ Use correct business domain setting

Data Quality Checklist:
- Remove test data or dummy entries
- Check for reasonable value ranges
- Verify date ranges make sense
- Remove obviously incorrect entries
- Ensure consistent units of measurement
```

#### **Charts Not Displaying**
```
Problem: Visualizations show blank or error messages

Solutions:
✅ Check that data has sufficient non-null values
✅ Verify numeric columns for chart creation
✅ Try different chart types
✅ Reduce data complexity (fewer categories)
✅ Check browser compatibility (Chrome recommended)

Technical Fixes:
- Clear browser cache
- Disable ad blockers
- Enable JavaScript
- Try incognito/private browsing mode
- Update browser to latest version
```

### 🤖 AI Features Issues

#### **AI Insights Not Working**
```
Problem: AI analysis fails or returns generic responses

Solutions:
✅ Verify OpenAI API key is configured (if using real AI)
✅ Check internet connection for API calls
✅ Try with mock responses enabled for testing
✅ Provide more specific business context
✅ Try simpler questions first

API Configuration:
1. Check .env file has correct OPENAI_API_KEY
2. Verify API key has sufficient credits
3. Test with simple dataset first
4. Enable debug mode for error details
5. Try switching to mock responses temporarily
```

#### **Q&A Not Understanding Questions**
```
Problem: AI gives irrelevant answers to questions

Solutions:
✅ Use more specific business terminology
✅ Reference actual column names in questions
✅ Provide context about your industry
✅ Ask one question at a time
✅ Try suggested questions first

Question Improvement Tips:
- Include time periods in questions
- Reference specific metrics or categories
- Use business language, not technical jargon
- Ask about relationships between variables
- Build on previous successful questions
```

### 📊 Dashboard and Export Issues

#### **Dashboard Not Loading**
```
Problem: Dashboard builder crashes or won't load

Solutions:
✅ Reduce number of charts in dashboard
✅ Try simpler chart types first
✅ Check data size isn't too large
✅ Clear browser cache and restart
✅ Try building dashboard in steps

Performance Optimization:
- Limit dashboard to 6-8 charts maximum
- Use sampling for large datasets
- Avoid complex chart types with big data
- Save dashboard frequently during building
- Test with smaller dataset first
```

#### **Export Failures**
```
Problem: PDF/PowerPoint export fails or incomplete

Solutions:
✅ Reduce dashboard complexity before export
✅ Try exporting individual charts first
✅ Check available disk space
✅ Try different export formats
✅ Ensure charts have finished loading

Export Troubleshooting:
1. Wait for all charts to fully render
2. Try exporting during low-usage times
3. Break large dashboards into smaller sections
4. Use image exports instead of native formats
5. Check file permissions in download folder
```

### 🌐 Web Interface Issues

#### **Streamlit App Not Starting**
```
Problem: Application won't launch or crashes on startup

Solutions:
✅ Check Python environment and dependencies
✅ Verify all required packages are installed
✅ Try running from command line for error details
✅ Check port 8501 isn't already in use
✅ Update Streamlit to latest version

Command Line Debugging:
```bash
# Check Python version (3.8+ required)
python --version

# Install missing dependencies
pip install -r requirements.txt

# Run with verbose output
streamlit run src/dashboard.py --logger.level debug

# Try different port
streamlit run src/dashboard.py --server.port 8502
```

#### **Slow Performance**
```
Problem: Application runs slowly or becomes unresponsive

Solutions:
✅ Close other browser tabs and applications
✅ Use smaller datasets for testing
✅ Clear browser cache and cookies
✅ Try Chrome browser for best performance
✅ Restart the Streamlit application

Performance Optimization:
- Limit data to last 12 months if possible
- Use sampling for datasets over 10,000 rows
- Close unused browser tabs
- Restart application every few hours
- Monitor system memory usage
```

## Error Messages and Solutions

### 🚨 **Common Error Messages**

#### **"ModuleNotFoundError"**
```
Error: ModuleNotFoundError: No module named 'plotly'

Solution:
pip install plotly
# or install all requirements
pip install -r requirements.txt
```

#### **"API Key Error"**
```
Error: "Invalid API key" or "Rate limit exceeded"

Solutions:
1. Check .env file contains valid OPENAI_API_KEY
2. Verify API key has available credits
3. Enable mock responses for testing:
   - Set USE_MOCK_RESPONSES=true in .env
4. Wait a few minutes if rate limited
```

#### **"Memory Error"**
```
Error: "MemoryError" or "Out of memory"

Solutions:
1. Reduce dataset size
2. Close other applications
3. Use data sampling
4. Restart the application
5. Try on a machine with more RAM
```

#### **"File Permission Error"**
```
Error: "Permission denied" when exporting

Solutions:
1. Close any open exported files
2. Check download folder permissions
3. Try different export location
4. Run application as administrator (Windows)
5. Try different file format
```

## Performance Optimization

### ⚡ **Speed Improvements**

#### **Data Processing**
- **Sample Large Datasets**: Use 10,000 rows or less for initial analysis
- **Remove Unnecessary Columns**: Keep only relevant data columns
- **Optimize Data Types**: Use appropriate numeric types
- **Cache Results**: Enable caching for repeated analyses

#### **Visualization**
- **Limit Chart Complexity**: Avoid too many data points on single charts
- **Use Appropriate Chart Types**: Some charts perform better with large data
- **Progressive Loading**: Build dashboards incrementally
- **Image Optimization**: Use appropriate resolution for purpose

### 💾 **Memory Management**
- **Clear Cache Regularly**: Use memory cleanup features
- **Restart Application**: Restart every few hours for long sessions
- **Monitor Usage**: Keep track of memory consumption
- **Close Unused Tabs**: Limit browser tab usage

## Getting Additional Help

### 📞 **Support Resources**

#### **Self-Help Options**
1. **Documentation**: Check relevant guide sections
2. **Sample Data**: Try with provided sample datasets
3. **Error Logs**: Check browser console for detailed errors
4. **Community**: Search for similar issues online

#### **Technical Support**
1. **Error Details**: Provide specific error messages
2. **System Information**: Include OS, browser, Python version
3. **Data Description**: Describe your data structure (without sharing sensitive data)
4. **Steps to Reproduce**: Exact steps that cause the issue

#### **Debugging Information to Collect**
```
System Information:
- Operating System and version
- Python version
- Browser and version
- Available RAM and disk space

Application Information:
- Streamlit version
- Error messages (exact text)
- Steps that caused the error
- Size and type of data being analyzed

Data Information (non-sensitive):
- Number of rows and columns
- Data types and formats
- Business domain/industry
- Time range of data
```

### 🔍 **Advanced Troubleshooting**

#### **Debug Mode**
Enable debug mode for detailed error information:
```
# In .env file
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Or run with debug flags
streamlit run src/dashboard.py --logger.level debug
```

#### **Browser Developer Tools**
1. Open browser developer tools (F12)
2. Check Console tab for JavaScript errors
3. Check Network tab for failed requests
4. Check Sources tab for resource loading issues

#### **Application Logs**
Check application logs for detailed error information:
- Look for Python error tracebacks
- Check for API call failures
- Monitor memory usage patterns
- Review data processing warnings

---
*Remember: Most issues are related to data format or quality. Start by reviewing your data and trying with sample datasets to isolate the problem!*
"""
    
    def _generate_api_reference(self) -> str:
        """Generate API reference documentation"""
        return """
# 🔌 API Reference

## Core Classes and Methods

### DataProcessor
```python
from src.data_processor import DataProcessor

processor = DataProcessor()

# Load and validate data
data = processor.load_file("data.csv")
validated_data = processor.validate_data(data)
summary = processor.get_data_summary(data)
```

### IntelligentDataAnalyzer
```python
from src.intelligent_analyzer import IntelligentDataAnalyzer

analyzer = IntelligentDataAnalyzer()

# Perform comprehensive analysis
results = analyzer.analyze_dataframe(
    data=df,
    business_domain="sales",
    target_audience="executives"
)
```

### IntelligentVisualizationEngine
```python
from src.intelligent_visualizer import IntelligentVisualizationEngine

viz_engine = IntelligentVisualizationEngine()

# Create smart dashboard
dashboard = viz_engine.create_smart_dashboard(
    data=df,
    business_domain="sales",
    chart_theme="business"
)
```

### AdvancedInsightsEngine
```python
from src.advanced_insights import AdvancedInsightsEngine, StorytellingMode

insights = AdvancedInsightsEngine()

# Generate data story
story = insights.create_data_story(
    data=df,
    mode=StorytellingMode.EXECUTIVE_BRIEF,
    target_audience="Business Executives"
)

# Interactive Q&A
answer = insights.interactive_qa_session(df, "What are the main trends?")
```

## Configuration Reference

### Environment Variables (.env)
```bash
# AI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000

# Application Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=50
DEFAULT_ENCODING=utf-8
ENABLE_CACHING=true

# Visualization Settings
DEFAULT_CHART_THEME=business
ENABLE_PLOTLY_EXPORT=true
CHART_EXPORT_DPI=300
DEFAULT_SAMPLE_SIZE=1000
```

### Configuration Class
```python
from src.config import Config

# Access configuration
api_key = Config.OPENAI_API_KEY
max_file_size = Config.MAX_FILE_SIZE_MB
chart_theme = Config.DEFAULT_CHART_THEME
```

## Data Models

### DataQualityReport
```python
@dataclass
class DataQualityReport:
    total_rows: int
    total_columns: int
    missing_values: Dict[str, int]
    duplicate_rows: int
    data_types: Dict[str, str]
    quality_score: float
    recommendations: List[str]
```

### AnalysisResult
```python
@dataclass
class AnalysisResult:
    summary_stats: Dict[str, Any]
    correlations: pd.DataFrame
    trends: List[Dict[str, Any]]
    insights: List[str]
    ai_explanation: str
    quality_report: DataQualityReport
```

### ChartConfig
```python
@dataclass
class ChartConfig:
    chart_id: str
    chart_type: str
    title: str
    x_column: str
    y_column: str
    color_column: Optional[str]
    chart_data: pd.DataFrame
    styling: Dict[str, Any]
```

## Error Handling

### Custom Exceptions
```python
from src.exceptions import (
    DataProcessingError,
    VisualizationError,
    AIAnalysisError,
    ConfigurationError
)

try:
    result = analyzer.analyze_dataframe(data)
except DataProcessingError as e:
    print(f"Data processing failed: {e}")
except AIAnalysisError as e:
    print(f"AI analysis failed: {e}")
```

### Error Response Format
```python
{
    "success": false,
    "error_type": "DataProcessingError",
    "message": "Invalid data format",
    "details": {
        "column": "date_column",
        "issue": "Invalid date format"
    },
    "suggestions": [
        "Use YYYY-MM-DD format for dates",
        "Check for missing values"
    ]
}
```

## Extension Points

### Custom Analysis Modules
```python
# Create custom analyzer
class CustomAnalyzer:
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        # Custom analysis logic
        return {"custom_insights": "..."}

# Register with main analyzer
analyzer.register_custom_analyzer("custom", CustomAnalyzer())
```

### Custom Chart Types
```python
# Create custom chart
class CustomChart:
    def create_chart(self, data: pd.DataFrame, config: ChartConfig):
        # Custom visualization logic
        return plotly_figure

# Register with visualization engine
viz_engine.register_chart_type("custom_chart", CustomChart())
```

### Custom Export Formats
```python
# Create custom exporter
class CustomExporter:
    def export(self, dashboard, output_path: str):
        # Custom export logic
        pass

# Register with export system
exporter.register_format("custom", CustomExporter())
```
"""
    
    def generate_complete_documentation(self) -> Dict[str, str]:
        """Generate all documentation sections"""
        
        documentation = {}
        
        for section_name, generator_func in self.docs_sections.items():
            try:
                documentation[section_name] = generator_func()
            except Exception as e:
                documentation[section_name] = f"Error generating {section_name}: {str(e)}"
        
        return documentation
    
    def save_documentation_files(self, output_dir: str = "docs"):
        """Save documentation as markdown files"""
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        documentation = self.generate_complete_documentation()
        
        for section_name, content in documentation.items():
            filename = f"{section_name}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return len(documentation)
    
    def render_documentation_interface(self):
        """Render documentation interface in Streamlit"""
        
        st.markdown("## 📖 User Documentation")
        
        # Documentation sections
        doc_tabs = st.tabs([
            "🚀 Getting Started",
            "📁 Data Upload",
            "🔍 Analysis Features",
            "🎨 Dashboard Creation",
            "🤖 AI Insights",
            "📤 Export Options",
            "🔧 Troubleshooting",
            "🔌 API Reference"
        ])
        
        documentation = self.generate_complete_documentation()
        
        with doc_tabs[0]:
            st.markdown(documentation['getting_started'])
        
        with doc_tabs[1]:
            st.markdown(documentation['data_upload'])
        
        with doc_tabs[2]:
            st.markdown(documentation['analysis_features'])
        
        with doc_tabs[3]:
            st.markdown(documentation['dashboard_creation'])
        
        with doc_tabs[4]:
            st.markdown(documentation['ai_insights'])
        
        with doc_tabs[5]:
            st.markdown(documentation['export_options'])
        
        with doc_tabs[6]:
            st.markdown(documentation['troubleshooting'])
        
        with doc_tabs[7]:
            st.markdown(documentation['api_reference'])
        
        # Export documentation
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download All Docs"):
                # Create zip file with all documentation
                import zipfile
                import io
                
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for section_name, content in documentation.items():
                        zip_file.writestr(f"{section_name}.md", content)
                
                st.download_button(
                    "📦 Download Documentation ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=f"bi_assistant_docs_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip"
                )
        
        with col2:
            if st.button("📄 Generate PDF"):
                st.info("PDF generation feature coming soon!")
        
        with col3:
            if st.button("🌐 Create Website"):
                st.info("Static site generation feature coming soon!")


# Export main class
__all__ = ['DocumentationGenerator']
