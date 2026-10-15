# NHS GP Appointments Data Engineering Pipeline

This project is being developed as part of the London Success Academy Data Engineering programme. The aim is to build a reproducible data pipeline using publicly available NHS GP appointment data.

The main business question for the project is:

**How is GP appointment capacity being used, and where is it being lost?**

The pipeline will progressively extract, clean, validate, model and analyse the supplied datasets. Week 1 focuses on extraction and understanding the raw data before any transformations are applied.

## Data Sources

The project uses three supplied NHS GP appointment datasets:

| Dataset | Rows | Coverage |
|---|---:|---|
| Appointments Regional | 596,821 | Jan 2020 – Jun 2022 |
| National Categories | 817,394 | Aug 2021 – Jun 2022 |
| Actual Duration | 137,793 | Dec 2021 – Jun 2022 |

Together, the three source datasets contain **1,552,008 rows**.

The datasets have different grains and date ranges, so their appointment totals should not be combined into a single overall appointment figure.