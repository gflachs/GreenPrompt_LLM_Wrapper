import unittest
import src.app.llm_wrapper_manager as manager

class TestWrapperManager(unittest.TestCase):
    def test(self):
        config_path = "src/data/config_tinyllama.json"
        wrapper = manager.load_llm_config(config_path)
        wrapper.llm.download_model()
        wrapper.start_monitoring()

        question = "Whats the most used currency in China?"
        answer = wrapper.get_answer(question)
        self.assertIn("yuan", answer.lower())
    
        wrapper.stop_monitoring()
        wrapper.shutdown_llm()
    
    
if __name__ == "__main__":
    unittest.main()