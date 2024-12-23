# app/main.py
from fastapi import FastAPI, HTTPException
from .models import CommandRequest, CommandResponse
from .llm_wrapper import LLMWrapper
import logging

app = FastAPI(title="LLM Wrapper Command API")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

modeltyp = "text-generation"
model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Instantiate the LLMWrapper
wrapper = LLMWrapper(modeltyp=None, model = None)


@app.post("/command", response_model=CommandResponse)
async def handle_command(command_request: CommandRequest):
    command = command_request.command.lower()
    params = command_request.params or {}

    try:
        if command == "deploy":
            wrapper.llm._modeltyp = params.get("model_type")
            wrapper.llm.model = params.get("model_name")
            if not wrapper.llm.model_type or not wrapper.llm.model_name:
                raise ValueError("Parameters 'model_type' and 'model_name' are required for deploy command.")
            wrapper.llm.download_model()
            return CommandResponse(status="success", detail="LLM deployed successfully.")
        
        elif command == "shutdown":
            wrapper.llm.shutdown()
            return CommandResponse(status="success", detail="LLM shutdown successfully.")
        
        elif command == "status":
            logger.info("Launch command status")
            status_info = wrapper.llm.get_status()
            logger.info(f"status info = {status_info}")
            return CommandResponse(status="success", data=status_info)
        
    except Exception as e:
        logger.error(f"Error handling command '{command}': {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
