import boto3
import time
import json, decimal

#connect to dynamodb
dynamo = boto3.resource('dynamodb', region_name="us-east-1")

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def get_all(table):
    #access the table and get the items data in the table
    dynamo_table = dynamo.Table(table)
    response = dynamo_table.scan(
        TableName=table
        )
    result = response['Items']
    result = json.dumps(result, default=decimal_default)
    return result
