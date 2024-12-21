import gc
import logging
import psutil  # for memory monitoring

import torch
from transformers import pipeline

logging.basicConfig(
    filename="llm.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class RestartError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class LLMModel:
    def __init__(self, modeltyp, model):
        self._modeltyp = modeltyp
        self._model = model
        self._pipe = None
        self._message = None
        self._answer = None
        self._prompt = None
        self._status = "not ready"  # Standardstatus auf "not ready" gesetzt
        self._process = psutil.Process()
        self._init_memory_usage = self._process.memory_info().rss

    _status_codes = {
        "not ready": "LLM Wrapper is not able to process prompts",
        "ready": "LLM Wrapper is ready to process prompts",  # Nur "ready" und "not ready"
    }

    def download_model(self, attempt=0):
        """
        downloads a model from huggingface via the api with self.modeltyp and self.model
        """
        try:
            self._pipe = pipeline(
                self.modeltyp,
                model=self.model,
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )
            if self._isresponsive():
                self._status = "ready"
                logging.info(f"{self._status_codes[self.status]}, model = {self.model}")
            else:
                logging.info(f"Downloaded LLM is unresponsive. Status set to 'not ready'.")
                self._status = "not ready"  # Status direkt hier setzen
        except Exception as e:
            self._status = "failure"
            logging.error(f"Failed to download the LLM-Model {self.model} because of following Exception: {e}")
            logging.error(f"{self._status_codes[self._status]}, model = {self.model}")

    def shutdown(self):
        """Tries to shut down the LLM and check resource usage."""
        try:
            self._status = "stopping"
            del self._pipe
            gc.collect()
            self._pipe = None

            # Erhöht den Grenzwert auf 30% anstatt 20%
            memory_threshold = self._init_memory_usage * 1.3

            if self._process.memory_info().rss > memory_threshold:
                logging.error(f"Shutdown failed: memory usage exceeds the threshold.")
                self._status = "failure"
            else:
                self._status = "idle"
                logging.info("Shutdown completed successfully.")
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")
            self._status = "failure"

    def restart(self, attempt=0):
        """Restarts the llm, attempts up to 3 times."""
        if attempt >= 3:
            self._status = "failure"
            logging.error(f"failed to restart the llm after {attempt} attempts.")
            return

        if self.status == "idle":
            logging.info("Restart not possible, because no LLM is running.")
            return

        try:
            logging.info(f"Restarting the llm (attempt {attempt + 1}).")
            self.shutdown()
            self._status = "not ready"
            self.download_model(attempt=attempt)
        except Exception as e:
            logging.error(f"Error when restarting the llm {self.model}, exception: {e}")
            logging.error(f"Attempt {attempt + 1} failed. Retrying...")
            self.restart(attempt=attempt + 1)

    def _isresponsive(self):
        """Checks if the model can respond to queries."""
        example = "What's the capital of Germany?"
        logging.info("Model responsiveness check started.")

        try:
            llmresponse = self.answer_question(example)

            if llmresponse is None:
                logging.warning(f"The model {self.model} did not provide any response.")
                return False
            if isinstance(llmresponse, str):
                logging.info(f"The model {self.model} successfully responded: {llmresponse}")
                return True

            logging.error(f"Unexpected response type from the model {self.model}: {type(llmresponse)}")
            return False
        except Exception as e:
            logging.error(f"Error during model responsiveness check: {e}")
            return False

    def answer_question(self, question):
        """Generates an answer to the given question with the downloaded LLM."""
        if self._pipe is None:
            logging.info("No LLM in pipe")
            return

        self._message = [{"role": "user", "content": question}]
        self._prompt = self._pipe.tokenizer.apply_chat_template(self._message, tokenize=False, add_generation_prompt=True)
        output = self._pipe(self._prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        parts = output[0]["generated_text"].split("<|assistant|>\n")
        if len(parts) > 1:
            self._answer = parts[1]
        else:
            self._answer = output[0]["generated_text"]

        return self.answer
