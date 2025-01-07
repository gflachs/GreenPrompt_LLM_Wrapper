from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_model import LLMModel  
import asyncio
import logging

app = FastAPI()


llm_instance = None


logging.basicConfig(
    filename="llm_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class PromptRequest(BaseModel):
    question: str


@app.post("/deploy")
def deploy_model(model_type: str, model_name: str):
    global llm_instance
    llm_instance = LLMModel(modeltyp=model_type, model=model_name)
    llm_instance.download_model()
    logging.info(f"Model deployed: {model_name}")
    return {"message": "Model deployed successfully", "model": model_name}


@app.post("/prompt")
async def handle_prompt(request: PromptRequest):
    global llm_instance

    
    if not llm_instance or not llm_instance._pipe:
        logging.error("No model deployed when /prompt was called.")
        raise HTTPException(status_code=400, detail="No model is currently deployed")

    try:
        
        timeout = 10.0

        
        async def process_prompt():
            
            await asyncio.sleep(1)  
            answer = "Simulated Answer"
            sci_score = 42  # Simulated SCI-Score
            return {"answer": answer, "sci_score": sci_score}

       
       
        response = await asyncio.wait_for(process_prompt(), timeout=timeout)
        logging.info(f"Prompt processed successfully: {request.question}")
        return response

    except asyncio.TimeoutError:
        
        logging.error("Timeout while processing prompt.")
        raise HTTPException(status_code=504, detail="Request timed out")

    except Exception as e:
        
        logging.error(f"Error processing prompt: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/answer")
def ask_question(question: str):
    if not llm_instance or not llm_instance._pipe:
        return {"error": "No model is currently deployed"}
    answer = llm_instance.answer_question(question)
    return {"question": question, "answer": answer}

@app.post("/stop")
def stop_model():
    global llm_instance
    llm_instance = None
    logging.info("Model stopped successfully.")
    return {"message": "Model stopped successfully"}

@app.get("/status")
def get_status():
    if not llm_instance:
        return {"status": "No model deployed"}
    return {"status": "Model deployed", "model": llm_instance.model, "type": llm_instance.modeltyp}

