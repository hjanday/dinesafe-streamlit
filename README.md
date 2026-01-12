# Toronto DineSafe Dashboard
I chose **Apache Parquet** as our data storage format for several key reasons:

- **Performance**: Parquet is a columnar storage format that's optimized for analytics workloads. It provides 10-100x faster query performance compared to CSV files
- **Compression**: Parquet files are highly compressed (often 80-90% smaller than CSV), reducing storage requirements and network transfer times
- **Schema Evolution**: Parquet preserves data types and schema information, eliminating the need to re-parse data types on every load
- **Cross-Platform**: Parquet is language-agnostic and works seamlessly with Python, R, Java, and other data science tools
- **Streamlit Compatibility**: Parquet files load much faster in Streamlit applications, providing better user experience

### Design Architecture
The project follows a **modular, pipeline-based architecture**:

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

## Data Source

**Source**: [City of Toronto Open Data Portal - DineSafe Dataset](https://open.toronto.ca/dataset/dinesafe/)

**Update Frequency**: The dashboard automatically loads the latest data when the pipeline is run.

**Data Coverage**: All restaurant inspections in Toronto with location data.
