import unittest
import src.app.wrapper.llm_wrapper_manager as manager
import json

class TestWrapperManager(unittest.TestCase):
    def test_wrapper_creation_with_config(self):
        config_path = "src/data/config_tinyllama.json"

        with open(config_path, 'r') as file:
            json_str = json.dumps(json.load(file))
            wrapper = manager.WrapperManager().create_wrapper(json_str)
        
        self.assertEqual(str(type(wrapper)), "<class 'src.app.wrapper.llm_wrapper.LLMWrapper'>")
        wrapper.llm.download_model()
        wrapper.start_monitoring()

        question = "Whats the most used currency in China?"
        answer = wrapper.get_answer(question)
        self.assertIn("yuan", answer.lower())
    
        wrapper.stop_monitoring()
        wrapper.shutdown_llm()
    
    
if __name__ == "__main__":
    unittest.main()