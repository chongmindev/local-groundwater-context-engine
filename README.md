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

- **Ingestion**: Fetches groundwater data from external APIs
- **Storage**: Stores time-series data locally for querying
- **Computation**: Derives trend and confidence signals per site
- **Visualization**: Displays results on an interactive map

This separation allows the system to handle messy data while keeping computation and presentation cleanly decoupled.

**Tech Stack:** Python, SQLite, Folium (Leaflet.js)  
Processes ~6M rows of groundwater measurements

The system prioritizes interpretability and robustness over model complexity, focusing on reliable signals from imperfect real-world data.

## Demo Preview
![Groundwater Map](demo_map.png)

## Live Demo
[View Interactive Map](https://chongmindev.github.io/local-groundwater-context-engine/map.html)

## Features
- Ingests groundwater measurements from public APIs into a local database
- Computes per-site groundwater trends (change over time)
- Assigns confidence levels based on data availability
- Handles uneven and incomplete real-world data
- Visualizes results on an interactive geospatial map

## Motivation
Groundwater data is often fragmented, uneven, and difficult to interpret directly.  
This project focuses on converting raw measurements into simple signals that can support local understanding and decision-making.

## Data Source
Data from the California Department of Water Resources (DWR)  
Periodic Groundwater Level Measurements Dataset: https://data.cnra.ca.gov/dataset/periodic-groundwater-level-measurements  
Accessed via CKAN API