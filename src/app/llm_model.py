# pragma: no cover
import logging
import torch
from transformers import pipeline

# pragma: no cover
logging.basicConfig(
    filename="llm.log",  
    filemode="w",        
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LLMModel:
    def __init__(self, modeltyp, model):
        self._modeltyp = modeltyp
        self._model = model
        self._pipe = None
        self._message = None
        self._answer = None
        self._prompt = None

    
   
    def download_model(self):
        """
        downloads a model from huggingface via the api with self.modeltyp and self.model
        """
        try:
            self._pipe = pipeline(self.modeltyp, model= self.model, torch_dtype=torch.bfloat16, device_map="auto")
            logging.info("Successfully downloaded the desired model")
        except Exception as e:
            logging.error(f"Failed to download the LLM-Model {self.model} because of following Exception: {e}")
            


    def answer_question(self, question):
        """
        generates an answer to the given question with the downloaded LLM

        Args: 
            question (str): The question that should be answered by the llm.

        Retruns:
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
        
        self._prompt = self._pipe.tokenizer.apply_chat_template(self.message, tokenize=False, add_generation_prompt=True)
        output = self._pipe(self._prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        parts = output[0]["generated_text"].split("<|assistant|>\n")
        if len(parts) > 1:
            self._answer = parts[1]
        else:
            self._answer = output[0]["generated_text"]
        
        return self.answer
    

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
