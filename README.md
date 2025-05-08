# NASA-Near-Earth-Object-NEO-Tracking-Insights-Using-Public-API-
Developed an interactive web application to analyze NASA’s asteroid dataset, enabling users to query and  visualize Near-Earth Object (NEO) data efficiently. 
# 🚀 NASA Asteroid Data Collector

This Python project fetches Near Earth Object (NEO) data from NASA's public API and stores it in a MySQL database. The dataset includes details such as asteroid names, estimated diameters, magnitude, and whether they are potentially hazardous.

---

## 📌 Features

- Connects to the [NASA NEO API](https://api.nasa.gov/)
- Fetches asteroid data within a given date range
- Parses relevant information such as:
  - Name
  - Absolute Magnitude
  - Estimated Diameter (min and max)
  - Hazardous status
- Stores the extracted data into a MySQL database table
- Ensures table is created only if it doesn't already exist

---

## 🛠 Technologies Used

- Python 3.x
- Requests library
- `pymysql` for MySQL interaction
- NASA Open API

---

## 📦 Requirements

- Python 3.x
- MySQL Server running locally
- NASA API Key (get it [here](https://api.nasa.gov/))
- Python packages:
  ```bash
  pip install requests pymysql
