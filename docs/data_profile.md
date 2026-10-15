# Data Profile

## Overview

This profile covers the three NHS GP appointment datasets used in the project. The purpose of the profiling stage was to understand the structure, coverage and quality of the supplied data before any transformations are applied.

The three datasets contain 1,552,008 rows in total.

## 1. Appointments Regional

**File:** `appointments_regional.csv`

- Rows: 596,821
- Columns: 7
- Date coverage: January 2020 to June 2022
- ICBs: 42
- Missing values: 0

### Columns

| Column | Data Type |
|---|---|
| icb_ons_code | string |
| appointment_month | string |
| appointment_status | string |
| hcp_type | string |
| appointment_mode | string |
| time_between_book_and_appointment | string |
| count_of_appointments | integer |

### Grain

Each row represents an appointment count for a particular combination of ICB, month, appointment status, healthcare professional type, appointment mode and booking-to-appointment time band.

### Profile findings

There are 3 appointment statuses, 3 HCP types, 5 appointment modes and 8 booking-wait categories.

The dataset contains 21,604 rows that appear to be exact duplicates. These should not simply be removed. The supplied data has had lower-level geographical fields removed, meaning records that were originally distinct can appear identical at the remaining level of detail. These records will need to be aggregated and their appointment counts summed during transformation.

Some booking-wait labels also contain inconsistent spacing. Examples include:

- `15  to 21 Days`
- `22  to 28 Days`
- `8  to 14 Days`

The total of `count_of_appointments` is 742,804,525.

---

## 2. National Categories

**File:** `national_categories.csv`

- Rows: 817,394
- Columns: 8
- Date coverage: 1 August 2021 to 30 June 2022
- ICBs: 42
- Sub-ICB locations: 106
- Missing values: 0

### Columns

| Column | Data Type |
|---|---|
| appointment_date | string |
| icb_ons_code | string |
| sub_icb_location_name | string |
| service_setting | string |
| context_type | string |
| national_category | string |
| count_of_appointments | integer |
| appointment_month | string |

### Grain

Each row represents an appointment count for a particular sub-ICB location and date, split by service setting, context type and national category.

### Profile findings

The dataset contains 5 service settings, 3 context types and 18 national categories.

`appointment_date` is supplied in day-first `DD/MM/YYYY` format. This needs to be parsed explicitly during transformation rather than relying on automatic date interpretation.

A binary inspection of the source file confirmed that it begins with the UTF-8 BOM bytes:

`EF BB BF`

Pandas handles this when loading the CSV, which is why the BOM was not visible in the displayed `appointment_date` column name.

No exact duplicate rows were detected.

The total of `count_of_appointments` is 296,046,770.

---

## 3. Actual Duration

**Source file:** `actual_duration.csv.xlsx`

The supplied file is an Excel workbook despite its unusual `.csv.xlsx` filename. During extraction it was converted to `actual_duration.csv` while the original source file was retained in the raw data directory.

- Rows: 137,793
- Columns: 8
- Date coverage: 1 December 2021 to 30 June 2022
- Sub-ICB locations: 106
- ICBs: 42
- Regions: 7
- Missing values: 0

### Columns

| Column | Data Type |
|---|---|
| sub_icb_location_code | string |
| sub_icb_location_ons_code | string |
| sub_icb_location_name | string |
| icb_ons_code | string |
| region_ons_code | string |
| appointment_date | string |
| actual_duration | string |
| count_of_appointments | integer |

### Grain

Each row represents an appointment count for a particular sub-ICB location and date within an actual consultation-duration band.

### Profile findings

There are 7 duration categories:

- `1-5 Minutes`
- `6-10 Minutes`
- `11-15 Minutes`
- `16-20 Minutes`
- `21-30 Minutes`
- `31-60 Minutes`
- `Unknown / Data Quality`

The duration bands require an explicit logical sort order because alphabetical sorting does not put `6-10 Minutes` in the correct position.

The appointment dates in this dataset use `YYYY-MM-DD` format, unlike the day-first dates found in the National Categories dataset.

No exact duplicate rows were detected.

The total of `count_of_appointments` is 167,980,692.

---

## Data Quality Issues Identified

Profiling identified the main issues that need to be handled during transformation:

1. The actual-duration source is supplied as an Excel workbook with the filename `actual_duration.csv.xlsx` and therefore requires conversion during extraction.
2. `national_categories.csv` contains a UTF-8 BOM.
3. National Categories uses day-first appointment dates, while Actual Duration uses ISO-style dates.
4. Appointments Regional contains 21,604 exact-looking duplicate rows. These must be aggregated rather than removed because lower-level geographical information was removed from the supplied dataset.
5. Some categorical labels contain inconsistent spacing, and ordered bands such as booking wait and appointment duration require explicit logical ordering.

No transformations have been applied to the raw source data during this profiling stage.