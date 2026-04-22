# Local Groundwater Context Engine  
**Chong Min**

## Overview
This project builds an end-to-end groundwater analytics system that transforms raw well measurements into interpretable, decision-oriented signals.

It ingests public groundwater monitoring data, computes statistically grounded per-site trend signals, and visualizes them spatially to highlight groundwater conditions across California.

The system is designed to make noisy environmental time-series data easier to understand for local planning, policy review, and public context.

---

## Signal Definition
Each well is summarized as:

- **Status** (Improving / Stable / Declining)
- **Estimated change since SGMA implementation**
- **Statistical significance of change**
- **Confidence based on sample size and data coverage**

Signals compare **pre-SGMA vs post-SGMA groundwater conditions**, focusing on long-term structural shifts rather than short-term fluctuations.

SGMA reference date:

- **Sustainable Groundwater Management Act (SGMA)** enacted on **September 16, 2014**

---

## Statistical Methodology

For each well:

1. Measurements are split into:
   - **Pre-SGMA** observations
   - **Post-SGMA** observations

2. Change is estimated as:

- Post-period average minus pre-period average

3. Statistical significance is evaluated using the **Mann–Whitney U Test**, a nonparametric test robust to irregular and non-normal environmental data.

4. Wells are classified as:

- **Improving**: significant positive shift  
- **Declining**: significant negative shift  
- **Stable**: no statistically significant change

This framework prioritizes interpretability while remaining more rigorous than arbitrary score thresholds.

---

## System Design

The system is structured into modular layers:

- **Ingestion** — Fetches groundwater data incrementally from external APIs
- **Access** — Handles retrieval and querying from the local SQLite database
- **Compute** — Derives per-site statistical trend signals
- **Visualization** — Displays results on an interactive geospatial map

This separation allows the system to handle messy real-world data while keeping computation and presentation cleanly decoupled.

---

## Tech Stack

- **Python**
- **SQLite**
- **SciPy**
- **Folium**
- **GitHub Actions**

Processes **~6 million groundwater measurement rows** locally.

---

## Data Pipeline & Automation

- Incremental ingestion using CKAN API (`msmt_date > latest_date`)
- Metadata table tracks most recent successful ingestion timestamp
- Appends new rows using `ON CONFLICT DO NOTHING` to prevent duplicates
- Scheduled refresh via GitHub Actions every 12 hours (UTC 00:00 / 12:00)
- Map visualization regenerates automatically after each pipeline run

---

## Demo Preview

![Groundwater Map](demo_map.png)

---

## Live Demo

[View Interactive Map](https://chongmindev.github.io/local-groundwater-context-engine/)

---

## Features

- Incremental ingestion from California public groundwater APIs
- Computes per-site groundwater change relative to SGMA implementation
- Uses nonparametric significance testing (Mann–Whitney U)
- Filters wells with insufficient observations
- Handles missing, sparse, and unevenly sampled real-world data
- Interactive statewide geospatial visualization
- Popup summaries for each well site
- Automatically updated freshness indicator

---

## Motivation

Groundwater data is often fragmented, irregular, and difficult to interpret directly.

This project converts raw measurements into simple, explainable signals that help users understand whether groundwater conditions appear to be improving, stable, or declining over time.

It is intended as a practical example of turning public environmental data into usable local intelligence.

---

## Data Source

Data from the California Department of Water Resources (DWR)

**Periodic Groundwater Level Measurements Dataset**  
https://data.cnra.ca.gov/dataset/periodic-groundwater-level-measurements

Accessed via CKAN API.