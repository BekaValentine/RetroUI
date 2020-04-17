import math
import re
import textwrap

from retroui.terminal.view import *


class TextView(View):
    """
    A `TextView` displays text and provides line breaking and alignment
    capabilities.

    Slots:

        `text`
            The text that the `TextView` displays.

        `_text_pars`
            An internal representation of the lines of text as paragraphs
            computed after line breaks.

        `line_break_mode`
            The specification for how to break lines. Possible values are

            `'word_wrapping'`
                Default value. Wraps by breaking between words at white space.

            `'char_wrapping'`
                Wraps by breaking between characters, possibly in the middle of
                words.

            `'clipping'`
                Text is not wrapped but simply omitted beyond the edge of the
                view.

            `'truncating_head'`
                Text is displayed by showing the end of the text, and replacing
                the beginning with an ellipsis.

            `'truncating_tail'`
                Text is displayed by showing the beginning of the text, and
                replacing the end with an ellipsis.


            `'truncating_both'`
                Text is displayed by showing the beginning and end of the text,
                and replacing the middle with an ellipsis.


        `line_break_width`
            The width at which to break lines of text. A `None` value indicates
            no line breaking.

        `alignment`
            Whether the text is aligned left, center, right, or justified.
    """

    @staticmethod
    def split_at_length(text, length):
        """
        Splits a string into sequential segments no longer than the given
        length.
        """

        parts = []
        while len(text) != 0:
            parts.append(text[:length])
            text = text[length:]

        return parts

    @staticmethod
    def align(text, alignment, width):
        """
        Aligns a text line in the specified direction within the given width.
        """

        if alignment == 'right':
            return TextView.right_align(text, width)
        elif alignment == 'center':
            return TextView.center_align(text, width)
        elif alignment == 'justified':
            return TextView.justify(text, width)
        else:
            return TextView.left_align(text, width)

    @staticmethod
    def left_align(text, width):
        """
        Aligns the text left, by padding the right edge with spaces up to the
        given width.
        """

        return text.ljust(width, ' ')

    @staticmethod
    def right_align(text, width):
        """
        Aligns the text right, by padding the left edge with spaces up to the
        given width.
        """

        return text.rjust(width, ' ')

    @staticmethod
    def center_align(text, width):
        """
        Aligns the text center, by padding the left and right edges with spaces
        up to the given width.
        """

        rwidth = math.ceil(len(text) + 0.5 * (width - len(text)))
        return text.rjust(rwidth, ' ').ljust(width, ' ')

    @staticmethod
    def justify(text, width):
        """
        Aligns the text justified, by inserting spaces between words up to the
        given width.
        """

        words = text.split()

        if len(words) < 2:
            return text.ljust(width, ' ')

        spaces = (len(words) - 1) * [' ']

        space_index = 0
        while len(''.join(words) + ''.join(spaces)) < width:
            spaces[space_index] += ' '
            space_index = (space_index + 1) % (len(spaces) - 1)

        new_text = ''
        for i, word in enumerate(words[:-1]):
            new_text += word + spaces[i]
        new_text += words[-1]
        return new_text

    __slots__ = ['text', '_text_pars', 'line_break_mode',
                 'line_break_width', 'alignment']

    def __init__(self):
        super().__init__()

        self.text = ''
        self._text_pars = []
        self.line_break_width = None
        self.line_break_mode = 'word_wrapping'
        self.alignment = 'left'

        self.recalculate_text_pars()

    def set_text(self, text):
        """
        Set the text of the view.

        Will recalculate `_text_pars`.
        """

        self.text = text

        self.recalculate_text_pars()

    def set_line_break_mode(self, mode):
        """
        Set the line break mode.

        Will recalculate `_text_pars`.
        """

        self.line_break_mode = mode

        self.recalculate_text_pars()

    def set_line_break_width(self, width):
        """
        Set the line break width.

        Will recalculate `_text_pars`.
        """

        self.line_break_width = width

        self.recalculate_text_pars()

    def set_alignment(self, align):
        """
        Set the text alignment.
        """

        if align in ('left', 'right', 'center', 'justified'):
            self.alignment = align
        else:
            self.alignment = 'left'

    def recalculate_text_pars(self):
        """
        Re-calculates the `_text_pars` property.

        Will recalculate size.
        """

        lines = self.text.split('\n')
        self._text_pars = []
        for line in lines:
            if self.line_break_width is not None:

                if self.line_break_mode == 'char_wrapping':
                    par = []
                    if not line:
                        par = ['']
                    else:
                        par = TextView.split_at_length(
                            line, self.line_break_width)
                    self._text_pars.append(par)

                elif self.line_break_mode == 'clipping':
                    self._text_pars.append([line[:self.line_break_width]])

                elif self.line_break_mode == 'truncating_head':
                    if len(line) <= self.line_break_width:
                        par = [line]
                    else:
                        par = ['...' + line[-self.line_break_width + 3:]]

                    self._text_pars.append(par)

                elif self.line_break_mode == 'truncating_tail':
                    if len(line) <= self.line_break_width:
                        par = [line]
                    else:
                        par = [line[:self.line_break_width - 3] + '...']

                    self._text_pars.append(par)

                elif self.line_break_mode == 'truncating_middle':
                    if len(line) <= self.line_break_width:
                        par = [line]
                    else:
                        head_length = int(0.5 * (self.line_break_width - 3))
                        tail_length = self.line_break_width - 3 - head_length
                        par = [line[:head_length] +
                               '...' + line[-tail_length:]]

                    self._text_pars.append(par)

                else:  # default, includes 'word_wrapping':
                    if not line:
                        par = ['']
                    else:
                        par = textwrap.wrap(line, width=self.line_break_width)
                    self._text_pars.append(par)

            else:
                self._text_pars.append([line])

        self.recalculate_size()

    def recalculate_size(self):
        """
        Recalculates the size of the view based on the `_text_pars` property.

        The resulting size will perfectly fit the text.
        """

        if self.line_break_width is not None:
            new_height = 0
            for par in self._text_pars:
                new_height += len(par)
            self.set_size(Size(self.line_break_width, new_height))
        else:
            new_width = 0
            for par in self._text_pars:
                for line in par:
                    if len(line) > new_width:
                        new_width = len(line)
            new_height = len(self._text_pars)
            self.set_size(Size(new_width, new_height))

    def draw(self):
        lines = []
        for par in self._text_pars:
            lines += [TextView.align(line, self.alignment,
                                     self.size.width) for line in par]

        tixel_lines = [[Tixel(c, Color.White, Color.Black)
                        for c in line] for line in lines]

        return tixel_lines
