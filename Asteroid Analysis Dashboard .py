import streamlit as st
import pymysql
import pandas as pd
import sqlite3
from datetime import date

# Connect to the MySQL database
connection = pymysql.connect(
            host="localhost",
            user="root",
            password="Tn70ad4830@",
            database="asternoids")

st.title("Asteroid Analysis Dashboard 🚀")

# List of query titles and corresponding SQL queries
queries = {
    "1. Count how many times each asteroid has approached Earth": 
        "SELECT neo_reference_id, COUNT(*) AS approach_count FROM close_approach GROUP BY neo_reference_id",

    "2. Average velocity of each asteroid over multiple approaches": 
        "SELECT neo_reference_id, AVG(relative_velocity_kmph) AS avg_velocity FROM close_approach GROUP BY neo_reference_id",

    "3. List top 10 fastest asteroids": 
        "SELECT neo_reference_id, MAX(relative_velocity_kmph) AS max_velocity FROM close_approach GROUP BY neo_reference_id ORDER BY max_velocity DESC LIMIT 10",

    "4. Potentially hazardous asteroids that approached Earth > 3 times": 
        """
        SELECT a.id, a.name, COUNT(c.neo_reference_id) AS approaches 
        FROM asteroids a 
        JOIN close_approach c ON a.id = c.neo_reference_id 
        WHERE a.is_potentially_hazardous_asteroid = 1 
        GROUP BY a.id 
        HAVING approaches > 3
        """,

    "5. Month with the most asteroid approaches": 
        "SELECT MONTH(close_approach_date) AS month, COUNT(*) AS approach_count FROM close_approach GROUP BY month ORDER BY approach_count DESC LIMIT 1",

    "6. Asteroid with the fastest ever approach speed": 
        "SELECT neo_reference_id, relative_velocity_kmph FROM close_approach ORDER BY relative_velocity_kmph DESC LIMIT 1",

    "7. Sort asteroids by maximum estimated diameter (descending)": 
        "SELECT id, name, estimated_diameter_max_km FROM asteroids ORDER BY estimated_diameter_max_km DESC",

    "8. Asteroid whose closest approach is getting nearer over time": 
        """
        SELECT neo_reference_id, close_approach_date, miss_distance_km 
        FROM close_approach 
        WHERE neo_reference_id = (
            SELECT neo_reference_id 
            FROM close_approach 
            GROUP BY neo_reference_id 
            ORDER BY COUNT(*) DESC 
            LIMIT 1
        ) 
        ORDER BY close_approach_date
        """,

    "9. Asteroid name with date and distance of closest approach": 
        """
        SELECT a.name, c.close_approach_date, c.miss_distance_km 
        FROM asteroids a 
        JOIN close_approach c ON a.id = c.neo_reference_id 
        WHERE (a.id, c.miss_distance_km) IN (
            SELECT neo_reference_id, MIN(miss_distance_km) 
            FROM close_approach 
            GROUP BY neo_reference_id
        )
        """,

    "10. Asteroids with velocity > 50,000 km/h": 
        """
        SELECT DISTINCT a.name 
        FROM asteroids a 
        JOIN close_approach c ON a.id = c.neo_reference_id 
        WHERE c.relative_velocity_kmph > 50000
        """,
    
    "11. Asteroid with Largest Diameter Difference": 
        """
        SELECT name, estimated_diameter_max_km - estimated_diameter_min_km AS diameter_difference
        FROM asteroids
        ORDER BY diameter_difference DESC
        LIMIT 1
        """,

    "12. Asteroids Approached on Weekends": """
        SELECT neo_reference_id, close_approach_date
        FROM close_approach
        WHERE DAYOFWEEK(close_approach_date) IN (1, 7)
        """,

    "13. Avg Distance of Hazardous Asteroids": """
        SELECT AVG(miss_distance_km) AS avg_miss_distance_hazardous
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE a.is_potentially_hazardous_asteroid = 1
        """,

    "14. Repeated Dates of Approaches": """
        SELECT close_approach_date, COUNT(*) AS approach_count
        FROM close_approach
        GROUP BY close_approach_date
        HAVING approach_count > 1
        """,

    "15. Bright & Fast Asteroids": """
        SELECT a.name, ca.relative_velocity_kmph, a.absolute_magnitude_h
        FROM asteroids a
        JOIN close_approach ca ON a.id = ca.neo_reference_id
        WHERE ca.relative_velocity_kmph > 50000 AND a.absolute_magnitude_h < 22
        """,

    "16. Most Active Orbiting Body": """
        SELECT orbiting_body, COUNT(*) AS total_approaches
        FROM close_approach
        GROUP BY orbiting_body
        ORDER BY total_approaches DESC
        LIMIT 1
        """,

    "17. Top 5 Most Frequent Earth Visitors": """
        SELECT neo_reference_id, COUNT(*) AS frequency
        FROM close_approach
        GROUP BY neo_reference_id
        ORDER BY frequency DESC
        LIMIT 5
        """,

    "18. Monthly Trend of Hazardous Approaches": """
        SELECT MONTH(close_approach_date) AS month, COUNT(*) AS hazardous_approaches
        FROM close_approach ca
        JOIN asteroids a ON ca.neo_reference_id = a.id
        WHERE a.is_potentially_hazardous_asteroid = 1
        GROUP BY month
        ORDER BY month
        """
}


