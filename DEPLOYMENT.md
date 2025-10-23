# Deployment Guide for Streamlit Cloud

## Quick Setup

1. **Push your code to GitHub** (make sure all files are committed)

2. **Go to share.streamlit.io** and connect your GitHub repo

3. **Set the main file path** to: `streamlit_dashboard/app.py`

4. **Make sure you have data** - either:
   - Run the data pipeline locally and commit the data files
   - Or set up the data pipeline to run automatically on deployment

## Important Notes

- Streamlit Cloud handles ports automatically (no port conflicts)
- The `run_dashboard.py` script is simplified for cloud deployment
- Make sure your `requirements.txt` has all dependencies
- Data files need to be in the repo or generated during deployment

## Local Development

For local testing, use:
```bash
streamlit run streamlit_dashboard/app.py
```

The cleanup script is only for local development if you get port conflicts.
