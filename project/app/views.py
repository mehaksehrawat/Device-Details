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
    deviceId = request.query_params.get('id')
    data = redis_instance.get(deviceId)
    if data:
        data = eval(data)[-1]
        return JsonResponse(data)
    else:
        return JsonResponse({"msg": "Device id not found"})

@api_view(['GET'])
def get_device_location(request):
    deviceId = request.query_params.get('id')
    data = redis_instance.get(deviceId)
    if data:
        newData = eval(data)[-1]
        data = (newData.get('latitude'), newData.get('longitude'))
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"msg": "Device id not found"})


@api_view(['GET'])
def get_all_location(request):
    deviceId = request.query_params.get('id')
    startTime = request.query_params.get('start_time')
    endTime = request.query_params.get('end_time')
    if startTime or endTime:
        try:
            startTime = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%SZ")
            endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return JsonResponse({"msg": "Start time or end time is not valid"})

    data = redis_instance.get(deviceId)
    if data:
        all_data = eval(data)
        location_data = []
        for data in all_data:
            time_stamp = datetime.strptime(data.get('time_stamp'), "%Y-%m-%dT%H:%M:%SZ")
            if startTime!= None and endTime != None and time_stamp >= startTime and time_stamp <= endTime:
                location_data.append((data.get('latitude'), data.get('longitude'), data.get('time_stamp')))
        return JsonResponse(location_data, safe=False)
    else:
        return JsonResponse({"msg": "Data not found"})


