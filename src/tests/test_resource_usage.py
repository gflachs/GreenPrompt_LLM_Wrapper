import unittest
import psutil  # for memory monitoring
from src.app.llm_model import LLMModel

class TestLLMModelResourceUsage(unittest.TestCase):

    def test_shutdown_memory_release(self):
       
        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        # Memory utilization before shutdown
        process = psutil.Process()
        memory_before_download = process.memory_info().rss 
        print(f"Speicherverbrauch vor downlaod: {memory_before_download / 1e6} MB")

        llm.download_model()
        memory_before_shutdown = process.memory_info().rss 
        print(f"Speicherverbrauch nach downlaod: {memory_before_shutdown / 1e6} MB")

        # Shutdown
        llm.shutdownllm()

        # Memory utilization after shutdown
        memory_after_shutdown = process.memory_info().rss
        print(f"Speicherverbrauch nach shutdown: {memory_after_shutdown / 1e6} MB")

        # Check whether the memory requirement has decreased after the shutdown
        self.assertLess(memory_after_shutdown, memory_before_shutdown, 
                        "Memory usage after shutdown should be less than before.")


if __name__ == '__main__':
    unittest.main()