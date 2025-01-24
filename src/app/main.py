import json
import logging
import time
from typing import Any, Dict, List, Tuple


from fastapi import FastAPI

from src.app.models.request import ModelConfig, Prompt, PromptResponse
from src.app.wrapper.llm_wrapper_manager import WrapperManager
from src.app.sci.sci_score import start_calc_sci_score, end_calc_sci_score

logging.basicConfig(
    filename="app.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

SUCCESS = "success"
FAILURE = "failure"
ERROR = "error"
STATUS_NOT_READY = "not ready"
STATUS_READY = "ready"
STATUS_FAILURE = "failure"
STATUS_IDLE = "idle"

app = FastAPI(title="LLM Wrapper Command API")

global wrapper
wrapper = None


@app.get("/get_status")
async def get_status() -> Dict[str, str]:
    """returns the status of the llm model or STATUS_IDLE if no wrapper is deployed.

    Returns:
        Dict[str, str]: a dictionary with the response status and message
    """
    logging.info("Manager: request get_status")
    if wrapper is None:
        response = STATUS_IDLE
    else: 
        response = wrapper.llm.status
        
    return {"status": SUCCESS, "message": response}

@app.post("/deploy")
async def deploy(config: ModelConfig):
    """deploys a wrapper and initiales the llm model defined within the config

    Args:
        config (ModelConfig): json fullfilling the requirements of ModelConfig

    Returns:

    """
    logging.info("Manager: request deploy")
    global wrapper 
    if wrapper is None:
        try:
            wrapper = WrapperManager().create_wrapper(json.dumps(config.model_dump(mode='json')))
            if wrapper is None:
                deployment_result = f"The Wrapper was unable to deploy the model {config.model}"
                response_status = FAILURE
                
            elif wrapper.llm.status == STATUS_READY:
                deployment_result = f"The Wrapper succesfully deployed the model {config.model}"
                response_status = SUCCESS
            return {"status": response_status, "message": deployment_result}
        
        except Exception as e:
            logging.error(f"Manager: Error during deployment: {e}")

    else:
        deployment_result = f"Unable to deploy the model {config.model}, because there is already a model deployed."
        response_status = FAILURE
        return {"status": response_status, "message": deployment_result}
    

@app.post("/process_prompt", response_model=PromptResponse)
async def process_prompt(prompt: Prompt) -> Dict[str, int]:
    """forwards the prompt to the llm and calculates the sci score.add()

    Returns:
        Dict[str, int]: a dictionary with the llm response and the calculated sci score
    """
    logging.info("Manager: request process_prompt")
    global wrapper

    if wrapper is None:
        answer = "The wrapper is not available"
        sci_score = 0
    else:
        question = prompt.question
        powerstat = start_calc_sci_score()
        start_time = time.time()
        answer = wrapper.get_answer(question)
        end_time = time.time()
        time_diff_in_ms = (end_time - start_time) * 1000
        sci_score = end_calc_sci_score(powerstat, len(answer.split()), time_diff_in_ms, "DE")
    return {"answer": answer, "sci_score": sci_score}


@app.post("/shutdown")
async def shutdown():
    """Shuts down the currently deployed model if there is one.

    Returns:
        Dict[str, str]: a dictionary with the response status and message
    """
    logging.info("Manager: request shutdown")
    global wrapper

    if wrapper is None:
        return {"status": FAILURE, "message": "No model is currently deployed."}
    
    try:
        wrapper.shutdown_llm()
        wrapper = None
        return {"status": SUCCESS, "message": "The model has been successfully shut down."}
    except Exception as e:
        logging.error(f"Manager: Error during shutdown: {e}")
        return {"status": FAILURE, "message": "An error occurred during shutdown."}