# Toronto DineSafe Dashboard

A comprehensive data pipeline and interactive Streamlit dashboard for exploring Toronto Public Health's DineSafe inspection data with heatmap visualizations and advanced filtering capabilities.

## Overview

This project ingests, cleans, and stores restaurant inspection data from the City of Toronto's Open Data portal, then visualizes it in an interactive dashboard built with Streamlit. The dashboard features an interactive heatmap showing restaurant locations and inspection frequency, along with comprehensive analytics and filtering options.

## Architecture & Design Philosophy

### Why Parquet Files?
I chose **Apache Parquet** as our data storage format for several key reasons:

- **Performance**: Parquet is a columnar storage format that's optimized for analytics workloads. It provides 10-100x faster query performance compared to CSV files
- **Compression**: Parquet files are highly compressed (often 80-90% smaller than CSV), reducing storage requirements and network transfer times
- **Schema Evolution**: Parquet preserves data types and schema information, eliminating the need to re-parse data types on every load
- **Cross-Platform**: Parquet is language-agnostic and works seamlessly with Python, R, Java, and other data science tools
- **Streamlit Compatibility**: Parquet files load much faster in Streamlit applications, providing better user experience

### Design Architecture
The project follows a **modular, pipeline-based architecture**:

```
Data Source → ETL Pipeline → Storage → Dashboard
     ↓              ↓           ↓         ↓
Toronto API → Clean/Process → Parquet → Streamlit
```

**Key Design Principles:**
- **Separation of Concerns**: Data pipeline, storage, and visualization are completely separate modules
- **Caching Strategy**: Multi-level caching (Streamlit cache + Parquet files) for optimal performance
- **Error Handling**: Graceful degradation with clear error messages for users
- **Scalability**: Architecture supports adding new data sources or visualization types
- **Maintainability**: Simple, readable code with clear documentation

## Project Structure

```
dinesafe-streamlit/
├── data_pipeline/           # Data fetching and processing
│   ├── retrieve_and_clean.py    # Fetch data from Toronto Open Data API
│   └── store_data.py           # Save data locally with metadata
├── streamlit_dashboard/     # Streamlit application
│   ├── app.py                  # Main dashboard application
│   ├── data_load.py           # Data loading utilities with caching
│   └── utils.py              # Visualization and utility functions
├── data/                    # Local data storage (created automatically)
│   ├── dinesafe_data_*.parquet
│   └── metadata.json
├── requirements.txt         # Python dependencies
├── run_dashboard.py        # Orchestration script
└── README.md               # This file
```

## Quick Start

### Option 1: One-Command Setup (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run everything (data pipeline + dashboard)
python run_dashboard.py
```

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run data pipeline
python data_pipeline/retrieve_and_clean.py

# 3. Launch dashboard
streamlit run streamlit_dashboard/app.py
```

## Dashboard Features

### Interactive Heatmap
- **Location Visualization**: Interactive map showing restaurant locations
- **Inspection Frequency**: Bubble size and color indicate inspection count
- **Hover Details**: Click on locations to see establishment details
- **Top Establishments**: Table showing most frequently inspected restaurants

### Analytics Dashboard
- **Severity Distribution**: Bar chart showing inspection severity levels
- **Establishment Status**: Pie chart of business status distribution
- **Timeline Analysis**: Line chart showing inspections over time
- **Business Types**: Horizontal bar chart of establishment types

### Advanced Filtering
- **Date Range**: Filter by inspection date range
- **Severity Levels**: Select specific severity levels (Critical, Significant, Minor, etc.)
- **Establishment Status**: Filter by business status (Pass, Conditional Pass, Closed, etc.)
- **Business Type**: Filter by establishment type (Restaurant, Food Truck, etc.)
- **Business Name**: Search by establishment name

### Data Management
- **Interactive Data Table**: Browse and search through filtered data
- **Data Export**: Download filtered data as CSV
- **Real-time Metrics**: Live summary statistics
- **Cached Loading**: Fast dashboard performance with data caching

## Data Pipeline

The data pipeline automatically:

1. **Fetches Data**: Downloads from Toronto Open Data API
2. **Cleans Data**: Handles data types, missing values, and formatting
3. **Stores Locally**: Saves as Parquet files for fast loading
4. **Generates Metadata**: Creates summary statistics and data info

### Manual Pipeline Execution

```bash
python data_pipeline/retrieve_and_clean.py
```

This will:
- Download the latest DineSafe data
- Clean and process the data
- Save to `data/` directory
- Generate metadata for the dashboard

## Dashboard Usage

### Navigation
- **Heatmap Tab**: Interactive map visualization
- **Analytics Tab**: Charts and statistical analysis
- **Data Table Tab**: Browse and export data
- **About Tab**: Project information and data source details

### Filtering
Use the sidebar to filter data by:
- Date range (start and end dates)
- Severity levels (multi-select)
- Establishment status (multi-select)
- Business types (multi-select)
- Business name (text search)

### Data Export
- Click "Download CSV" in the Data Table tab
- Exports only the currently filtered data
- Includes all original columns and data

## Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Polars for high-performance data operations
- **Visualization**: Plotly for interactive charts and maps
- **Caching**: Streamlit's built-in caching for performance
- **Storage**: Local Parquet files for fast data access

### Performance Features
- **Data Caching**: 1-hour cache for data loading
- **Lazy Loading**: Data loaded only when needed
- **Efficient Filtering**: Polars-based filtering for speed
- **Memory Optimization**: Streaming data processing

### Data Fields
- **Establishment Info**: Name, Address, Type, Status, ID
- **Inspection Details**: Date, Severity, Action, Outcome, Fine Amount
- **Location Data**: Latitude, Longitude coordinates
- **Business Metrics**: Inspection frequency, compliance history

## Data Source

**Source**: [City of Toronto Open Data Portal - DineSafe Dataset](https://open.toronto.ca/dataset/dinesafe/)

**Update Frequency**: The dashboard automatically loads the latest data when the pipeline is run.

**Data Coverage**: All restaurant inspections in Toronto with location data.

## Development

### Prerequisites
- Python 3.9+
- pip package manager

### Installation
```bash
# Clone or download the project
cd dinesafe-streamlit

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running in Development
```bash
# Run data pipeline
python data_pipeline/retrieve_and_clean.py

# Run dashboard in development mode
streamlit run streamlit_dashboard/app.py --server.runOnSave true
```

## Troubleshooting

### Common Issues

1. **"No data found" error**
   - Run the data pipeline first: `python data_pipeline/retrieve_and_clean.py`

2. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

3. **Dashboard won't start**
   - Check if port 8501 is available
   - Try: `streamlit run streamlit_dashboard/app.py --server.port 8502`

4. **Slow performance**
   - Data is cached for 1 hour - subsequent loads will be faster
   - Use filters to reduce data size

### Data Pipeline Issues
- Check internet connection for API access
- Verify Toronto Open Data API is available
- Check disk space for data storage

## License

This project is for educational and research purposes. Data is sourced from the City of Toronto Open Data Portal.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the dashboard.

---

**Built with Streamlit, Polars, and Plotly**

