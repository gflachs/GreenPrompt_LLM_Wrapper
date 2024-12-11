import logging
import asyncio
from threading import Thread
from src.app.llm_model import LLMModel, RestartError
import time

logging.basicConfig(
    filename="wrapper.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class LLMWrapper:

    def __init__(self, modeltyp, model):
        self._is_llm_healthy = True
        self._monitoring_task = None
        self.llm = LLMModel(modeltyp=modeltyp, model = model)
        self._max_timeout = 120 # Abbruch während des periodischen Health checks wenn festgestellt wird, dass llm bereits seit mehr als 120 sekunden prompting
        self._started_prompting = None
        self._llm_restarting = False

    async def _health_check_function(self):
        """Die Funktion, die durch das Monitoring überprüft wird."""
        try:
            logging.info("performing health check")
            if time.time() - self._started_prompting > self._max_timeout:
                return False
            if self.llm.status in ["idle", "ready", "stopping"] \
                or self._started_prompting is None \
                or (time.time() - self._started_prompting) <= self._max_timeout:
                return True
            return False
        except Exception as e:
            logging.error(f"Health-Check-Error: {e}")
            return False

    async def _monitor_health(self):
        """Die Überwachungslogik, die alle 60 Sekunden ausgeführt wird."""
        while True:
            self._is_healthy = await self._health_check_function()
            if self._is_healthy:
                logging.info("the llm is healthy")
            else:
                logging.warning("the llm is unhealthy - try to restart")
                self._llm_restarting = True
                self.llm.restart()
                while self._llm_restarting:
                    if self.llm.status in ["ready", "prompting"]:
                        self._llm_restarting = False
                    elif self.llm.status == "failure":
                        raise RestartError
                    await asyncio.sleep(10) # Zeit bis zur Überprüfung ob der restart erforlgreich oder erfolglos war

            await asyncio.sleep(60) # Zeit bis zum nächsten periodischen Health check

    def start_monitoring(self):
        """Startet das Health-Monitoring in einem separaten Thread."""
        if self._monitoring_task is None:
            loop = asyncio.new_event_loop()

            def run_loop():
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._monitor_health())

            self._monitoring_task = Thread(target=run_loop, daemon=True)
            self._monitoring_task.start()

    def stop_monitoring(self):
        """Beendet das Health-Monitoring."""
        if self._monitoring_task:
            self._monitoring_task = None

    def get_answer(self, question):
        self._started_prompting = time.time()
        logging.info("Task wird ausgeführt...")
        answer = self.llm.answer_question(question)
        logging.info(f"Answer: {answer} - Question: {question}")
        self._started_prompting = None
        return answer


if __name__ == "__main__":
    questions = ["Whats the capitol of France?",
                 "How much does a litre of water weigh?",
                 "Wie viele Cent ergeben einen Euro?",
                 "Che cos'è 7 + 5 ?",
                 "Was besagt das deutsche Reinheitsgebot?"]
    
    wrapper = LLMWrapper(modeltyp="text-generation", model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    wrapper.start_monitoring()

    wrapper.llm.download_model()

    try:
        for question in questions:
            if wrapper.llm.status == "ready":
                wrapper.get_answer(question)
            else:
                time.sleep(5)
    except RestartError as re:
        logging.error(f"LLM failed to restart {re}")
    except Exception as e:
        logging.error(f"wrapper failed for reasons unknown {e}")
    finally:
        wrapper.llm.shutdown()
        wrapper.stop_monitoring()