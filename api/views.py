from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DataMonitoringSerializer
from data_monitoring.models import DataMonitoring

# Create your views here.
class DataMonitoringViewSet(viewsets.ModelViewSet):
   queryset = DataMonitoring.objects.all()
   serializer_class = DataMonitoringSerializer

