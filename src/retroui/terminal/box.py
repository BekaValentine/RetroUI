from retroui.terminal.view import *
from retroui.terminal.clipview import *
from retroui.terminal.emptyview import *


class Box(View):
    """
    A `Box` is a view with border around it.

    Slots:

        `content_view`
            The view that is shown inside the box.
    """

    __slots__ = ['content_view']

    def __init__(self):
        super().__init__()

        self.content_view = EmptyView()

    def constrain_size(self, new_size):
        """
        Constrains the new size to be the constrained size of the content view
        plus the border.
        """

        if self.content_view is None:
            return Size(max(2, int(new_size.width)), max(2, int(new_size.height)))
        else:
            new_content_size = Size(new_size.width - 2, new_size.height - 2)
            constrained_content_size = self.content_view.constrain_size(
                new_content_size)

            return Size(2 + constrained_content_size.width, 2 + constrained_content_size.height)

    def size_did_change(self):
        """
        Inform the content view that its size has changed.
        """

        if self.content_view is not None:
            self.content_view.set_size(
                Size(self.size.width - 2, self.size.height - 2))

    def set_content_view(self, view):
        """
        Set the content view.

        Will resize the box to fit the content view.
        """

        self.content_view = view
        self.set_size(Size(2 + view.size.width, 2 + view.size.height))

    def draw(self):

        top_border = [Tixel('┌', Color.White, Color.Black)] + \
            (self.size.width - 2) * [Tixel('─', Color.White, Color.Black)] + \
            [Tixel('┐', Color.White, Color.Black)]

        bot_border = [Tixel('└', Color.White, Color.Black)] + \
            (self.size.width - 2) * [Tixel('─', Color.White, Color.Black)] + \
            [Tixel('┘', Color.White, Color.Black)]

        if self.content_view is not None:
            content_lines = self.content_view.draw()
        else:
            content_lines = []

        middle_lines = [[Tixel('│', Color.White, Color.Black)] + line +
                        [Tixel('│', Color.White, Color.Black)] for line in content_lines]

        return [top_border] + middle_lines + [bot_border]
