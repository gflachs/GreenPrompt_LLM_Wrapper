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

STATUS_NOT_READY = "not ready"
STATUS_READY = "ready"
STATUS_FAILURE = "failure"
STATUS_IDLE = "idle"

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
        self._status = STATUS_NOT_READY# Standardstatus auf "not ready" gesetzt
        self._process = psutil.Process()
        self._init_memory_usage = self._process.memory_info().rss
        self._restart_attempt = 0

    _status_codes = {
        "not ready": "LLM Wrapper is not able to process prompts",
        "ready": "LLM Wrapper is ready to process prompts",  # Nur "ready" und "not ready"
        "failure": "LLM Wrapper cannot deploy an LLM, or the deployed LLM is unable to process prompts despite repair attempts",
        "idle": "LLM Wrapper has no deployed LLM and is waiting for a new deployment"
    }

    def download_model(self):
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
                self._status = STATUS_READY
                self._restart_attempt = 0
                logging.info(f"{self._status_codes[self.status]}, model = {self.model}")
            else:
                self._status = STATUS_NOT_READY 
                logging.info(f"Downloaded LLM is unresponsive. Status set to '{self.status}'.")
        except Exception as e:
            self._status = STATUS_FAILURE
            logging.error(f"Failed to download the LLM-Model {self.model} because of following Exception: {e}")
            logging.error(f"{self._status_codes[self._status]}, model = {self.model}")

    def shutdown(self):
        """Tries to shut down the LLM and check resource usage."""
        try:
            self._status = STATUS_NOT_READY
            del self._pipe
            gc.collect()
            self._pipe = None

            # Erhöht den Grenzwert auf 40% anstatt 20%
            memory_threshold = self._init_memory_usage * 1.4

            if self._process.memory_info().rss > memory_threshold:
                logging.error(f"Shutdown failed: memory usage of {self._process.memory_info().rss / 1e6} MBexceeds the threshold of {memory_threshold / 1e6} MB.")
                self._status = STATUS_FAILURE
            else:
                self._status = STATUS_IDLE
                logging.info("Shutdown completed successfully.")
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")
            self._status = STATUS_FAILURE

    def restart(self):
        """Restarts the llm, attempts up to 3 times."""
        if self._restart_attempt >= 3:
            self._status = STATUS_FAILURE
            logging.error(f"failed to restart the llm after {self._restart_attempt} attempts.")
            return

        if self.status == STATUS_IDLE or self._pipe is None:
            logging.info("Restart not possible, because no LLM is running.")
            return

        try:
            self._restart_attempt +=  1
            logging.info(f"Restarting the llm (attempt {self._restart_attempt}).")
            self.shutdown()
            self.download_model()
        except Exception as e:
            logging.error(f"Error when restarting the llm {self.model}, exception: {e}")
            logging.error(f"Attempt {self._restart_attempt} failed. Retrying...")
            self.restart()

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
        self._prompt = question #self._pipe.tokenizer.apply_chat_template(self.message, tokenize=False, add_generation_prompt=True)
        output = self._pipe(self.prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        # parts = output[0]["generated_text"].split(question)
        parts = output[0]["generated_text"][output[0]["generated_text"].find(question)+len(question):]
        #if len(parts) > 1:
        #    self._answer = parts[1]
        #else:
        #   self._answer = output[0]["generated_text"]
        a = parts.strip("\n")
        return f"output (unstriped): {output} \n\nstripped: {a}"
    
    @property
    def modeltyp(self):
        return self._modeltyp

    @property
    def model(self):
        return self._model

    @property
    def message(self):
        return self._message

    @property
    def answer(self):
        return self._answer

    @property
    def prompt(self):
        return self._prompt

    @property
    def status(self):
        return self._status
