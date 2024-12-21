import unittest
from src.app.llm_wrapper import LLMWrapper
from src.app.llm_model import STATUS_FAILURE, STATUS_IDLE, STATUS_NOT_READY, STATUS_READY
from unittest.mock import patch
import time

class TestLLMWrapper(unittest.TestCase):
    
    def test_shutdown_llm(self):
        wrapper = LLMWrapper(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        wrapper.shutdown_llm()
        wrapper.llm._status = STATUS_READY
        wrapper.shutdown_llm()
        wrapper.llm._status = STATUS_FAILURE
        wrapper.shutdown_llm()
        wrapper.llm._status = STATUS_IDLE
        wrapper.shutdown_llm()
    
    def test_restart_llm(self):
        wrapper = LLMWrapper(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        wrapper.restart_llm()
        wrapper.llm._status = STATUS_READY
        wrapper.restart_llm()
        wrapper.llm._status = STATUS_FAILURE
        wrapper.restart_llm()
        wrapper.llm._status = STATUS_IDLE
        wrapper.restart_llm()
        
    def test_get_answer(self):
        wrapper = LLMWrapper(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        wrapper.llm.download_model()

        math_question = "Whats 17 + 25?"
        expected_math_answer = "42"
        math_answer = wrapper.get_answer(math_question)
        
        question = "Whats the capitol of germany?"
        expected_answer = "Berlin"
        answer = wrapper.get_answer(question)

        self.assertIn(expected_math_answer, math_answer)
        self.assertIn(expected_answer, answer) 
        
    def test_start_monitoring(self):
        wrapper = LLMWrapper(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        wrapper.start_monitoring()
        wrapper.stop_monitoring() 

if __name__ == "__main__":
    unittest.main()