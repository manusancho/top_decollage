import logging

from .analyzer import Analyzer
from ..apis.framex import FrameXApi

logger = logging.getLogger("top_decollage.analyzer")


class BisectionAnalyzer(Analyzer):
    """
    Analyzer based on a bisection algorithm to help.
    """
    min = None
    max = None

    def __init__(self, context=None, launched=None) -> None:
        super().__init__()

        if "min" in context:
            assert int(context["min"]) == context["min"] and context["min"] >= 0
            self.min = context["min"]
        else:
            self.min = 0
            context["min"] = self.min
        if "max" in context:
            assert int(context["max"]) == context["max"] and context["max"] > 0
            self.max = context["max"]
        else:
            self.max = FrameXApi(context).get_frames()
            context["max"] = self.max
            
        if launched == True:
            self.max = context["max"] = context["current"]
            logger.debug('New max is %s' % context["max"])
        elif launched == False:
            # manage special case when window is less than two frames
            if self.max - self.min == 1:
                self.min = context["min"] = context["current"] + 1
            else:
                self.min = context["min"] = context["current"]
            logger.debug('New min is %s' % context["min"])            
            
        logger.debug('Bisection analizer initialized with %s-%s' % (self.min, self.max))

    def get_next(self, context):
        if 'rounds' in context:
            context["rounds"] += 1
        else:
            context["rounds"] = 1
            
        context["current"] = int(self.min + (self.max - self.min) / 2)
        return context["current"]
    