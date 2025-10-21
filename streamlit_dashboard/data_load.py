import streamlit as st
import polars as pl
import pandas as pd
from pathlib import Path
import json
from typing import Optional, Dict, Any
import sys
import os

# Add the parent directory to the path so we can import from data_pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_pipeline.store_data import load_latest_data


@st.cache_data(ttl=3600, show_spinner="Loading DineSafe data...")  # Cache for 1 hour
def load_dinesafe_data() -> pl.DataFrame:
    """
    Load the DineSafe data with caching for performance.
    
    Returns:
        Polars DataFrame with inspection data
    """
    try:
        df = load_latest_data()
        # Convert to pandas for better caching compatibility
        return df.to_pandas()
    except FileNotFoundError as e:
        st.error(f"Data not found: {e}")
        st.info("Please run the data pipeline first: `python data_pipeline/retrieve_and_clean.py`")
        return None


@st.cache_data(ttl=3600)
def load_metadata() -> Optional[Dict[str, Any]]:
    """
    Load metadata about the dataset.
    
    Returns:
        Dictionary with dataset metadata
    """
    try:
        data_dir = Path("data")
        metadata_path = data_dir / "metadata.json"
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        st.warning(f"Could not load metadata: {e}")
        return None


def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a summary of the loaded data.
    
    Args:
        df: Pandas DataFrame with inspection data
    
    Returns:
        Dictionary with data summary statistics
    """
    if df is None:
        return {}
    
    summary = {
        "total_inspections": len(df),
        "unique_establishments": df["Establishment ID"].nunique(),
        "date_range": {
            "start": df["Inspection Date"].min(),
            "end": df["Inspection Date"].max()
        },
        "severity_counts": df["Severity"].value_counts().sort_values(ascending=False).to_dict(),
        "status_counts": df["Establishment Status"].value_counts().sort_values(ascending=False).to_dict(),
        "establishment_types": df["Establishment Type"].value_counts().sort_values(ascending=False).to_dict()
    }
    
    return summary


def filter_data(df: pd.DataFrame, 
                severity_filter: list = None,
                status_filter: list = None,
                establishment_type_filter: list = None,
                date_range: tuple = None,
                business_name_filter: str = None) -> pd.DataFrame:
    """
    Filter the data based on various criteria.
    
    Args:
        df: Pandas DataFrame with inspection data
        severity_filter: List of severity levels to include
        status_filter: List of establishment statuses to include
        establishment_type_filter: List of establishment types to include
        date_range: Tuple of (start_date, end_date)
        business_name_filter: String to filter business names
    
    Returns:
        Filtered Pandas DataFrame
    """
    if df is None:
        return None
    
    filtered_df = df.copy()
    
    # Filter by severity
    if severity_filter:
        filtered_df = filtered_df[filtered_df["Severity"].isin(severity_filter)]
    
    # Filter by establishment status
    if status_filter:
        filtered_df = filtered_df[filtered_df["Establishment Status"].isin(status_filter)]
    
    # Filter by establishment type
    if establishment_type_filter:
        filtered_df = filtered_df[filtered_df["Establishment Type"].isin(establishment_type_filter)]
    
    # Filter by date range
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        if start_date:
            # Convert date to datetime for comparison
            start_datetime = pd.to_datetime(start_date)
            filtered_df = filtered_df[filtered_df["Inspection Date"] >= start_datetime]
        if end_date:
            # Convert date to datetime for comparison
            end_datetime = pd.to_datetime(end_date)
            filtered_df = filtered_df[filtered_df["Inspection Date"] <= end_datetime]
    
    # Filter by business name (case-insensitive partial match)
    if business_name_filter:
        filtered_df = filtered_df[
            filtered_df["Establishment Name"].str.lower().str.contains(business_name_filter.lower(), na=False)
        ]
    
    return filtered_df


def get_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare data for heatmap visualization.
    
    Args:
        df: Pandas DataFrame with inspection data
    
    Returns:
        Pandas DataFrame suitable for heatmap plotting
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Filter out null coordinates
    df_coords = df.dropna(subset=["Latitude", "Longitude"])
    
    if df_coords.empty:
        return pd.DataFrame()
    
    # Group by latitude/longitude and count inspections
    heatmap_data = (
        df_coords
        .groupby(["Latitude", "Longitude", "Establishment Name", "Establishment Address"])
        .agg({
            "Inspection ID": "count",  # Count inspections
            "Severity": lambda x: x.value_counts().to_dict(),  # Severity breakdown
            "Establishment Status": "first"  # First status
        })
        .rename(columns={"Inspection ID": "inspection_count", "Establishment Status": "status"})
        .sort_values("inspection_count", ascending=False)
        .reset_index()
    )
    
    return heatmap_data
