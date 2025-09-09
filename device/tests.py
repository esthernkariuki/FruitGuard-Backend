from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from device.models import Device
from users.models import User

#Create your tests here.
class DeviceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="brianmutunga@gmail.com",
            password="Securepass123",
            first_name="Brian",
            last_name="Mutunga",
            phone_number="0790345678",
            user_type="farmer"
        )
        
        self.device = Device.objects.create(
            status="active",
            user_id=self.user
        )
        self.device_url = reverse('device-list') 
        self.device_detail_url = reverse('device-detail', args=[self.device.device_id])

    def test_list_devices(self):
        response = self.client.get(self.device_url)
        print("List devices response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['device_id'], self.device.device_id)
        self.assertEqual(response.data[0]['status'], "active")
        self.assertEqual(response.data[0]['user_id'], self.user.id) 
        self.assertEqual(response.data[0]['created_at'], self.device.created_at.strftime('%Y-%m-%d'))


    def test_create_device(self):
        
        data = {
            "status": "inactive",
            "user_id": self.user.id  
        }
        response = self.client.post(self.device_url, data, format='json')
        print("Create device response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Failed with: {response.data}")
        self.assertEqual(response.data['status'], "inactive")
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertTrue(Device.objects.filter(device_id=response.data['device_id']).exists())

    