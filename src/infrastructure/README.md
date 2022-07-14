The end goal of this package is to be run in a CICD pipeline to deploy upon merge to main. 
It should also be able to be run with a script for other neuroscience labs to deploy a self-hosted app with minimal effort. 
This includes somewhat of a bad practice to use root access keys, but creates a more simple deployment for labs who have little development experience and allows them to create the deployment user with correct permissions to deploy. It is highly recommended to delete the access credentials once the new user is created. Also, remember to run the "delete infrastructure" docker command once completed. 


So, 
- docker image with command and script to start up infrastructure service and returns url. single scirpt to be handed directly into github actions so, all is done in github actions is secrets are pulled into environemtn variables and script is run. 
- same docker image with new command to close infrastructure service. will not run on github actions. Needs to be run locally by user with same deploy user credentials. 
- same docker image with command and script to create user with permissions to run these above tasks. Will not run on github actions. Needs to be run locally by user. will rely on root credentials as environment variables unless user has the knowledge to create a user with iam etc permissions to run cdk script. 
- credentials should be and will be passed with environment variables. 
- user forks repo to self host and have the ability to access secrets. 

