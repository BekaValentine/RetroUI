from retroui.terminal.color import *
from retroui.terminal.event import *
from retroui.terminal.tixel import *
from retroui.terminal.view import *
from retroui.terminal.emptyview import *


class SplitView(View):
    """
    A `SplitView` displays two subviews either stacked vertically or placed
    side by side.

    Slots:

        `is_vertical`
            Whether the `SplitView` is vertical and stacks its subviews one
            above the other, or horizontal, and places them side by side.

        `has_divider`
            Whether or not the `SplitView` has a divider between the two
            subviews.

        `ratio`
            The proportion of the `SplitView` that is taken up by the first
            subview.

        `first_subview`
            The top or left subview view.

        `second_subview`
            The bottom or right subview view.
    """

    __slots__ = ['is_vertical', 'has_divider',
                 'ratio', 'first_subview', 'second_subview']

    def __init__(self):
        super().__init__()

        self.is_vertical = True
        self.has_divider = True
        self.ratio = 0.5
        self.first_subview = EmptyView()
        self.second_subview = EmptyView()

    def set_first_subview(self, view):
        self.first_subview = view
        view.set_superview(self)

    def set_second_subview(self, view):
        self.second_subview = view
        view.set_superview(self)

    def subviews(self):
        return [self.first_subview, self.second_subview]

    def size_did_change(self):
        """
        Update the sizes of the subviews in response to the `SplitView`
        changing its size.
        """

        self.recalculate_sizes()

    def set_is_vertical(self, yn):
        """
        Set whether or not the `SplitView` is vertical.

        Will recalculate the sizes of the subviews.
        """

        self.is_vertical = bool(yn)
        self.recalculate_sizes()

    def set_has_divider(self, yn):
        """
        Sets whether or not the `SplitView` has a divider.

        Will recalculate the sizes of the subviews.
        """

        self.has_divider = bool(yn)
        self.recalculate_sizes()

    def set_ratio(self, r):
        """
        Sets the ratio of the subviews.

        Will recalculate the sizes of the subviews.
        """

        if r < 0:
            r = 0
        elif r > 1:
            r = 1

        self.ratio = r

        self.recalculate_sizes()

    def recalculate_sizes(self):
        """
        Recalculates the sizes of the subviews based on the size of the
        `SplitView`, the ratio, and whether or not the `SplitView` has a
        divider.
        """

        if self.is_vertical:
            if self.has_divider:
                usable_height = self.size.height - 1
            else:
                usable_height = self.size.height

            top_height = int(self.ratio * usable_height)
            bottom_height = usable_height - top_height
            self.first_subview.set_size(Size(self.size.width, top_height))
            self.second_subview.set_size(Size(self.size.width, bottom_height))
        else:
            if self.has_divider:
                usable_width = self.size.width - 1
            else:
                usable_width = self.size.width

            left_width = int(self.ratio * usable_width)
            right_width = usable_width - left_width
            self.first_subview.set_size(Size(left_width, self.size.height))
            self.second_subview.set_size(Size(right_width, self.size.height))

    def key_press(self, ev):
        """
        Handle a key press.

        When the key code is an arrow key, moves the divider in the
        appropriate direction by 1 line or two columns, if possible,
        otherwise passes the key press along to the next responder.
        """

        line_ratio = 1.0 / self.size.height
        column_ratio = 2.0 / self.size.width

        if self.is_vertical and ev.key_code == 'Up':
            self.set_ratio(self.ratio - line_ratio)
        elif self.is_vertical and ev.key_code == 'Down':
            self.set_ratio(self.ratio + line_ratio)
        elif not self.is_vertical and ev.key_code == 'Left':
            self.set_ratio(self.ratio - column_ratio)
        elif not self.is_vertical and ev.key_code == 'Right':
            self.set_ratio(self.ratio + column_ratio)
        else:
            super().key_press(ev)

    def draw(self):

        if self.is_vertical:
            if self.has_divider:
                divider_symbol = '─'
                lines = self.first_subview.draw() +\
                    [self.size.width * [Tixel(divider_symbol, Color.White, Color.Black)]] +\
                    self.second_subview.draw()
            else:
                lines = self.first_subview.draw() + self.second_subview.draw()
        else:
            if self.has_divider:
                divider_symbol = '│'
                divider_lines = self.size.height * \
                    [[Tixel(divider_symbol, Color.White, Color.Black)]]
                left_lines = self.first_subview.draw()
                right_lines = self.second_subview.draw()
                lines = []
                for y in range(self.size.height):
                    lines.append(left_lines[y] +
                                 divider_lines[y] + right_lines[y])
            else:
                left_lines = self.first_subview.draw()
                right_lines = self.second_subview.draw()
                lines = []
                for y in range(self.size.height):
                    lines.append(left_lines[y] + right_lines[y])

        return self.bound_lines(lines)
