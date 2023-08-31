import paho.mqtt.client as mqtt
import requests
import json
import time
from datetime import datetime


def fetch_temperature():
    response = requests.get('http://api.weatherapi.com/v1/current.json?key=6b479f638e674c5ea7493033233108&q=Vienna&aqi=no')
    data = response.json()
    return data['current']['temp_c']

def on_message(client, userdata, message):
    print("Server sends command")
    
    payload_ = json.loads(message.payload.decode())
    activate_heat_pump_ = payload_.get("activate_heat_pump", None)
    
    if activate_heat_pump_ is not None:
        print(f"Activate Heat Pump: {activate_heat_pump_}")
        
        fake_api_endpoint = "https://heat-pump-enpoint.free.beeceptor.com"
        requests.post(fake_api_endpoint, json={"activate_heat_pump": activate_heat_pump_})

client = mqtt.Client()
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.subscribe("heat_pump")

client.loop_start()

last_temperature = None
while True:
    current_temp_ = fetch_temperature()

    if last_temperature is None or abs(current_temp_ - last_temperature) >= 0.1:
        payload_ = {
            "Temperature": current_temp_, 
            "timestemp": datetime.now().strftime("%d-%m-%y %H:%M")
        }
        
        print(f"Publishing temperature: {current_temp_}")
        client.publish("Temperature", json.dumps(payload_))
        last_temperature = current_temp_
    
    time.sleep(30)