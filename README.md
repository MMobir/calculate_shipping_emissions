## Getting Started

Follow these instructions to set up the project, obtain the required API keys, and run the application.

### Prerequisites

1. **Python 3.12.3**: Ensure that you have Python 3.12.3 installed on your machine.

### Installation

1. **Clone the Repository**

   Clone the repository to your local machine using the following command:

   ```sh
   git clone https://github.com/yourusername/repository.git

2. **Set Up the Virtual Environment** 
    Create and activate a virtual environment to manage your dependencies:
    ```sh
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

3. **Install Dependencies**
    Install the required packages using the provided requirements.txt file:
    ```sh
    pip install -r requirements.txt

### Configuration

1. **Obtain a Mapbox API Access Token**
   - Sign up for a Mapbox account at [mapbox.com](https://www.mapbox.com/).
   - Navigate to the Tokens page and create a new token.

2. **Set Up Configuration**

   Add your Mapbox API access token to the `config/config.json` file:

   ```json
   {
       "MAPBOX_ACCESS_TOKEN": "your_mapbox_access_token_here"
   }
### Contact information
Feel free to reach out for further information: mahmoudmobir@gmail.com

## Methdology statement

Our carbon emissions calculator offers a streamlined and comprehensive approach to estimating the carbon footprint of various transportation methods. This methodology is designed to be robust, transparent, and adaptable to various transport scenarios, leveraging the latest international standards and technological advancements. Below is a detailed overview of our methodology and ho it differs from existing solutions like Lune.

### Accreditation

