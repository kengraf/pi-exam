#!/bin/bash

STACK_NAME=`jq -r 'map(select(.ParameterKey == "DeployName"))[0].ParameterValue' parameters.json`
S3BUCKET=`jq -r 'map(select(.ParameterKey == "S3bucketName"))[0].ParameterValue' parameters.json`

echo "Creating stack..."

# upload lambda functions
zip ${STACK_NAME}.zip -xi ${STACK_NAME}.py
aws s3 cp ${STACK_NAME}.zip s3://${S3BUCKET}/${STACK_NAME}.zip

# upload cf stack
aws cloudformation create-stack --stack-name ${STACK_NAME} --template-body file://cfStack.json --capabilities CAPABILITY_NAMED_IAM --parameters file://parameters.json --tags Key=ProjectName,Value=${STACK_NAME}  --output text

echo "Waiting on ${STACK_NAME} create completion..."
aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME}
aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq .Stacks[0].Outputs
