#!/usr/bin/env python3
"""
Orchestration script for the Toronto DineSafe Dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def run_data_pipeline():
    """Run the data pipeline to fetch and clean data."""
    print("🔄 Running data pipeline...")
    try:
        result = subprocess.run([
            sys.executable, "data_pipeline/retrieve_and_clean.py"
        ], check=True, capture_output=True, text=True)
        print("✅ Data pipeline completed successfully!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Data pipeline failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def run_dashboard():
    """Run the Streamlit dashboard."""
    print("🚀 Starting Streamlit dashboard...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_dashboard/app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Dashboard failed to start: {e}")

def main():
    """Main orchestration function."""
    print("🍽️ Toronto DineSafe Dashboard Orchestrator")
    print("=" * 50)
    
    # Check if data exists
    data_dir = Path("data")
    if not data_dir.exists() or not list(data_dir.glob("*.parquet")):
        print("📥 No data found. Running data pipeline first...")
        if not run_data_pipeline():
            print("❌ Cannot proceed without data. Exiting.")
            return
    else:
        print("✅ Data already exists. Skipping data pipeline.")
    
    print("\n🚀 Starting dashboard...")
    print("Dashboard will be available at: http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard")
    print("-" * 50)
    
    run_dashboard()

if __name__ == "__main__":
    main()
