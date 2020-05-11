import paho.mqtt.client as mqtt
import threading


class MQTTTransceiver:
    PRESSURE_TOPIC = 'Ventilator/pressure'
    FLOWRATE_TOPIC = 'Ventilator/flow_rate'
    FLOWRATE_TOPIC = 'Ventilator/volume'
    FIO2_CONFIG_TOPIC = 'Config/fio2'

    def __init__(self):
        mqtt_subscriber()

    def mqtt_publish(topic, value):
        client = mqtt.Client()
        client.connect("localhost", 1883, 60)
        client.publish(topic, value)
        client.disconnect()

    def sender(topic, value):
        thread = threading.Thread(target=mqtt_publish, args=(topic, value,))
        thread.start()

    def mqtt_subscriber(self):
        client = mqtt.Client()
        client.subscribe(self.FIO2_CONFIG_TOPIC)
        client.on_message = on_message
        client.loop_forever()

    def on_message(client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
