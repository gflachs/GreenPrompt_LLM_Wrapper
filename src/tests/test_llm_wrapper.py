import time
import unittest
import datetime

import schedule

import src.app.llm_wrapper
from src.app.llm_model import (STATUS_FAILURE, STATUS_IDLE, STATUS_NOT_READY, STATUS_READY)
from src.app.llm_wrapper import LLMWrapper
import torch


modeltyp =  "text-generation"
model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
uses_chat_template =  {"uses_chat_template":True}

prompting =  {
    "max_new_tokens": 256, 
    "do_sample": True,
    "temperature": 0.7,
    "top_k": 50, 
    "top_p": 0.95}
deployment = {
    "torch_dtype": torch.bfloat16,
    "device_map": "auto"}


# global var for counting the number of function calls
call_count = 0

def mock_counter():
    """mocks the execution of the LLMWrapper.health_check_wrapper function and counts how often it was called"""
    global call_count
    call_count += 1

class TestLLMWrapper(unittest.TestCase):

    def test_init(self):
        wrapper = LLMWrapper(modeltyp=modeltyp, model = model, prompting_config=prompting, deployment_config=deployment, **uses_chat_template)
        self.assertTrue(wrapper._is_llm_healthy)
        self.assertIsNotNone(wrapper.llm)
        self.assertEqual(wrapper._max_timeout, 240, "Wrong max_timeout")
        self.assertIsNone(wrapper._continous_task)
        self.assertIsNone(wrapper._prompting_starting_time)
    
    def test_shutdown_llm(self):
        wrapper = LLMWrapper(modeltyp=modeltyp, model = model, prompting_config=prompting, deployment_config=deployment, **uses_chat_template)
        wrapper.shutdown_llm()
        wrapper.llm._status = STATUS_READY
        wrapper.shutdown_llm()
        wrapper.llm._status = STATUS_FAILURE
        wrapper.shutdown_llm()
        wrapper.llm._status = STATUS_IDLE
        wrapper.shutdown_llm()
    
    def test_restart_llm(self):
        wrapper = LLMWrapper(modeltyp=modeltyp, model = model, prompting_config=prompting, deployment_config=deployment, **uses_chat_template)
        wrapper.restart_llm()
        wrapper.llm._status = STATUS_READY
        wrapper.restart_llm()
        wrapper.llm._status = STATUS_FAILURE
        wrapper.restart_llm()
        wrapper.llm._status = STATUS_IDLE
        wrapper.restart_llm()
        
    def test_get_answer(self):
        wrapper = LLMWrapper(modeltyp=modeltyp, model = model, prompting_config=prompting, deployment_config=deployment, **uses_chat_template)
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
        wrapper = LLMWrapper(modeltyp=modeltyp, model = model, prompting_config=prompting, deployment_config=deployment, **uses_chat_template)
        wrapper.start_monitoring()

        wrapper._prompting_starting_time = 0
        time.sleep(70)
        self.assertTrue(wrapper._is_llm_healthy)

        wrapper._prompting_starting_time = None
        wrapper.llm._status = STATUS_FAILURE
        time.sleep(70)
        self.assertFalse(wrapper._is_llm_healthy, msg= f"failed at {datetime.datetime.now()}")

        wrapper.llm._status = STATUS_READY
        time.sleep(70)
        self.assertTrue(wrapper._is_llm_healthy)

        wrapper.stop_monitoring() 

    def setUp(self):
        """init the test_schedular_runs (is called befor each test but only necessary for test_schedular_runs)"""
        global call_count
        call_count = 0  # reset the counter to 0
        self.cease_event = None

        # schedule the mock_counter
        schedule.every(1).seconds.do(mock_counter)

    def tearDown(self):
        """finishes the schedular thread after each test (only used in test_scheduler_runs)"""
        if self.cease_event:
            self.cease_event.set()

    def test_scheduler_runs(self):
        """checks rather the scheduled task is performed after the call of run_continuosly"""
        # start the schedular defined in setUp
        self.cease_event = src.app.llm_wrapper.run_continuously(interval=0.5)

        time.sleep(3)  # delay to allow mutliple calls within the run_continuosly function

        # was the mock up function called at least two times? If yes the run_continuosly function works
        self.assertGreaterEqual(call_count, 2)

        # stop the schedular run in src.app.llm_wrapper.run_continuosly
        self.cease_event.set()


if __name__ == "__main__":
    unittest.main()