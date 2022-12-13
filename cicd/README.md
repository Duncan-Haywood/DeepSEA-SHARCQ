# Usage

- you will need to change `OWNER_REPO` in the `cicd/pipeline.py` file at the top to your own repository

## undeploy

- to undeploy, see the undeploy.sh script and instructions there. there should be some secrets and roles and parameters and a pipeline which don't get torn down. Maybe some Docker containers in ECR.

## deploy

- to deploy, first `upload_github_token.sh` Then for the github token with the follwoing details: """Authentication will be done by a secret called `github-token` in AWS Secrets Manager (unless specified otherwise).The token should have these permissions: repo to read the repository and admin:repo_hook if you plan to use webhooks (true by default)""".
- then run deploy.sh from this folder and see instructions in the comments in that file. push to github main branch before running this. create an user with the policy attached: AdministratorAccess and programatic access credentials when it asks. After the pipeline is up and running, delete that user, as it is a security vulnerability.
