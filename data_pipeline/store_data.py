import pandas as pd
import polars as pl
from pathlib import Path
import json
from datetime import datetime
from typing import Optional


def save_data_locally(df: pl.DataFrame, filename: Optional[str] = None) -> str:
    """
    Save the cleaned data locally as a parquet file for fast loading.
    
    Args:
        df: Cleaned Polars DataFrame
        filename: Optional custom filename. Defaults to timestamped filename.
    
    Returns:
        Path to saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dinesafe_data_{timestamp}.parquet"
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    filepath = data_dir / filename
    
    # Convert to pandas for parquet saving (Polars parquet support varies)
    df_pandas = df.to_pandas()
    df_pandas.to_parquet(filepath, index=False)
    
    print(f"Data saved to: {filepath}")
    print(f"Shape: {df.shape}")
    return str(filepath)


def save_metadata(df: pl.DataFrame, filepath: str) -> None:
    """
    Save metadata about the dataset for dashboard loading.
    
    Args:
        df: Cleaned Polars DataFrame
        filepath: Path to the data file
    """
    metadata = {
        "filepath": filepath,
        "shape": df.shape,
        "columns": df.columns,
        "date_range": {
            "min": df["Inspection Date"].min().strftime("%Y-%m-%d") if "Inspection Date" in df.columns else None,
            "max": df["Inspection Date"].max().strftime("%Y-%m-%d") if "Inspection Date" in df.columns else None
        },
        "last_updated": datetime.now().isoformat(),
        "unique_establishments": df["Establishment ID"].n_unique() if "Establishment ID" in df.columns else 0,
        "total_inspections": len(df)
    }
    
    metadata_path = Path(filepath).parent / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved to: {metadata_path}")


def load_latest_data() -> pl.DataFrame:
    """
    Load the most recent data file from the data directory.
    
    Returns:
        Polars DataFrame with the latest data
    """
    data_dir = Path("data")
    if not data_dir.exists():
        raise FileNotFoundError("No data directory found. Run the data pipeline first.")
    
    # Find the most recent parquet file
    parquet_files = list(data_dir.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError("No parquet files found in data directory.")
    
    latest_file = max(parquet_files, key=lambda x: x.stat().st_mtime)
    
    # Load with pandas then convert to polars
    df_pandas = pd.read_parquet(latest_file)
    df = pl.from_pandas(df_pandas)
    
    print(f"Loaded data from: {latest_file}")
    print(f"Shape: {df.shape}")
    return df
