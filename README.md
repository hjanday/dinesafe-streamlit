# DineSafe Toronto Dashboard

A data pipeline and interactive Streamlit dashboard for exploring Toronto Public Health's DineSafe inspection data.

## 🚀 Overview

This project ingests, cleans, and stores restaurant inspection data from the City of Toronto’s Open Data portal, then visualizes it in an interactive dashboard built with Streamlit.

## 📁 Project Structure

```
dinesafe_dashboard/
├── data_pipeline/        # Fetch, clean, and upload data to cloud storage
│   ├── retrieve_and_clean.py
│   ├── store_data.py
│   
├── streamlit_dashboard/            # Streamlit app and reusable components
│   ├── app.py
│   ├── data_load.py
│   └── utils.py
|
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 🧹 Data Pipeline

* Downloads raw CSV data from the City of Toronto Open Data API
* Cleans and casts fields using Polars
* Uploads the cleaned dataset to cloud storage (e.g., AWS S3 or Google Cloud Storage)

Run the pipeline:

```bash
python data_pipeline/fetch_and_clean.py
```

## 📊 Streamlit Dashboard

Launch the interactive dashboard locally:

```bash
streamlit run dashboard/app.py
```

### Dashboard Features

* Filter inspections by:

  * Infraction severity
  * Establishment status
  * Business name
* Visual summaries (charts, tables)
* Map of restaurant locations using latitude and longitude

## ☁️ Requirements

* Python 3.9+
* For all dependencies see ```requirements.txt```

Install dependencies:

```bash
pip install -r requirements.txt
```


## 📄 Data Source

City of Toronto Open Data Portal:
[DineSafe Inspections Dataset](https://open.toronto.ca/dataset/dinesafe/)

