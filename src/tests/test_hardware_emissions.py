import unittest
from app.hardware_emissions import calculate_hardware_emissions

class TestHardwareEmissions(unittest.TestCase):
    def test_calculate_hardware_emissions(self):
        # Exemple : 200 kgCO2 sur une durée de 5 ans
        total_emissions_kg = 200
        lifetime_years = 5
        result = calculate_hardware_emissions(total_emissions_kg, lifetime_years)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

if __name__ == "__main__":
    unittest.main()
