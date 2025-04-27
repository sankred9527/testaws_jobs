from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import Jobs
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os
import json
import boto3
import jwt
from datetime import datetime,timezone, timedelta

SECRET_KEY ='fake_secret_key_asjkdjkasd'

def verify_jwt(request):    
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])    

def index(request):
    return HttpResponse("index page")


def live(request):
    return HttpResponse("live")


def send_job_to_sqs(job) :
    sqs = boto3.client('sqs')

    sqs_url = os.environ["TEST_SQS_QUEUE_URL"]    

    msg_attr = {}    

    response = sqs.send_message(
        QueueUrl=sqs_url,
        DelaySeconds=0,
        MessageAttributes=msg_attr,
        MessageBody=(json.dumps(job, separators=(',', ':')))
    )
    return response

@csrf_exempt
def add_job(request):
    verify_jwt(request)
    if request.method == 'POST':
        
        uuid_key = request.POST.get('uuid_key')
        job_name = request.POST.get('job_name')
        content = request.POST.get('content')        
        
        if uuid_key and job_name and content :
            try:                
                job = Jobs(uuid_key=uuid_key, job_name=job_name, content=content, status=0, 
                        create_at=datetime.now().isoformat(), start_time=datetime(1970, 1, 1).isoformat(), end_time=datetime(1970, 1, 1).isoformat() )
                job.save(unique=True)
                ret = send_job_to_sqs(Jobs.Schema().dump(job))
                return JsonResponse({"success":True, "msg": uuid_key})
            except Exception as e :
                return JsonResponse({"success":False, "msg":f"error is {e}"})
        else:
            return JsonResponse({"success":False, "msg":f"error is {e}"})
    return JsonResponse({"success":False, "msg":"only support POST"})


@csrf_exempt
def query_job(request):
    verify_jwt(request)
    if request.method == 'GET':
        
        uuid_key = request.GET.get('uuid')
        
        if uuid_key :
            try:                                    
                query_result = Jobs.query(uuid__eq = uuid_key)
                
                job = None
                for _job in query_result:
                    job = _job
                    break
                if job != None :                    
                    return JsonResponse({"success":True, "msg": Jobs.Schema().dump(job)})  
                else:
                    return JsonResponse({"success":False, "msg":"can not find job"})  
            except Exception as e :
                return JsonResponse({"success":False, "msg":f"error is1 {e}"})
        else:
            return JsonResponse({"success":False, "msg": "error"})
    return JsonResponse({"success":False, "msg":"only support GET"})



@csrf_exempt
def obtain_token(request):

    USER_DATA = {
        'username': 'admin',
        'password': 'admin123'
    }

    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == USER_DATA['username'] and password == USER_DATA['password']:            
            expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)
            payload = {
                'username': username,
                'exp': expiration_time
            }            
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': f'Invalid credentials {username},{password}'}, status=401)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


            
    