from enum import Enum


class Commands(Enum):
    START = 'start'
    CLEAR = 'clear'

    # set_context conversation commands
    SET_CONTEXT = 'set_context'
    CANCEL = 'cancel'
