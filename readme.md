# what this is

A quick start for (some) things Camunda. Uses a Vendor Onboarding process as an example Use Case. Assumes that the 
Camunda Engine is up and running and that the REST-API is enabled (you may want to see [camunda_quick_start.md](.
/docs/camunda_quick_start.md) for more). BPMN diagrams and forms are deployed to the Camunda Engine via the [Camunda 
Modeler](https://camunda.com/download/modeler/) (you may want to use the [token simulator](https://github.
com/camunda/camunda-modeler-token-simulation-plugin) as well..)   


## where things are

- the business logic is described by the diagrams and forms under `./src/0_camunda_risk_assessment/`
- a template for the python code (service handlers for the Camunda external tasks) is in `./src/1.service_workers/` 
  (you may want to use this directory for the service handlers as well)
- a mock RAMP server (for queries made by the python code) is under `./src/mock_RAMP/` (it is a flask app)
- examples of simple Camunda functionality to see how individual components function are under `./src/piece_by_piece/`
- a first working example that shows the deployment to the Camunda Engine, a service handler in python and a mock 
  interaction between RAMP and the python code is in `./src/poquito/`  
