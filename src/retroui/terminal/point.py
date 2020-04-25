class Point(object):
    """
    A point in the two dimensional plane.

    Slots:

        `x`
            The x-axis coordinate.

        `y`
            The y-axis coordinate.
    """

    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.x: int = x
        self.y: int = y

    def __repr__(self):
        # type: () -> str
        return 'Point(%i,%i)' % (self.x, self.y)
