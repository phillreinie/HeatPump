import paho.mqtt.client as mqtt
import json
import csv

temperature_threshold = 23


        
def write_csv(_time, _temp, _activate):
    file_ = "log.csv"
    columns_ = ["Time", "Temperature", "Activate_Heat_Pump"]

    try:
        with open(file_, 'r') as f:
            pass
    except FileNotFoundError:
        with open(file_, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=columns_)
            csv_writer.writeheader()

    with open(file_, 'a', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=columns_)
        csv_writer.writerow({"Time": _time, "Temperature": _temp, "Activate_Heat_Pump": _activate})

# whenever the server gets a new temperature from client
def on_message(_client, _userdata_, _message):
    payload_ = json.loads(_message.payload.decode())
    temp_ = payload_.get("Temperature", None)
    timestamp_ = payload_.get("timestemp", None)

    if temp_ is not None:
        activate_heat_pump_ = temp_ < temperature_threshold
        write_csv(timestamp_, temp_, activate_heat_pump_)
        
        payload_new_ = json.dumps({"activate_heat_pump": activate_heat_pump_})
        _client.publish("heat_pump", payload_new_)

client = mqtt.Client()
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.subscribe("Temperature")
client.loop_forever()
        

client = mqtt.Client()
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.subscribe("Temperature")
client.loop_forever()


        
    
    
