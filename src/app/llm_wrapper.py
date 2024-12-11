import logging
import time
import schedule  # [Änderung] Import von schedule
from src.app.llm_model import LLMModel, RestartError

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
        self.llm = LLMModel(modeltyp=modeltyp, model=model)
        self._max_timeout = 120  # Timeout für den Health-Check
        self._started_prompting = None
        self._llm_restarting = False

    def health_check_wrapper(self):
        """Health-Check alle 60 Sekunden ausgeführt."""
        if self._is_llm_healthy:
            logging.info("The LLM is healthy")
        else:
            logging.warning("The LLM is unhealthy, trying to restart...")
            self._llm_restarting = True
            self.llm.restart()

    def start_monitoring(self):
        """Startet das Health-Monitoring mit schedule."""
        schedule.every(60).seconds.do(self.health_check_wrapper)  # [Änderung] Verwenden von schedule

        while True:
            schedule.run_pending()
            time.sleep(60)  # Wartezeit für den nächsten Health-Check

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
