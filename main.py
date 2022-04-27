import datetime
import serial
import config
import paho.mqtt.client as mqtt
import database

client = mqtt.Client()
client.connect(host="localhost", port=config.mqtt_broker_port)
ser = serial.Serial(config.serial_device, baudrate=config.baud_rate, timeout=1)
db = database.Database().get()
while True:
    s = ser.readline().decode()
    if s and s.startswith(config.packet_prefix) and s.endswith(config.packet_suffix):
        s = s.replace(config.packet_prefix, "")
        s = s.replace(config.packet_suffix, "")
        s = s.replace("temp=", "")
        temp = float(s)
        print(temp)
        client.publish("a_temp", temp)
        db['temperature'].insert(dict(timestamp=datetime.datetime.timestamp(datetime.datetime.now()), temperature=temp))
        db.commit()

