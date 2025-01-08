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

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{config_path}' wasn`t found.")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{config_path}' doesn`t contain a valid json strucutr.")


if __name__ == "__main__":
    config_path = "src/data/config_tinyllama.json"
    wrapper = load_llm_config(config_path)
    wrapper.llm.download_model()
    wrapper.start_monitoring()

    question = "Whats the most used currency in China?"
    answer = wrapper.get_answer(question)
    print(answer)
    
    wrapper.stop_monitoring()
    wrapper.shutdown_llm()