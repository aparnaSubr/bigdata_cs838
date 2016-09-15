
set RESOURCE_GROUP=%1
set LOCATION="eastus"
set DEPLOYMENT_NAME=%1

call azure group create -n %RESOURCE_GROUP% -l %LOCATION%
call azure group deployment create -f cluster-deployment-template.json -e cluster-deployment-parameters.json -g %RESOURCE_GROUP% -n %DEPLOYMENT_NAME%

rem echo %RESOURCE_GROUP%
