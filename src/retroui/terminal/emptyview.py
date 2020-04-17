from retroui.terminal.view import *


class EmptyView(View):
    """
    An `EmptyView` is a view used as a placeholder for other views that are
    currently set but will be set in the future.

    Displays the text "empty" in the center of the view.
    """

    def draw(self):

        top_height = int(0.5 * (self.size.height - 1))
        bottom_height = self.size.height - 1 - top_height
        left_width = int(0.5 * (self.size.width - 5))
        right_width = self.size.width - 5 - left_width

        lines = top_height * [self.size.width * [Tixel(' ', Color.White, Color.Black)]] + \
            [left_width * [Tixel(' ', Color.White, Color.Black)] + [Tixel(c, Color.White, Color.Black) for c in 'empty'] + right_width * [Tixel(' ', Color.White, Color.Black)]] + \
            bottom_height * [self.size.width *
                             [Tixel(' ', Color.White, Color.Black)]]

        return self.bound_lines(lines)
