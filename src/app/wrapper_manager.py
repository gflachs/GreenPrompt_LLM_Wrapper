import json
from src.app.llm_wrapper import LLMWrapper
import torch

# everything within this manager could or should be taken to the LLMWrapper class or at least be made a class within the same script

def load_llm_config(config_path):
    """Loads the configuration from a JSON file."""

    try:
        # read json config file
        with open(config_path, 'r') as file:
            config_data = json.load(file)

        if not isinstance(config_data, dict):
            raise ValueError("The JSON-config needs to contain a dictionary.")

        # read args and kwargs
        args = config_data.get("args", [])
        kwargs = config_data.get("kwargs", {})

        if not isinstance(args, list):
            raise ValueError("The 'args'-key needs to contain a list.")

        if not isinstance(kwargs, dict):
            raise ValueError("The 'kwargs'-key needs to contain a dictionary.")
        
        if isinstance(kwargs["torch_dtype"], str) and kwargs["torch_dtype"] == "torch.bfloat16":
            kwargs["torch_dtype"] = torch.bfloat16

        # call target function (create LLMWrapper with config)
        return LLMWrapper(*args, **kwargs)

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{config_path}' wasn`t found.")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{config_path}' doesn`t contain a valid json strucutr.")


if __name__ == "__main__":
    config_path = "src/data/test_config.json"
    wrapper = load_llm_config(config_path)
    wrapper.llm.download_model()
    wrapper.start_monitoring()

    question = "How many people live in the capitol of germany?"
    answer = wrapper.get_answer(question)
    print(answer)
    
    wrapper.stop_monitoring()
    wrapper.shutdown_llm()