import logging

from bernard import layers as lyr
from bernard.analytics import page_view
from bernard.engine import BaseState
from bernard.i18n import intents as its
from bernard.i18n import translate as t
from bernard.platforms.facebook import layers as fbl
from bernard.platforms.telegram.layers import KeyboardButton, ReplyKeyboard

from .store import cs
from .apis.framex import FrameXApi
from .analysis.bisection import BisectionAnalyzer

logger = logging.getLogger("top_decollage.states")


class CustomBaseState(BaseState):
    """
    Root class for Number Bot.
    """

    @page_view("/bot/error")
    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """

        self.send(lyr.Text(t.ERROR))

    @page_view("/bot/confused")
    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """
        self.send(lyr.Text(t.CONFUSED))

    async def handle(self) -> None:
        raise NotImplementedError

    def get_analyzer_class(self):
        """
        Return class to request timestamps to show to the user.
        Must be a child of VideoApi
        """
        return BisectionAnalyzer

    def get_video_api_class(self):
        """
        Return a class to request video frames.
        Must return a child class of VideoApi.
        """
        return FrameXApi


class S000xAbort(CustomBaseState):
    """
    Abort the conversation
    """

    @page_view("/bot/abort")
    async def handle(self) -> None:
        self.send(
            lyr.Text(t.ABORT_MESSAGE),
        )


class S001xWelcome(CustomBaseState):
    """
    Welcome user and ask to play
    """
    @page_view("/bot/welcome")
    @cs.inject()    
    async def handle(self, context=None) -> None:
        
        # reset environment
        if context and "min" in context:
            del context["min"]
        if context and "max" in context:
            del context["max"]
        if context and "rounds" in context:
            del context["rounds"]
        if context and "current" in context:
            del context["current"]
        
        name = await self.request.user.get_friendly_name()

        self.send(
            lyr.Text(t("WELCOME", name=name)),
            lyr.Text(t.SHALL_WE_PLAY),
            ReplyKeyboard(
                keyboard=[
                    [
                        KeyboardButton(t.NOT_NOW),
                        KeyboardButton(t.PLAY),
                    ]
                ],
                one_time_keyboard=True,                
            ),
        )


class S002xInstructions(CustomBaseState):
    """
    Display the instructions
    """
    @page_view("/bot/instructions")
    @cs.inject()    
    async def handle(self, context=None) -> None:

        self.send(
            lyr.Text(t.INSTRUCTIONS),
            lyr.Text(t.ARE_YOU_READY),
            ReplyKeyboard(
                keyboard=[
                    [
                        KeyboardButton(t.NOT_REALLY),
                        KeyboardButton(t.READY),
                    ]
                ],
                one_time_keyboard=True,
            ),
        )


class S003xShowFrame(CustomBaseState):
    """
    Fetch a frame and ask user if rocket is still in the launch pad
    """

    # noinspection PyMethodOverriding
    @page_view("/bot/show-frame")
    @cs.inject()
    async def handle(self, context) -> None:

        # recover last answer
        try:
            launched = self.trigger.launched
        except:
            launched = None
        
        # adapt question depending on round
        if "current" in context:
            question = t.IS_LAUNCHED_QUESTION_REPEAT
        else:
            question = t.IS_LAUNCHED_QUESTION

        analyzer = self.get_analyzer_class()(context, launched)
        next_frame = analyzer.get_next(context)

        # get frame url
        frame_api = self.get_video_api_class()(context)
        frame_url = frame_api.get_frame(next_frame)
        
        self.send(
            lyr.Markdown("[](%s)" % 
                frame_url
            ),
            lyr.Markdown(question),
            ReplyKeyboard(
                keyboard=[
                    [
                        KeyboardButton(t.TMINUS),
                        KeyboardButton(t.TPLUS),
                    ],
                ],
                one_time_keyboard=True,
            )
        )


class S004xCongrats(CustomBaseState):
    """
    Congratulate user and show results. 
    """

    @page_view("/bot/congrats")
    @cs.inject()
    async def handle(self, context) -> None:
        
        rounds = context.get('rounds', 'few')
        t_zero_frame = context.get('current')
        
        logger.info("Found frame %s in %s rounds" % (
            t_zero_frame,
            rounds,
        ))
        
        self.send(
            lyr.Markdown("[](%s)" % 
                'https://cdn-icons-png.flaticon.com/512/7626/7626666.png'
            ),
            lyr.Markdown(
                t(
                    'CONGRATULATIONS',
                    t_zero_frame=t_zero_frame,
                    rounds=rounds,
                )
            ),
            lyr.Markdown(t.PLAY_AGAIN),
            ReplyKeyboard(
                keyboard=[
                    [
                        KeyboardButton(t.ABORT),
                        KeyboardButton(t.RESTART),
                    ]
                ],
                one_time_keyboard=True,
            )
        )