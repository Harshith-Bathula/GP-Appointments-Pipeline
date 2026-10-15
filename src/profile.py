from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


# Load the three datasets
regional_df = pd.read_csv(RAW_DIR / "appointments_regional.csv")
categories_df = pd.read_csv(RAW_DIR / "national_categories.csv")
duration_df = pd.read_csv(RAW_DIR / "actual_duration.csv")


# Display basic information
datasets = {
    "Appointments Regional": regional_df,
    "National Categories": categories_df,
    "Actual Duration": duration_df
}

for name, df in datasets.items():
    print(f"\n{'=' * 60}")
    print(name)
    print("=" * 60)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn names:")
    for column in df.columns:
        print(f"  - {repr(column)}")

    print("\nFirst 5 rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nDistinct value counts:")
    print(df.nunique())

# Check date ranges
regional_months = pd.to_datetime(
    regional_df["appointment_month"],
    format="%Y-%m"
)

category_dates = pd.to_datetime(
    categories_df["appointment_date"],
    format="%d/%m/%Y"
)

duration_dates = pd.to_datetime(
    duration_df["appointment_date"],
    format="%Y-%m-%d"
)

print("\n" + "=" * 60)
print("DATE RANGES")
print("=" * 60)

print(
    f"Appointments Regional: "
    f"{regional_months.min().date()} to {regional_months.max().date()}"
)

print(
    f"National Categories: "
    f"{category_dates.min().date()} to {category_dates.max().date()}"
)

print(
    f"Actual Duration: "
    f"{duration_dates.min().date()} to {duration_dates.max().date()}"
)
print("\n" + "=" * 60)
print("EXACT DUPLICATE ROWS")
print("=" * 60)

for name, df in datasets.items():
    duplicate_count = df.duplicated().sum()
    print(f"{name}: {duplicate_count:,}")

print("\n" + "=" * 60)
print("CATEGORICAL VALUES")
print("=" * 60)

columns_to_check = {
    "Appointments Regional": [
        "appointment_status",
        "hcp_type",
        "appointment_mode",
        "time_between_book_and_appointment"
    ],
    "National Categories": [
        "service_setting",
        "context_type",
        "national_category"
    ],
    "Actual Duration": [
        "actual_duration"
    ]
}

for name, columns in columns_to_check.items():
    print(f"\n{name}")

    df = datasets[name]

    for column in columns:
        print(f"\n{column}:")
        for value in sorted(df[column].unique()):
            print(f"  - {repr(value)}")

print("\n" + "=" * 60)
print("BOM CHECK")
print("=" * 60)

categories_path = RAW_DIR / "national_categories.csv"

with open(categories_path, "rb") as file:
    first_three_bytes = file.read(3)

print(f"First 3 bytes: {first_three_bytes}")

if first_three_bytes == b"\xef\xbb\xbf":
    print("UTF-8 BOM detected")
else:
    print("No UTF-8 BOM detected")

print("\n" + "=" * 60)
print("APPOINTMENT TOTALS")
print("=" * 60)

for name, df in datasets.items():
    total = df["count_of_appointments"].sum()
    print(f"{name}: {total:,}")