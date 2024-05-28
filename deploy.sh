#!/bin/bash

DEPLOY_NAME=`jq -r 'map(select(.ParameterKey == "DeployName"))[0].ParameterValue' parameters.json`
S3BUCKET=`jq -r 'map(select(.ParameterKey == "S3bucketName"))[0].ParameterValue' parameters.json`

echo "Creating stack...${DEPLOY_NAME}"

# upload lambda functions
zip ${DEPLOY_NAME}.zip -xi ${DEPLOY_NAME}.py
aws s3 cp ${DEPLOY_NAME}.zip s3://${S3BUCKET}/${DEPLOY_NAME}.zip

# upload cf stack
aws cloudformation create-stack --stack-name ${DEPLOY_NAME} --template-body file://cfStack.json --capabilities CAPABILITY_NAMED_IAM --parameters file://parameters.json --tags Key=ProjectName,Value=${DEPLOY_NAME}  --output text

echo "Waiting on ${DEPLOY_NAME} create completion..."
aws cloudformation wait stack-create-complete --stack-name ${DEPLOY_NAME}
aws cloudformation describe-stacks --stack-name ${DEPLOY_NAME} | jq .Stacks[0].Outputs
