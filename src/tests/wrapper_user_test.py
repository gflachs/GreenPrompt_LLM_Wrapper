from src.app.llm_wrapper import LLMWrapper  # Importiere den Wrapper
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
    questions = [
        "What's the capital of France?",
        "How much does a litre of water weigh?",
        "Wie viele Cent ergeben einen Euro?",
        "Che cos'è 7 + 5 ?",
        "Was besagt das deutsche Reinheitsgebot?"
    ]
    
    # Erstelle den Wrapper mit den gewünschten Modellparametern
    wrapper = LLMWrapper(modeltyp="text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")
    
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