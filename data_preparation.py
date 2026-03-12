"""
ABC Company - Housing Data Analysis Project
Data Preparation Module

Cleans, transforms, and creates calculated fields for the Kaggle
Transformed Housing Data (rituparnaghosh18/transformed-housing-data-2).
"""

import pandas as pd
import numpy as np
import os

# Path produced by data_collection.py
RAW_CSV = "data/raw/Transformed_Housing_Data2.csv"
PREPARED_CSV = "data/prepared/transformed_housing_data.csv"


# ── Column-name mapping ────────────────────────────────────────────
# Maps the original Kaggle column names to shorter, code-friendly names
COLUMN_MAP = {
    "Sale_Price": "price",
    "No of Bedrooms": "bedrooms",
    "No of Bathrooms": "bathrooms",
    "Flat Area (in Sqft)": "sqft_living",
    "Lot Area (in Sqft)": "sqft_lot",
    "No of Floors": "floors",
    "No of Times Visited": "times_visited",
    "Overall Grade": "grade",
    "Area of the House from Basement (in Sqft)": "sqft_above",
    "Basement Area (in Sqft)": "sqft_basement",
    "Age of House (in Years)": "house_age",
    "Latitude": "lat",
    "Longitude": "long",
    "Living Area after Renovation (in Sqft)": "sqft_living_renovated",
    "Lot Area after Renovation (in Sqft)": "sqft_lot_renovated",
    "Years Since Renovation": "years_since_renovation",
    "Ever_Renovated_Yes": "ever_renovated",
    "Waterfront_View_Yes": "waterfront",
}


def load_raw_data(path=RAW_CSV):
    """Load the raw Kaggle housing CSV data."""
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} records from {path}")
    return df


def clean_data(df):
    """Clean the dataset: rename, fill, remove outliers."""
    df = df.copy()

    # 1. Rename columns for convenience
    df.rename(columns=COLUMN_MAP, inplace=True)

    # 2. Derive a single 'condition' column from one-hot encoded columns
    condition_cols = {
        "Condition_of_the_House_Excellent": "Excellent",
        "Condition_of_the_House_Good": "Good",
        "Condition_of_the_House_Okay": "Okay",
        "Condition_of_the_House_Fair": "Fair",
    }
    # Default = "Average" when none of the dummies is 1
    df["condition"] = "Average"
    for col, label in condition_cols.items():
        if col in df.columns:
            df.loc[df[col] == 1, "condition"] = label

    # 3. Derive a zipcode_group column from one-hot encoded columns
    zg_cols = [c for c in df.columns if c.startswith("Zipcode_Group_")]
    df["zipcode_group"] = "Other"
    for col in zg_cols:
        group_label = col.replace("Zipcode_Group_Zipcode_Group_", "Group ")
        df.loc[df[col] == 1, "zipcode_group"] = group_label

    # 4. Drop the original one-hot columns (no longer needed for viz)
    drop_cols = list(condition_cols.keys()) + zg_cols
    df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True, errors="ignore")

    # 5. Fill any nulls
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # 6. Remove invalid rows
    df = df[df["price"] > 0]

    # 7. Cap bedrooms at reasonable max
    df.loc[df["bedrooms"] > 10, "bedrooms"] = df["bedrooms"].median()

    print(f"After cleaning: {len(df)} records, {len(df.columns)} columns")
    return df


def add_calculated_fields(df):
    """
    Add calculated / derived fields for analysis.

    Calculated Fields:
    1.  house_age             – already in dataset (Age of House in Years)
    2.  is_renovated          – readable Yes / No from ever_renovated flag
    3.  years_since_renovation – already in dataset
    4.  age_group             – categorised house age bracket
    5.  price_per_sqft        – price per sq ft of living area
    6.  total_rooms           – bedrooms + bathrooms
    7.  price_bin             – binned price range
    8.  basement_ratio        – basement area / total living area
    9.  renovation_impact     – estimated price boost from renovation
    10. size_category         – Small / Medium / Large / Luxury
    """
    df = df.copy()

    # 1. house_age — already present from the Kaggle data

    # 2. Is Renovated (human-readable)
    df["is_renovated"] = df["ever_renovated"].apply(lambda x: "Yes" if x == 1 else "No")

    # 3. years_since_renovation — already present

    # 4. Age Group
    def categorize_age(age):
        if age <= 10:
            return "0-10 (New)"
        elif age <= 25:
            return "11-25 (Modern)"
        elif age <= 50:
            return "26-50 (Mid-age)"
        elif age <= 75:
            return "51-75 (Old)"
        else:
            return "76+ (Very Old)"

    df["age_group"] = df["house_age"].apply(categorize_age)

    # 5. Price per Sqft
    df["price_per_sqft"] = (df["price"] / df["sqft_living"].replace(0, np.nan)).round(2)

    # 6. Total Rooms
    df["total_rooms"] = df["bedrooms"] + df["bathrooms"]

    # 7. Price Bin
    bins = [0, 200000, 400000, 600000, 800000, 1000000, float("inf")]
    labels = ["<200K", "200K-400K", "400K-600K", "600K-800K", "800K-1M", "1M+"]
    df["price_bin"] = pd.cut(df["price"], bins=bins, labels=labels)

    # 8. Basement Ratio
    df["basement_ratio"] = (
        df["sqft_basement"] / df["sqft_living"].replace(0, np.nan)
    ).round(3)

    # 9. Renovation Impact (price difference vs non-renovated median)
    median_not_renovated = df.loc[df["is_renovated"] == "No", "price"].median()
    df["renovation_impact"] = df.apply(
        lambda r: r["price"] - median_not_renovated if r["is_renovated"] == "Yes" else 0,
        axis=1,
    )

    # 10. Size Category
    def categorize_size(sqft):
        if sqft < 1200:
            return "Small"
        elif sqft < 2200:
            return "Medium"
        elif sqft < 3500:
            return "Large"
        else:
            return "Luxury"

    df["size_category"] = df["sqft_living"].apply(categorize_size)

    print(f"Added calculated fields. Total columns: {len(df.columns)}")
    return df


def save_prepared_data(df, output_path=PREPARED_CSV):
    """Save the prepared dataset."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved prepared data -> {output_path}")
    return output_path


def prepare_data():
    """Full data preparation pipeline."""
    df = load_raw_data()
    df = clean_data(df)
    df = add_calculated_fields(df)
    save_prepared_data(df)
    return df


if __name__ == "__main__":
    prepare_data()
