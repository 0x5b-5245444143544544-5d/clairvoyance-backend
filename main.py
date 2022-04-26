import serial
import config
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect(host="localhost", port=config.mqtt_broker_port)
ser = serial.Serial(config.serial_device, baudrate=config.baud_rate, timeout=1)
while True:
    s = ser.readline().decode()
    if s and s.startswith(config.packet_prefix) and s.endswith(config.packet_suffix):
        s = s.replace(config.packet_prefix, "")
        s = s.replace(config.packet_suffix, "")
        s = s.replace("temp=", "")
        temp = float(s)
        print(temp)
        client.publish("a_temp", temp)

