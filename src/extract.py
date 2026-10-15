from pathlib import Path
import shutil
import hashlib
import json
from datetime import datetime

import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = Path(r"D:\Internship\week 1\Data")
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Source files
SOURCE_FILES = [
    "appointments_regional.csv",
    "national_categories.csv",
    "actual_duration.csv.xlsx",
]

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

# Check that all source files exist
for file_name in SOURCE_FILES:
    source_path = SOURCE_DIR / file_name

    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    print(f"Found: {file_name}")

# Copy source files into the raw data folder
for file_name in SOURCE_FILES:
    source_path = SOURCE_DIR / file_name
    destination_path = RAW_DIR / file_name

    shutil.copy2(source_path, destination_path)

    print(f"Copied: {file_name}")

# Convert the actual duration Excel file to CSV
excel_path = RAW_DIR / "actual_duration.csv.xlsx"
csv_path = RAW_DIR / "actual_duration.csv"

duration_df = pd.read_excel(excel_path)
duration_df.to_csv(csv_path, index=False)

print(f"Converted: {excel_path.name} -> {csv_path.name}")

# Check row counts
regional_df = pd.read_csv(RAW_DIR / "appointments_regional.csv")
categories_df = pd.read_csv(RAW_DIR / "national_categories.csv")
duration_csv_df = pd.read_csv(RAW_DIR / "actual_duration.csv")

print("\nRow counts:")
print(f"appointments_regional.csv: {len(regional_df):,}")
print(f"national_categories.csv: {len(categories_df):,}")
print(f"actual_duration.csv: {len(duration_csv_df):,}")

# Create manifest
manifest = {
    "extraction_time": datetime.now().isoformat(),
    "files": []
}

files_for_manifest = [
    ("appointments_regional.csv", regional_df),
    ("national_categories.csv", categories_df),
    ("actual_duration.csv", duration_csv_df),
]

for file_name, dataframe in files_for_manifest:
    file_path = RAW_DIR / file_name

    file_info = {
        "file_name": file_name,
        "file_size_bytes": file_path.stat().st_size,
        "sha256": calculate_sha256(file_path),
        "row_count": len(dataframe)
    }

    manifest["files"].append(file_info)

manifest_path = RAW_DIR / "manifest.json"

with open(manifest_path, "w", encoding="utf-8") as file:
    json.dump(manifest, file, indent=4)

print(f"\nManifest created: {manifest_path}")