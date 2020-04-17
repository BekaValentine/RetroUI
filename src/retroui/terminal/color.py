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
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a


Color.Black = Color(0, 0, 0, 255)
Color.White = Color(255, 255, 255, 255)
Color.Red = Color(255, 0, 0, 255)
Color.Orange = Color(255, 127, 0, 255)
Color.Yellow = Color(255, 255, 0, 255)
Color.Green = Color(0, 255, 0, 255)
Color.Teal = Color(0, 255, 255, 255)
Color.Blue = Color(0, 0, 255, 255)
Color.Purple = Color(127, 0, 255, 255)
Color.Magenta = Color(255, 0, 255, 255)
Color.Clear = Color(0, 0, 0, 0)
