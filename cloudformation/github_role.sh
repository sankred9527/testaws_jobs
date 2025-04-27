#!/bin/bash
# Usage: ./run.sh

# Define the variables
PROJECT_NAME="sankred9527"
REPOSITORY_NAME="testaws_jobs"
AWS_ACCOUNT_ID="551056440474"
ORGANIZATION="sankred9527"
S3BucketName="testjobs-787jh31jlam"

aws cloudformation deploy \
    --stack-name "$PROJECT_NAME-role-for-github-stack" \
    --template-file templates/github_role.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        RespositoryName="$REPOSITORY_NAME" \
        AWSAccountId="$AWS_ACCOUNT_ID" \
        Organization="$ORGANIZATION" \
        ProjectName="$PROJECT_NAME" \
        S3BucketName="$S3BucketName" 
