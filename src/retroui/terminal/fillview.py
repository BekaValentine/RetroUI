from retroui.terminal.tixel import *
from retroui.terminal.view import *


class FillView(View):
    """
    A `FillView` is a view that draws a solid swatch of characters.

    Slots:

        `fill_character`
            The character to fill the view with.
    """

    __slots__ = ['fill_character']

    def __init__(self):
        super().__init__()

        self.fill_character = ' '

    def set_fill_character(self, character):
        """
        Sets the fill character.
        """
        self.fill_character = character

    def draw(self):
        return self.size.height * [self.size.width * [Tixel(self.fill_character, None, None)]]
