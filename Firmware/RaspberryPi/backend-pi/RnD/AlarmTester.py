import sys

sys.path.append('..')

from MQTTTransceiver import MQTTTransceiver
from Alarm import AlarmManager, AlarmType, AlarmLevel
import time
import logging

logger = logging.getLogger(__name__)

mqtt = MQTTTransceiver()
alarms = AlarmManager(mqtt)

pmax = 15
p=20
alarms.raise_alarm(AlarmType.PMAX_REACHED, AlarmLevel.MINOR, "Current pressure (%.1f) has exceeded Pmax (%.0f)" % (p,pmax))

time.sleep(5)
p = 14.5
alarms.clear_alarm(AlarmType.PMAX_REACHED, "Current pressure (%.1f) has dropped below pmax (%.0f)" % (p, pmax))

exit()
