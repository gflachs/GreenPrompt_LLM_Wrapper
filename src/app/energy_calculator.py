def calculate_energy_consumed(power_watts, duration_hours):
    """
    Calculate energy consumption in kWh.
    :param power_watts: Power consumption of the LLM hardware in watts.
    :param duration_hours: Duration of the operation in hours.
    :return: Energy consumed in kWh.
    """
    return (power_watts / 1000) * duration_hours
