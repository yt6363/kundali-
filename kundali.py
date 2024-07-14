import pyswisseph as swe
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calculate_planetary_positions(date_time, latitude, longitude):
    jd = swe.julday(date_time.year, date_time.month, date_time.day, 
                    date_time.hour + date_time.minute / 60.0)
    planets = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN]
    positions = {}
    for planet in planets:
        lon, lat, dist = swe.calc_ut(jd, planet, swe.FLG_SIDEREAL)[:3]
        sign = int(lon // 30) + 1
        positions[swe.get_planet_name(planet)] = {'degree': lon % 30, 'sign': sign}
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
