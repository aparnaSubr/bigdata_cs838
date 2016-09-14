#!/bin/bash

RESOURCE_GROUP=$1
LOCATION="eastus"
DEPLOYMENT_NAME=$1

azure group create -n ${RESOURCE_GROUP} -l ${LOCATION}
azure group deployment create -f cluster-deployment-template.json -e cluster-deployment-parameters.json -g ${RESOURCE_GROUP} -n ${DEPLOYMENT_NAME}
