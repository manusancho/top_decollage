from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.i18n import (
    intents as its,
)

from .states import *
from .triggers import *

transitions = [
    # start at any point
    Tr(
        dest=S001xWelcome,
        factory=trg.Text.builder(its.START),
    ),
    # restart at any point
    Tr(
        dest=S001xWelcome,
        factory=trg.Text.builder(its.RESTART),
    ),
    # abort before start
    Tr(
        dest=S000xAbort,
        origin=S001xWelcome,
        factory=trg.Text.builder(its.NOT_NOW),
    ),
    # abort at any point
    Tr(
        dest=S000xAbort,
        factory=trg.Text.builder(its.ABORT),
    ),
    # display instructions
    Tr(
        dest=S002xInstructions,
        origin=S001xWelcome,
        factory=trg.Text.builder(its.PLAY),
    ),
    # start game
    Tr(
        dest=S003xShowFrame,
        factory=trg.Text.builder(its.READY),
    ),
    # loop until finish (use intent to infere launched)
    Tr(
        dest=S003xShowFrame,
        origin=S003xShowFrame,
        factory=ProcessAnswer.builder(intent=its.TMINUS, launched=False),
    ),
    Tr(
        dest=S003xShowFrame,
        origin=S003xShowFrame,
        factory=ProcessAnswer.builder(intent=its.TPLUS, launched=True),
    ),
    # game over
    Tr(
        dest=S004xCongrats,
        origin=S003xShowFrame,
        factory=ProcessAnswer.builder(tolerance=1, jump_if_finish=True),
    ),
]