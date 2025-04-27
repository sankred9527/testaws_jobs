#!/bin/bash
# Usage: ./ecs.sh   

# Define the variables
PROJECT_NAME="sankred9527"
PROJECT_ENV="dev"
APP_NAME="testaws_jobs"
DEFAULT_SECURITY_GROUP="sg-05ff49adf68ea0bde"
VPC_ID="vpc-0102a7508b40f1213"
PRIVATE_SUBNET_1="subnet-03886210cdca39a3e"
PRIVATE_SUBNET_2="subnet-0ebe6ab1d4eff03c5"
PUBLIC_SUBNET_1="subnet-09fe8ff47d3333585"
PUBLIC_SUBNET_2="subnet-064f6e7ebd01c438c"
IMAGE_URL="551056440474.dkr.ecr.ap-northeast-1.amazonaws.com/sankred9527/testaws_jobs:dev"
CERTIFICATE_ARN="arn:aws:acm:ap-northeast-1:551056440474:certificate/55a35f13-cfbd-46f7-a49d-de382f72c64a"
S3BucketName="testjobs-787jh31jlam"


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
            DefaultSecurityGroup="$DEFAULT_SECURITY_GROUP" \
            VpcId="$VPC_ID" \
            PrivateSubnet1="$PRIVATE_SUBNET_1" \
            PrivateSubnet2="$PRIVATE_SUBNET_2" \
            PublicSubnet1="$PUBLIC_SUBNET_1" \
            PublicSubnet2="$PUBLIC_SUBNET_2" \
            ImageUrl="$IMAGE_URL" \
            CertificateArn="$CERTIFICATE_ARN" \
            S3BucketName="$S3BucketName" \
        --profile $PROFILE
        ;;
    "destroy")
        aws cloudformation delete-stack --stack-name "$PROJECT_NAME-ecs-stack"
        ;;
    *)
        echo "use deploy or destroy"
        exit 1
        ;;
esac
    