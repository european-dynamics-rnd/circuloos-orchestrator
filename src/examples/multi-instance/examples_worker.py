r"""
this is a template of a service handler for external tasks in Camunda

topics
handlersList
"""

from concurrent.futures.thread import ThreadPoolExecutor
import requests, json, logging

from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.utils.log_utils import log_with_context

logger = logging.getLogger(__name__)
# configuration for the Client
default_config = {
    "maxTasks": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}


class CamundaHandlers:
    """

    """

    def __init__(self, helperInstance):
        self.helper = helperInstance
        ## uncomment the next line if you want the logging text in stdout
        # self.helper.configure_logging()  # can get a bit verbose (tasks continue polling after completing)

    def create_list(self, task: ExternalTask):
        print(f'empty handler executed from this python code!')
        suppliersCollection = ["test1", "test2"]

        self.helper.error_handling(task=task)
        self.helper.task_log(task)
        return task.complete({'suppliersCollection': suppliersCollection})


class Helpers:
    """
    you don't need to worry about this at all. this is no more than a collection of auxiliary methods - mainly for
    logging
    """

    def configure_logging(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                            handlers=[logging.StreamHandler()])

    def error_handling(self, task, failure=False, bpmn_error=False, vars={"var1": "value1", "success": False}):
        if failure:
            # this marks task as failed in Camunda
            return task.failure(error_message="task failed", error_details="failed task details",
                                max_retries=3, retry_timeout=5000)
        elif bpmn_error:
            return task.bpmn_error(error_code="BPMN_ERROR_CODE", error_message="BPMN Error occurred",
                                   variables=vars)

    def task_log(self, task):
        log_context = {"WORKER_ID": task.get_worker_id(),
                       "TASK_ID": task.get_task_id(),
                       "TOPIC": task.get_topic_name()}
        log_with_context(f"handle_task started: business key = {task.get_business_key()}", log_context)


if __name__ == '__main__':
    helper = Helpers()
    handlers = CamundaHandlers(helperInstance=helper)

    # list here (comma separated string values) the Camunda `topics` to which your methods subscribe (could be the
    # name of each of your methods)
    topics = [
        "create_list"
    ]
    # add here all the methods of the CamundaHandlers Class (they should correspond one-to-one with the `topics`);
    # these get in the next line to the threads that subscribe to the Camunda Engine
    handlersList = [
        handlers.create_list
    ]

    executor = ThreadPoolExecutor(max_workers=len(topics))

    for index, topic in enumerate(topics):
        executor.submit(
            ExternalTaskWorker(worker_id=topic[index],base_url="http://localhost:8089/engine-rest", config=default_config).subscribe, topic, handlersList[index]
        )
