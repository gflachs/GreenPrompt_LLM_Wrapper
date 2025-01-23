import unittest
from app.sci_calculator import calculate_sci

class TestSCICalculator(unittest.TestCase):
    def test_calculate_sci(self):
        # Données d'entrée fictives
        E = 0.5  # kWh
        I = 400  # gCO2/kWh
        M = 4.57  # gCO2
        R = 100  # Nombre d'unités fonctionnelles
        result = calculate_sci(E, I, M, R)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_calculate_sci_with_zero_r(self):
        E = 0.5
        I = 400
        M = 4.57
        R = 0  # Cas spécial : R = 0 doit lever une exception
        with self.assertRaises(ValueError):
            calculate_sci(E, I, M, R)

if __name__ == "__main__":
    unittest.main()
