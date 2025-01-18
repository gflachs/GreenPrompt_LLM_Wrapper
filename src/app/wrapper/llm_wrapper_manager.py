import json
import logging

import torch

from src.app.wrapper.llm_model import (STATUS_FAILURE, STATUS_IDLE,
                                   STATUS_NOT_READY, STATUS_READY)
from src.app.wrapper.llm_wrapper import LLMWrapper

logging.basicConfig(
    filename="manager.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class WrapperManager:
    def create_wrapper(self, config: str):
        """creates a LLMWrapper Object based on a json structured config
        
        Args: 
            config (str): json formatted string containing the config data for the llm model from hugging face.

        Returns:
            LLMWrapper: LLMWrapper object with downloaded llm model
        """
        try:
            logging.info("Start of wrapper creation")
            config_data = json.loads(config)

            if not isinstance(config_data, dict):
                logging.error("Manager: Value Error because config is not of type dict")
                raise ValueError("The JSON-config needs to contain a dictionary.")

            # read args and kwargs
            model = config_data.get("model")
            modeltyp = config_data.get("modeltyp")
            uses_chat_template = {"uses_chat_template": config_data.get("uses_chat_template")}
            args = config_data.get("args", {})
            prompting_config = args.get("prompting", {})
            deployment_config = args.get("deployment", {})
        

            if not isinstance(args, dict):
                logging.error("Manager: Value Error because args is not of type dict")
                raise ValueError("The 'args'-key needs to contain a list.")

            if not isinstance(prompting_config, dict):
                logging.error("Manager: Value Error because prompting_config is not of type dict")
                raise ValueError("The 'prompting'-key needs to contain a dictionary.")
            
            if not isinstance(deployment_config, dict):
                logging.error("Manager: Value Error because deployment_config is not of type dict")
                raise ValueError("The 'deployment'-key needs to contain a dictionary.")
            
            if "torch_dtype" in deployment_config.keys():
                if isinstance(deployment_config["torch_dtype"], str) and deployment_config["torch_dtype"] == "torch.bfloat16":
                    deployment_config["torch_dtype"] = torch.bfloat16

            # call target function (create LLMWrapper with config)
            return LLMWrapper(model=model, modeltyp=modeltyp, prompting_config=prompting_config, deployment_config=deployment_config, **uses_chat_template)

        except json.JSONDecodeError:
            logging.error("Manager: Value Error because the given config '{config}' doesn`t contain a valid json structur.")
            raise ValueError(f"The given config '{config}' doesn`t contain a valid json structur.")