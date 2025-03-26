#!/bin/bash

ENVIRONMENT=${1:-prod}
REGION=${2:-us-east-1}

# Deploy core infrastructure
aws cloudformation deploy \
  --template-file infrastructure/cfn-templates/cost-data-pipeline.yml \
  --stack-name cost-data-pipeline-${ENVIRONMENT} \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides EnvironmentName=${ENVIRONMENT} \
  --region ${REGION}

# Get outputs from core stack
CORE_OUTPUTS=$(aws cloudformation describe-stacks \
  --stack-name cost-data-pipeline-${ENVIRONMENT} \
  --query 'Stacks[0].Outputs' \
  --region ${REGION})

COST_BUCKET=$(echo $CORE_OUTPUTS | jq -r '.[] | select(.OutputKey=="CostBucketName") | .OutputValue')

# Deploy Athena resources
aws cloudformation deploy \
  --template-file infrastructure/cfn-templates/athena-resources.yml \
  --stack-name athena-resources-${ENVIRONMENT} \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
      EnvironmentName=${ENVIRONMENT} \
      CostBucketName=${COST_BUCKET} \
  --region ${REGION}

# Get Athena outputs
ATHENA_OUTPUTS=$(aws cloudformation describe-stacks \
  --stack-name athena-resources-${ENVIRONMENT} \
  --query 'Stacks[0].Outputs' \
  --region ${REGION})

ATHENA_DATABASE=$(echo $ATHENA_OUTPUTS | jq -r '.[] | select(.OutputKey=="AthenaDatabaseName") | .OutputValue')

# Deploy QuickSight dashboard (requires QuickSight admin ARN)
QUICKSIGHT_ADMIN_ARN="arn:aws:quicksight:${REGION}:${AWS::AccountId}:user/default/YOUR_QUICKSIGHT_USER"

aws cloudformation deploy \
  --template-file infrastructure/cfn-templates/quicksight-dashboard.yml \
  --stack-name quicksight-dashboard-${ENVIRONMENT} \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
      EnvironmentName=${ENVIRONMENT} \
      AthenaDatabaseName=${ATHENA_DATABASE} \
      AthenaTableName="daily_costs_${ENVIRONMENT}" \
      QuickSightUserArn=${QUICKSIGHT_ADMIN_ARN} \
  --region ${REGION}

echo "Deployment complete for environment: ${ENVIRONMENT}"