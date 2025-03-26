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