# Local Groundwater Context Engine  
**Chong Min**

## Overview
This project builds an end-to-end data system that transforms raw groundwater well measurements into interpretable, decision-oriented signals.

It ingests real-world environmental data, computes per-site trends and confidence levels, and visualizes them spatially to highlight local groundwater conditions across California.

## Signal Definition
Each well is summarized as:
- Status (Improving / Stable / Declining)
- Change in groundwater level over time
- Confidence based on data availability

## System Design
The system is structured into modular layers:

- **Ingestion**: Fetches groundwater data from external APIs incrementally
- **Access**: Handles retrieval and querying from the local database
- **Compute**: Derives per-site trend and confidence signals
- **Visualization**: Displays results on an interactive geospatial map

This separation allows the system to handle messy data while keeping computation and presentation cleanly decoupled.

**Tech Stack:** Python, SQLite, Folium (Leaflet.js)  
Processes ~6M rows of groundwater measurements

The system prioritizes interpretability and robustness over model complexity, focusing on reliable signals from imperfect real-world data.

## Data Pipeline & Automation
- Incremental ingestion using CKAN API (`msmt_date > latest_date`)  
- Metadata table tracks last ingestion timestamp  
- Appends new rows using `ON CONFLICT DO NOTHING` to avoid duplicates  
- GitHub Actions runs ingestion every 12 hours (UTC 00:00 and 12:00)  
- Map visualization automatically regenerates after each ingestion  

## Demo Preview
![Groundwater Map](demo_map.png)

## Live Demo
[View Interactive Map](https://chongmindev.github.io/local-groundwater-context-engine/index.html)

## Features
- Incremental ingestion from public groundwater APIs
- Computes per-site groundwater trends (change over time)
- Assigns confidence levels based on data availability
- Robust handling of missing or uneven real-world data
- Interactive spatial visualization of local groundwater status
- Displays last updated time relative to most recent 12-hour cycle

## Motivation
Groundwater data is often fragmented, uneven, and difficult to interpret directly.  
This project converts raw measurements into simple, actionable signals to support local understanding and decision-making.

## Data Source
Data from the California Department of Water Resources (DWR)  
Periodic Groundwater Level Measurements Dataset: https://data.cnra.ca.gov/dataset/periodic-groundwater-level-measurements  
Accessed via CKAN API