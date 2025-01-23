from app.energy_calculator import calculate_energy_consumed
from app.carbon_intensity import get_carbon_intensity
from app.hardware_emissions import calculate_hardware_emissions

def main():
    print("\n=== Welcome to the SCI-Score Calculator ===")
    print("This tool calculates the carbon impact of your LLM model.\n")

    # Step 1: LLM Selection
    llm_profiles = {
        1: {"name": "GPT-3", "power": 500, "emissions_kg": 200, "lifetime_years": 5},
        2: {"name": "GPT-J", "power": 350, "emissions_kg": 150, "lifetime_years": 4},
        3: {"name": "TinyLlama", "power": 200, "emissions_kg": 100, "lifetime_years": 6},
    }

    print("Select the LLM model you are using:")
    for key, value in llm_profiles.items():
        print(f"{key}. {value['name']} - Estimated power consumption: {value['power']}W")

    while True:
        try:
            choice = int(input("\nEnter the number corresponding to your LLM model: "))
            if choice in llm_profiles:
                llm = llm_profiles[choice]
                print(f"\nYou selected: {llm['name']}")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Please enter a valid number.")

    # Step 2: Display the SCI Formula
    print("\nThe formula used to calculate the SCI-Score is:")
    print("SCI = ((E * I) + M) / R")
    print("Where:")
    print("E = Energy consumed (in kWh)")
    print("I = Carbon intensity (in gCO2/kWh)")
    print("M = Hardware emissions (in gCO2)")
    print("R = Functional units (e.g., number of requests or users)\n")

    # Step 3: Calculate Energy Consumed (E)
    num_requests = int(input("Enter the number of requests your model will process: "))
    avg_runtime_per_request = 0.02  # Average runtime per request in hours
    duration_hours = num_requests * avg_runtime_per_request
    E = calculate_energy_consumed(llm["power"], duration_hours)
    print(f"Energy consumed (E): {E:.2f} kWh\n")

    # Step 4: Calculate Carbon Intensity (I)
    region_code = input("Enter the region code (e.g., DE for Germany, FR for France): ")
    I = get_carbon_intensity(region_code)
    print(f"Carbon intensity (I): {I:.2f} gCO2/kWh\n")

    # Step 5: Calculate Hardware Emissions (M)
    M = calculate_hardware_emissions(llm["emissions_kg"], llm["lifetime_years"])
    print(f"Hardware emissions (M): {M:.2f} gCO2\n")

    # Step 6: Functional Units (R)
    R = num_requests
    print(f"Functional units (R): {R}\n")

    # Step 7: Calculate SCI-Score
    sci_score = ((E * I) + M) / R
    print("\n=== Final Result ===")
    print(f"SCI-Score for {llm['name']}: {sci_score:.2f} gCO2 per functional unit\n")


if __name__ == "__main__":
    main()
