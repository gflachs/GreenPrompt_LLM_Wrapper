import unittest
from app.energy_calculator import measure_energy

class TestEnergyCalculator(unittest.TestCase):
    def test_measure_energy(self):
        # Test avec une durée de 3600 secondes (1 heure)
        duration_seconds = 3600
        result = measure_energy(duration_seconds)
        # Vérifiez si le résultat est un float et raisonnable (valeur estimée ici)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

if __name__ == "__main__":
    unittest.main()
