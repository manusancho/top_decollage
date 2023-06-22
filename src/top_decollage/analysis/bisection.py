import logging

from .analyzer import Analyzer

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
            self.min = int(context["min"])
        else:
            self.min = context["min"] = 0
        if "max" in context:
            assert int(context["max"]) == context["max"] and context["max"] > 0
            self.max = int(context["max"])
        else:
            self.max = context["max"] = context['frames']
            
        if launched == True:
            self.max = context["max"] = context["current"]
            logger.debug('New max is %s' % context["max"])
        elif launched == False:
            self.min = context["min"] = context["current"]
            logger.debug('New min is %s' % context["min"])            

    def get_next(self, context):
        
        if 'rounds' in context:
            context["rounds"] += 1
        else:
            context["rounds"] = 1
        logger.debug('Round %s' % context["rounds"])
        
        context["current"] = int(self.min + (self.max - self.min) / 2)
        logger.debug('Current frame %s' % context["current"])
        return context["current"]
    