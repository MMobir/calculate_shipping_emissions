import os
import json
import sys

try:
    from utils import (
        convert_distance_to_km,
        get_coordinates,
        determine_distance_type,
        calculate_land_distance,
        calculate_air_distance,
        calculate_sea_distance
    )
except ImportError:
    from calculate_emissions.utils import (
        convert_distance_to_km,
        get_coordinates,
        determine_distance_type,
        calculate_land_distance,
        calculate_air_distance,
        calculate_sea_distance
    )

# Load configuration file
config_file_path = os.path.join(os.path.dirname(__file__), '../../config.json')
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

# Extract Mapbox access token
MAPBOX_ACCESS_TOKEN = config.get('MAPBOX_ACCESS_TOKEN')

# Define paths to data files
data_dir = os.path.join(os.path.dirname(__file__), '../data')

un_locode_file_path = os.path.join(data_dir, 'un_locode.csv')
iata_icao_file_path = os.path.join(data_dir, 'iata_icao_airport_coordinates.csv')
emission_factors_file_path = os.path.join(data_dir, 'emission_factors.xlsx')

def calculate_distance(route: dict, method: dict):
    if route.get('distance'):
        # Direct distance provided by user
        distance = float(route['distance'])
        unit = route['unit']
        return convert_distance_to_km(distance, unit)
    else:
        # Calculate distance based on source and destination
        source = route['source']
        destination = route['destination']

        source_coordinates = get_coordinates(source, un_locode_file_path, iata_icao_file_path)
        destination_coordinates = get_coordinates(destination, un_locode_file_path, iata_icao_file_path)

        # Determine distance type
        distance_type = determine_distance_type(method, emission_factors_file_path)
        distance_calculation_method = ''
        if distance_type == 'land':
            distance_calculation_method = "mapbox"
            return calculate_land_distance(source_coordinates, destination_coordinates), distance_calculation_method
        elif distance_type == 'air':
            distance_calculation_method = "great_circle_distance"
            return calculate_air_distance(source_coordinates, destination_coordinates), distance_calculation_method
        elif distance_type == 'sea':
            distance_calculation_method = "great_circle_distance_2"
            return calculate_sea_distance(source_coordinates, destination_coordinates), distance_calculation_method
        return 0.0, distance_calculation_method

if __name__ == "__main__":
    # Example route and method definitions
    route = {
        "source": {
            "airport_code": "JFK"
        },
        "destination": {
            "airport_code": "SFO"
        }
    }

    method = {
        "method": "cargo_plane"
    }

    # Calculate distance
    distance, distance_calculation_method = calculate_distance(route, method)

    # Print results
    print(f"Calculated Distance: {distance} km")
    print(f"Distance Calculation Method: {distance_calculation_method}")