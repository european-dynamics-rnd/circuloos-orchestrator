# Camunda Quick Start

## options for deployment 
this is the short story, the longer one is here: https://docs.camunda.
io/docs/components/best-practices/architecture/deciding-about-your-stack-c7/#understanding-the-stacks-architecture  

#### use ‘Camunda Run’ & deployment via its REST API: 
- download Camunda Run: https://camunda.com/download/ & extract 
- start the engine: `./start.bat --rest --webapps --swaggerui`
- got these parameters from: https://docs.camunda.org/manual/7.16/user-guide/camunda-bpm-run/#example-application 
  and you may want to use them to avoid loading the examples 
    - access the engine via the webapps in: `localhost:8080`
- credentials: `demo/ demo` (it's in the configuration.yaml)
- each engine session is persisted in the h2 db: you need to delete existing deployments if you want a fresh start: 
  https://docs.camunda.org/manual/7.16/reference/rest/deployment/delete-deployment/  
- watch this series of tutorials on how to use it with a simple application: https://www.youtube.com/watch?
  v=TlFojzQNopA&list=PLJG25HlmvsOX8TiIGUZcVW-ez053YsOX0&index=2  


if you want to write a Springboot app build it each time: 
https://www.youtube.com/watch?app=desktop&v=QXt5FzW4eMA&list=PLJG25HlmvsOVssaiPmavxv3htN_dXS3BW&index=2 
if you want to see the architecture (how the two options are formed): https://docs.camunda.
io/docs/components/best-practices/architecture/deciding-about-your-stack-c7/#understanding-the-stacks-architecture  
external task (python/ any): 
external tasks are the preferred way of introducing code to the business logic modelled in Camunda. They are closer 
to the ideas motivating the online engine of Camunda 8 and they are preferred because they separate the resources 
(computation) and the logic between the main flow and the side-jobs that need to happen as a service. the long story 
is here: https://docs.camunda.io/docs/components/best-practices/development/invoking-services-from-the-process-c7/    

## how it works 
the business flow waits for external workers to finish the job. The ‘external task’ inside Camunda ‘declares a 
topic’ (type of service needed) and the ‘external worker’ (code) needs to poll the Camunda REST API to see if the 
‘topic’ they have subscribed to is there among the list of external tasks (see image here: https://docs.camunda.
org/manual/latest/user-guide/process-engine/external-tasks/#the-external-task-pattern ). Once the external worker 
finds the relevant topic in this list (‘published’ on the API), then the code executes and must POST to the API that 
it has completed its execution. Then can the Camunda Engine continue to the rest of the business logic (the ‘wait’ 
is released). for more read: https://docs.camunda.
io/docs/components/best-practices/development/invoking-services-from-the-process-c7/#external-tasks        
Note that calls to external tasks are preferred over the use of JavaDelegates, despite adding a slight overhead. on 
why external tasks are preferred over JavaDelegates is described in this blog: https://blog.bernd-ruecker.
com/moving-from-embedded-to-remote-workflow-engines-8472992cc371   

## how to do it: 
- start the camunda engine (it will wait until it can see a handler subscribed to this topic)
- run the external code (worker) that subscribes to the topic 
- the camunda engine will pick it up once it subscribes & execute it

implementation of a worker in python:
https://github.com/camunda-community-hub/camunda-external-task-client-python3 
https://github.com/konstantinosGombakis/camundaExternalTask/blob/main/python/externalRaiseTemperature.py 
demo-processorcestrator-server.eurodyn.com/    (requires VPN under eurodyn) 

## summary of required steps: 
install the library that describes the ‘subscription’, ‘context’, etc.: 

```commandline
pip install camunda-external-task-client-python3 
pip install pydantic
```

you will be making at least these two imports:
```python
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
```
add the code that describes the ‘handler’ (work that needs to be done):

```python
def handle_task(task: ExternalTask) -> TaskResult:...
``` 

subscribe the ‘worker’ to the Camunda topic: 
```python
ExternalTaskWorker(worker_id="1", config=default_config).subscribe("topicName", handle_task)
```

run the code locally python -m <moduleName> the Worker does polling to check if they can connect to the topic
the Camunda Engine will pick it up


## BPMN and business logic modelling
You may want to start with the common patterns of BPMN with 

this documentation page: https://docs.camunda.io/docs/components/concepts/workflow-patterns/ 

and these videos: 
Common Patterns 1: https://www.youtube.com/watch?v=yAvm_re5YGA&list=PLJG25HlmvsOU3BRisp_oocXxQC0avO-Ov&index=2 
escalating or failure: use interrupting or non-interrupting boundary events on the tasks to show that the task 
itself may fail (use error) or need something more to be done (escalation); if different outcomes from the task need 
to be handled, then it’s just a (XOR?) gateway  
Common Patterns 2: https://www.youtube.com/watch?v=l4w1n2KUR6Q&list=PLJG25HlmvsOU3BRisp_oocXxQC0avO-Ov&index=3&pp=iAQB 
same task multiple times (or same set of eyes): annotate the task as a ‘multi-instance’ & use an interrupting 
conditional event to exit (may model the logic that a user does not approve) 



**Modelling Best Practices:** 
video: https://www.youtube.com/watch?v=YOgYvzF1DRM&list=PLJG25HlmvsOU3BRisp_oocXxQC0avO-Ov&index=6 
documentation: https://docs.camunda.io/docs/components/best-practices/modeling/creating-readable-process-models/ 


**DMN + BPMN: risk modelling example:** https://www.youtube.com/watch?v=aDjo8qiQYx0 
dealing with microservices/ external actors: https://www.youtube.com/watch?v=wjFFpN3qzhQ 



**other things you may need for Camunda**

- FEEL expressions: https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-expressions-introduction/ 
- variable scoping: https://docs.camunda.io/docs/components/concepts/variables/#variable-scopes each subprocess 
defines a new scope, with the outer scope being more general (global) and when the subprocess finishes the variables 
are ‘merged’ updates from the inner scopes are propagated upwards/ outwards; all variables live in the context of 
the process instance and are accessible by the workers (https://docs.camunda.
io/docs/components/modeler/bpmn/data-flow/ ); you can also map variables from the inner scope to new names in the 
outer scope (https://docs.camunda.io/docs/components/concepts/variables/#inputoutput-variable-mappings )
- process variables and visibility (Camunda 7 docs):https://docs.camunda.org/manual/7.
  21/user-guide/process-engine/variables/ 



