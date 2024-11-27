# pragma: no cover
import unittest
from app.llm_model import LLMModel

# pragma: no cover
class TestLLMModel(unittest.TestCase):

    # pragma: no cover
    def test_init(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        self.assertEqual(llm.modeltyp, "text-generation")
        self.assertEqual(llm.model, "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertIsNone(llm.message)
        self.assertIsNone(llm.answer)
        self.assertIsNone(llm._prompt)


    # pragma: no cover
    def test_getter(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        self.assertEqual(llm.modeltyp, "text-generation")
        self.assertEqual(llm.model, "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertIsNone(llm.message)
        self.assertIsNone(llm.answer)
        self.assertIsNone(llm._prompt)


    # pragma: no cover
    def test_download_model(self):
        llm = LLMModel(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)

        llm.download_model()
        self.assertIsNotNone(llm._pipe)
        
    # pragma: no cover
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

# pragma: no cover
if __name__ == '__main__':
    unittest.main()
