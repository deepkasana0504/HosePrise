"""
ABC Company - Housing Data Analysis Project
Data Collection Module

Downloads the Transformed Housing Data from Kaggle using kagglehub.
Dataset: rituparnaghosh18/transformed-housing-data-2
"""

import os
import shutil

# Install dependency if needed:  pip install kagglehub[pandas-datasets]
import kagglehub


DATASET_HANDLE = "rituparnaghosh18/transformed-housing-data-2"
DATASET_FILE = "Transformed_Housing_Data2.csv"
RAW_OUTPUT_DIR = "data/raw"
RAW_OUTPUT_PATH = os.path.join(RAW_OUTPUT_DIR, DATASET_FILE)


def download_housing_data(output_path=RAW_OUTPUT_PATH):
    """Download the transformed housing dataset from Kaggle."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Download (cached after first call)
    dataset_dir = kagglehub.dataset_download(DATASET_HANDLE)
    src = os.path.join(dataset_dir, DATASET_FILE)

    if not os.path.exists(src):
        raise FileNotFoundError(
            f"Expected file '{DATASET_FILE}' not found in {dataset_dir}. "
            f"Available: {os.listdir(dataset_dir)}"
        )

    shutil.copy2(src, output_path)
    print(f"Dataset copied -> {output_path}  ({os.path.getsize(output_path):,} bytes)")
    return output_path


if __name__ == "__main__":
    download_housing_data()
