import logging

from bernard.engine.request import Request
from bernard.engine.triggers import Text

from .store import cs

logger = logging.getLogger("top_decollage.triggers")


class ProcessAnswer(Text):
    """
    Trigger to process user yes/no answer and pass
    it to state so that it can update the context.
    @:param request: the request object
    """
    def __init__(self, request: Request, **kwargs):
        super(Text, self).__init__(request)
        self.intent = kwargs.get('intent', None)
        self.launched = kwargs.get('launched', None)
        self.tolerance = int(kwargs.get('tolerance', 1))
        self.jump_if_finish = kwargs.get('jump_if_finish', None)

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:

        finished = (context.get('max') - context.get('min')) <= self.tolerance
        if finished:
            # rank trigger only if jump_if_finish's value is True
            return 1.0 if self.jump_if_finish else 0.0
        elif self.jump_if_finish:
            return 0.0
        else:
            return await super(ProcessAnswer, self).rank()
        


