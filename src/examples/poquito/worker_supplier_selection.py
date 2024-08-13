import logging
from concurrent.futures.thread import ThreadPoolExecutor

import requests
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
        self.topics = [
            "query_RAMP_catalogue",
            "filter_generic_suppliers",
            "search_trusted",
            "filter_trusted",
            "request_proof_of_work",
            "repeat_request",
            "unresponsive_supplier"
        ]  # add the subscription here (each method in this class)

        self.helper = helperInstance
        ## uncomment the next line if you want the logging text in stdout
        # self.helper.configure_logging()  # can get a bit verbose (tasks continue polling after completing)

    def query_RAMP_catalogue(self, task: ExternalTask) -> TaskResult:
        print(f'Material: {str(task.get_variable("Material"))}')

        payload = {
            'Material': str(task.get_variable('Material')),
            'Color': str(task.get_variable('Color')),
            'Normative': str(task.get_variable('Normative'))
        }
        r = requests.post('http://127.0.0.1:5000/fetch_new_supplier', json=payload)
        print(f'REST response: {r.text}')

        # suppliersCollection = ['foo', 'bar']
        suppliersCollection = [
            {
                'id': '999',
                'companyName': 'somethinghere'
            },
            {
                'id': '000',
                'companyName': 'sdf442'
            }
        ]

        self.helper.error_handling(task=task)
        self.helper.task_log(task)
        return task.complete({"nowHasCollectionOfSupplierCandidates": True, 'suppliersCollection': suppliersCollection})

    def filter_generic_suppliers(self, task: ExternalTask) -> TaskResult:
        suppliersCollection = task.get_variable('suppliersCollection')
        maxDistance = task.get_variable('maxDistance')
        deliveryDate = task.get_variable('DeliveryDate')
        sourceMaterial = task.get_variable('SourceMaterial')
        priceLimit = task.get_variable('PriceLimit')
        minReputation = task.get_variable('minReputation')

        print(f'filtered with data from: maxDistance, DeliveryDate, SourceMaterial, PriceLimit, minReputation ')
        self.helper.error_handling(task=task)
        self.helper.task_log(task)
        return task.complete({"nowHas_sortedCollectionOfSuppliers": True, 'suppliersCollection': suppliersCollection})
        # return task.complete({"nowHas_sortedCollectionOfSuppliers": True, 'suppliersCollection': json.dumps(suppliersCollection)})

    def search_trusted(self, task: ExternalTask):
        print(f'searched among the trusted and here are the results...')
        return task.complete()

    def filter_trusted(self, task: ExternalTask):
        print(f'filter_trusted: complete')
        return task.complete()

    def request_proof_of_work(self, task: ExternalTask):
        print(f'Requesting proof of work for: {str(task.get_variable("supplier"))}')

        # We can also correlate the message here and call receive task

        return task.complete()

    def unresponsive_supplier(self, task: ExternalTask):
        print(f'unresponsive supplier: {str(task.get_variable("supplier"))}')
        return task.complete()

    def repeat_request(self, task: ExternalTask):
        print("repeating request")
        return task.complete()

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
    # add here all the methods of the CamundaHandlers Class here..(they should correspond one-to-one to the topics)
    handlersList = [
        handlers.query_RAMP_catalogue,
        handlers.filter_generic_suppliers,
        handlers.search_trusted,
        handlers.filter_trusted,
        handlers.request_proof_of_work,
        handlers.repeat_request,
        handlers.unresponsive_supplier
    ]

    # handlersList = handlers.list_methods()[:-1]
    print(f'handlersList: {handlersList}')
    executor = ThreadPoolExecutor(max_workers=len(handlers.topics))

    for index, topic in enumerate(handlers.topics):
        executor.submit(
            ExternalTaskWorker(worker_id=topic[index], config=default_config).subscribe, topic, handlersList[index]
        )
