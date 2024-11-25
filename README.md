# sqlalchemy-challenge
readme_content = """
# Climate Analysis and Flask API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-orange)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-red)

## Overview

This project performs climate data analysis and exposes the results via a Flask API. The data is sourced from a SQLite database containing measurements from weather stations in Hawaii. The app includes static and dynamic routes to explore precipitation data, station information, and temperature statistics.

## Objectives

1. Analyze climate data using SQLAlchemy ORM queries, Pandas, and Matplotlib.
2. Build a Flask API to serve the analysis results.
3. Provide clear and accessible endpoints for precipitation, station data, and temperature analysis.

---

## Features

### API Endpoints

#### **1. Homepage**
- **Route**: `/`
- **Description**: Lists all available API routes with descriptions and usage instructions.

#### **2. Precipitation Data**
- **Route**: `/api/v1.0/precipitation`
- **Description**: Returns the last 12 months of precipitation data as JSON, with the date as the key and precipitation as the value.
- **Example Output**:
  ```json
  {
      "2016-08-23": 0.0,
      "2016-08-24": 0.08,
      "2016-08-25": 0.08
  }