selected_query = st.sidebar.selectbox("Choose a Query", list(queries.keys()))

if st.button("Run Query"):
    sql = queries[selected_query]
    df = pd.read_sql(sql, connection)
    st.write(f"### Result for: {selected_query}")
    st.dataframe(df)
    
import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime


menu = st.sidebar.radio("Select Option", ["Filter Criteria", "Queries"])


# Show filter UI only when selected in sidebar
if menu == "Filter Criteria":
    # Filters layout in main page
    col1, col2, col3 = st.columns(3)

    with col1:
        mag_min = st.slider("Min Magnitude", 10.0, 35.0, (13.8, 32.6))
        diam_min = st.slider("Min Estimated Diameter (km)", 0.0, 5.0, (0.0, 4.62))
        diam_max = st.slider("Max Estimated Diameter (km)", 0.0, 10.0, (0.0, 10.33))

    with col2:
        velocity = st.slider("Relative Velocity (km/h)", 0, 200000, (1418, 173071))
        au = st.slider("Astronomical Unit", 0.0, 1.0, (0.0, 0.5))
        hazardous = st.selectbox("Only Show Potentially Hazardous", ["All", "Yes", "No"])

    with col3:
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
        end_date = st.date_input("End Date", datetime(2025, 4, 13))
        filter_button = st.button("Filter")

    # Run filter query
    if filter_button:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="Tn70ad4830@",
            database="asternoids"
        )
        cursor = connection.cursor()

        query = """
            SELECT 
                asteroids.id, asteroids.name, asteroids.absolute_magnitude_h, 
                asteroids.estimated_diameter_min_km, asteroids.estimated_diameter_max_km, 
                asteroids.is_potentially_hazardous_asteroid,
                close_approach.close_approach_date, close_approach.relative_velocity_kmph, 
                close_approach.miss_distance_km, close_approach.orbiting_body
            FROM asteroids
            JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            WHERE asteroids.absolute_magnitude_h BETWEEN %s AND %s
            AND asteroids.estimated_diameter_min_km BETWEEN %s AND %s
            AND asteroids.estimated_diameter_max_km BETWEEN %s AND %s
            AND close_approach.relative_velocity_kmph BETWEEN %s AND %s
            AND close_approach.close_approach_date BETWEEN %s AND %s
        """
        params = [
            mag_min[0], mag_min[1],
            diam_min[0], diam_min[1],
            diam_max[0], diam_max[1],
            velocity[0], velocity[1],
            start_date, end_date
        ]

        if hazardous == "Yes":
            query += " AND asteroids.is_potentially_hazardous_asteroid = 1"
        elif hazardous == "No":
            query += " AND asteroids.is_potentially_hazardous_asteroid = 0"

        cursor.execute(query, params)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(results, columns=columns)

        st.subheader("Filtered Asteroids")
        st.dataframe(df, use_container_width=True)

elif menu == "Queries":
    st.write("🔍 You selected **Queries** — custom queries or analytics will appear here.")
