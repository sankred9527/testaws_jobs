import json
import logging
import boto3
import os
import random
import time
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')
table_name = os.environ["TEST_DYNAMO_TABLE"]
table = dynamodb.Table(table_name)

sts_client = boto3.client('sts')
response = sts_client.get_caller_identity()    
account_id = response.get('Account')

def upload_to_s3(uuid_key) :
    s3 = boto3.client('s3')
    bucket_name = "testjobs-787jh31jlam"
    object_key = f"{uuid_key}-result.txt"
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=bytearray("hello world".encode()))

    return f"https://testjobs-787jh31jlam.s3.ap-northeast-1.amazonaws.com/{object_key}"


def update_status(uuid_key, new_status, result_url, start_handle_time, end_handle_time):
    
    primary_key = {
        'uuid': uuid_key,        
    }
    
    update_expression = 'SET #status_alias = :new_value, result_url = :rurl, start_time = :start_time, end_time = :end_time'
    expression_attribute_names = {
        '#status_alias': 'status'
    }
    expression_attribute_values = {
        ':new_value': new_status,
        ':rurl' : result_url,
        ':start_time' : start_handle_time,
        ':end_time' : end_handle_time,
    }

    try:
        
        response = table.update_item(
            Key=primary_key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='UPDATED_NEW'
        )

        
        updated_attributes = response.get('Attributes')
        if updated_attributes:
            logger.info(f"new attr ={updated_attributes}")
        else:
            logger.info("not modify")
    except Exception as e:
        logger.info(f"modify error: {e}")


    

def lambda_handler(event, context):    
    for record in event['Records']:
        try:
            message_body = json.loads(record['body'])
            logger.info(f"Received message: {message_body}")       
            start_handle_time = datetime.now().isoformat()
            time.sleep(random.randint(2,4))   
            end_handle_time = datetime.now().isoformat()
            result_url = upload_to_s3(message_body["uuid"])
            update_status(message_body["uuid"], 1, result_url,  start_handle_time, end_handle_time)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")    
    return {
        'statusCode': 200,
        'body': json.dumps('Messages processed successfully')
    }


if __name__ == "__main__":
    update_status("1d021930-afb9-4a42-bad8-047ceeebfedc", 1)