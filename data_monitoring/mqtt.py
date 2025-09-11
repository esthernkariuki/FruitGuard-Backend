import json
import requests
import paho.mqtt.client as mqtt
from django.conf import settings

device_map = {}

def fetch_device_map():
    global device_map
    try:
        response = requests.get(settings.MQTT_API_URL.replace('/data_monitoring/', '/device/'))
        response.raise_for_status()
        devices = response.json()
        device_map = {d['device_identifier']: d['device_id'] for d in devices}
    except Exception:
        pass
        

def on_connect(client, userdata, flags, rc):
    client.subscribe(settings.MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        device_key = str(payload.get('device_id'))
        device_pk = device_map.get(device_key)

        if device_pk is None:
            return

        api_payload = {
            "device": device_pk,
            "trap_fill_level": payload.get('distance', 0)
        }
        response = requests.post(settings.MQTT_API_URL, json=api_payload)
    except Exception:
        pass
        

def mqtt_thread():
    client = mqtt.Client(client_id="backendClient")
    client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
    client.tls_set() 
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
    client.loop_forever()
