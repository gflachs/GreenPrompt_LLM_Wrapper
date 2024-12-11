import gc
import logging
import psutil  # for memory monitoring

import torch
import asyncio
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
        self._status = "idle"
        self._process = psutil.Process()
        self._init_memory_usage = self._process.memory_info().rss

    _status_codes = {
        "not ready": " LLM Wrapper is not able to process prompts",
        "failure": "LLM Wrapper cannot deploy an LLM, or the deployed LLM is unable to process prompts despite repair attempts",
        "idle": "LLM Wrapper has no deployed LLM and is waiting for a new deployment",
        "ready": "LLM Wrapper has an LLM deployed and is ready to process prompts",
        "prompting": "LLM Wrapper is currently in use by the Prompting Service",
        "deploying": "LLM is currently being deployed to the Wrapper",
        "stopping": "LLM Wrapper is in the process of stopping its current LLM",
        "shutdown": "LLM Wrapper is being shut down",
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
                logging.info(
                    f"downloaded llm is unresposive try to restart attempt = {attempt + 1}"
                )
                if attempt <= 3:
                    self.restart(attempt=attempt + 1)
        except Exception as e:
            self._status = "failure"
            logging.error(
                f"Failed to download the LLM-Model {self.model} because of following Exception: {e}"
            )
            logging.error(f"{self._status_codes[self._status]}, model = {self.model}")



    def shutdown(self):
        """
        discards the llm and sets the wrapper to the same state as after initialization
        """
        if self.status == "idle":
            logging.info("Shutdown canceled: Wrapper is already idle.")
            return

        try:
            self._status = "stopping"
            del self._pipe
            gc.collect()
            self._pipe = None
            
            if (self._init_memory_usage * 1.2) < self._process.memory_info().rss: # current resource usage is greater than init usage + 20% than the shutdown wasn't succesfull
                
                logging.error(f"“Error when shutting down the llm {self.model}: shutdown wasn't succesfull") 
                self._status = "failure" 
            else:
                self._message = None
                self._answer = None
                self._prompt = None
                self._status = "idle"
                logging.info("shutdown llm")
                logging.info(f"Status: {self.status} - {self._status_codes[self.status]}")
        except Exception as e:
            logging.error(f"“Error when shutting down the llm: {e}")
            self._status = "failure"



    def restart(self, attempt=0):
        """
        Restarts the llm. If unable to restart the llm for instance the llm is unresponsive it will start another attempt.

        Args:
            attempt (int): number of attempt to restart the llm. Default is 0. If attempt >= 3 will set the Wrapper status to failure
        """
        if attempt >= 3:
            self._status = "failure"
            logging.error(f"failed to restart the llm number of attempts = {attempt}")
            logging.error(
                f"Status: {self.status} - {self._status_codes[self.status]}, model = {self.model}"
            )
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
            logging.error(f"Error when restarting the llm {self.model}, excepion: {e}")
            logging.error(f"Attempt {attempt + 1} failed. New attempt...")
            self.restart(attempt=attempt + 1)



    def answer_question(self, question):
        """
        generates an answer to the given question with the downloaded LLM

        Args:
            question (str): The question that should be answered by the llm.

        Returns:
            string: The answer
            or None: if no llm has been downloaded
        """
        logging.debug(question)

        if self._pipe is None:
            logging.info("No LLM in pipe")
            return

        self._message = [
            {"role": "user", "content": question},
        ]

        logging.info(f"new message forwarded to the llm - {self.message}")

        self._prompt = self._pipe.tokenizer.apply_chat_template(
            self.message, tokenize=False, add_generation_prompt=True
        )
        output = self._pipe(
            self._prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )
        parts = output[0]["generated_text"].split("<|assistant|>\n")
        if len(parts) > 1:
            self._answer = parts[1]
        else:
            self._answer = output[0]["generated_text"]

        return self.answer



    def _isresponsive(self):
        """
        Checks if the model can respond to queries.
        sends a prompt to the downloaded llm and returns true if the llm is returning an answer otherwise returns false

        Returns:
            bool: true if the llm can send answer questions otherwise false
        """
        example = "What's the capitol of germany?"
        logging.info("Überprüfung der Modellantwort mit Testfrage gestartet.")
        
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
    def status(self):
        return self._status
