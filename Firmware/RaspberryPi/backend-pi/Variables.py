import logging
import logging.config

logger = logging.getLogger(__name__)


class Variables:
    BUS_1 = 1 # first inspiratory pressure sensor
    BUS_2 = 3 # second inspiratory pressure sensor
    BUS_3 = 4 # first expiratory pressure sensor
    BUS_4 = 5 # second expiratory pressure sensor
    fio2 = 0    # fio2 value
    ie = 1      # I:E ratio
    rr = 10     # respiratory rate (RR)
    vt = 5      # tidal volume
    peep = 1200 # PEEP
