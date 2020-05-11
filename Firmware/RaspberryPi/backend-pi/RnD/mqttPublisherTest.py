#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import random

# This is the Publisher

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.publish("Ventilator/pressure", random.uniform(0,20));
client.disconnect();

client.connect("localhost", 1883, 60)
client.publish("Ventilator/flow_rate", random.uniform(0,20));
client.disconnect();
