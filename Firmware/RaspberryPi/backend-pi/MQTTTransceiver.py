import paho.mqtt.client as mqtt
import threading
import logging
import logging.config
from Variables import Variables

logger = logging.getLogger(__name__)
client = None


class MQTTTransceiver:
    PRESSURE_TOPIC = 'Ventilator/pressure'
    FLOWRATE_TOPIC = 'Ventilator/flow_rate'
    VOLUME_TOPIC = 'Ventilator/volume'
    CHART_DATA_TOPIC = 'Ventilator/chart_data'
    MIN_VOL_TOPIC = 'Ventilator/min_volume'
    PEAK_PRESSURE_TOPIC = 'Ventilator/peak_pressure'
    FIO2_CONFIG_TOPIC = 'Config/fio2'
    RR_CONFIG_TOPIC = 'Config/rr'
    PEEP_CONFIG_TOPIC = 'Config/peep'
    VT_CONFIG_TOPIC = 'Config/vt'
    IE_CONFIG_TOPIC = 'Config/ie'

    MQTT_HOST = "127.0.0.1"
    MQTT_PORT = 1883

    def __init__(self):
        # Setup an mqtt client
        self.setup_client()
        # Start mqtt_subscriber service in a thread
        thread = threading.Thread(target=self.mqtt_subscriber, args=())
        thread.start()

    def setup_client(self):
        global client
        client = mqtt.Client()
        client.connect(self.MQTT_HOST, self.MQTT_PORT, 60)

    def mqtt_publish(self, topic, value):
        logger.debug("MQTT Send: [%s] - [%s]" % (topic, value))
        client.publish(topic, value)

    def sender(self, topic, value):
        thread = threading.Thread(
            target=self.mqtt_publish, args=(topic, value,))
        thread.start()

    def mqtt_subscriber(self):
        global client

        client.subscribe(self.FIO2_CONFIG_TOPIC)
        client.subscribe(self.RR_CONFIG_TOPIC)
        client.subscribe(self.PEEP_CONFIG_TOPIC)
        client.subscribe(self.VT_CONFIG_TOPIC)
        client.subscribe(self.IE_CONFIG_TOPIC)
        client.on_message = self.on_message
        client.loop_forever()

    def on_message(self, client, obj, msg):
        if (msg.topic == self.FIO2_CONFIG_TOPIC):
            Variables.fio2 = float(msg.payload.decode())
            logger.debug("FIO2 receved: %.2f" % Variables.fio2)
        elif (msg.topic == self.RR_CONFIG_TOPIC):
            Variables.rr = float(msg.payload.decode())
            logger.debug("RR receved: %.2f" % Variables.rr)
        elif (msg.topic == self.PEEP_CONFIG_TOPIC):
            Variables.peep = float(msg.payload.decode())
            logger.debug("PEEP receved: %.2f" % Variables.peep)
        elif (msg.topic == self.VT_CONFIG_TOPIC):
            Variables.vt = float(msg.payload.decode())
            logger.debug("VT receved: %.2f" % Variables.vt)
        elif (msg.topic == self.IE_CONFIG_TOPIC):
            Variables.ie = float(msg.payload.decode())
            #TODO remove ie_i and ie_e
            Variables.ie_i = Variables.ie
            Variables.ie_e = 1
            logger.debug("IE receved: %.2f" % Variables.ie)
        else:
            logger.debug("Message [%s] - [%s] not found" % (msg.topic, msg.payload.decode()))

    def clean_up(self):
        client.disconnect()
