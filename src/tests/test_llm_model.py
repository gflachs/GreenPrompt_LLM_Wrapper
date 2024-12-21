import unittest
import time
from src.app.llm_model import LLMModel

class TestLLMModel(unittest.TestCase):

    
    def test_init(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        self.assertEqual(llm.modeltyp, "text-generation")
        self.assertEqual(llm.model, "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertIsNone(llm.message)
        self.assertIsNone(llm.answer)
        self.assertIsNone(llm._prompt)
        self.assertEqual(llm.status, "idle")


    def test_download_model(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertEqual(llm.status, "idle")

        llm.download_model()
        self.assertIsNotNone(llm._pipe)
        self.assertEqual(llm.status, "ready")

        llm.download_model(attempt=4)
        
  
    def test_answer_question(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()

        math_question = "Whats 17 + 25?"
        expected_math_answer = "42"
        math_answer = llm.answer_question(math_question)
        
        question = "Whats the capitol of germany?"
        expected_answer = "Berlin"
        answer = llm.answer_question(question)

        self.assertIn(expected_math_answer, math_answer)
        self.assertIn(expected_answer, answer)  

    def test_isllmresponsive(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertFalse(llm._isllmresponsive())
        
        llm.download_model()
        self.assertTrue(llm._isllmresponsive())
        
    def test_isllmresponsive_unresponsive(self):
        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()
        llm.answer_question = lambda x: None 
        self.assertFalse(llm._isllmresponsive())

    def test_shutdownllm(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.shutdownllm()
        self.assertEqual(llm.status, "idle")

        llm.download_model()
        self.assertEqual(llm.status, "ready")

        max_allowed_time = 1
        start_time = time.time()
        llm.shutdownllm()
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertEqual(llm.status, "idle")
        self.assertLessEqual(elapsed_time, max_allowed_time, 
                             f"Shutdown performance test failed: elapsed time {elapsed_time:.2f}s exceeds {max_allowed_time:.2f}s")

    def test_restartllm(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.restartllm()
        self.assertEqual(llm.status, "idle")

        llm.download_model()
        self.assertEqual(llm.status, "ready")

        max_allowed_time = 60
        start_time = time.time()
        llm.restartllm()
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertEqual(llm.status, "ready")
        self.assertLessEqual(elapsed_time, max_allowed_time, 
                             f"Restart performance test failed: elapsed time {elapsed_time:.2f}s exceeds {max_allowed_time:.2f}s")

        llm.restartllm(attempt=3)
        self.assertEqual(llm.status, "failure")
             

if __name__ == '__main__':
    unittest.main()