import logging
import threading
import time

import schedule

from src.app.wrapper.llm_model import (STATUS_FAILURE, STATUS_IDLE,
                                   STATUS_NOT_READY, STATUS_READY, LLMModel)

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
    def __init__(self, modeltyp:str, model:str, prompting_config:dict, deployment_config:dict, **other_configs):
        self._is_llm_healthy = True
        self.llm = LLMModel(modeltyp=modeltyp, model=model, prompting_config=prompting_config, deployment_config=deployment_config, **other_configs)
        self.llm.download_model()
        self._max_timeout = 240  # Timeout für den Health-Check
        self._continous_task = None
        self._prompting_starting_time = None

    def health_check_wrapper(self):
        """Health-Check every 60 seconds."""
        if self._prompting_starting_time is not None:
            if (time.time() - self._prompting_starting_time) > self._max_timeout:
                logging.warning("Wrapper: The LLM is unhealthy (dreaming), trying to restart...")
                self.restart_llm()

        if self.llm.status in [STATUS_READY, STATUS_IDLE, STATUS_NOT_READY]:
            self._is_llm_healthy = True
            logging.info("Wrapper: The LLM is healthy")
            if self._prompting_starting_time is not None:
                logging.debug(f"Wrapper: trying to answer since {time.time() - self._prompting_starting_time:.2f} seconds")
        else: 
            self._is_llm_healthy = False
            logging.warning("Wrapper: The LLM is unhealthy, trying to restart...")
            self.restart_llm()

    def start_monitoring(self):
        """Start health monitoring with schedule."""
        if self._continous_task is None:
            schedule.every(60).seconds.do(self.health_check_wrapper)  # [Änderung] Verwenden von schedule
            self._continous_task = run_continuously()

    def stop_monitoring(self):
        """Ends health monitoring."""
        if self._continous_task is None:
            return
        self._continous_task.set()
        self._continous_task = None

    def get_answer(self, question):
        self._prompting_starting_time = time.time()
        logging.info("Wrapper: task is being executed...")
        answer = self.llm.answer_question(question)
        logging.info(f"Answer: {answer} - Question: {question}")
        return answer
    
    
    def shutdown_llm(self):
        if self.llm.status == STATUS_READY:
            self.llm.shutdown()
        elif self.llm.status == STATUS_FAILURE:
            logging.info("Wrapper ignores shutdown request because llm is in failure state")
        elif self.llm.status == STATUS_IDLE:
            logging.info("Wrapper ignores shutdown request because no llm is deployed/running")
        elif self.llm.status == STATUS_NOT_READY:
            logging.info("Wrapper ignores shutdown request because llm is already performing a shutdown or a restart")



    def restart_llm(self):
        if self.llm.status == STATUS_READY:
            self.llm.restart()
        elif self.llm.status == STATUS_FAILURE:
            logging.info("Wrapper ignores restart request because llm is in failure state")
        elif self.llm.status == STATUS_IDLE:
            logging.info("Wrapper ignores restart request because no llm is deployed/running")
        elif self.llm.status == STATUS_NOT_READY:
            logging.info("Wrapper ignores restart request because llm is already performing a shutdown or a restart")