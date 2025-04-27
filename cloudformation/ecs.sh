#!/bin/bash
# Usage: ./ecs.sh   

# Define the variables
PROJECT_NAME="sankred9527"
PROJECT_ENV="dev"
ACCOUNT_ID="551056440474"
APP_NAME="testaws_jobs"
IMAGE_URL="${ACCOUNT_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/${PROJECT_NAME}/${APP_NAME}:dev"
CERTIFICATE_ARN="arn:aws:acm:ap-northeast-1:${ACCOUNT_ID}:certificate/55a35f13-cfbd-46f7-a49d-de382f72c64a"
S3BucketName="testjobs-787jh31jlam"
IAMROLE="arn:aws:iam::${ACCOUNT_ID}:role/${PROJECT_NAME}-github-role"


if [ $# -eq 0 ]; then
    echo "ecs.sh deploy or destroy"
    exit 1
fi


param=$1

case $param in
    "deploy")
        aws cloudformation deploy \
        --template-file templates/ecs.yaml \
        --stack-name "$PROJECT_NAME-ecs-stack" \
        --capabilities CAPABILITY_NAMED_IAM \
        --parameter-overrides \
            ProjectName="$PROJECT_NAME" \
            ProjectEnv="$PROJECT_ENV" \
            AppName="$APP_NAME" \
            ImageUrl="$IMAGE_URL" \
            CertificateArn="$CERTIFICATE_ARN" \
            S3BucketName="$S3BucketName"  \
            IAMROLE="$IAMROLE"
        ;;
    "destroy")
        aws cloudformation delete-stack --stack-name "$PROJECT_NAME-ecs-stack"
        ;;
    *)
        echo "use deploy or destroy"
        exit 1
        ;;
esac
    