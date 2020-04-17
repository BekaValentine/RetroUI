class Event(object):
    """
    A user input event.

    Slots:

        `key_code`
            The numeric code for the key pressed during the input event.

        `has_ctrl_modifier`
            Whether or not the Ctrl key was press.

        `has_alt_modifier`
            Whether or not the Alt key was pressed.

        `has_shift_modifier`
            Whether or not the Shift key was pressed.
    """

    __slots__ = ['key_code', 'has_ctrl_modifier',
                 'has_alt_modifier', 'has_shift_modifier']

    def __init__(self, ch, ctrl, alt, shift):
        self.key_code = ch
        self.has_ctrl_modifier = ctrl
        self.has_alt_modifier = alt
        self.has_shift_modifier = shift
