import os
import json
import sys
import pandas as pd

# Define paths to data files
data_dir = os.path.join(os.path.dirname(__file__), '../data')
emission_factors_file_path = os.path.join(data_dir, 'emission_factors.xlsx')

# Load the emission factors from the provided Excel file
electricity_intensity_df = pd.read_excel(emission_factors_file_path, sheet_name='electricity_intensity')
emission_factors_df = pd.read_excel(emission_factors_file_path, sheet_name='emission_factors')

def get_emission_factor(method: dict, distance: float, country_code=None):
    """
    Fetch the emission factor for the given method and country code.

    Parameters:
    - method (dict): Dictionary containing method information.
    - distance (float): Distance traveled.
    - country_code (str, optional): The country code for electricity intensity.

    Returns:
    - float: Emission factor for the specified method.
    - str: Calculation method used.
    """
    try:
        method_name = method.get('method')
        fuel = method.get('fuel')
        load = method.get('load')
        trade_lane = method.get('trade_lane')

        if 'plane' in method_name:
            if distance > 1600:
                method_name = f"{method_name}_long_haul"
            else:
                method_name = f"{method_name}_short_haul"

        emission_factor_calculation_method = method_name

        query = emission_factors_df['method'] == method_name
        is_electric = emission_factors_df.loc[emission_factors_df['method'] == method_name, 'is_electric'].values[0]

        if fuel:
            query = query & (emission_factors_df['fuel'] == fuel)
        if load:
            query = query & (emission_factors_df['load'] == load)
        if trade_lane:
            query = query & (emission_factors_df['trade_lane'] == trade_lane)

        matching_rows = emission_factors_df[query]

        if matching_rows.empty:
            raise ValueError(f"Emission factor for method {method_name}, fuel {fuel}, load {load} not found.")

        if len(matching_rows) > 1:
            emission_factor = matching_rows['emission_factor'].mean()
        else:
            emission_factor = matching_rows['emission_factor'].values[0]

        if is_electric.lower() == "yes":
            if country_code:
                electricity_intensity = get_electricity_intensity(electricity_intensity_df, country_code=country_code)
            else:
                electricity_intensity = get_electricity_intensity(electricity_intensity_df)
            emission_factor *= electricity_intensity

        return emission_factor, emission_factor_calculation_method

    except KeyError as e:
        raise ValueError(f"Required column is missing: {e}")
    except IndexError:
        raise ValueError(f"Method {method_name} not found in emission factors.")
    except Exception as e:
        raise ValueError(f"An error occurred while fetching the emission factor: {e}")


def get_electricity_intensity(electricity_intensity_df, country_code=None):
    """
    Fetch the electricity intensity for the given region.

    Parameters:
    - electricity_intensity_df (pd.DataFrame): DataFrame containing electricity intensity data.
    - country_code (str, optional): The country code for which to fetch the electricity intensity.

    Returns:
    - float: The electricity intensity for the specified region or the global average if the region is not found or not provided.
    """
    if country_code:
        try:
            intensity = electricity_intensity_df.loc[
                electricity_intensity_df['country_code'] == country_code, 'value'].values[0]
        except IndexError:
            # Fall back to global average if country code not found
            intensity = electricity_intensity_df.loc[
                electricity_intensity_df['country_code'] == 'global_average', 'value'].values[0]
    else:
        # Fall back to global average if country code not provided
        intensity = electricity_intensity_df.loc[
            electricity_intensity_df['country_code'] == 'global_average', 'value'].values[0]
    return intensity

if __name__ == "__main__":
    # Example usage
    method = {
        "method": "cargo_plane"
    }
    distance = 3500.0
    country_code = "USA"

    emission_factor, method_used = get_emission_factor(method, distance, country_code)

    print(f"Emission Factor: {emission_factor} kgCO2e/km")
    print(f"Calculation Method: {method_used}")