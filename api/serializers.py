from rest_framework import serializers
from data_monitoring.models import DataMonitoring 
from device.models import Device

class DataMonitoringSerializer(serializers.ModelSerializer):
   class Meta:
       model = DataMonitoring
       fields = '__all__' 


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
