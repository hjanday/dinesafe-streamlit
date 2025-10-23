import requests
import pandas as pd
import polars as pl
import io
# toronto open data uses ckan api
# docs are here: https://docs.ckan.org/en/latest/api/

# base url for the api
BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"


def cast_dinesafe_types(df: pl.DataFrame) -> pl.DataFrame:
    # convert columns to the right data types
    return df.with_columns([
        pl.col("_id").cast(pl.Int64),
        pl.col("Establishment ID").cast(pl.Utf8),
        pl.col("Inspection ID").cast(pl.Utf8),
        pl.col("Establishment Name").cast(pl.Utf8),
        pl.col("Establishment Type").cast(pl.Utf8),
        pl.col("Establishment Address").cast(pl.Utf8),
        pl.col("Establishment Status").cast(pl.Categorical),
        pl.col("Min. Inspections Per Year").str.replace_all("O", "0").cast(pl.Int64),
        pl.col("Infraction Details").cast(pl.Utf8),
        pl.col("Inspection Date").str.strptime(pl.Date, "%Y-%m-%d"),
        pl.col("Severity").cast(pl.Categorical),
        pl.col("Action").cast(pl.Utf8),
        pl.col("Outcome").cast(pl.Utf8),
        pl.col("Amount Fined").str.replace_all(r"[\$,]", "").cast(pl.Float64),
        pl.col("Latitude").cast(pl.Float64),
        pl.col("Longitude").cast(pl.Float64),
        pl.col("unique_id").cast(pl.Utf8),
        
    ])

def get_datasource(package_id="dinesafe") -> pl.DataFrame:
    # get info about the dataset
    url = f"{BASE_URL}/api/3/action/package_show"
    params = {"id": package_id}
    package = requests.get(url, params=params).json()

    if not package.get("success"):
        raise Exception("Failed to fetch package metadata.")
    
    # list to hold all the data
    df_total = []

    # go through each file in the dataset
    for resource in package["result"]["resources"]:
        if resource["datastore_active"]:
            url = BASE_URL + "/datastore/dump/" + resource["id"]
            resource_dump_data = requests.get(url).text
            
            df = pl.read_csv(io.StringIO(resource_dump_data), infer_schema=False)
            df_total.append(df)
    
    # combine all the dataframes
    cdf = pl.concat(df_total)
    cdf = cast_dinesafe_types(cdf)
    return cdf

if __name__ == "__main__":
    # get the data from toronto
    print("Fetching DineSafe data from Toronto Open Data...")
    df = get_datasource()
    
    # save it to files
    from store_data import save_data_locally, save_metadata
    
    filepath = save_data_locally(df)
    save_metadata(df, filepath)
    
    print(f"\nData pipeline completed successfully!")
    print(f"Total records: {df.shape[0]:,}")
    print(f"Unique establishments: {df['Establishment ID'].nunique():,}")
    print(f"Date range: {df['Inspection Date'].min()} to {df['Inspection Date'].max()}")