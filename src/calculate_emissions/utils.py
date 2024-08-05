import numpy as np
import requests
import pandas as pd
from typing import Optional



def parse_coordinates(coord_str):
    """
    Parses coordinates from the format '4042N 07400W' to decimal degrees.
    
    Args:
        coord_str (str): The coordinates string to parse.
    
    Returns:
        tuple: A tuple containing latitude and longitude in decimal degrees.
    """
    coord_str = str(coord_str).strip()  # Ensure the input is a string and strip any extra whitespace

    try:
        # Split the string based on whitespace and filter out any empty strings
        parts = list(filter(None, coord_str.split(' ')))
        lat_str = parts[0]
        lon_str = parts[1]
        
    except ValueError as e:
        raise ValueError(f"Input should be in the format '4042N 07400W', got '{coord_str}'") from e

    def convert_to_decimal(degree_min_str):
        """
        Converts a degree minute string (e.g., '4042N') to decimal degrees.
        
        Args:
            degree_min_str (str): The degree minute string to convert.
        
        Returns:
            float: The decimal degree value.
        """
        degrees = int(degree_min_str[:-3])
        minutes = int(degree_min_str[-3:-1])
        direction = degree_min_str[-1]
        
        decimal_degrees = degrees + minutes / 60
        
        if direction in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        
        return decimal_degrees
    
    latitude = convert_to_decimal(lat_str)
    longitude = convert_to_decimal(lon_str)
    
    return latitude, longitude


def get_coordinates_from_locode(locode: str, un_locodes_csv_path: str):
    """
    Fetches the geographic coordinates for a given UN/LOCODE from a CSV file.
    
    Args:
        locode (str): The UN/LOCODE of the location.
        csv_path (str): The path to the CSV file containing location data.
    
    Returns:
        tuple: A tuple containing the latitude and longitude of the location.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(un_locodes_csv_path, encoding = 'utf-8')

        # Fetch location by LOCODE from the DataFrame
        location = df[df['locode'] == locode]
        if not location.empty:
            coord_str = location['coordinates'].values[0]
            return parse_coordinates(coord_str)
        else:
            raise ValueError(f"Coordinates not found for LOCODE: {locode}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching coordinates for LOCODE {locode}: {e}")

def get_coordinates_from_address(address: dict):
    query = ', '.join(filter(None, [address.get('street_line1'), address.get('city'), address.get('postcode'), address.get('country_code')]))
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json?access_token={MAPBOX_ACCESS_TOKEN}"
    response = requests.get(url)
    response_data = response.json()

    if response_data['features']:
        coordinates = response_data['features'][0]['geometry']['coordinates']
        return coordinates[1], coordinates[0]  # return as (lat, lon)
    return (0.0, 0.0)

def get_coordinates_from_airport_code(airport_code: str, iata_icao_csv_path: str):
    """
    Fetches the geographic coordinates for a given airport code (IATA or ICAO) from a CSV file.
    
    Args:
        airport_code (str): The IATA or ICAO code of the airport.
        iata_icao_csv_path (str): The path to the CSV file containing airport data.
    
    Returns:
        tuple: A tuple containing the latitude and longitude of the airport.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(iata_icao_csv_path, encoding = 'utf-8')

        # Determine the appropriate column to search based on the length of the airport code
        if len(airport_code) == 3:
            # Search in the IATA column
            location = df[df['iata'] == airport_code]
        elif len(airport_code) == 4:
            # Search in the ICAO column
            location = df[df['icao'] == airport_code]
        else:
            raise ValueError(f"Invalid airport code length for code: {airport_code}")

        # Check if the location was found
        if not location.empty:
            # Fetch the latitude and longitude
            latitude = location['latitude'].values[0]
            longitude = location['longitude'].values[0]
            return float(latitude), float(longitude)
        else:
            raise ValueError(f"Coordinates not found for airport code: {airport_code}")
    
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching coordinates for airport code {airport_code}: {e}")

def get_coordinates(location: dict, un_locode_file_path: str, iata_icao_file_path: str):
    if location.get('locode') and location['locode'].get('locode'):
        return get_coordinates_from_locode(location['locode']['locode'], un_locode_file_path)
    elif location.get('coordinates') and location['coordinates'].get('lat') and location['coordinates'].get('lon'):
        return (location['coordinates']['lat'], location['coordinates']['lon'])
    elif location.get('address'):
        return get_coordinates_from_address(location['address'])
    elif location.get('airport_code'):
        return get_coordinates_from_airport_code(location['airport_code'], iata_icao_file_path)
    else:
        return (0.0, 0.0)
    
def convert_distance_to_km(distance: float, unit: str):
    if unit == 'mi':
        return distance * 1.60934
    elif unit == 'nm':
        return distance * 1.852
    return distance

def determine_distance_type(method: dict, emission_factors_file_path: str):
    try:
        # Load the Excel file
        df = pd.read_excel(emission_factors_file_path, sheet_name='emission_factors')
        
        # Extract the provided method or vessel_type
        method_key = method.get('method') or method.get('vessel_type')
        
        if not method_key:
            raise ValueError("Method or vessel_type must be provided in the method dictionary")
        
        # Check if 'plane' is in the method_key
        if 'plane' in method_key:
            return 'air'
        
        # Look for the provided method in the DataFrame
        result = df.loc[df['method'] == method_key, 'distance_calculation_method']
        
        # If a match is found, return the value
        if not result.empty:
            return result.values[0]
        
        # If no match is found, return None or raise an error
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def calculate_land_distance(source_coordinates, destination_coordinates):
    """
    Calculates the driving distance between two sets of coordinates using the Mapbox Directions API.
    
    Args:
        source_coordinates (tuple): The (latitude, longitude) of the source location.
        destination_coordinates (tuple): The (latitude, longitude) of the destination location.
    
    Returns:
        float: The distance in kilometers.
    """
    lat1, lon1 = source_coordinates
    lat2, lon2 = destination_coordinates
    
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {
        'access_token': MAPBOX_ACCESS_TOKEN,
        'geometries': 'geojson',
        'overview': 'full'
    }
    
    response = requests.get(url, params=params)
    response_data = response.json()
    
    if 'routes' in response_data and len(response_data['routes']) > 0:
        distance_meters = response_data['routes'][0]['distance']
        distance_kilometers = distance_meters / 1000  # Convert meters to kilometers
        return distance_kilometers
    else:
        raise ValueError("Unable to calculate distance using Mapbox API")

def calculate_air_distance(source_coordinates, destination_coordinates):
    """
    Calculates the great circle distance between two sets of coordinates using the Haversine formula.
    
    Args:
        source_coordinates (tuple): The (latitude, longitude) of the source location.
        destination_coordinates (tuple): The (latitude, longitude) of the destination location.
    
    Returns:
        float: The distance in kilometers.
    """
    lat1, lon1 = source_coordinates
    lat2, lon2 = destination_coordinates
    R = 6371.0  # Earth radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    return distance

def calculate_sea_distance(source_coordinates, destination_coordinates):
    """
    Calculates the sea distance between two sets of coordinates.

    For now, this function calculates the air distance (great circle distance) between 
    the source and destination coordinates and multiplies it by 2 as a placeholder.
    In the future, this function needs to be updated to calculate the distance based on 
    sea routes.

    Args:
        source_coordinates (tuple): The (latitude, longitude) of the source location.
        destination_coordinates (tuple): The (latitude, longitude) of the destination location.

    Returns:
        float: The estimated sea distance in kilometers.
    """
    distance = calculate_air_distance(source_coordinates, destination_coordinates) * 2
    return distance
