#!/bin/bash

STACK_NAME=$1

if [ -z "$1" ]
  then
    echo "No STACK_NAME argument supplied"
    exit 1
fi

sed -ri "s/YOUR-DOMAIN-NAME/${STACK_NAME}/" parameters.json

S3BUCKET=$STACK_NAME-$(tr -dc a-f0-9 </dev/urandom | head -c 10)
sed -ri "s/YOUR-BUCKET-NAME/${S3BUCKET}/" parameters.json

echo "Creating stack..."

# upload lambda functions
zip pi-exam.zip -xi pi-exam.py
aws s3 cp fetch.zip s3://${S3BUCKET}/pi-exam.zip

# upload cf stack
aws cloudformation create-stack --stack-name ${STACK_NAME} --template-body file://cfStack.json --capabilities CAPABILITY_NAMED_IAM --parameters file://parameters.json --tags file://tags.json --output text

echo "Waiting on ${STACK_NAME} create completion..."
aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME}
aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq .Stacks[0].Outputs
