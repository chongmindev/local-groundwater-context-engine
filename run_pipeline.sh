#!/bin/bash
cd /Users/cmin/VSCode/local-groundwater-context-engine
python3 src/ingestion/ingest_measurements.py
python3 -m src.visualization.map
git add .
git commit -m "Update pipeline"
git push