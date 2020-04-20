import math

from retroui.terminal.view import *
from retroui.terminal.clipview import *
from retroui.terminal.emptyview import *


class Box(View):
    """
    A `Box` is a view with border around it.

    Slots:

        `content_view`
            The view that is shown inside the box.

        `title`
            The title to show at the top of the box.

        `title_style`
            The style to use to display the title. Possible values are:

            `None`
                Do not display the title at all. Default.

            `'plain'`
                Displays just the title text with no visible title bar.

            `'fit_bar'`
                Displays the title inside a title bar that closely fits the
                title text.

            `'full_width_bar'`
                Displays the title inside a title bar that is the width of the
                box.

        `title_alignment`
            The horizontal alignment of the title at the top of the box.
            Possible values are:

            `'left'`
                Align the title to the left side of the box.

            `'center'`
                Align the title to the middle of the box.

            `'right'`
                Align the title to the right of the box.
    """

    __slots__ = ['content_view', 'title', 'title_style', 'title_alignment']

    def __init__(self):
        super().__init__()

        self.content_view = EmptyView()

        self.title = ''
        self.title_style = None
        self.title_alignment = 'left'

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

    def set_title(self, title):
        self.title = title

    def set_title_style(self, style):
        if style is None or style in ['plain', 'fit_bar', 'full_width_bar']:
            self.title_style = style
        else:
            self.title_style = None

    def set_title_alignment(self, alignment):
        if alignment in ['left', 'center', 'right']:
            self.title_alignment = alignment
        else:
            self.title_alignment = 'left'

    def draw(self):

        max_title_width = self.size.width - 4
        title = self.title
        if len(title) > max_title_width:
            title = title[:max_title_width - 3] + '...'

        if self.title_style is None:
            top_border = '┌' + (self.size.width - 2) * '─' + '┐'
        elif self.title_style == 'plain':
            if self.title_alignment == 'left':
                top_border = '┌ ' + title + ' ' + \
                    (self.size.width - 4 - len(title)) * '─' + '┐'

            elif self.title_alignment == 'right':
                top_border = '┌' + (self.size.width - 4 -
                                    len(title)) * '─' + ' ' + title + ' ┐'

            elif self.title_alignment == 'center':
                top_border = '┌' + \
                    math.floor(0.5 * (self.size.width - 4 - len(title))) * '─' + \
                    ' ' + title + ' ' + \
                    math.ceil(0.5 * (self.size.width - 4 - len(title))) * '─' + \
                    '┐'
            top_border = [Tixel(c, Color.White, Color.Black)
                          for c in top_border]

        elif self.title_style == 'fit_bar':
            if self.title_alignment == 'left':
                top_border = Tixel.tixels('┌', Color.White, Color.Black) + \
                    Tixel.tixels(' ' + title + ' ', Color.Black, Color.White) + \
                    Tixel.tixels((self.size.width - 4 - len(title))
                                 * '─' + '┐', Color.White, Color.Black)

            elif self.title_alignment == 'right':
                top_border = Tixel.tixels('┌' + (self.size.width - 4 - len(title)) * '─', Color.White, Color.Black) + \
                    Tixel.tixels(' ' + title + ' ', Color.Black, Color.White) + \
                    Tixel.tixels('┐', Color.White, Color.Black)

            elif self.title_alignment == 'center':
                top_border = Tixel.tixels('┌' + math.floor(0.5 * (self.size.width - 4 - len(title))) * '─', Color.White, Color.Black) + \
                    Tixel.tixels(' ' + title + ' ', Color.Black, Color.White) + \
                    Tixel.tixels(math.ceil(
                        0.5 * (self.size.width - 4 - len(title))) * '─' + '┐', Color.White, Color.Black)

        elif self.title_style == 'full_width_bar':
            if self.title_alignment == 'left':
                top_border = Tixel.tixels('┌', Color.White, Color.Black) + \
                    Tixel.tixels(' ' + title + (self.size.width - 3 - len(title)) * ' ', Color.Black, Color.White) + \
                    Tixel.tixels('┐', Color.White, Color.Black)

            elif self.title_alignment == 'right':
                top_border = Tixel.tixels('┌', Color.White, Color.Black) + \
                    Tixel.tixels((self.size.width - 3 - len(title)) * ' ' + title + ' ', Color.Black, Color.White) + \
                    Tixel.tixels('┐', Color.White, Color.Black)

            elif self.title_alignment == 'center':
                top_border = Tixel.tixels('┌', Color.White, Color.Black) + \
                    Tixel.tixels(math.floor(0.5 * (self.size.width - 2 - len(title))) * ' ' + title + math.ceil(0.5 * (self.size.width - 2 - len(title))) * ' ', Color.Black, Color.White) + \
                    Tixel.tixels('┐', Color.White, Color.Black)

        bot_border = Tixel.tixels(
            '└' + (self.size.width - 2) * '─' + '┘', Color.White, Color.Black)

        if self.content_view is not None:
            content_lines = self.content_view.draw()
        else:
            content_lines = []

        middle_lines = [[Tixel('│', Color.White, Color.Black)] + line +
                        [Tixel('│', Color.White, Color.Black)] for line in content_lines]

        return [top_border] + middle_lines + [bot_border]
