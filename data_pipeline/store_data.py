import pandas as pd
import polars as pl
from pathlib import Path
import json
from datetime import datetime
from typing import Optional


def save_data_locally(df: pl.DataFrame, filename: Optional[str] = None) -> str:
    """
    save the data as a parquet file so we can load it fast later
    
    Args:
        df: Cleaned Polars DataFrame
        filename: Optional custom filename. Defaults to timestamped filename.
    
    Returns:
        Path to saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dinesafe_data_{timestamp}.parquet"
    
    # make the data folder if it doesnt exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    filepath = data_dir / filename
    
    # convert to pandas because polars parquet support is weird
    df_pandas = df.to_pandas()
    df_pandas.to_parquet(filepath, index=False)
    
    print(f"Data saved to: {filepath}")
    print(f"Shape: {df.shape}")
    return str(filepath)


def save_metadata(df: pl.DataFrame, filepath: str) -> None:
    """
    save some info about the dataset so the dashboard can show it
    
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
        "unique_establishments": df["Establishment ID"].nunique() if "Establishment ID" in df.columns else 0,
        "total_inspections": len(df)
    }
    
    metadata_path = Path(filepath).parent / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved to: {metadata_path}")


def load_latest_data() -> pl.DataFrame:
    """
    load the newest data file from the data folder
    
    Returns:
        Polars DataFrame with the latest data
    """
    data_dir = Path("data")
    if not data_dir.exists():
        raise FileNotFoundError("No data directory found. Run the data pipeline first.")
    
    # find the newest parquet file
    parquet_files = list(data_dir.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError("No parquet files found in data directory.")
    
    latest_file = max(parquet_files, key=lambda x: x.stat().st_mtime)
    
    # load with pandas then convert to polars
    df_pandas = pd.read_parquet(latest_file)
    df = pl.from_pandas(df_pandas)
    
    print(f"Loaded data from: {latest_file}")
    print(f"Shape: {df.shape}")
    return df
