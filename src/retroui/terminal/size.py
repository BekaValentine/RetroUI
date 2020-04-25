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
        # type: (int,int) -> None
        self.width = width  # type: int
        self.height = height  # type: int

    def __repr__(self):
        # type: () -> str
        return 'Size(%i,%i)' % (self.width, self.height)
