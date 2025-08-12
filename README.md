# Smart Business Intelligence Assistant 🤖📊

An intelligent data analysis tool that automatically generates visualizations and insights from raw data using Python and AI.

## 🚀 Features

- **Automatic Data Processing**: Upload CSV/Excel files and get instant analysis
- **AI-Powered Insights**: Natural language explanations of data patterns and trends
- **Interactive Visualizations**: Dynamic charts and graphs using Plotly and Matplotlib
- **Smart Dashboard Generation**: Automated dashboard creation in seconds
- **Natural Language Reports**: Clear explanations like "Sales dipped 12% in June due to reduced orders in category X"

## 🛠️ Tech Stack

- **Python**: Data processing with Pandas, NumPy
- **Visualization**: Matplotlib, Plotly, Seaborn
- **AI Integration**: OpenAI API for natural language insights
- **Web Interface**: Streamlit for user-friendly dashboard
- **Data Formats**: CSV, Excel support

## 📁 Project Structure

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

## 🚀 Quick Start

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
streamlit run src/dashboard.py
```

## 📊 Usage

1. Upload your CSV or Excel file
2. Watch as the AI automatically analyzes your data
3. View generated visualizations and insights
4. Download the generated dashboard

## 🔧 Development Status

- [x] Project setup and structure
- [x] Core data processing module
- [x] AI integration
- [x] Visualization engine
- [x] Web interface foundation
- [ ] File upload system enhancement
- [ ] Dashboard generation advanced features
- [ ] Natural language insights enhancement
- [ ] Final documentation

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Haya Lakhani - [GitHub](https://github.com/lakhani-haya)