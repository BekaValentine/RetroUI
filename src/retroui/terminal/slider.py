import math
from retroui.terminal.view import *


class Slider(View):
    """
    A `Slider` is a control for selecting a value in a fixed range of values.
    They're UI analogs of volume sliders on things like audio mixers.

    Slots:

        `value`
            The current value of the slider. Ranges between 0 and the number of
            divisions minus one.

        `divisions`
            The number of divisions in the slider. Ranges between 3 and the size
            of the slider in its sliding dimension. Default: 3

        `is_vertical`
            Whether or not the slider is vertical. Default: False.
    """

    __slots__ = ['value', 'divisions', 'is_vertical']

    def __init__(self):
        super().__init__()

        self.value = 0
        self.divisions = 3
        self.is_vertical = False

    def constrain_size(self, size):
        """
        Constrain the size to be a minimum of 3 in the sliding direction, and to
        be 3 wide for vertical sliders, and 1 high for horizontal sliders.
        """

        if self.is_vertical:
            return Size(3, max(3, size.height))
        else:
            return Size(max(3, size.width), 1)

    def set_is_vertical(self, yn):
        """
        Set whether or not the slider is vertical.
        """

        self.is_vertical = bool(yn)
        self.recalculate_size()

    def recalculate_size(self):
        """
        Force a recalculation of the size using the current size as the basis.
        """

        self.set_size(self.size)

    def set_value(self, val):
        """
        Set the value of the slider.
        """

        self.value = max(0, min(self.divisions - 1, int(val)))

    def set_divisions(self, divs):
        """
        Set how many divisions the slider has.
        """

        if self.is_vertical:
            self.divisions = max(3, min(self.size.height, int(divs)))
        else:
            self.divisions = max(3, min(self.size.width, int(divs)))
        self.set_value(self.value)

    def key_press(self, ev):
        if self.is_vertical and ev.key_code == 'Up':
            self.set_value(self.value + 1)
        elif self.is_vertical and ev.key_code == 'Down':
            self.set_value(self.value - 1)
        elif not self.is_vertical and ev.key_code == 'Left':
            self.set_value(self.value - 1)
        elif not self.is_vertical and ev.key_code == 'Right':
            self.set_value(self.value + 1)
        else:
            super().key_press(ev)

    def draw(self):

        if self.is_vertical:
            position = math.floor(
                self.value * (self.size.height - 1) / (self.divisions - 1))
            pre = self.size.height - position - 1
            post = position
            lines = pre * [' | '] + ['==='] + post * [' | ']
            return [[Tixel(c, Color.White, Color.Black)
                     for c in line] for line in lines]
        else:
            position = math.floor(
                self.value * (self.size.width - 1) / (self.divisions - 1))
            pre = position
            post = self.size.width - position - 1
            line = pre * '-' + '|' + post * '-'
            return [[Tixel(c, Color.White, Color.Black) for c in line]]