In order to get accreditation against the [GLEC Framework](https://www.smartfreightcentre.org/en/our-programs/global-logistics-emissions-council/), please reach out to [Smart Freight Center](https://smartfreightcentre.org/en/)

### Methodology Overview

Our emissions calculations follow the [GHG Protocol](https://ghgprotocol.org/) and the [GLEC Framework](https://www.smartfreightcentre.org/en/our-programs/global-logistics-emissions-council/). The methodology involves the following steps:

#### Inputs

1. **Route**: Distance in km/miles/nm or point-to-point coordinates.
2. **Shipment**: Cargo weight in kg, metric tonnes, or TEUs.
3. **Method**: Mode of transport.

#### Calculation Steps

1. **Calculate the Route**
    - If the distance is provided directly, we use it (converting miles or nautical miles to kilometers, if necessary).
    - If a route between two places is provided:
        - **Determine Coordinates**:
            - For ports, airports, or railway stations, we use their geographic coordinates.
                - if UN/LOCODE are provided, convert them into geographic coordinates using [UN/LOCODE database](https://service.unece.org/trade/locode/).
                - if Airport code provided, convert it into geographic coordinates using this [open source data source](https://github.com/ip2location/ip2location-iata-icao)
            - For addresses, we convert the address to coordinates using [Mapbox](https://www.mapbox.com/).
            - If coordinates are provided directly, we use them as is.
        - **Calculate Distance**:
            - **Land**: Use Mapbox to determine the distance between coordinates.
            - **Air**: Use Great Circle Distance.
            - **Sea**: Use a custom algorithm (Shorter Feasible Distance) based on the [Pub. 151](https://msi.nga.mil/api/publications/download?key=16694076/SFH00000/Pub151bk.pdf). If the algorithm fails, fall back to Great Circle Distance multiplied by 2.0.
    - If transshipment information is provided, map it to one of the transhipment emission factors supported by the GLEC framework: Transshipment, Storage + transshipment, Warehouse, Liquid buk terminal, Maritime container terminal. If not specified by the user, we assume **ambient** temperature related emission factors at logistical hubs.
2. **Convert Shipment Information**
    - If the mass is provided in kg or tonnes, convert it directly to tonnes.
    - If the shipment is in TEUs, convert based on the specified cargo type (container_only, lightweight, average, heavyweight).
3. **Calculate Emissions Intensity Factor for the Method**
    - **Emission Factors**: All emission factors are extracted from the [GLEC Framework](https://smart-freight-centre-media.s3.amazonaws.com/documents/GLEC_FRAMEWORK_v3_UPDATED_02_04_24.pdf) (Part 3: Data, pages 75-124). These factors will be updated if there is an update to the GLEC framework.
    - **Simple Methods**: Trucks, planes, trains, etc.
        - **Direct Emissions**: Constant intensity.
        - **Airplane Emissions**: Based on distance:
            - Short Haul: Up to 1600 km.
            - Long Haul: Over 1600 km.
        - **Electricity Emissions**: Based on country-specific electricity mix and default intensity factors.
    - **Advanced Methods**: Sea transport with detailed methodologies for various vessel types and conditions. These are documented in separate detailed methodology documents.
4. **Complete Carbon Emissions Calculation**
    - Multiply total mass, total distance, and intensity factor, converting the result into Tonnes of CO2e.

### Detailed Methodologies

#### Emission Factors

All emission factors are extracted from the [GLEC Framework](https://smart-freight-centre-media.s3.amazonaws.com/documents/GLEC_FRAMEWORK_v3_UPDATED_02_04_24.pdf) (Part 3: Data, pages 75-124). The factors cover various modes of transport and are updated in accordance with any updates to the GLEC framework. This ensures our calculations remain accurate and aligned with the latest standards.

[Simple Shipping Methods](docs/SimpleShippingMethods.md)

[Transshipment emission factors](docs/TransshipmentEmissionsFactors.md)

#### Sea Transport Methods

Our methodology for sea transport is detailed in specific documents for different types of sea transport:

[Sea Shipping Methods](docs/SeaShippingMethods.md)

[Container Shipping Methods](docs/ContainerShippingMethods.md)

[Identified Shipping Method](docs/IdentifiedShippingMethods.md)

#### Air Transport Emissions Differentiation

For air transport, we differentiate emissions based on the distance traveled:

- **Short Haul**: Up to 1600 km.
- **Long Haul**: Over 1600 km.

This method ensures accurate emission estimates without requiring detailed input from the user about the aircraft type.

### Example Calculation

#### Input Data

```json
{
    "shipment": {
        "mass": {
            "amount": 2000.0,
            "unit": "kg"
        }, 
        "transshipment": "Warehouse"
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
    "is_shipment": true,
    "shipped_at": "2023-11-20T10:20:30Z",
    "name": "Air Shipment Example",
    "country_code": "USA"
}
```

Output

```json
{
    "id": "unique_emission_calculation_id",
    "is_shipment": true,
    "shipped_at": "2023-11-20T10:20:30Z",
    "emissions-mass": {
        "amount": "1245536.5542370558",
        "unit": "kgCO2e"
    },
    "mass": {
        "amount": 2.0,
        "unit": "t"
    },
    "distance": {
        "amount": 4151.788514123519,
        "unit": "km",
        "distance_calculation_method": "great_circle_distance"
    },
    "emission_factor": {
        "methodology": "cargo_plane_long_haul",
        "emission_factor": 150.0,
        "unit": "kgCO2e"
    },
    "idempotency_key": null,
    "request": {
        "shipment": {
            "containers": null,
            "cargo_type": "average",
            "mass": {
                "amount": 2000.0,
                "unit": "kg"
            }
        },
        "route": {
            "distance": null,
            "source": {
                "address": null,
                "coordinates": null,
                "locode": null,
                "airport_code": "JFK"
            },
            "destination": {
                "address": null,
                "coordinates": null,
                "locode": null,
                "airport_code": "SFO"
            }
        },
        "method": {
            "method": "cargo_plane",
            "fuel": null,
            "load": null,
            "trade_lane": null
        },
        "is_shipment": true,
        "shipped_at": "2023-11-20T10:20:30Z",
        "name": "Air Shipment Example",
        "country_code": null,
        "idempotency_key": null
    }
}

```