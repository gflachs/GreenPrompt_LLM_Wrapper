import unittest
import time
from src.app.llm_model import LLMModel, STATUS_FAILURE, STATUS_IDLE, STATUS_READY, STATUS_NOT_READY

class TestLLMModel(unittest.TestCase):
    
    def test_init(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        self.assertEqual(llm.modeltyp, "text-generation")
        self.assertEqual(llm.model, "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertIsNone(llm.message)
        self.assertIsNone(llm.answer)
        self.assertIsNone(llm._prompt)
        self.assertEqual(llm.status, STATUS_NOT_READY)

    def test_download_model(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertEqual(llm.status, STATUS_NOT_READY)

        llm.download_model()
        self.assertIsNotNone(llm._pipe)
        self.assertEqual(llm.status, STATUS_READY)
        
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

    def test_isresponsive(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertFalse(llm._isresponsive())
        
        llm.download_model()
        self.assertTrue(llm._isresponsive())
        
    def test_isresponsive_unresponsive(self):
        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()
        llm.answer_question = lambda x: None 
        self.assertFalse(llm._isresponsive())

    def test_shutdown(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.shutdown()
        self.assertEqual(llm.status, STATUS_IDLE)

        llm.download_model()
        self.assertEqual(llm.status, STATUS_READY)

        max_allowed_time = 1
        start_time = time.time()
        llm.shutdown()
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertEqual(llm.status, STATUS_IDLE)
        self.assertLessEqual(elapsed_time, max_allowed_time,
                             f"Shutdown performance test failed: elapsed time {elapsed_time:.2f}s exceeds {max_allowed_time:.2f}s")

    def test_restart(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.restart()
        self.assertEqual(llm.status, STATUS_NOT_READY)

        llm.download_model()
        self.assertEqual(llm.status, STATUS_READY)

        max_allowed_time = 60
        start_time = time.time()
        llm.restart()
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertEqual(llm.status, STATUS_READY)
        self.assertLessEqual(elapsed_time, max_allowed_time, 
                             f"Restart performance test failed: elapsed time {elapsed_time:.2f}s exceeds {max_allowed_time:.2f}s")

        llm._restart_attempt = 3
        llm.restart()
        self.assertEqual(llm.status, STATUS_FAILURE)
             

if __name__ == '__main__':
    unittest.main()