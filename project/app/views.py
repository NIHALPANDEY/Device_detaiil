from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import redis
import json
from datetime import datetime
from django.conf import settings

# Create your views here.

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0, decode_responses=True)

@api_view(['GET'])
def get_device_info(request):
    device_id = request.query_params.get('id')
    data = redis_instance.get(device_id)
    if data:
        data = eval(data)[-1]
        return JsonResponse(data)
    else:
        return JsonResponse({"msg": "Device id not found"})

@api_view(['GET'])
def get_device_location(request):
    device_id = request.query_params.get('id')
    data = redis_instance.get(device_id)
    if data:
        latest_data = eval(data)[-1]
        data = (latest_data.get('latitude'), latest_data.get('longitude'))
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"msg": "Device id not found"})


@api_view(['GET'])
def get_all_location(request):
    device_id = request.query_params.get('id')
    start_time = request.query_params.get('start_time')
    end_time = request.query_params.get('end_time')
    if start_time or end_time:
        try:
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
            end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return JsonResponse({"msg": "Start time or end time is not valid"})

    data = redis_instance.get(device_id)
    if data:
        all_data = eval(data)
        location_data = []
        for data in all_data:
            time_stamp = datetime.strptime(data.get('time_stamp'), "%Y-%m-%dT%H:%M:%SZ")
            if start_time!= None and end_time != None and time_stamp >= start_time and time_stamp <= end_time:
                location_data.append((data.get('latitude'), data.get('longitude'), data.get('time_stamp')))
        return JsonResponse(location_data, safe=False)
    else:
        return JsonResponse({"msg": "Data not found"})


