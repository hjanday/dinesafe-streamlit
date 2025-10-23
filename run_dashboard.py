#!/usr/bin/env python3
"""
Simple script to run the Toronto DineSafe Dashboard
This works for both local development and Streamlit Cloud deployment
"""

import sys
import os
from pathlib import Path

def check_data_exists():
    """Check if we have data files, if not run the data pipeline"""
    data_dir = Path("data")
    if not data_dir.exists() or not list(data_dir.glob("*.parquet")):
        print("No data found, need to run data pipeline first")
        return False
    return True

def main():
    """Main function - just run the streamlit app"""
    print("Toronto DineSafe Dashboard")
    print("=" * 40)
    
    # Check if we have data
    if not check_data_exists():
        print("Cannot run without data. Make sure to run data pipeline first.")
        return
    
    print("Data found, starting dashboard...")
    
    # For Streamlit Cloud, we just import and run the app directly
    # The actual streamlit run command is handled by the cloud platform
    try:
        # Import the app module to make sure it works
        from streamlit_dashboard import app
        print("App module loaded successfully")
    except ImportError as e:
        print(f"Error loading app: {e}")
        return

if __name__ == "__main__":
    main()
