from retroui.terminal.minmax import minmax


class Color(object):
    """
    A `Color` represents an RGBA color.

    Slots:

        `red`
            The red value, from 0 to 255.

        `green`
            The green value, from 0 to 255.

        `blue`
            The blue value, from 0 to 255.

        `alpha`
            The alpha value, from 0 to 255.
    """

    __slots__ = ['red', 'green', 'blue', 'alpha']

    def __init__(self, r, g, b, a):
        # type: (int,int,int,int) -> None
        self.red = minmax(r, 0, 255)  # type: int
        self.green = minmax(g, 0, 255)  # type: int
        self.blue = minmax(b, 0, 255)  # type: int
        self.alpha = minmax(a, 0, 255)  # type: int

    def __repr__(self):
        # type: () -> str
        return 'Color(%s,%s,%s,%s)' % (self.red, self.green, self.blue, self.alpha)


Black = Color(0, 0, 0, 255)  # type: Color
Grey = Color(127, 127, 127, 255)  # type: Color
Gray = Grey  # type: Color
White = Color(255, 255, 255, 255)  # type: Color
Red = Color(255, 0, 0, 255)  # type: Color
Orange = Color(255, 127, 0, 255)  # type: Color
Yellow = Color(255, 255, 0, 255)  # type: Color
Green = Color(0, 255, 0, 255)  # type: Color
Teal = Color(0, 255, 255, 255)  # type: Color
Blue = Color(0, 0, 255, 255)  # type: Color
Purple = Color(127, 0, 255, 255)  # type: Color
Magenta = Color(255, 0, 255, 255)  # type: Color
Clear = Color(0, 0, 0, 0)  # type: Color
