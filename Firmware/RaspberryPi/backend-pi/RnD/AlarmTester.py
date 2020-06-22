import sys

sys.path.append('..')

from MQTTTransceiver import MQTTTransceiver
from Alarm import AlarmManager, AlarmType, AlarmLevel
import time

mqtt = MQTTTransceiver()
alarms = AlarmManager(mqtt)

pmax = 15
p=20
alarms.raise_alarm(AlarmType.PIP_REACHED, AlarmLevel.MINOR, "Current pressure (%.1f) has exceeded Pmax (%.0f)" % (p,pmax))

time.sleep(1)
p = 14.5
alarms.clear_alarm(AlarmType.PIP_REACHED, "Current pressure (%.1f) has dropped below pmax (%.0f)" % (p, pmax))
