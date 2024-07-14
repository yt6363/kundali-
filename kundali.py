import ephem
import datetime
import streamlit as st
import pandas as pd

def calculate_planetary_positions(date_time, latitude, longitude):
    observer = ephem.Observer()
    observer.date = date_time
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    
    planets = [ephem.Sun(), ephem.Moon(), ephem.Mars(), ephem.Mercury(), ephem.Jupiter(), ephem.Venus(), ephem.Saturn()]
    positions = {}
    
    for planet in planets:
        planet.compute(observer)
        lon = (planet.ra / ephem.degree) % 360
        sign = int(lon // 30) + 1
        positions[planet.name] = {'degree': lon % 30, 'sign': sign}
    
    return positions

def get_lat_long(country):
    coordinates = {
        'USA': {
            'New York': (40.7128, -74.0060),
            'Los Angeles': (34.0522, -118.2437),
            'Chicago': (41.8781, -87.6298),
            'Houston': (29.7604, -95.3698)
        },
        'India': {
            'Delhi': (28.7041, 77.1025),
            'Mumbai': (19.0760, 72.8777),
            'Bangalore': (12.9716, 77.5946),
            'Chennai': (13.0827, 80.2707)
        }
    }
    return coordinates[country]

def main():
    st.title("Kundali (Vedic Astrology Birth Chart) Generator")

    year = st.number_input("Enter the year (e.g., 2024):", min_value=2000, max_value=2100, value=2024)
    month = st.number_input("Enter the month (1-12):", min_value=1, max_value=12, value=7)
    day = st.number_input("Enter the day (1-31):", min_value=1, max_value=31, value=14)
    hour = st.number_input("Enter the hour (0-23):", min_value=0, max_value=23, value=12)
    minute = st.number_input("Enter the minute (0-59):", min_value=0, max_value=59, value=0)
    
    country = st.selectbox("Select the country:", ['USA', 'India'])
    cities_dict = get_lat_long(country)
    city = st.selectbox("Select the city:", list(cities_dict.keys()))
    latitude, longitude = cities_dict[city]

    date_time = datetime.datetime(year, month, day, hour, minute)

    positions = calculate_planetary_positions(date_time, latitude, longitude)
    
    data = []
    for planet, pos in positions.items():
        data.append([planet, pos['sign'], pos['degree']])

    df = pd.DataFrame(data, columns=['Planet', 'Sign', 'Degree'])

    st.write("Planetary Positions:")
    st.dataframe(df)

if __name__ == "__main__":
    main()
