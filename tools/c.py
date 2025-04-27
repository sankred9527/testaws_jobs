#!/usr/bin/env python3
import threading
import requests
import uuid
import argparse
import random
import os
import time
import json
import boto3
 
base_url = f'http://{os.environ["TEST_URL"]}/testjobs/'

dynamodb = boto3.resource('dynamodb')

def get_token():
        
    username = 'admin'
    password = 'admin123'
    
    token_url = f'{base_url}api/token/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(token_url, data=data)
    print(response)
    print(response.text)
    if response.status_code == 200:
        access_token = response.json().get('token')
        return access_token
    
    return None
        

global_token = get_token()


def add_job() :    

    
    headers = {
        'Authorization': f'Bearer {global_token}'
    }

    job_data = {
        'uuid_key': str(uuid.uuid4()),
        'job_name': f'test job is {random.randint(0,10240)}',
        'content': f'test job content is {random.randint(0,10240)}',    
    }

    try:
        response = requests.post(base_url + 'job/add/', data=job_data, headers=headers)
        print('add job ret='+response.text)            
        ret = json.loads(response.text)
        if ret["success"] :
            return ret["msg"]        
            
    except requests.RequestException as e:
        print('request err', e)

    return None



def query_job(uuid_key) :
    headers = {
        'Authorization': f'Bearer {global_token}'
    }

    try:
        q = {
            "uuid_key" : uuid_key
        }
        response = requests.get(base_url + 'job/query/', params=q, headers=headers)
        if response.status_code == 200:
            print(f'query job success : {response.text}')
        else:
            print('query job failed=', response.text)    
            
    except requests.RequestException as e:
        print('request err', e)


def add_thread(i, result_arr) :
    ret = add_job()    
    if ret != None :
        result_arr[i] = ret

def query_dynamodb_items(primary_keys):
    table_name = os.environ["TEST_DYNAMO_TABLE"]
    table = dynamodb.Table(table_name)
    
    keys = [{'uuid_key': key } for key in primary_keys]   
    request_items = {
        table.name: {
            'Keys': keys
        }
    }

    try:        
        response = dynamodb.batch_get_item(RequestItems=request_items)        
        items = response.get('Responses', {}).get(table.name, [])                
        unprocessed_keys = response.get('UnprocessedKeys')
        while unprocessed_keys:
            response = dynamodb.batch_get_item(RequestItems=unprocessed_keys)
            items.extend(response.get('Responses', {}).get(table.name, []))
            unprocessed_keys = response.get('UnprocessedKeys')

        
        found_keys = [item.get('uuid_key') for item in items]
        for key in primary_keys:
            if key not in found_keys:
                print(f"can't find item uuid={key} ")

        return items
    except Exception as e:
        print(f"batch query error: {e}")
        return []

def add_10_jobs() :        
    
    batch_size = 3
   
    result_arr = [None] * batch_size
    threads = []
    for i in range(batch_size):
        thread = threading.Thread(target=add_thread, args=(i,result_arr,), name=f"Thread-{i}")
        threads.append(thread)
        thread.start()
        print(f"add job {i}")
        time.sleep(1)
    
    
    for thread in threads:
        thread.join()

    print(f"add {batch_size} job finish ") 
    print(result_arr)
    result_arr = [i for i in result_arr if i is not None]

    time.sleep(3)
    items = query_dynamodb_items(result_arr)
    print(items)
    

def main():
    parser = argparse.ArgumentParser(description='add query job')

    parser.add_argument('--addmany', action='store_true', help='add 10 job')
    parser.add_argument('--add', action='store_true', help='add one job')
    parser.add_argument('--query', type=str, help='add job')
    

    args = parser.parse_args()
    if args.addmany:
        add_10_jobs()
    elif args.add :        
        add_job()
    elif args.query != None :        
        query_job(args.query)

    

if __name__ == '__main__':
    main()