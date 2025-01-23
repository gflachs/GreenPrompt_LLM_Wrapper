def calculate_hardware_emissions(emissions_kg, lifetime_years):
    """
    Calculate the hardware emissions per hour in gCO2.
    :param emissions_kg: Total emissions for the hardware in kgCO2.
    :param lifetime_years: Hardware lifetime in years.
    :return: Emissions per hour in gCO2.
    """
    # Convert lifetime to total hours
    total_hours = lifetime_years * 365 * 24
    # Convert emissions to grams and calculate per hour
    emissions_per_hour = (emissions_kg * 1000) / total_hours
    return emissions_per_hour
