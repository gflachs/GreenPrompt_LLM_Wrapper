import torch
from src.app.wrapper.llm_wrapper import LLMWrapper  # Importiere den Wrapper
import time
import logging
import asyncio

logging.basicConfig(
    filename="wrapper.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    modeltyp =  "text-generation"
    model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    uses_chat_template =  {"uses_chat_template":True}

    prompting =  {
        "max_new_tokens": 256, 
        "do_sample": True,
        "temperature": 0.7,
        "top_k": 50, 
        "top_p": 0.95}
    deployment = {
        "torch_dtype": torch.bfloat16,
        "device_map": "auto"}
    
    
    questions = [
        "What's the capital of France?",
        "How much does a litre of water weigh?",
        "Wie viele Cent ergeben einen Euro?",
        "Che cos'è 7 + 5 ?",
        "Was besagt das deutsche Reinheitsgebot?"
    ]
    
    # Erstelle den Wrapper mit den gewünschten Modellparametern
    wrapper = LLMWrapper(modeltyp=modeltyp, model = model, prompting_config=prompting, deployment_config=deployment, **uses_chat_template)
    
    # Starte das Health-Monitoring, das den Health-Check alle 60 Sekunden ausführt
    wrapper.start_monitoring()
# Lade das Modell herunter
    wrapper.llm.download_model()

    # Warte, bis das Modell bereit ist
    while wrapper.llm.status != "ready":
        logging.info("Waiting for the model to be ready...")
        time.sleep(5)  # Warte 5 Sekunden, bevor erneut geprüft wird

    # Beantworte die Fragen, wenn das Modell bereit ist
    try:
        for question in questions:
            logging.info(f"Question: {question}")
            while True:
                if wrapper.llm.status == "ready":
                    wrapper.get_answer(question)
                    break
                else:
                    logging.warning("Model not ready yet, waiting...")
                    asyncio.run(asyncio.sleep(5))  # Warte 5 Sekunden, bevor erneut geprüft wird
    except LLMWrapper.RestartError as re:
        logging.error(f"LLM failed to restart {re}")
    except Exception as e:
        logging.error(f"Wrapper failed for reasons unknown {e}")
    finally:
        # Führe den Shutdown durch und stoppe das Monitoring
        wrapper.stop_monitoring()
        wrapper.shutdown_llm()