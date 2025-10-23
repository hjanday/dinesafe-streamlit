import streamlit as st
import pandas as pd
import polars as pl
from datetime import datetime, date
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from data_pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from data_load import load_dinesafe_data, load_metadata, filter_data, get_heatmap_data, get_data_summary
    from utils import (
        create_map_plot, create_severity_chart, create_status_chart, 
        create_timeline_chart, create_establishment_type_chart,
        create_summary_metrics, display_summary_cards
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# basic page setup
st.set_page_config(
    page_title="Toronto DineSafe Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# setup plotly for maps
import plotly.io as pio
pio.templates.default = "plotly"

# some basic css to make it look decent
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # main title
    st.markdown('<h1 class="main-header">Toronto DineSafe Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # check if we have data files
    data_dir = Path("data")
    if not data_dir.exists():
        st.error("Data directory not found. Please ensure data files are included in deployment.")
        st.info("Make sure the 'data' folder with parquet files is in your repository.")
        return
    
    # try to load the data
    with st.spinner("Loading DineSafe data..."):
        try:
            df = load_dinesafe_data()
            metadata = load_metadata()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Please check that data files are properly included in your deployment.")
            return
    
    if df is None or df.empty:
        st.error("Unable to load data. Please run the data pipeline first.")
        st.info("Run: `python data_pipeline/retrieve_and_clean.py`")
        return
    
    # sidebar for filtering
    st.sidebar.header("Filters")
    
    # date picker stuff
    st.sidebar.subheader("Date Range")
    date_col1, date_col2 = st.sidebar.columns(2)
    
    with date_col1:
        start_date = st.date_input(
            "Start Date",
            value=df["Inspection Date"].min().date(),
            min_value=df["Inspection Date"].min().date(),
            max_value=df["Inspection Date"].max().date()
        )
    
    with date_col2:
        end_date = st.date_input(
            "End Date",
            value=df["Inspection Date"].max().date(),
            min_value=df["Inspection Date"].min().date(),
            max_value=df["Inspection Date"].max().date()
        )
    
    # filter by severity
    st.sidebar.subheader("Severity")
    severity_options = df["Severity"].unique().tolist()
    severity_filter = st.sidebar.multiselect(
        "Select Severity Levels",
        options=severity_options,
        default=severity_options
    )
    
    # filter by status
    st.sidebar.subheader("Establishment Status")
    status_options = df["Establishment Status"].unique().tolist()
    status_filter = st.sidebar.multiselect(
        "Select Status",
        options=status_options,
        default=status_options
    )
    
    # filter by type
    st.sidebar.subheader("Establishment Type")
    type_options = df["Establishment Type"].unique().tolist()
    establishment_type_filter = st.sidebar.multiselect(
        "Select Types",
        options=type_options,
        default=type_options
    )
    
    # search by name
    st.sidebar.subheader("Business Name")
    business_name_filter = st.sidebar.text_input(
        "Search by Business Name",
        placeholder="Enter business name..."
    )
    
    # actually filter the data
    filtered_df = filter_data(
        df,
        severity_filter=severity_filter if severity_filter else None,
        status_filter=status_filter if status_filter else None,
        establishment_type_filter=establishment_type_filter if establishment_type_filter else None,
        date_range=(start_date, end_date),
        business_name_filter=business_name_filter if business_name_filter else None
    )
    
    # show how many records we have
    st.sidebar.markdown("---")
    st.sidebar.metric("Filtered Records", f"{len(filtered_df):,}")
    st.sidebar.metric("Original Records", f"{len(df):,}")
    
    # check if we have any data left
    if filtered_df is None or filtered_df.empty:
        st.warning("No data matches your filter criteria. Try adjusting the filters.")
        return
    
    # show some basic stats
    st.header("Summary")
    metrics = create_summary_metrics(filtered_df)
    display_summary_cards(metrics)
    
    st.markdown("---")
    
    # different tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Map", "Analytics", "Data Table", "About"])
    
    with tab1:
        st.header("Toronto Restaurant Inspections Map")
        st.markdown("Interactive map showing restaurant locations and inspection frequency")
        
        # get data ready for the map
        map_data = get_heatmap_data(filtered_df)
        
        if not map_data.empty:
            # make the map
            fig = create_map_plot(map_data, "Toronto Restaurant Inspections Map")
            st.plotly_chart(fig, use_container_width=True)
            
            # show the places with most inspections
            st.subheader("Most Inspected Establishments")
            top_establishments = map_data.head(10)[['Establishment Name', 'Establishment Address', 'inspection_count']]
            st.dataframe(top_establishments, use_container_width=True)
        else:
            st.warning("No location data available for map visualization.")
    
    with tab2:
        st.header("Analytics Dashboard")
        
        # put charts in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_severity_chart(filtered_df), use_container_width=True)
            st.plotly_chart(create_status_chart(filtered_df), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_timeline_chart(filtered_df), use_container_width=True)
            st.plotly_chart(create_establishment_type_chart(filtered_df), use_container_width=True)
    
    with tab3:
        st.header("Data Table")
        st.markdown("Browse the filtered inspection data")
        
        # just show the dataframe
        display_df = filtered_df
        
        # tell them how many records
        st.info(f"Showing {len(display_df):,} records")
        
        # actually show the data
        st.dataframe(
            display_df,
            use_container_width=True,
            height=600
        )
        
        # let them download the data
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"dinesafe_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with tab4:
        st.header("About This Dashboard")
        
        st.markdown("""
        ### Toronto DineSafe Dashboard
        
        This interactive dashboard visualizes restaurant inspection data from the City of Toronto's DineSafe program.
        
        #### Features:
        - **Interactive Heatmap**: Visualize restaurant locations and inspection frequency
        - **Analytics Charts**: Explore severity distribution, establishment status, and trends over time
        - **Advanced Filtering**: Filter by date range, severity, status, establishment type, and business name
        - **Data Export**: Download filtered data as CSV
        
        #### Data Source:
        - **Source**: [City of Toronto Open Data Portal](https://open.toronto.ca/dataset/dinesafe/)
        - **Last Updated**: {last_updated}
        - **Total Records**: {total_records:,}
        - **Unique Establishments**: {unique_establishments:,}
        
        #### Technical Details:
        - Built with Streamlit and Plotly
        - Data processed with Polars for performance
        - Cached data loading for fast dashboard updates
        
        #### Data Fields:
        - **Establishment Info**: Name, Address, Type, Status
        - **Inspection Details**: Date, Severity, Action, Outcome
        - **Location**: Latitude and Longitude coordinates
        - **Financial**: Fine amounts (where applicable)
        """.format(
            last_updated=metadata.get('last_updated', 'Unknown') if metadata else 'Unknown',
            total_records=metadata.get('total_inspections', len(df)) if metadata else len(df),
            unique_establishments=metadata.get('unique_establishments', df["Establishment ID"].nunique()) if metadata else df["Establishment ID"].nunique()
        ))
        
        st.markdown("---")
        st.markdown("**Built with Streamlit, Polars, and Plotly**")

if __name__ == "__main__":
    main()
