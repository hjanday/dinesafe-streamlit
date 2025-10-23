import streamlit as st
import pandas as pd
from pathlib import Path
import json

# Simple test app to check if Streamlit Cloud deployment works
st.set_page_config(
    page_title="DineSafe Test",
    page_icon="🍽️",
    layout="wide"
)

def main():
    st.title("DineSafe Dashboard Test")
    st.write("This is a simple test to see if the app loads on Streamlit Cloud")
    
    # Check if data directory exists
    data_dir = Path("data")
    st.write(f"Data directory exists: {data_dir.exists()}")
    
    if data_dir.exists():
        files = list(data_dir.glob("*"))
        st.write(f"Files in data directory: {[f.name for f in files]}")
        
        # Try to load data
        parquet_files = list(data_dir.glob("*.parquet"))
        if parquet_files:
            st.write(f"Found parquet files: {[f.name for f in parquet_files]}")
            try:
                df = pd.read_parquet(parquet_files[0])
                st.write(f"Data loaded successfully! Shape: {df.shape}")
                st.write("First few rows:")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Error loading data: {e}")
        else:
            st.warning("No parquet files found")
    else:
        st.error("Data directory not found")
    
    # Check metadata
    metadata_path = data_dir / "metadata.json"
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            st.write("Metadata loaded:")
            st.json(metadata)
        except Exception as e:
            st.error(f"Error loading metadata: {e}")
    else:
        st.warning("No metadata file found")

if __name__ == "__main__":
    main()
