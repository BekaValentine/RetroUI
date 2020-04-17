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
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point(%i,%i)' % (self.x, self.y)
