import ephem
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calculate_planetary_positions(date_time, latitude, longitude):
    observer = ephem.Observer()
    observer.date = date_time
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    
    planets = [ephem.Sun(), ephem.Moon(), ephem.Mars(), ephem.Mercury(), ephem.Jupiter(), ephem.Venus(), ephem.Saturn()]
    positions = {}
    
    for planet in planets:
        planet.compute(observer)
        lon = np.degrees(planet.ra) % 360
        sign = int(lon // 30) + 1
        positions[planet.name] = {'degree': lon % 30, 'sign': sign}
    
    return positions

def plot_kundali(positions):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.axis('off')

    diamond_coords = np.array([[4, 8], [0, 4], [4, 0], [8, 4], [4, 8]])
    for i in range(12):
        rot_coords = np.dot(diamond_coords - 4, np.array([[np.cos(np.pi/6 * i), -np.sin(np.pi/6 * i)], 
                                                          [np.sin(np.pi/6 * i), np.cos(np.pi/6 * i)]])) + 4
        ax.plot(rot_coords[:, 0], rot_coords[:, 1], 'k')
        ax.text(rot_coords[1, 0] + 0.2, rot_coords[1, 1], f'{i+1}', fontsize=12, ha='center', va='center')
    
    for planet, pos in positions.items():
        degree = pos['degree']
        sign = pos['sign']
        x = (sign - 1) % 3 * 4
        y = (sign - 1) // 3 * 4
        ax.text(x + 2, y + 2, f'{planet}\n{degree:.2f}°', fontsize=10, ha='center', va='center')

    return fig

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
    fig = plot_kundali(positions)

    st.pyplot(fig)

if __name__ == "__main__":
    main()
