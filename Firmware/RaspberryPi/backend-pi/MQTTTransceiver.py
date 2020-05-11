import paho.mqtt.client as mqtt
import threading


class MQTTTransceiver:
    PRESSURE_TOPIC = 'Ventilator/pressure'
    FLOWRATE_TOPIC = 'Ventilator/flow_rate'
    FLOWRATE_TOPIC = 'Ventilator/volume'
    FIO2_CONFIG_TOPIC = 'Config/fio2'

    def __init__(self):
        thread = threading.Thread(target=self.mqtt_subscriber, args=(self,))
        thread.start()

    def mqtt_publish(topic, value):
        client = mqtt.Client()
        client.connect("127.0.0.1", 1883, 60)
        client.publish(topic, value)
        client.disconnect()

    def sender(topic, value):
        thread = threading.Thread(target=mqtt_publish, args=(topic, value,))
        thread.start()

    def mqtt_subscriber(self):
        client = mqtt.Client()
        client.connect("127.0.0.1", 1883, 60)
        client.subscribe(self.FIO2_CONFIG_TOPIC)
        client.on_message = self.on_message
        client.loop_forever()

    def on_message(client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
