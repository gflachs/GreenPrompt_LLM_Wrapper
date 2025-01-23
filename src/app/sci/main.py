#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import time

def estimate_energy_cpu(tpw_watts, duration_s):
    """
    Estimates the CPU energy consumption over 'duration_s' seconds,
    based on CPU usage and nominal power (TPW/RPW/TDP).
    Returns E in kWh (kilowatt-hours).
    """
    usage_samples = []
    sampling_interval = 1  # sample every 1 second

    for _ in range(duration_s):
        cpu_percent = psutil.cpu_percent(interval=sampling_interval)
        usage_samples.append(cpu_percent)

    # Average CPU usage over the period
    avg_cpu_usage_percent = sum(usage_samples) / len(usage_samples)
    
    # Approximate average power (Watts)
    power_avg_watts = tpw_watts * (avg_cpu_usage_percent / 100.0)
    
    # Convert duration from seconds to hours
    duration_h = duration_s / 3600.0

    # Energy in Wh
    wh_consumed = power_avg_watts * duration_h
    
    # Convert Wh to kWh (1 kWh = 1000 Wh)
    kwh_consumed = wh_consumed / 1000.0
    return kwh_consumed


def get_grid_intensity(country_code):
    """
    Returns the carbon intensity (gCO₂/kWh) based on the country code.
    If not found, returns a default value (e.g., 300 gCO₂/kWh).
    
    Note: In a real-world scenario, you could call an API (e.g., Electricity Maps)
    to get real-time data or use a broader lookup table.
    """
    # Indicative average values for demonstration
    intensities = {
        "DE": 300,  # Germany (example)
        "FR": 60,   # France (example)
        "US": 400,  # United States (variable)
        "CN": 600   # China (example)
    }

    # Normalize input to uppercase and strip
    country_code = country_code.upper().strip()

    # Return the matched value or a default (300 gCO₂/kWh if not found)
    return intensities.get(country_code, 300)


def calculate_hardware_carbon(E_kwh, I_gco2_per_kwh):
    """
    Calculates the hardware emissions (M) in a simplified manner:
    M = E * I.
    Returns M in grams of CO₂.
    """
    return E_kwh * I_gco2_per_kwh


def calculate_sci(E_kwh, I_gco2_per_kwh, M_gco2, R):
    """
    Calculates SCI:
        SCI = ((E * I) + M) / R
    - E: kWh
    - I: gCO₂/kWh
    - M: gCO₂
    - R: result metric (e.g., number of requests)
    
    Returns SCI (gCO₂ per unit).
    """
    usage_carbon = E_kwh * I_gco2_per_kwh  # gCO₂
    total_carbon = usage_carbon + M_gco2   # gCO₂
    sci = total_carbon / R
    return sci


def main():
    print("===================================================")
    print("       Welcome to the SCI Calculation Tool         ")
    print("===================================================")

    # 1) Ask for the CPU's nominal power
    while True:
        try:
            tpw_input = input("\n1) Please enter your CPU's nominal power (in Watts): ")
            tpw_watts = float(tpw_input)
            if tpw_watts <= 0:
                raise ValueError("The value must be positive.")
            break
        except ValueError as e:
            print(f"Invalid value: {e}")

    # 2) Ask for the duration in seconds
    while True:
        try:
            duration_input = input("2) Please enter the duration (in seconds) for which the software ran: ")
            duration_s = int(duration_input)
            if duration_s <= 0:
                raise ValueError("The duration must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid value: {e}")

    # => Compute E (in kWh)
    E_kwh = estimate_energy_cpu(tpw_watts, duration_s)
    print(f"\nEstimated CPU energy consumption (E): {E_kwh:.6f} kWh")

    # 3) Ask for the country code to determine carbon intensity
    country_code = input("\n3) Which country are you in? (e.g., DE, FR, US...). "
                         "If unknown, DE (Germany) will be used by default: ")
    if not country_code:
        country_code = "DE"  # default
    I_gco2_per_kwh = get_grid_intensity(country_code)
    print(f"Carbon intensity (I) for {country_code.upper()} = {I_gco2_per_kwh} gCO₂/kWh")

    # 4) Calculate M (hardware carbon) = E * I (simplified)
    M_gco2 = calculate_hardware_carbon(E_kwh, I_gco2_per_kwh)
    print(f"\nM (hardware carbon) = E * I = {M_gco2:.4f} gCO₂")

    # 5) Ask for R (number of results)
    while True:
        try:
            r_input = input("\n5) Please enter the number of 'results' (e.g., requests handled): ")
            R = int(r_input)
            if R <= 0:
                raise ValueError("The number must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid value: {e}")

    # 6) Calculate SCI
    sci_score = calculate_sci(E_kwh, I_gco2_per_kwh, M_gco2, R)

    print("\n===================================================")
    print(f"  SCI = ((E * I) + M) / R  = {sci_score:.6f} gCO₂ per unit")
    print("===================================================")

    # -----------------------------
    # Write the results to a .log file
    # -----------------------------
    log_filename = "sci_score.log"
    current_time = time.ctime()

    try:
        with open(log_filename, "a") as log_file:
            log_file.write(f"=== SCI Calculation Log Entry ===\n")
            log_file.write(f"Timestamp: {current_time}\n")
            log_file.write(f"CPU Nominal Power (W): {tpw_watts}\n")
            log_file.write(f"Measurement Duration (s): {duration_s}\n")
            log_file.write(f"Country Code: {country_code.upper()}\n")
            log_file.write(f"Grid Intensity (gCO₂/kWh): {I_gco2_per_kwh}\n")
            log_file.write(f"Estimated CPU Energy (kWh): {E_kwh:.6f}\n")
            log_file.write(f"Hardware Carbon (M) (gCO₂): {M_gco2:.4f}\n")
            log_file.write(f"Result Metric (R): {R}\n")
            log_file.write(f"SCI Score (gCO₂/unit): {sci_score:.6f}\n")
            log_file.write("=================================\n\n")
        print(f"\n(Logged SCI score to '{log_filename}')")
    except Exception as e:
        print(f"Error writing to log file: {e}")


if __name__ == "__main__":
    main()
