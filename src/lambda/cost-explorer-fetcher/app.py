import boto3
import json
import datetime
import os
from dateutil.relativedelta import relativedelta

def lambda_handler(event, context):
    # Initialize clients
    ce = boto3.client('ce')
    s3 = boto3.client('s3')
    athena = boto3.client('athena')
    
    # Date ranges (last 30 days and current month)
    end_date = datetime.date.today()
    start_date_30d = end_date - datetime.timedelta(days=30)
    start_date_mtd = end_date.replace(day=1)
    
    # Get cost and usage data
    def get_cost_data(start_date, end_date, granularity='DAILY'):
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity=granularity,
            Metrics=['UnblendedCost', 'UsageQuantity'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'REGION'}
            ]
        )
        return response
    
    # Get Savings Plans utilization
    def get_savings_plans_utilization():
        response = ce.get_savings_plans_utilization(
            TimePeriod={
                'Start': start_date_30d.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY'
        )
        return response
    
    # Get RI recommendations
    def get_ri_recommendations():
        response = ce.get_reservation_utilization(
            TimePeriod={
                'Start': start_date_30d.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SUBSCRIPTION_ID'}]
        )
        return response
    
    try:
        # Fetch all data
        cost_data_30d = get_cost_data(start_date_30d, end_date)
        cost_data_mtd = get_cost_data(start_date_mtd, end_date, 'MONTHLY')
        savings_plans_data = get_savings_plans_utilization()
        ri_data = get_ri_recommendations()
        
        # Prepare data for storage
        data_to_store = {
            'metadata': {
                'report_date': end_date.strftime('%Y-%m-%d'),
                'time_generated': datetime.datetime.utcnow().isoformat()
            },
            'cost_data_30d': cost_data_30d,
            'cost_data_mtd': cost_data_mtd,
            'savings_plans_data': savings_plans_data,
            'ri_data': ri_data
        }
        
        # Store raw data in S3
        s3_key = f"raw/{end_date.strftime('%Y/%m/%d')}/cost_data.json"
        s3.put_object(
            Bucket=os.environ['COST_BUCKET'],
            Key=s3_key,
            Body=json.dumps(data_to_store)
        )
        
        # Process and store in Athena-optimized format
        process_for_athena(data_to_store, end_date)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Cost data collected successfully')
        }
        
    except Exception as e:
        print(f"Error collecting cost data: {str(e)}")
        raise e

def process_for_athena(data, report_date):
    # Process data into flattened format for Athena
    # This would be implemented to create CSV/Parquet files
    # optimized for Athena queries
    pass