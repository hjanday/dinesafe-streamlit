import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import polars as pl
from typing import Dict, List, Any, Optional
import numpy as np


def create_map_plot(df: pd.DataFrame, title: str = "Toronto Restaurant Inspections Map") -> go.Figure:
    """
    Create an interactive map showing restaurant locations and inspection frequency.
    
    Args:
        df: Pandas DataFrame with map data
        title: Plot title
    
    Returns:
        Plotly figure object
    """
    if df.empty:
        return go.Figure()
    
    # Create the map using Plotly's scatter_mapbox
    fig = go.Figure()
    
    # Add scatter plot on map
    fig.add_trace(go.Scattermapbox(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(
            size=df['inspection_count'] * 3,  # Size based on inspection count
            color=df['inspection_count'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Inspection Count"),
            sizemode='diameter',
            sizemin=8,
            sizeref=2,  # Scale factor for size
            opacity=0.8
        ),
        text=df['Establishment Name'] + '<br>' + 
             df['Establishment Address'] + '<br>' +
             'Inspections: ' + df['inspection_count'].astype(str),
        hovertemplate='<b>%{text}</b><br>' +
                      'Latitude: %{lat}<br>' +
                      'Longitude: %{lon}<extra></extra>',
        name='Restaurants'
    ))
    
    # Update layout for map
    fig.update_layout(
        title=title,
        mapbox=dict(
            style="open-street-map",  # Use OpenStreetMap style
            center=dict(
                lat=df['Latitude'].mean(),  # Center on Toronto
                lon=df['Longitude'].mean()
            ),
            zoom=10  # Zoom level for Toronto
        ),
        height=600,
        showlegend=False
    )
    
    return fig


def create_severity_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing inspection severity distribution.
    
    Args:
        df: Polars DataFrame with inspection data
    
    Returns:
        Plotly figure object
    """
    if df is None or df.empty:
        return go.Figure()
    
    severity_counts = df["Severity"].value_counts().sort_values(ascending=False)
    
    fig = px.bar(
        x=severity_counts.index,
        y=severity_counts.values,
        title="Inspection Severity Distribution",
        labels={'x': 'Severity', 'y': 'Count'},
        color=severity_counts.values,
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    return fig


def create_status_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart showing establishment status distribution.
    
    Args:
        df: Polars DataFrame with inspection data
    
    Returns:
        Plotly figure object
    """
    if df is None or df.empty:
        return go.Figure()
    
    status_counts = df["Establishment Status"].value_counts()
    
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Establishment Status Distribution"
    )
    
    fig.update_layout(height=400)
    
    return fig


def create_timeline_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a timeline chart showing inspections over time.
    
    Args:
        df: Polars DataFrame with inspection data
    
    Returns:
        Plotly figure object
    """
    if df is None or df.empty:
        return go.Figure()
    
    # Group by date and count inspections
    timeline_data = (
        df
        .groupby("Inspection Date")
        .size()
        .reset_index(name="inspection_count")
        .sort_values("Inspection Date")
    )
    
    fig = px.line(
        x=timeline_data["Inspection Date"],
        y=timeline_data["inspection_count"],
        title="Inspections Over Time",
        labels={'x': 'Date', 'y': 'Number of Inspections'}
    )
    
    fig.update_layout(height=400)
    
    return fig


def create_summary_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create summary metrics for display in the dashboard.
    
    Args:
        df: Polars DataFrame with inspection data
    
    Returns:
        Dictionary with summary metrics
    """
    if df is None or df.empty:
        return {}
    
    metrics = {
        "total_inspections": len(df),
        "unique_establishments": df["Establishment ID"].nunique(),
        "avg_inspections_per_establishment": len(df) / df["Establishment ID"].nunique(),
        "most_common_severity": df["Severity"].mode().iloc[0] if not df["Severity"].mode().empty else "N/A",
        "date_range_days": (df["Inspection Date"].max() - df["Inspection Date"].min()).days if not df["Inspection Date"].empty else 0
    }
    
    return metrics


def display_summary_cards(metrics: Dict[str, Any]) -> None:
    """
    Display summary metrics as cards in the dashboard.
    
    Args:
        metrics: Dictionary with summary metrics
    """
    if not metrics:
        st.warning("No metrics available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Inspections",
            value=f"{metrics.get('total_inspections', 0):,}"
        )
    
    with col2:
        st.metric(
            label="Unique Establishments",
            value=f"{metrics.get('unique_establishments', 0):,}"
        )
    
    with col3:
        st.metric(
            label="Avg Inspections/Establishment",
            value=f"{metrics.get('avg_inspections_per_establishment', 0):.1f}"
        )
    
    with col4:
        st.metric(
            label="Most Common Severity",
            value=metrics.get('most_common_severity', 'N/A')
        )


def create_establishment_type_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a horizontal bar chart showing establishment types.
    
    Args:
        df: Polars DataFrame with inspection data
    
    Returns:
        Plotly figure object
    """
    if df is None or df.empty:
        return go.Figure()
    
    type_counts = df["Establishment Type"].value_counts().sort_values(ascending=False)
    
    fig = px.bar(
        x=type_counts.values,
        y=type_counts.index,
        orientation='h',
        title="Establishment Types",
        labels={'x': 'Count', 'y': 'Establishment Type'},
        color=type_counts.values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=max(400, len(type_counts) * 30),  # Dynamic height based on number of types
        showlegend=False
    )
    
    return fig
