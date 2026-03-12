"""
ABC Company - Housing Data Analysis Project
Visualization Module

Creates interactive Plotly charts for all four scenarios.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# ── Colour palette ──────────────────────────────────────────────────
COLORS = {
    "primary": "#2C3E50",
    "secondary": "#3498DB",
    "accent": "#E74C3C",
    "success": "#27AE60",
    "warning": "#F39C12",
    "info": "#1ABC9C",
    "light": "#ECF0F1",
    "dark": "#2C3E50",
}

PALETTE = [
    "#3498DB", "#E74C3C", "#27AE60", "#F39C12", "#9B59B6",
    "#1ABC9C", "#E67E22", "#2980B9", "#C0392B", "#16A085",
]

LAYOUT_DEFAULTS = dict(
    font=dict(family="Segoe UI, Roboto, sans-serif", size=13, color="#2C3E50"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(248,249,250,1)",
    margin=dict(l=50, r=30, t=60, b=50),
    hoverlabel=dict(bgcolor="white", font_size=12),
)


# ══════════════════════════════════════════════════════════════════════
# Scenario 1 – Overall Data Overview (KPI cards returned as dict)
# ══════════════════════════════════════════════════════════════════════
def create_overview_kpis(df):
    """Return key metrics for the dataset overview."""
    return {
        "total_records": int(len(df)),
        "avg_price": round(df["price"].mean(), 2),
        "median_price": round(df["price"].median(), 2),
        "total_basement_sqft": int(df["sqft_basement"].sum()),
        "avg_sqft_living": round(df["sqft_living"].mean(), 2),
        "avg_bedrooms": round(df["bedrooms"].mean(), 2),
        "avg_bathrooms": round(df["bathrooms"].mean(), 2),
        "pct_renovated": round((df["is_renovated"] == "Yes").mean() * 100, 1),
        "avg_house_age": round(df["house_age"].mean(), 1),
        "total_sales_value": int(df["price"].sum()),
    }


def create_overview_charts(df):
    """Create supplemental overview charts."""
    # Price distribution
    fig = px.histogram(
        df, x="price", nbins=40,
        title="Distribution of House Prices",
        color_discrete_sequence=[COLORS["secondary"]],
        labels={"price": "Sale Price ($)", "count": "Number of Houses"},
    )
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_layout(bargap=0.05)
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════
# Scenario 2 – Total Sales by Years Since Renovation (Histogram)
# ══════════════════════════════════════════════════════════════════════
def create_sales_by_renovation_years(df, price_filter=None):
    """Histogram: total sales by years since renovation, coloured by price bin."""
    renovated = df[df["is_renovated"] == "Yes"].copy()

    if price_filter and price_filter != "All":
        renovated = renovated[renovated["price_bin"] == price_filter]

    fig = px.histogram(
        renovated,
        x="years_since_renovation",
        color="price_bin",
        nbins=30,
        title="Total Sales by Years Since Renovation",
        labels={
            "years_since_renovation": "Years Since Renovation",
            "count": "Number of Sales",
            "price_bin": "Price Range",
        },
        color_discrete_sequence=PALETTE,
        category_orders={"price_bin": ["<200K", "200K-400K", "400K-600K",
                                        "600K-800K", "800K-1M", "1M+"]},
    )
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_layout(
        barmode="stack",
        xaxis_title="Years Since Renovation",
        yaxis_title="Number of Sales",
        legend_title="Price Range",
    )
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════
# Scenario 3 – Distribution of House Age by Renovation Status (Pie)
# ══════════════════════════════════════════════════════════════════════
def create_age_renovation_pie(df, renovation_filter=None):
    """Pie chart: distribution of house age groups by renovation status."""
    data = df.copy()
    if renovation_filter and renovation_filter != "All":
        data = data[data["is_renovated"] == renovation_filter]

    age_counts = data["age_group"].value_counts().reset_index()
    age_counts.columns = ["age_group", "count"]

    ordered_groups = ["0-10 (New)", "11-25 (Modern)", "26-50 (Mid-age)",
                      "51-75 (Old)", "76+ (Very Old)"]
    age_counts["age_group"] = pd.Categorical(age_counts["age_group"],
                                              categories=ordered_groups, ordered=True)
    age_counts.sort_values("age_group", inplace=True)

    fig = px.pie(
        age_counts,
        values="count",
        names="age_group",
        title="Distribution of House Age by Renovation Status",
        color_discrete_sequence=PALETTE,
        hole=0.35,
    )
    fig.update_traces(textinfo="percent+label", textposition="outside",
                      pull=[0.03] * len(age_counts))
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_layout(legend_title="Age Group")
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════
# Scenario 4 – House Age Distribution by Bathrooms/Bedrooms/Floors
# ══════════════════════════════════════════════════════════════════════
def create_age_by_features(df, feature="bedrooms"):
    """Grouped bar chart: average house age by feature value."""
    valid_features = {"bedrooms", "bathrooms", "floors"}
    if feature not in valid_features:
        feature = "bedrooms"

    grouped = df.groupby([feature, "age_group"]).size().reset_index(name="count")

    ordered_groups = ["0-10 (New)", "11-25 (Modern)", "26-50 (Mid-age)",
                      "51-75 (Old)", "76+ (Very Old)"]
    grouped["age_group"] = pd.Categorical(grouped["age_group"],
                                           categories=ordered_groups, ordered=True)
    grouped.sort_values([feature, "age_group"], inplace=True)

    feature_labels = {
        "bedrooms": "Number of Bedrooms",
        "bathrooms": "Number of Bathrooms",
        "floors": "Number of Floors",
    }

    fig = px.bar(
        grouped,
        x=feature,
        y="count",
        color="age_group",
        barmode="group",
        title=f"House Age Distribution by {feature_labels[feature]}",
        labels={
            feature: feature_labels[feature],
            "count": "Number of Houses",
            "age_group": "Age Group",
        },
        color_discrete_sequence=PALETTE,
        category_orders={"age_group": ordered_groups},
    )
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_layout(
        xaxis_title=feature_labels[feature],
        yaxis_title="Number of Houses",
        legend_title="Age Group",
    )
    return fig.to_json()


# ══════════════════════════════════════════════════════════════════════
# Additional helper visualisations
# ══════════════════════════════════════════════════════════════════════
def create_price_vs_sqft_scatter(df):
    """Scatter plot: price vs sqft_living coloured by condition."""
    fig = px.scatter(
        df, x="sqft_living", y="price",
        color="condition",
        title="Price vs. Living Area (Coloured by Condition)",
        labels={"sqft_living": "Living Area (sqft)", "price": "Price ($)",
                "condition": "Condition"},
        color_discrete_sequence=PALETTE,
        opacity=0.6,
    )
    fig.update_layout(**LAYOUT_DEFAULTS)
    return fig.to_json()


def create_renovation_impact_box(df):
    """Box plot: price distribution by renovation status."""
    fig = px.box(
        df, x="is_renovated", y="price",
        color="is_renovated",
        title="Price Distribution: Renovated vs. Not Renovated",
        labels={"is_renovated": "Renovated", "price": "Price ($)"},
        color_discrete_sequence=[COLORS["secondary"], COLORS["success"]],
    )
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_layout(showlegend=False)
    return fig.to_json()
