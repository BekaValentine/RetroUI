class Size(object):
    """
    A size in the two dimensional plane.

    Slots:

        `width`
            The width of the size.

        `height`
            The height of the size.
    """

    __slots__ = ['width', 'height']

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __repr__(self):
        return 'Size(%i,%i)' % (self.width, self.height)
