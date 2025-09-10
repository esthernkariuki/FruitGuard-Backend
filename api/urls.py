

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataMonitoringViewSet
from .views import DeviceViewSet

router = DefaultRouter()
router.register(r"data_monitoring", DataMonitoringViewSet, basename="data_monitoring")

router = DefaultRouter()
router.register(r'device', DeviceViewSet)

urlpatterns=[
    path('', include(router.urls)),
]