
# Nexus — Enterprise Sales Intelligence Platform

## Overview

Nexus is a Data Analyst portfolio project that transforms sales
transactions into interactive business insights.

## Technology Stack

- Python
- Pandas and NumPy
- Streamlit
- Plotly
- SQLite
- SQL

## Features

- Executive KPI dashboard
- Interactive date, region, category, segment and channel filters
- Monthly revenue and profit trends
- Regional and category comparisons
- Product profitability analysis
- Discount versus profit analysis
- Customer segment and channel insights
- Illustrative three-month revenue trend forecast
- Rule-based business alerts
- Searchable transaction explorer
- CSV exports
- SQL business analysis queries

## Setup

Install Python 3.10 or later.

```bash
python -m pip install -r requirements.txt
python generate_data.py
python load_sql.py
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Dataset

The project generates a synthetic sales dataset for demonstration.
It does not contain real customer or company information.

## Important Limitations

The forecast uses a simple linear trend, not a validated forecasting
model. Alert thresholds are illustrative. Returned orders are modeled
using simplified assumptions. Results should not be interpreted as
real company financial performance.

## Portfolio Objective

Demonstrate practical skills in data preparation, exploratory analysis,
SQL, KPI development, visualization and business communication.