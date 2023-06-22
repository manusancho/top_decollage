import logging
from typing import Optional

from bernard import layers as lyr
from bernard.engine.request import Request
from bernard.engine.triggers import Text, BaseTrigger
from bernard.i18n.intents import Intent

from .store import cs

logger = logging.getLogger("top_decollage.triggers")


class LoopTrigger(Text):
    """
    Trigger to process user yes/no answer and update
    the context accordingly.
    @:param request: the request object
    """
    def __init__(self, request: Request, **kwargs):
        self.launched = kwargs.get('launched', None)
        self.intent = kwargs.get('intent', None)
        self.tolerance = kwargs.get('tolerance', 0)
        self.check_finish = kwargs.get('check_finish', False)
        self.jump_to_finish = kwargs.get('jump_to_finish', False)
        super(Text, self).__init__(request)
        
    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        min = context.get("min")
        max = context.get("max")

        if self.jump_to_finish:
            return 1.0
        elif self.check_finish:
            logger.info("Checking T0. Window: %s-%s. Tolerance: %s" % (min, max, self.tolerance))
            return 1.0 if max - min <= self.tolerance else 0.0
        else:
            return await super().rank()


class FinishTrigger(Text):
    """
    Trigger to process user yes/no answer and update
    the context accordingly.
    @:param request: the request object
    """
    def __init__(self, request: Request, **kwargs):
        self.tolerance = kwargs.get('tolerance', 0)
        super(Text, self).__init__(request)
        
    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        min = context.get("min")
        max = context.get("max")

        logger.info("Checking T0. Window: %s-%s. Tolerance: %s" % (min, max, self.tolerance))
        return 1.0 if max - min <= self.tolerance else 0.0

