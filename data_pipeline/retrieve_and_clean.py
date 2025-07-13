import requests
import pandas as pd
import polars as pl
import io
# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/

# BASE URL
BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"


def cast_dinesafe_types(df: pl.DataFrame) -> pl.DataFrame:
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
    # Get package metadata
    url = f"{BASE_URL}/api/3/action/package_show"
    params = {"id": package_id}
    package = requests.get(url, params=params).json()

    if not package.get("success"):
        raise Exception("Failed to fetch package metadata.")
    
    # Define total df
    df_total = []

    # Loop over the dataset and create an appended total 
    for resource in package["result"]["resources"]:
        if resource["datastore_active"]:
            url = BASE_URL + "/datastore/dump/" + resource["id"]
            resource_dump_data = requests.get(url).text
            
            df = pl.read_csv(io.StringIO(resource_dump_data), infer_schema=False)
            df_total.append(df)
    
    # concate all df's
    cdf = pl.concat(df_total)
    cdf = cast_dinesafe_types(cdf)
    return cdf

res = get_datasource()
print(res.shape)
print(res)