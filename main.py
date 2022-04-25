import asyncio
import serial
import config
import paho.mqtt.client as mqtt


async def read_serial():
    ser = serial.Serial(config.serial_device, baudrate=config.baud_rate, timeout=1)
    while True:
        s = ser.read(10000)
        print(s.decode("utf-8"))

