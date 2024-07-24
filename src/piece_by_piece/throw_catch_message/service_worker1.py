from concurrent.futures.thread import ThreadPoolExecutor
import logging

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
    def __init__(self, helperInstance):
        self.topics = ["service_me", "another_topic"]    # add the subscription here

        self.helper = helperInstance
        ## uncomment the next line if you want the logging text in stdout
        # self.helper.configure_logging()  # can get a bit verbose (tasks continue polling after completing)

    def service_me(self, task: ExternalTask) -> TaskResult:
        print(f'have sent the REST req here...\n')
        self.helper.error_handling(task=task)
        self.helper.task_log(task)
        return task.complete({"req": True, "msg": "REST request has been sent"})

    def another_topic(self, task: ExternalTask) -> TaskResult:
        print(f'servicing another task...\n')
        self.helper.error_handling(task=task)
        self.helper.task_log(task)
        return task.complete({"registration": True, "msg": "another thing happened"})



class Helpers:
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





# python how to get a list of callable methods in my class


if __name__ == '__main__':
    helper = Helpers()
    handlers = CamundaHandlers(helperInstance=helper)


    # how to get this list from the class itself: https://realpython.com/python-callable-instances/#creating-callable-instances-with-__call__-in-python
    handlersList = [handlers.service_me, handlers.another_topic]

    # https://github.com/camunda-community-hub/camunda-external-task-client-python3/blob/master/camunda/external_task/external_task_worker.py

    # handlersList = handlers.list_methods()[:-1]
    print(f'handlersList: {handlersList}')
    executor = ThreadPoolExecutor(max_workers=len(handlers.topics))

    for index, topic in enumerate(handlers.topics):
        executor.submit(
            ExternalTaskWorker(worker_id=topic[index], config=default_config).subscribe, topic, handlersList[index]
        )