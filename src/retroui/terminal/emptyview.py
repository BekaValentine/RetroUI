from typing import List

from retroui.terminal.color import Color, Black, White
from retroui.terminal.tixel import Tixel
from retroui.terminal.view import View


class EmptyView(View):
    """
    An `EmptyView` is a view used as a placeholder for other views that are
    currently set but will be set in the future.

    Displays the text "empty" in the center of the view.
    """

    def draw(self):
        # type: () -> List[List[Tixel]]

        top_height = int(0.5 * (self.size.height - 1))
        bottom_height = self.size.height - 1 - top_height
        left_width = int(0.5 * (self.size.width - 5))
        right_width = self.size.width - 5 - left_width

        lines = top_height * [self.size.width * [Tixel(' ', White, Black)]] + \
            [left_width * [Tixel(' ', White, Black)] + [Tixel(c, White, Black) for c in 'empty'] + right_width * [Tixel(' ', White, Black)]] + \
            bottom_height * [self.size.width *
                             [Tixel(' ', White, Black)]]

        return self.bound_lines(lines)
