import unittest
import psutil  # for memory monitoring
from src.app.llm_model import LLMModel

class TestLLMModelResourceUsage(unittest.TestCase):

    def test_shutdown_memory_release(self):
        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()

        # Memory utilization before shutdown
        process = psutil.Process()
        memory_before_shutdown = process.memory_info().rss 

        # Shutdown
        llm.shutdownllm()

        # Memory utilization after shutdown
        memory_after_shutdown = process.memory_info().rss

        # Check whether the memory requirement has decreased after the shutdown
        self.assertLess(memory_after_shutdown, memory_before_shutdown, 
                        "Memory usage after shutdown should be less than before.")
