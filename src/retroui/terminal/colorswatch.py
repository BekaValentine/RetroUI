from typing import List

from retroui.terminal.color import Color
from retroui.terminal.tixel import Tixel
from retroui.terminal.view import View


class ColorSwatch(View):
    """
    A `ColorSwatch` is a view that displays a small patch of color.

    Slots:

        `color`
            The color to display.
    """

    __slots__ = ['color']

    def __init__(self):
        self.color = Color(0, 0, 0, 255)  # type: Color

    def set_color(self, color):
        # type: (Color) -> None
        """
        Set the color of the swatch.
        """

        self.color = color

    def draw(self):
        # type: () -> List[List[Tixel]]

        return self.size.height * [self.size.width * [Tixel(' ', self.color, self.color)]]
