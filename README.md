# AWS Cost Optimization Dashboard

A serverless dashboard for monitoring and optimizing AWS costs.

## Features

- Automated daily cost data collection from AWS Cost Explorer API
- Data storage in S3 with Athena for SQL querying
- QuickSight dashboard for cost visualization
- Savings Plans and Reserved Instance recommendations
- Cost anomaly detection

## Architecture

![Architecture Diagram](docs/architecture-diagram.png)

## Components

1. **AWS Cost Explorer API** - Collects cost and usage data
2. **Lambda Functions** - Process and store cost data
3. **S3** - Storage for raw and processed cost data
4. **Athena** - SQL queries on cost data
5. **QuickSight** - Visualization and dashboards

## Deployment

1. Clone this repository
2. Configure AWS credentials with appropriate permissions
3. Run deployment script:

```bash
./src/scripts/deploy.sh [environment] [region]


## Final Notes
1. Cost Considerations:
-Athena charges per query - optimize queries
-QuickSight has its own pricing model
-S3 costs are minimal for cost data
2. Permissions Required:
-Cost Explorer read access
-QuickSight admin access for dashboard creation
-Lambda execution roles
3. Enhancements:
-Add anomaly detection
-Implement custom recommendations engine
-Add Slack/email alerts for cost spikes
-Integrate with AWS Budgets

This implementation provides a complete serverless solution for AWS cost monitoring and optimization with automated data collection, processing, and visualization.