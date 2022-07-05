aws ecr public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/x1k9w9z9

docker build -t deepsharcq ./src/api

docker tag deepsharcq:latest public.ecr.aws/x1k9w9z9/deepsharcq:latest

docker push public.ecr.aws/x1k9w9z9/deepsharcq:latest
