from retroui.terminal.view import *
from retroui.terminal.textview import *


class SummaryView(View):
    """
    A `SummaryView` is way to display text with a toggle-able limit on how much
    can be seen.

    Slots:

        `_text_view`
            The enclosed text view for showing the summary.

        `summarized_text`
            The text to summarize.

        `summary_length`
            The maximum length of the text to show when summarized. The text
            will include an ellipsis at the end, so that the `summarized_text`
            is clipped to three less than the `summary_length`.

        `is_expanded`
            Whether or not the summary is expanded to show the whole text.
    """

    __slots__ = ['_text_view', 'summarized_text',
                 'summary_length', 'is_expanded']

    def __init__(self):
        super().__init__()

        self._text_view = TextView()
        self.summarized_text = ''
        self.summary_length = 4 * 80  # 4 lines of 80 column text
        self.is_expanded = False

    def constrain_size(self, size):
        """
        Constrain the size to be one taller than the contained text view, after
        setting its line break width to be the given width.
        """

        self._text_view.set_line_break_width(size.width)
        self.adjust_text_view()
        return Size(max(1, size.width), self._text_view.size.height + 1)

    def set_summarized_text(self, text):
        """
        Sets the text being summarized.
        """

        self.summarized_text = text
        self.adjust_size()

    def set_summary_length(self, l):
        """
        Sets the summary length.
        """

        self.summary_length = int(l)
        self.adjust_size()

    def toggle_expanded(self):
        """
        Toggles whether the view is expanded to show the full text or not.
        """

        self.set_is_expanded(not self.is_expanded)

    def set_is_expanded(self, yn):
        """
        Set whether the view is expanded to show the full text or not.
        """

        self.is_expanded = bool(yn)
        self.adjust_size()

    def adjust_text_view(self):
        """
        Update the content of the text view and constrain its size.
        """

        self._text_view.set_line_break_width(max(1, self.size.width))

        if self.is_expanded:
            self._text_view.set_text(self.summarized_text)
        else:
            self._text_view.set_text(
                self.summarized_text[:self.summary_length - 3] + '...')

    def adjust_size(self):
        """
        Trigger an update in the height of the view by setting it to 1.
        """

        self.set_size(Size(self.size.width, 1))

    def key_press(self, ev):
        if ev.key_code == 'Left':
            self.set_is_expanded(False)
        elif ev.key_code == 'Right':
            self.set_is_expanded(True)
        else:
            super().key_press(ev)

    def draw(self):
        self.adjust_text_view()

        lines = self._text_view.draw()

        if self.is_expanded:
            pre = int((self.size.width - 14) / 2)
            post = self.size.width - 14 - pre
            lines += [[Tixel(c, Color.White, Color.Black)
                       for c in (pre * '-' + ' [ Collapse ] ' + post * '-')]]
        else:
            pre = int((self.size.width - 12) / 2)
            post = self.size.width - 12 - pre
            lines += [[Tixel(c, Color.White, Color.Black)
                       for c in (pre * '-' + ' [ Expand ] ' + post * '-')]]

        return lines
