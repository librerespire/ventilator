import logging
import logging.config

logger = logging.getLogger(__name__)


class Variables:
    BUS_1 = 1 # first inspiratory pressure sensor
    BUS_2 = 3 # second inspiratory pressure sensor
    BUS_3 = 4 # first expiratory pressure sensor
    BUS_4 = 5 # second expiratory pressure sensor
    fio2 = 0
    rr = 10
    #TODO remove ie_i and ie_e as those are no need
    # we can use only ie for ie_ratio as 4:1 is equalant to 1:0.25
    # so we can keep 1 as constant and ie as portion of it
    ie_i = 1  # I part of IE ratio
    ie_e = 1  # E part of IE ratio
    vt = 5
    peep = 1200
    ie = 1
