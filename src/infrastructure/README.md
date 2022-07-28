The end goal of this package is to be run in a CICD pipeline to deploy upon merge to main. 
It should also be able to be run with a script for other neuroscience labs to deploy a self-hosted app with minimal effort. 
- For use, create an aws account, go to iam and create a user which has the role attached to it that's described in the bootstrap_iam_role.json. Then get the environment variables from that user (using expiring token accesss). export them as environment variables on your laptop. and run the deploy.sh script from src/infrastructure file. 
Also, remember to run the "delete infrastructure" docker command once completed. 


So, 
- docker image with command and script to start up infrastructure service and returns url. single scirpt to be handed directly into github actions so, all is done in github actions is secrets are pulled into environemtn variables and script is run. 
- same docker image with new command to close infrastructure service. will not run on github actions. Needs to be run locally by user with same deploy user credentials. 
- same docker image with command and script to create user with permissions to run these above tasks. Will not run on github actions. Needs to be run locally by user. will rely on root credentials as environment variables unless user has the knowledge to create a user with iam etc permissions to run cdk script. 
- credentials should be and will be passed with environment variables. 
- user forks repo to self host and have the ability to access secrets. 

# Components:

### rest api stack:
- lambda on proxy api gateway
    - get request for signed url for s3 bucket upload
    - get request for signed url for zipped results s3 bucket download
    - fast api in docker container
- cognito authentication
- iam policy for correct user bucket use
- s3 upload bucket has sqs listener


### frontend stack
- dash code from docker container uvicorn server
- calls rest api on two buttons for folder upload and download
- buttons call code to get signed url, then post/get folder to url. 
- sign in and sign up functionality for authentication
- badge for uploading/processing/completed
### unzip app stack:
- lambda docker container
- listens to zipped queue
- unzips files
- uploads to unzipped s3
- sqs listener to unzipped s3
- one lambda per folder
### AI stack:
- lambda docker container
- listener to unzip queue
- downloads from unzip s3.
- prediction.
- uploads to unzipped results s3
- sqs queue listening to results s3
- one lambda per file

### zip app stack:
- listens unzipped results sqs
- zips folders
- TODO: how do we know when all files are ready?
- uploads zips to zipped results s3
- s3 sends notification s3n to frontend to notify user the files are ready.
