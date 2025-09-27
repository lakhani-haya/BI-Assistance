# Business Intelligence Assistant 

An intelligent data analysis tool that automatically generates visualizations and insights from raw data using Python and AI.

## Features

- **Automatic Data Processing**: Upload CSV/Excel files and get instant analysis
- **AI-Powered Insights**: Natural language explanations of data patterns and trends
- **Interactive Visualizations**: Dynamic charts and graphs using Plotly and Matplotlib
- **Smart Dashboard Generation**: Automated dashboard creation in seconds
- **Natural Language Reports**: Clear explanations like "Sales dipped 12% in June due to reduced orders in category X"

## Tech Stack

- **Python**: Data processing with Pandas, NumPy
- **Visualization**: Matplotlib, Plotly, Seaborn
- **AI Integration**: OpenAI API for natural language insights
- **Web Interface**: Streamlit for user-friendly dashboard
- **Data Formats**: CSV, Excel support

## Project Structure

```
BI-Assistance/
├── src/
│   ├── data_processor.py      # Core data processing logic
│   ├── ai_analyzer.py         # AI-powered analysis
│   ├── visualizer.py          # Chart generation
│   └── dashboard.py           # Web interface
├── templates/
├── static/
├── data/
│   └── samples/              # Sample datasets
├── tests/
├── requirements.txt
└── README.md
```

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/lakhani-haya/BI-Assistance.git
cd BI-Assistance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

4. Run the application:
```bash
# Option 1: Use the launcher script
python run_dashboard.py

# Option 2: Direct Streamlit command
streamlit run app.py
```

## Usage

1. **Launch the Dashboard**: Run `python run_dashboard.py` 
2. **Upload Data**: Use the sidebar to upload CSV/Excel files or load sample data
3. **Configure Analysis**: Choose business category, theme, and analysis options
4. **Run Analysis**: Click "🚀 Run Analysis" to generate insights and visualizations
5. **Explore Results**: View interactive charts, AI insights, and dashboard summaries
6. **Export**: Download results in JSON, CSV, or HTML format

## Development Status

- [x] Project setup and structure
- [x] Core data processing module
- [x] AI integration
- [x] Visualization engine
- [x] Web interface foundation
- [x] Enhanced file upload & processing
- [x] Dashboard generation advanced features
- [x] Natural language insights enhancement **NEW: AI Storytelling & Q&A**
- [ ] Final documentation

## Step 8 Complete: Natural Language Insights Enhancement

**Advanced AI Capabilities Now Available:**

### AI-Powered Data Storytelling
- **6 Storytelling Modes**: Executive Brief, Detailed Analysis, Narrative Story, Problem-Solution, Opportunity Focus, Comparative Study
- **Interactive Q&A**: Ask questions about your data in natural language
- **Business Opportunity Mining**: AI identifies growth and optimization opportunities
- **Performance Diagnosis**: Automated health checks and improvement recommendations
- **Enhanced Insights**: Deep pattern analysis with actionable business recommendations

### 💬 Natural Language Interface
- **Ask Questions**: "What are the main trends in sales?" or "Which factors drive customer satisfaction?"
- **Get AI Answers**: Detailed, contextual responses with confidence scoring
- **Follow-up Suggestions**: AI recommends related questions for deeper analysis
- **Visualization Suggestions**: Charts and graphs recommended for each insight

### 🎯 Business Intelligence Features
- **Industry-Specific Analysis**: Tailored insights for retail, finance, operations, marketing
- **Stakeholder Targeting**: Content customized for executives, analysts, operations teams
- **Action-Oriented Output**: Specific, implementable recommendations with ROI estimates
- **Professional Reports**: Export stories and insights in multiple formats

### 🌐 Enhanced Web Interface
Navigate to the **AI Insights** tab in the dashboard to access:
- Story Generation with customizable modes and audiences
- Interactive Q&A with your data
- Deep insights generation with business context
- Opportunity mining for growth identification
- Performance diagnosis with improvement roadmaps

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Haya Lakhani - [GitHub](https://github.com/lakhani-haya)