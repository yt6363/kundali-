import ephem
import datetime
import streamlit as st
import matplotlib.pyplot as plt

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

def plot_kundali(positions):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Coordinates for the diamond chart
    squares = [
        [(5, 9), (6, 8), (5, 7), (4, 8)],  # 1
        [(6, 8), (7, 7), (6, 6), (5, 7)],  # 2
        [(7, 7), (8, 6), (7, 5), (6, 6)],  # 3
        [(6, 6), (7, 5), (6, 4), (5, 5)],  # 4
        [(5, 5), (6, 4), (5, 3), (4, 4)],  # 5
        [(4, 4), (5, 3), (4, 2), (3, 3)],  # 6
        [(3, 3), (4, 2), (3, 1), (2, 2)],  # 7
        [(4, 8), (5, 7), (4, 6), (3, 7)],  # 8
        [(3, 7), (4, 6), (3, 5), (2, 6)],  # 9
        [(2, 6), (3, 5), (2, 4), (1, 5)],  # 10
        [(1, 5), (2, 4), (1, 3), (0, 4)],  # 11
        [(2, 2), (3, 1), (2, 0), (1, 1)],  # 12
    ]

    # Draw the diamond chart
    for square in squares:
        square.append(square[0])  # Close the square
        xs, ys = zip(*square)
        ax.plot(xs, ys, 'k')

    # Number the houses
    house_centers = [
        (5, 8), (6, 7), (7, 6), (6, 5), (5, 4), (4, 3), (3, 2), (4, 6), (3, 5), (2, 4), (1, 3), (2, 2)
    ]
    
    for i, (cx, cy) in enumerate(house_centers):
        ax.text(cx, cy, f'{i+1}', fontsize=12, ha='center', va='center')

    # Plot planetary positions
    for planet, pos in positions.items():
        degree = pos['degree']
        sign = pos['sign']
        cx, cy = house_centers[sign - 1]
        ax.text(cx, cy, f'{planet}\n{degree:.2f}°', fontsize=10, ha='center', va='center')

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
