import paho.mqtt.client as mqtt
import threading
import logging
import logging.config
from Variables import Variables

logger = logging.getLogger(__name__)


class MQTTTransceiver:
    PRESSURE_TOPIC = 'Ventilator/pressure'
    FLOWRATE_TOPIC = 'Ventilator/flow_rate'
    VOLUME_TOPIC = 'Ventilator/volume'
    MIN_VOL_TOPIC = 'Ventilator/min_volume'
    PEAK_PRESSURE_TOPIC = 'Ventilator/peak_pressure'
    FIO2_CONFIG_TOPIC = 'Config/fio2'
    RR_CONFIG_TOPIC = 'Config/rr'
    PEEP_CONFIG_TOPIC = 'Config/peep'
    VT_CONFIG_TOPIC = 'Config/vt'
    IE_CONFIG_TOPIC = 'Config/ie'
    va = Variables()

    def __init__(self):
        thread = threading.Thread(target=self.mqtt_subscriber, args=())
        thread.start()

    def mqtt_publish(self, topic, value):
        client = mqtt.Client()
        client.connect("127.0.0.1", 1883, 60)
        logger.debug("MQTT Send: [%s] - [%s]" % (topic, value))
        client.publish(topic, value)
        client.disconnect()

    def sender(self, topic, value):
        thread = threading.Thread(
            target=self.mqtt_publish, args=(topic, value,))
        thread.start()

    def mqtt_subscriber(self):
        client = mqtt.Client()
        client.connect("127.0.0.1", 1883, 60)
        client.subscribe(self.FIO2_CONFIG_TOPIC)
        client.subscribe(self.RR_CONFIG_TOPIC)
        client.subscribe(self.PEEP_CONFIG_TOPIC)
        client.subscribe(self.VT_CONFIG_TOPIC)
        client.subscribe(self.IE_CONFIG_TOPIC)
        client.on_message = self.on_message
        client.loop_forever()

    def on_message(self, client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        if (msg.topic == self.FIO2_CONFIG_TOPIC):
            self.va.set_fio2(float(msg.payload.decode()))
            logger.debug("FIO2 receved: %.2f" % self.va.fio2)
        elif (msg.topic == self.RR_CONFIG_TOPIC):
            self.va.set_rr(float(msg.payload.decode()))
            logger.debug("RR receved: %.2f" % self.va.rr)
        elif (msg.topic == self.PEEP_CONFIG_TOPIC):
            self.va.set_peep(float(msg.payload.decode()))
            logger.debug("PEEP receved: %.2f" % self.va.peep)
        elif (msg.topic == self.VT_CONFIG_TOPIC):
            self.va.set_vt(float(msg.payload.decode()))
            logger.debug("VT receved: %.2f" % self.va.vt)
        elif (msg.topic == self.IE_CONFIG_TOPIC):
            self.va.set_ie(float(msg.payload.decode()))
            logger.debug("IE receved: %.2f" % self.va.ie)
        else:
            logger.debug("Message [%s] - [%s] not found" % (msg.topic, msg.payload.decode()))
