class Tixel(object):
    """
    A `Tixel` is a textual picture element, corresponding to a single character
    with a foreground and background color.

    When used for rendering images, it would correspond to two pixels vertically
    stacked.

    Slots:

        `character`
            The character shown in the tixel.

        `foreground_color`
            The foreground color of the tixel, i.e. the color of the character.

        `background_color`
            The background color of the tixel.

    """

    def __init__(self, ch, fg, bg):
        if len(ch) >= 1:
            self.character = ch[0]
        else:
            self.character = ' '
        self.foreground_color = fg
        self.background_color = bg

    def render_to_screen_tixel(self):
        """
        Converts the tixel to the representation required for `ScreenManager` to
        properly draw it.

        Does not include alpha blending information.
        """

        if self.foreground_color is None:
            fg = None
        else:
            fg = (self.foreground_color.red, self.foreground_color.green,
                  self.foreground_color.blue)

        if self.background_color is None:
            bg = None
        else:
            bg = (self.background_color.red, self.background_color.green,
                  self.background_color.blue)

        return (self.character, fg, bg)
