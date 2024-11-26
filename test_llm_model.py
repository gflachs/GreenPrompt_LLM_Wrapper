import unittest
from llm_model import LLMModel

class TestLLMModel(unittest.TestCase):

    def test_successull_download(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()
        self.assertIsNotNone(llm._pipe)
        

    def test_simple_calculation(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()

        question = "Whats 17 + 25?"
        expected_answer = "42"
        answer = llm.answer_question(question)
        self.assertIn(expected_answer, answer)
        

    def test_simple_question(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()
        
        question = "Whats the capitol of germany?"
        expected_answer = "Berlin"
        answer = llm.answer_question(question)
        self.assertIn(expected_answer, answer)

    
    def test_no_model_downloaded(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)


if __name__ == '__main__':
    unittest.main()
