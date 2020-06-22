from datetime import datetime
from enum import Enum
from MQTTTransceiver import MQTTTransceiver
import json


class AlarmManager:
    active_alarms = {}

    def __init__(self, mqtt):
        self.mqtt = mqtt

    def raise_alarm(self, code, level, message):
        alarm = AlarmDetails(code, level, message)
        self.active_alarms[code] = alarm

        # send to GUI
        self.mqtt.mqtt_publish(MQTTTransceiver.ALARMS_TOPIC, alarm.get_json_payload())

    def clear_alarm(self, code, message):
        alarm = self.active_alarms.pop(code, None)
        if alarm is None:
            return

        alarm.disable_alarm()
        alarm.set_message(message)

        # send to GUI
        self.mqtt.mqtt_publish(MQTTTransceiver.ALARMS_TOPIC, alarm.get_json_payload())


class AlarmDetails:
    def __init__(self, code, level, message):
        self.code = code
        self.active = True
        self.level = level
        self.message = message
        self.active = True

    def get_json_payload(self):
        payload = {
            'time': datetime.now().isoformat(),
            'code': self.code.value,
            'active': self.active,
            'level': self.level.value,
            'message': self.message
        }
        return json.dumps(payload)

    def disable_alarm(self):
        self.active = False

    def set_message(self, message):
        self.message = message


class AlarmType(Enum):
    PMAX_REACHED = 1
    PIP_REACHED = 2


class AlarmLevel(Enum):
    MINOR = "MINOR"
    MAJOR = "MAJOR"
