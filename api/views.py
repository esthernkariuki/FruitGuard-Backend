from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DataMonitoringSerializer
from data_monitoring.models import DataMonitoring
from device.models import Device
from .serializers import DeviceSerializer

# Create your views here.
class DataMonitoringViewSet(viewsets.ModelViewSet):
   queryset = DataMonitoring.objects.all()
   serializer_class = DataMonitoringSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
