import os
import json
import sys
from typing import Dict

# Ensure the 'src' directory is in sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from calculate_emissions.calculate_mass import calculate_shipment_mass
from calculate_emissions.calculate_distance import calculate_distance
from calculate_emissions.calculate_emission_factor import get_emission_factor

def calculate_emissions(shipping_data: Dict):
    """
    Calculate the emissions for a given shipment based on the provided data.

    Parameters:
    - shipping_data (Dict): A dictionary containing shipment details.

    Returns:
    - str: A JSON string representing the calculated emissions and related data.
    """
    try:
        # Calculate the shipment mass
        shipment_mass = calculate_shipment_mass(shipping_data['shipment'])

        # Calculate the distance
        route = shipping_data['route']
        method = shipping_data['method']
        distance, distance_calculation_method = calculate_distance(route, method)

        # Get the emission factor
        country_code = shipping_data.get('country_code')
        emission_factor, emission_factor_calculation_method = get_emission_factor(method, distance, country_code)

        # Calculate emissions
        emissions = shipment_mass * distance * emission_factor

        # Prepare the output dictionary
        output_data = {
            "emissions": emissions,
            "shipment_mass": shipment_mass,
            "distance": distance,
            "distance_calculation_method": distance_calculation_method,
            "emission_factor": emission_factor,
            "emission_factor_calculation_method": emission_factor_calculation_method
        }

        # Convert the output data to JSON format
        return json.dumps(output_data, indent=4)
    except KeyError as e:
        raise ValueError(f"Required data is missing: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred while calculating emissions: {e}")

if __name__ == "__main__":
    # Example usage
    shipping_data = {
        "shipment": {
            "mass": {
                "amount": 2000.0,  # Ensure this is a float
                "unit": "kg"
            }
        },
        "route": {
            "source": {
                "airport_code": "JFK"
            },
            "destination": {
                "airport_code": "SFO"
            }
        },
        "method": {
            "method": "cargo_plane"
        },
        "is_shipment": True,
        "shipped_at": "2023-11-20T10:20:30Z",
        "name": "Air Shipment Example",
        "country_code": "USA"
    }

    outputs = calculate_emissions(shipping_data)
    print(outputs)