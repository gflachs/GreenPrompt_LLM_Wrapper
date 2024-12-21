import logging
import time
import schedule  # [Änderung] Import von schedule
import threading
from src.app.llm_model import LLMModel, RestartError

logging.basicConfig(
    filename="wrapper.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

class LLMWrapper:
    def __init__(self, modeltyp, model):
        self._is_llm_healthy = True
        self.llm = LLMModel(modeltyp=modeltyp, model=model)
        self._max_timeout = 240  # Timeout für den Health-Check
        self._continous_task = None
        self._prompting_starting_time = None

    def health_check_wrapper(self):
        """Health-Check alle 60 Sekunden ausgeführt."""
        if (time.time() - self._prompting_starting_time) > self._max_timeout:
            logging.warning("The LLM is unhealthy (dreaming), trying to restart...")
            self.llm.restart()

        if self.llm.status in ["ready", "idle", "not ready"]:
            self._is_llm_healthy = True
            logging.info("The LLM is healthy")
        else: 
            self._is_llm_healthy = False
            logging.warning("The LLM is unhealthy, trying to restart...")
            self.llm.restart()

    def start_monitoring(self):
        """Startet das Health-Monitoring mit schedule."""
        schedule.every(60).seconds.do(self.health_check_wrapper)  # [Änderung] Verwenden von schedule
        self._continous_task = run_continuously()

    def stop_monitoring(self):
        """Beendet das Health-Monitoring."""
        if self._continous_task is None:
            return
        self._continous_task.set()

    def get_answer(self, question):
        self._prompting_starting_time = time.time()
        logging.info("Task wird ausgeführt...")
        answer = self.llm.answer_question(question)
        logging.info(f"Answer: {answer} - Question: {question}")
        return answer
