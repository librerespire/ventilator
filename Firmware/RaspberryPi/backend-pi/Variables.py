import logging
import logging.config

logger = logging.getLogger(__name__)

class Variables:
    fio2 = 0
    rr = 0
    ie = 0
    vt = 0
    peep = 0

    def set_fio2(self, val):
        logger.debug("Fio2 set %.2f" % val)
        self.fio2 = val

    def get_fio2(self):
        logger.debug("Fio2 return %.2f" % self.fio2)
        return self.fio2

    def set_rr(self, val):
        self.rr = val

    def set_ie(self, val):
        self.ie = val

    def set_vt(self, val):
        self.vt = val

    def set_peep(self, val):
        self.peep = val
