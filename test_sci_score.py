import unittest
from sci_score import calculate_sci_score

class TestSCIScore(unittest.TestCase):
    def test_calculate_sci_score(self):
        prompt = "exemple: What is the capital of France?"
        response = "exemple The capital of France is Paris."
        score = calculate_sci_score(prompt, response)
        self.assertGreater(score, 0)

    def test_invalid_input(self):
        prompt = ""
        response = "Invalid response"
        score = calculate_sci_score(prompt, response)
        self.assertEqual(score, 0.0)

if __name__ == '__main__':
    unittest.main()
