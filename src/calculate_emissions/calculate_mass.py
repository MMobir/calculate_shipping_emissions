import re
from typing import Optional

def calculate_shipment_mass(shipment: dict) -> float:
    """
    Calculate the mass of the shipment.

    Parameters:
    shipment (dict): The shipment details.

    Returns:
    float: The mass of the shipment in tonnes.
    """
    
    # Conversion factors for cargo types
    cargo_conversion = {
        'lightweight': 6.0,
        'average': 10.0,
        'heavyweight': 14.5,
        'container_only': 2.0
    }
    
    mass_info = shipment.get('mass')
    containers = shipment.get('containers')
    cargo_type = shipment.get('cargo_type', 'average')
    
    if mass_info:
        mass = mass_info['amount']
        unit = mass_info['unit']
        
        # Convert mass to tonnes
        if unit == 'g':
            mass = mass / 1e6  # grams to tonnes
        elif unit == 'kg':
            mass = mass / 1e3  # kilograms to tonnes
        # if unit is 't', no conversion needed

        return mass

    if containers:
        if cargo_type not in cargo_conversion:
            cargo_type = 'average'  # default cargo type
        
        mass = containers * cargo_conversion[cargo_type]

        return mass

    raise ValueError("Either mass or containers must be provided.")

if __name__ == "__main__":
    # Example usage
    shipment = {
        "mass": {
            "amount": 5,
            "unit": "g"
        }
    }

    mass = calculate_shipment_mass(shipment)
    print(f"Calculated Shipment Mass: {mass} tonnes")