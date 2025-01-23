import unittest
from app.carbon_intensity import get_carbon_intensity

class TestCarbonIntensity(unittest.TestCase):
    def test_get_carbon_intensity(self):
        # Mock API response (simule une réponse pour éviter un appel réel)
        region_code = "DE"  # Code pour l'Allemagne
        api_key = "your_api_key"  # Remplacer par une vraie clé pour un vrai test
        try:
            result = get_carbon_intensity(region_code, api_key)
            self.assertIsInstance(result, (int, float))
            self.assertGreater(result, 0)
        except Exception as e:
            self.fail(f"API call failed: {e}")

if __name__ == "__main__":
    unittest.main()
