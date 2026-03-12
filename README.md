# ABC Company – Housing Market Analysis Project

## Overview

An interactive analytics platform for ABC Company that provides deep insights into housing prices, renovation impact, and property feature distributions. The application uses **Flask** as the web framework and **Plotly** for Tableau-style interactive visualizations.

**Data Source:** [Kaggle – Transformed Housing Data 2](https://www.kaggle.com/datasets/rituparnaghosh18/transformed-housing-data-2) (21,609 records, 31 columns)

---

## Project Structure

```
tab_project/
├── app.py                  # Flask web application (main entry point)
├── data_collection.py      # Kaggle dataset download module (kagglehub)
├── data_preparation.py     # Data cleaning & calculated fields
├── visualizations.py       # Plotly chart creation module
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── data/
│   ├── raw/                # Raw Kaggle dataset (auto-downloaded)
│   └── prepared/           # Transformed data with calculated fields
└── templates/
    ├── base.html           # Base layout (responsive navbar, footer)
    ├── index.html           # Landing page
    ├── dashboard.html       # Main dashboard (4 scenarios)
    └── storyboard.html     # Guided storyboard narrative
```

---

## Scenarios & Visualizations

| # | Scenario | Chart Type | Description |
|---|----------|------------|-------------|
| 1 | Overall Data Overview | KPI Cards + Histogram | Record count, avg price, total basement sqft, % renovated, avg age |
| 2 | Total Sales by Years Since Renovation | Stacked Histogram | Distribution of sales coloured by price range bins |
| 3 | House Age by Renovation Status | Donut Pie + Box Plot | Age group distribution and price comparison |
| 4 | House Age by Bathrooms/Bedrooms/Floors | Grouped Bar + Scatter | Feature-based age distribution with live filter |

**Total Visualizations: 7 interactive charts + 5 KPI cards**

---

## Calculated Fields (10 fields)

1. `house_age` – Years since the house was built
2. `is_renovated` – Whether house has been renovated (Yes/No)
3. `years_since_renovation` – Years since last renovation
4. `age_group` – Categorized house age bracket (New / Modern / Mid-age / Old / Very Old)
5. `price_per_sqft` – Price per square foot of living area
6. `total_rooms` – Total bedrooms + bathrooms
7. `price_bin` – Binned price range (<200K to 1M+)
8. `basement_ratio` – Ratio of basement to total living area
9. `renovation_impact` – Estimated price boost from renovation
10. `size_category` – Small / Medium / Large / Luxury

---

## Data Filters

- **Price Range Filter** – Filters Scenario 2 histogram by price bin
- **Renovation Status Filter** – Filters Scenario 3 pie chart by renovated/not renovated
- **Feature Filter** – Switches Scenario 4 between bedrooms, bathrooms, and floors
- All filters use AJAX API calls for real-time updates without page reload

---

## Setup & Installation

### Prerequisites
- Python 3.9 or higher

### Steps

```bash
# 1. Navigate to project folder
cd tab_project

# 2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

The app will:
- Auto-download the Kaggle housing dataset (21,609 records) via kagglehub
- Clean, rename columns, and add calculated fields
- Launch the Flask server at **http://localhost:5000**

### Pages
- **Home**: http://localhost:5000/
- **Dashboard**: http://localhost:5000/dashboard
- **Storyboard**: http://localhost:5000/storyboard

---

## API Endpoints

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/api/filter/renovation_hist` | GET | `price_bin` | Filter renovation histogram |
| `/api/filter/age_pie` | GET | `renovation` | Filter age pie chart |
| `/api/filter/age_features` | GET | `feature` | Switch feature chart |
| `/api/data/summary` | GET | – | JSON data summary |

---

## Performance Testing

- **Dataset**: 21,609 records with 28 columns (from Kaggle + calculated fields)
- **Filters**: 3 interactive filters with API-driven updates
- **Calculated Fields**: 10 derived metrics
- **Visualizations**: 7 interactive Plotly charts + 5 KPI cards
- **Responsive Design**: Bootstrap 5 grid, mobile-friendly layout
- **Chart Interactivity**: Zoom, pan, hover tooltips, download as PNG

---

## Technology Stack

- **Backend**: Python, Flask 3.0
- **Data**: Pandas, NumPy
- **Visualization**: Plotly 5.18 (Tableau-style interactive charts)
- **Frontend**: Bootstrap 5, Bootstrap Icons, Responsive CSS
- **Integration**: RESTful API endpoints, AJAX filtering

---

## Key Stakeholders

- Real Estate Analysts
- Marketing Teams
- Company Executives

---

© 2026 ABC Company – Housing Market Analysis
