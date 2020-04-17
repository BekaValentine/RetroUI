from retroui.terminal.view import *


class Scroller(View):
    """
    A `Scroller` is a view used to indicate where scrollable content is
    positioned, and what fraction of that content is currently visible.

    Slots:

        `is_vertical`
            Whether or not the scroller is vertical, or horizontal. True by
            default.

        `scroll_position`
            How far into the content the visible portion of the content is.
            Ranges from 0.0, for when the content is scrolled to the
            beginning, to 1.0 for when the content has scrolled to the end.

        `visible_fraction`
            The fraction of the content that is currently visible in its
            containing view. Ranges from 0.0 to 1.0.
    """

    __slots__ = ['is_vertical', 'position', 'visible_fraction']

    def __init__(self):

        super().__init__()

        self.is_vertical = True
        self.scroll_position = 0.0
        self.visible_fraction = 1.0

    def set_is_vertical(self, yn):
        """
        Set whether the scroller is vertical or horizontal.
        """

        self.is_vertical = bool(yn)

    def set_scroll_position(self, pos):
        """
        Set the scroll position.
        """

        self.scroll_position = max(0.0, min(1.0, float(pos)))

    def set_visible_fraction(self, frac):
        """
        Set the visible fraction.
        """

        self.visible_fraction = min(1.0, max(0.0, float(frac)))

    def constrain_size(self, new_size):
        """
        The size of a scroller is constrained to be at most 1 wide if the
        scroller is vertical, and 1 tall if the scroller is horizontal.
        """

        if self.is_vertical:
            return Size(1, new_size.height)
        else:
            return Size(new_size.width, 1)

    def draw(self):
        if self.is_vertical:
            scrollbar_height = max(
                1, int(self.visible_fraction * self.size.height))
            available_scrollbar_positions = self.size.height - scrollbar_height
            current_scrollbar_position = int(
                self.scroll_position * available_scrollbar_positions)

            blanksym = '│'
            barsym = '█'
            preblank = current_scrollbar_position * [blanksym]
            bar = scrollbar_height * [barsym]
            postblank = (available_scrollbar_positions -
                         current_scrollbar_position) * [blanksym]
            lines = preblank + bar + postblank
        else:
            scrollbar_width = max(
                1, int(self.visible_fraction * self.size.width))
            available_scrollbar_positions = self.size.width - scrollbar_width
            current_scrollbar_position = int(
                self.scroll_position * available_scrollbar_positions)

            blanksym = '─'
            barsym = '█'
            preblank = current_scrollbar_position * blanksym
            bar = scrollbar_width * barsym
            postblank = (available_scrollbar_positions -
                         current_scrollbar_position) * blanksym
            lines = [preblank + bar + postblank]

        tixel_lines = [[Tixel(c, Color.White, Color.Black)
                        for c in line] for line in lines]

        return tixel_lines
