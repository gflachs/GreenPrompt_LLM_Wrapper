import json
from src.app.llm_wrapper import LLMWrapper
import torch

class WrapperManager:
    def create_wrapper(self, config):
        """creates an LLMWrapper Object based on a json structured config"""

        try:
            config_data = json.load(config)

            if not isinstance(config_data, dict):
                raise ValueError("The JSON-config needs to contain a dictionary.")

            # read args and kwargs
            model = config_data.get("model")
            modeltyp = config_data.get("modeltyp")
            uses_chat_template = {"uses_chat_template": config_data.get("uses_chat_template")}
            args = config_data.get("args", {})
            prompting_config = args.get("prompting", {})
            deployment_config = args.get("deployment", {})
        

            if not isinstance(args, dict):
                raise ValueError("The 'args'-key needs to contain a list.")

            if not isinstance(prompting_config, dict):
                raise ValueError("The 'prompting'-key needs to contain a dictionary.")
            
            if not isinstance(deployment_config, dict):
                raise ValueError("The 'deployment'-key needs to contain a dictionary.")
            
            if "torch_dtype" in deployment_config.keys():
                if isinstance(deployment_config["torch_dtype"], str) and deployment_config["torch_dtype"] == "torch.bfloat16":
                    deployment_config["torch_dtype"] = torch.bfloat16

            # call target function (create LLMWrapper with config)
            return LLMWrapper(model=model, modeltyp=modeltyp, prompting_config=prompting_config, deployment_config=deployment_config, **uses_chat_template)

        except json.JSONDecodeError:
            raise ValueError(f"The given config '{config}' doesn`t contain a valid json structur.")