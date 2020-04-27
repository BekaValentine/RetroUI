import math
import textwrap

from retroui.terminal.color import White, Black
from retroui.terminal.tixel import Tixel, tixels
from retroui.terminal.view import View


class TextField(View):
    """
    A `TextField` is an input method for text.

    Slots:

        `text`
            The text to edit.

        `cursor_line`
            The line number where the cursor is located.

        `cursor_column`
            The column number where the cursor is located.

        `_lines`
            An internal representation of the lines of the `TextField`.

        `_move_column`
            An internal track of which column the user is trying to move to,
            independent of whether or not the destination line has that many
            columns.
    """

    __slots__ = ['text', 'cursor_position', '_lines', '_move_column']

    def __init__(self):
        super().__init__()

        self.text = ''  # type: str
        self.cursor_line = 0  # type: int
        self.cursor_column = 0  # type: int
        self._lines = []  # type: List[str]
        self._move_column = 0

    def set_text(self, new_text):
        # type: (str) -> None
        """
        Sets the text of the `TextField` and moves the cursor to the end.
        """

        self.text = new_text
        self._lines = new_text.split('\n')

    def set_cursor_position(self, line, col):
        self.cursor_line = line
        self.cursor_column = col

    def rendered_cursor_position(self):
        lines_before = sum([math.ceil(len(line + '\\') / self.size.width)
                            for line in self._lines[:self.cursor_line]]) + \
            math.floor(self.cursor_column / self.size.width)

        columns_before = self.cursor_column % self.size.width

        return (lines_before, columns_before)

    def key_press(self, ev):
        if ev.key_code == 'Home':
            self.cursor_line = 0
            self.cursor_column = 0
        elif ev.key_code == 'End':
            self.cursor_line = len(self._lines) - 1
            self.cursor_column = len(self._lines[self.cursor_line])
        elif ev.key_code == 'Right':
            if self.cursor_column + 1 <= len(self._lines[self.cursor_line]):
                self.cursor_column += 1
            elif self.cursor_line + 1 < len(self._lines):
                self.cursor_column = 0
                self.cursor_line = min(
                    self.cursor_line + 1, len(self._lines) - 1)

            self._move_column = self.cursor_column % self.size.width

        elif ev.key_code == 'Left':
            if self.cursor_column - 1 >= 0:
                self.cursor_column -= 1
            elif self.cursor_line - 1 >= 0:
                self.cursor_line -= 1
                self.cursor_column = len(self._lines[self.cursor_line])

            self._move_column = self.cursor_column % self.size.width

        elif ev.key_code == 'Down':

            # is there a pseudoline below the current pseudoline?
            has_another_pseudoline = len(
                self._lines[self.cursor_line]) + 1 > self.size.width * (1 + self.cursor_column // self.size.width)
            if has_another_pseudoline:
                self.cursor_column = min(
                    len(self._lines[self.cursor_line]), self.cursor_column + self.size.width)
            elif self.cursor_line + 1 < len(self._lines):
                self.cursor_line += 1

                destination = min(self._move_column, len(
                    self._lines[self.cursor_line]))
                self.cursor_column = destination

        elif ev.key_code == 'Up':
            if self.cursor_column >= self.size.width:
                next_pseudoline = self.cursor_column // self.size.width - 1
                self.cursor_column = self.size.width * next_pseudoline + self._move_column
            elif self.cursor_line - 1 >= 0:
                self.cursor_line -= 1
                pseudocolumn = self._move_column % self.size.width

                pseudolines = math.ceil(
                    (len(self._lines[self.cursor_line]) + 1) / self.size.width)
                length_of_last_pseudoline = len(
                    self._lines[self.cursor_line]) + 1 - self.size.width * (pseudolines - 1)

                if pseudocolumn < length_of_last_pseudoline:
                    self.cursor_column = len(
                        self._lines[self.cursor_line]) + 1 - length_of_last_pseudoline + pseudocolumn
                else:
                    self.cursor_column = len(
                        self._lines[self.cursor_line])

        elif len(ev.key_code) == 1 and ord(ev.key_code) in range(32, 127):
            new_line = self._lines[self.cursor_line]
            new_line = new_line[:self.cursor_column] + \
                ev.key_code + new_line[self.cursor_column:]
            new_lines = self._lines[:self.cursor_line] + \
                [new_line] + self._lines[self.cursor_line + 1:]
            self.set_text('\n'.join(new_lines))
            self.cursor_column += 1
        elif ev.key_code == 'Enter':
            new_line_a = self._lines[self.cursor_line][:self.cursor_column]
            new_line_b = self._lines[self.cursor_line][self.cursor_column:]
            new_lines = self._lines[:self.cursor_line] +\
                [new_line_a, new_line_b] +\
                self._lines[self.cursor_line + 1:]
            self.set_text('\n'.join(new_lines))
            self.cursor_line += 1
            self.cursor_column = 0
        elif ev.key_code == 'Backspace':
            if self.cursor_column > 0:
                new_line = self._lines[self.cursor_line]
                new_line = new_line[:self.cursor_column - 1] + \
                    new_line[self.cursor_column:]
                new_lines = self._lines[:self.cursor_line] + \
                    [new_line] + self._lines[self.cursor_line + 1:]
                self.set_text('\n'.join(new_lines))
                self.cursor_column -= 1
            elif self.cursor_line > 0:
                self.cursor_column = len(self._lines[self.cursor_line - 1])
                new_line = self._lines[self.cursor_line - 1] +\
                    self._lines[self.cursor_line]
                new_lines = self._lines[:self.cursor_line - 1] + \
                    [new_line] + self._lines[self.cursor_line + 1:]
                self.set_text('\n'.join(new_lines))
                self.cursor_line -= 1
        elif ev.key_code == 'Delete':
            if self.cursor_column < len(self._lines[self.cursor_line]):
                new_line = self._lines[self.cursor_line][:self.cursor_column] + \
                    self._lines[self.cursor_line][self.cursor_column + 1:]
                new_lines = self._lines[:self.cursor_line] + \
                    [new_line] + self._lines[self.cursor_line + 1:]
                self.set_text('\n'.join(new_lines))
            else:
                new_line = self._lines[self.cursor_line] +\
                    self._lines[self.cursor_line + 1]
                new_lines = self._lines[:self.cursor_line] + \
                    [new_line] + self._lines[self.cursor_line + 2:]
                self.set_text('\n'.join(new_lines))
        else:
            super().key_press(ev)

    def draw(self):
        rendered_text_lines = []
        for line in self._lines:
            line += '\\'
            while len(line) != 0:
                rendered_text_lines.append(line[:self.size.width])
                line = line[self.size.width:]

        rendered_lines = []
        cpos = self.rendered_cursor_position()

        for lno, line in enumerate(rendered_text_lines):
            rendered_line = []
            for cno, c in enumerate(line):
                if (lno, cno) == cpos:
                    rendered_line.append(Tixel(c, Black, White))
                else:
                    rendered_line.append(Tixel(c, White, Black))

            rendered_lines.append(rendered_line)

        return rendered_lines
