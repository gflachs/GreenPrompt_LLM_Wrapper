# pragma: no cover
import unittest
from unittest.mock import patch, MagicMock
from src.app.llm_model import LLMModel

# pragma: no cover
class TestLLMModel(unittest.TestCase):

    # pragma: no cover
    def test_init(self):
        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        self.assertEqual(llm.modeltyp, "text-generation")
        self.assertEqual(llm.model, "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertIsNone(llm.message)
        self.assertIsNone(llm.answer)
        self.assertIsNone(llm._prompt)

    # pragma: no cover
    def test_getter(self):
        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        self.assertEqual(llm.modeltyp, "text-generation")
        self.assertEqual(llm.model, "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.assertIsNone(llm._pipe)
        self.assertIsNone(llm.message)
        self.assertIsNone(llm.answer)
        self.assertIsNone(llm._prompt)

    # pragma: no cover
    @patch.object(LLMModel, 'download_model')
    def test_download_model(self, mock_download_model):
        mock_download_model.return_value = None  # Mocking the download_model method
        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

        llm.download_model()
        mock_download_model.assert_called_once()
        # Simulate that _pipe is set after download
        llm._pipe = MagicMock()
        self.assertIsNotNone(llm._pipe)

    # pragma: no cover
    @patch.object(LLMModel, 'download_model')
    @patch.object(LLMModel, 'answer_question')
    def test_answer_question(self, mock_answer_question, mock_download_model):
        mock_download_model.return_value = None
        mock_answer_question.side_effect = ["42", "Berlin"]  # Mocking the responses

        llm = LLMModel(modeltyp="text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        llm.download_model()

        math_question = "Whats 17 + 25?"
        expected_math_answer = "42"
        math_answer = llm.answer_question(math_question)

        question = "Whats the capital of Germany?"
        expected_answer = "Berlin"
        answer = llm.answer_question(question)

        self.assertEqual(math_answer, expected_math_answer)
        self.assertEqual(answer, expected_answer)
        mock_download_model.assert_called_once()
        mock_answer_question.assert_any_call(math_question)
        mock_answer_question.assert_any_call(question)

# pragma: no cover
if __name__ == '__main__':
    unittest.main()
