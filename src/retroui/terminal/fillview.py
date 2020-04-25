from typing import List

from retroui.terminal.color import Color, Black, White
from retroui.terminal.tixel import Tixel
from retroui.terminal.view import View


class FillView(View):
    """
    A `FillView` is a view that draws a solid swatch of characters.

    Slots:

        `fill_character`
            The character to fill the view with.
    """

    __slots__ = ['fill_character']

    def __init__(self):
        # type: () -> None
        super().__init__()

        self.fill_character = ' '  # type: str

    def set_fill_character(self, character):
        # type: (str) -> None
        """
        Sets the fill character.
        """
        self.fill_character = character

    def draw(self):
        # type: () -> List[List[Tixel]]
        return self.size.height * [self.size.width * [Tixel(self.fill_character, White, Black)]]
