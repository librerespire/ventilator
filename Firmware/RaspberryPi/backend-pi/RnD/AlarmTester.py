import sys

sys.path.append('..')

from MQTTTransceiver import MQTTTransceiver
from Alarm import AlarmManager, AlarmType, AlarmLevel
import time
import logging

logger = logging.getLogger(__name__)

print("going to mqtt")
mqtt = MQTTTransceiver()
print("going to AlarmManager")
alarms = AlarmManager(mqtt)

pmax = 15
p=20
print("going to raise an alarm")
alarms.raise_alarm(AlarmType.PMAX_REACHED, AlarmLevel.MINOR, "Current pressure (%.1f) has exceeded Pmax (%.0f)" % (p,pmax))

time.sleep(5)
p = 14.5
print("going to raise an alarm")
alarms.clear_alarm(AlarmType.PMAX_REACHED, "Current pressure (%.1f) has dropped below pmax (%.0f)" % (p, pmax))

logger.debug("Exiting")
exit()
