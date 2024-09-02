# Overview

This guide provides a quick start for working with various aspects of Camunda, using a Vendor Onboarding process as an example use case. It assumes that the Camunda Engine is up and running, with the REST API enabled. For more details, refer to the [Camunda Quick Start Guide](./docs/camunda_quick_start.md).

BPMN diagrams and forms are deployed to the Camunda Engine via the [Camunda Modeler](https://camunda.com/download/modeler/). You might also find the [Token Simulator](https://github.com/camunda/camunda-modeler-token-simulation-plugin) useful during the development and testing process.

## Directory Structure

- **Business Logic**: The business logic is defined by the diagrams and forms located in [./src/0_camunda_risk_assessment/](src/0.camunda_risk_assessment).
- **Service Handlers**: A template for the Python service handlers used for Camunda external tasks can be found in [./src/1.service_handlers/](src/1.service_handlers). You can use this directory for your own service handlers as well.
- **Mock RAMP Server**: A mock RAMP server, implemented as a Flask app, is available under [./src/mock_RAMP](src/mock_RAMP). This server handles queries made by the Python code.
- **Camunda Functionality Examples**: Examples demonstrating basic Camunda functionality, showing how individual components work, are located in [./src/examples/](src/examples).

## RAMP Communication Flow Summary

A summary of the integration with external components can be found in [camunda-RAMP-python.md](docs/README-camunda-RAMP-python.md).
