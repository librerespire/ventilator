import paho.mqtt.client as mqtt
import threading
import logging
import logging.config
from Variables import Variables

logger = logging.getLogger(__name__)
client = None


class MQTTTransceiver:
    CHART_DATA_TOPIC = 'Ventilator/chart_data'
    ACTUAL_TIDAL_VOLUME_TOPIC = 'Ventilator/vt'
    MINUTE_VOLUME_TOPIC = 'Ventilator/minute_volume'
    PIP_TOPIC = 'Ventilator/pip'
    PRESSURE_DATA_TOPIC = "Ventilator/pressure_data"

    CALIB_FLOW_RATE_CONFIG_TOPIC = 'Config/calib_flow_rate'
    FIO2_CONFIG_TOPIC = 'Config/fio2'
    RR_CONFIG_TOPIC = 'Config/rr'
    PEEP_CONFIG_TOPIC = 'Config/peep'
    VT_CONFIG_TOPIC = 'Config/vt'
    IE_CONFIG_TOPIC = 'Config/ie'
    PS_CONFIG_TOPIC = 'Config/ps'

    MQTT_HOST = "127.0.0.1"
    MQTT_PORT = 1883
    MQTT_KEEP_ALIVE = 60

    def __init__(self):
        # Setup an mqtt client
        self.setup_client()
        # Start mqtt_subscriber service in a thread
        thread = threading.Thread(target=self.mqtt_subscriber, args=())
        thread.start()

    def setup_client(self):
        global client
        client = mqtt.Client()
        client.connect(self.MQTT_HOST, self.MQTT_PORT, self.MQTT_KEEP_ALIVE)

    def mqtt_publish(self, topic, value):
        logger.debug("MQTT Send: [%s] - [%s]" % (topic, value))
        client.publish(topic, value)

    def sender(self, topic, value):
        thread = threading.Thread(
            target=self.mqtt_publish, args=(topic, value,))
        thread.start()

    def mqtt_subscriber(self):
        global client

        client.subscribe(self.CALIB_FLOW_RATE_CONFIG_TOPIC)
        client.subscribe(self.FIO2_CONFIG_TOPIC)
        client.subscribe(self.RR_CONFIG_TOPIC)
        client.subscribe(self.PEEP_CONFIG_TOPIC)
        client.subscribe(self.VT_CONFIG_TOPIC)
        client.subscribe(self.IE_CONFIG_TOPIC)
        client.subscribe(self.PS_CONFIG_TOPIC)
        client.on_message = self.on_message
        client.loop_forever()

    def on_message(self, client, obj, msg):
        if (msg.topic == self.CALIB_FLOW_RATE_CONFIG_TOPIC):
            Variables.calib_flow_rate = float(msg.payload.decode())
            logger.debug("Calibration flow rate received: %.2f" % Variables.calib_flow_rate)
        elif (msg.topic == self.FIO2_CONFIG_TOPIC):
            Variables.fio2 = float(msg.payload.decode())
            logger.debug("FIO2 received: %.2f" % Variables.fio2)
        elif (msg.topic == self.RR_CONFIG_TOPIC):
            Variables.rr = float(msg.payload.decode())
            logger.debug("RR received: %.2f" % Variables.rr)
        elif (msg.topic == self.PEEP_CONFIG_TOPIC):
            Variables.peep = float(msg.payload.decode())
            logger.debug("PEEP received: %.2f" % Variables.peep)
        elif (msg.topic == self.VT_CONFIG_TOPIC):
            Variables.vt = float(msg.payload.decode())
            logger.debug("VT received: %.2f" % Variables.vt)
        elif (msg.topic == self.IE_CONFIG_TOPIC):
            Variables.ie = float(msg.payload.decode())
            logger.debug("IE received: %.2f" % Variables.ie)
        elif (msg.topic == self.PS_CONFIG_TOPIC):
            Variables.ps = float(msg.payload.decode())
            logger.debug("PS received: %.2f" % Variables.ps)
        else:
            logger.debug("Message [%s] - [%s] not found" % (msg.topic, msg.payload.decode()))

    def clean_up(self):
        client.disconnect()
