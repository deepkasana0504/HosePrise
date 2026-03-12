"""
ABC Company - Housing Data Analysis Project
Flask Web Application

Serves the interactive dashboard and storyboard with embedded Plotly visualizations.
"""

import os
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify

from data_collection import download_housing_data, RAW_OUTPUT_PATH
from data_preparation import prepare_data, PREPARED_CSV
from visualizations import (
    create_overview_kpis,
    create_overview_charts,
    create_sales_by_renovation_years,
    create_age_renovation_pie,
    create_age_by_features,
    create_price_vs_sqft_scatter,
    create_renovation_impact_box,
)

app = Flask(__name__)

# ── Data initialization ──────────────────────────────────────────────
DATA_RAW_PATH = RAW_OUTPUT_PATH
DATA_PREPARED_PATH = PREPARED_CSV


def get_data():
    """Load prepared data; download from Kaggle + prepare if not present."""
    if not os.path.exists(DATA_PREPARED_PATH):
        if not os.path.exists(DATA_RAW_PATH):
            download_housing_data(DATA_RAW_PATH)
        prepare_data()
    return pd.read_csv(DATA_PREPARED_PATH)


# ── Routes ───────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page."""
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Main dashboard with all four scenarios."""
    df = get_data()
    kpis = create_overview_kpis(df)

    # Default charts
    overview_chart = create_overview_charts(df)
    renovation_hist = create_sales_by_renovation_years(df)
    age_pie = create_age_renovation_pie(df)
    age_bedrooms = create_age_by_features(df, "bedrooms")
    age_bathrooms = create_age_by_features(df, "bathrooms")
    age_floors = create_age_by_features(df, "floors")
    scatter_chart = create_price_vs_sqft_scatter(df)
    box_chart = create_renovation_impact_box(df)

    # Filter options
    price_bins = ["All", "<200K", "200K-400K", "400K-600K",
                  "600K-800K", "800K-1M", "1M+"]
    renovation_options = ["All", "Yes", "No"]

    return render_template(
        "dashboard.html",
        kpis=kpis,
        overview_chart=overview_chart,
        renovation_hist=renovation_hist,
        age_pie=age_pie,
        age_bedrooms=age_bedrooms,
        age_bathrooms=age_bathrooms,
        age_floors=age_floors,
        scatter_chart=scatter_chart,
        box_chart=box_chart,
        price_bins=price_bins,
        renovation_options=renovation_options,
    )


@app.route("/storyboard")
def storyboard():
    """Storyboard view – guided narrative."""
    df = get_data()
    kpis = create_overview_kpis(df)
    overview_chart = create_overview_charts(df)
    renovation_hist = create_sales_by_renovation_years(df)
    age_pie = create_age_renovation_pie(df)
    age_bedrooms = create_age_by_features(df, "bedrooms")
    scatter_chart = create_price_vs_sqft_scatter(df)
    box_chart = create_renovation_impact_box(df)

    return render_template(
        "storyboard.html",
        kpis=kpis,
        overview_chart=overview_chart,
        renovation_hist=renovation_hist,
        age_pie=age_pie,
        age_bedrooms=age_bedrooms,
        scatter_chart=scatter_chart,
        box_chart=box_chart,
    )


# ── API endpoints for dynamic filtering ──────────────────────────────

@app.route("/api/filter/renovation_hist")
def api_renovation_hist():
    """Filter the renovation histogram by price bin."""
    df = get_data()
    price_filter = request.args.get("price_bin", "All")
    chart = create_sales_by_renovation_years(df, price_filter)
    return jsonify({"chart": json.loads(chart)})


@app.route("/api/filter/age_pie")
def api_age_pie():
    """Filter the age pie chart by renovation status."""
    df = get_data()
    renovation_filter = request.args.get("renovation", "All")
    chart = create_age_renovation_pie(df, renovation_filter)
    return jsonify({"chart": json.loads(chart)})


@app.route("/api/filter/age_features")
def api_age_features():
    """Filter the age features chart by feature type."""
    df = get_data()
    feature = request.args.get("feature", "bedrooms")
    chart = create_age_by_features(df, feature)
    return jsonify({"chart": json.loads(chart)})


@app.route("/api/data/summary")
def api_data_summary():
    """Return data summary as JSON."""
    df = get_data()
    kpis = create_overview_kpis(df)
    return jsonify(kpis)


# ── Run ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
