import requests

def get_carbon_intensity(region_code, api_key=None):
    """
    Fetch the carbon intensity for a given region in gCO2/kWh.
    :param region_code: Region code (e.g., DE for Germany, FR for France).
    :param api_key: API key for CO2 Signal. If None, a default value is used.
    :return: Carbon intensity in gCO2/kWh.
    """
    if api_key:
        try:
            # Replace with actual API endpoint for carbon intensity
            url = f"https://api.co2signal.com/v1/latest?region={region_code}"
            headers = {"auth-token": api_key}
            response = requests.get(url, headers=headers)
            data = response.json()
            return data["data"]["carbonIntensity"]
        except Exception as e:
            print(f"Error fetching carbon intensity: {e}")
    
    # Default values by region
    default_values = {
        "DE": 400,  # Germany
        "FR": 50,   # France
        "US": 300   # United States
    }
    return default_values.get(region_code.upper(), 500)  # Default: 500 gCO2/kWh
