from typing import List

from retroui.terminal.color import Color, Black, White
from retroui.terminal.event import Event
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel
from retroui.terminal.view import View
from retroui.terminal.textview import TextView


class TextFoldView(View):
    """
    A `TextFoldView` is way to display text with a toggle-able limit on how much
    can be seen.

    Slots:

        `_text_view`
            The enclosed text view for showing the folded text.

        `folded_text`
            The text to summarize.

        `folded_length`
            The maximum length of the text to show when summarized. The text
            will include an ellipsis at the end, so that the `folded_text`
            is clipped to three less than the `folded_length`.

        `is_expanded`
            Whether or not the text is expanded to show the whole of it.
    """

    __slots__ = ['_text_view', 'folded_text',
                 'folded_length', 'is_expanded']

    def __init__(self):
        # type: () -> None
        super().__init__()

        self._text_view = TextView()  # type: TextView
        self.folded_text = ''  # type: str
        self.folded_length = 10 * 80  # type: int  # 10 lines of 80 column text
        self.is_expanded = False  # type: bool

    def constrain_size(self, size):
        # type: (Size) -> Size
        """
        Constrain the size to be one taller than the contained text view, after
        setting its line break width to be the given width.
        """

        self._text_view.set_line_break_width(size.width)
        self.adjust_text_view()
        return Size(max(1, size.width), self._text_view.size.height + 1)

    def set_folded_text(self, text):
        # type: (str) -> None
        """
        Sets the text being summarized.
        """

        self.folded_text = text
        self.adjust_size()

    def set_folded_length(self, l):
        # type: (int) -> None
        """
        Sets the folded length.
        """

        self.folded_length = int(l)
        self.adjust_size()

    def toggle_expanded(self):
        # type: () -> None
        """
        Toggles whether the view is expanded to show the full text or not.
        """

        self.set_is_expanded(not self.is_expanded)

    def set_is_expanded(self, yn):
        # type: (bool) -> None
        """
        Set whether the view is expanded to show the full text or not.
        """

        self.is_expanded = yn
        self.adjust_size()

    def adjust_text_view(self):
        # type: () -> None
        """
        Update the content of the text view and constrain its size.
        """

        self._text_view.set_line_break_width(max(1, self.size.width))

        if self.is_expanded:
            self._text_view.set_text(self.folded_text)
        else:
            self._text_view.set_text(
                self.folded_text[:self.folded_length - 3] + '...')

    def adjust_size(self):
        # type: () -> None
        """
        Trigger an update in the height of the view by setting it to 1.
        """

        self.set_size(Size(self.size.width, 1))

    def key_press(self, ev):
        # type: (Event) -> None
        if ev.key_code == 'Left':
            self.set_is_expanded(False)
        elif ev.key_code == 'Right':
            self.set_is_expanded(True)
        else:
            super().key_press(ev)

    def draw(self):
        # type: () -> List[List[Tixel]]
        self.adjust_text_view()

        lines = self._text_view.draw()

        if self.is_expanded:
            label = ' [ Show Less ] '
            pre = int((self.size.width - len(label)) / 2)
            post = self.size.width - len(label) - pre
            lines += [[Tixel(c, White, Black)
                       for c in (pre * '-' + label + post * '-')]]
        else:
            label = ' [ Show More ] '
            pre = int((self.size.width - len(label)) / 2)
            post = self.size.width - len(label) - pre
            lines += [[Tixel(c, White, Black)
                       for c in (pre * '-' + label + post * '-')]]

        return lines
