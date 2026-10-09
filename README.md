# Retail Sales & Profit Analytics Dashboard

## Project objective
A Python dashboard that converts retail order data into business KPIs, trends, product/region comparisons, customer recency indicators, and recommended actions.

## Dataset
This version generates a **synthetic demonstration dataset in `project.py`** using a fixed random seed. No external download is required. It is not actual company data and should not be described as real-world evidence.

If the submission form requires an external dataset URL, replace the synthetic data generator with a permitted dataset that was **not used in the course masterclasses**, record the exact dataset page URL here, and update the report accordingly. Do not claim that a dataset was externally sourced unless you actually used it.

## Features
- KPI cards: revenue, estimated profit, orders, unique customers, profit margin, average order value
- Filters for date range, region, product category, and channel
- Monthly revenue trend and regional performance
- Category performance and revenue-versus-profit analysis
- Customer recency / inactivity review
- CSV export for filtered records
- Methodology and limitations section

## Technology stack
Python, Pandas, NumPy, Streamlit, Plotly.

## Setup
1. Install Python 3.10 or later.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (optional but recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   streamlit run project.py
   ```

6. The dashboard should open in your browser, usually at `http://localhost:8501`.

## KPI definitions
- **Revenue:** sum of discounted order-line revenue.
- **Estimated profit:** simulated revenue less simulated costs and a discount penalty.
- **Orders:** count of unique order IDs.
- **Unique customers:** count of distinct customer IDs in the filtered view.
- **Average order value:** revenue divided by unique order IDs.
- **Customer inactivity:** last order is at least 180 days before the latest date in the filtered data.

## Business questions
1. Which region contributes the most revenue?
2. Which categories produce the strongest revenue and profit?
3. How does revenue change month by month?
4. Which categories may need a margin review?
5. Which customers may warrant retention follow-up?

## Limitations
The dataset is synthetic and the cost/profit values are illustrative. Customer inactivity is a simple recency flag, not a trained churn prediction model. Validate any recommendations using real, authorized data before business use.

## Submission checklist
- `project.py` — one Python file containing the dashboard logic
- `requirements.txt` — dependencies
- `README.md` — project overview, setup, KPI definitions, and dataset note
- `Project_Report.docx` — project documentation with illustrative charts
- GitHub repository URL — create a repository and upload these files individually

Do not submit a ZIP if the official form prohibits ZIP files. Rename the code/report files only if the submission form specifies a required naming convention.
