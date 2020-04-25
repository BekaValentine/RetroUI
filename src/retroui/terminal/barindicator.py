from typing import Callable, List, Optional

from retroui.terminal.color import Color, Black, White
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel
from retroui.terminal.view import View


class BarIndicator(View):
    """
    A `BarIndicator` is a view for display a fraction between 0 and 1.

    Common uses for `BarIndicator`s are as progress indicators, usage meters,
    etc.

    Slots

        `is_vertical`
            Whether or not the indicator should be drawn vertically. Defaults to
            `True`.

        `value`
            The fraction of the bar that is full. Values from from 0.0 to 1.0.

        `readout_formatter`
            A function to compute the string representation of `value` for
            displaying it symbolically. If this is set to `None`, then `value`
            is shown as a percentage.

        `readout_position`
            Where the readout should be displayed relative to the bar. Possible
            values are `'beginning'` (top or left of the bar), `'end'` (bottom
            or right of the bar), and `None`. Defaults to `'end'`.

        `readout_size`
            The size of the readout region.
    """

    __slots__ = ['is_vertical', 'value',
                 'readout_formatter', 'readout_position', 'readout_size']

    def __init__(self):
        # type: () -> None
        super().__init__()

        self.is_vertical = True  # type: bool
        self.value = 0.0  # type: float
        self.readout_formatter = None  # type: Optional[Callable[[float], str]]
        self.readout_position = 'end'  # type: Optional[str]
        self.readout_size = 4  # type: int

    def constrain_size(self, new_size):
        # type: (Size) -> Size
        """
        Constrain the new size to perfectly fit the content and verticality of
        the bar indicator.
        """
        if self.is_vertical:
            return Size(self.readout_size if self.readout_position is not None else 2, max(2, new_size.height))
        else:
            return Size(max(2, new_size.width), 1)

    def set_is_vertical(self, yn):
        # type: (bool) -> None
        """
        Set whether or not the indicator is vertical.
        """

        self.is_vertical = yn

    def set_value(self, value):
        # type: (float) -> None
        """
        Set the value of the indicator, constrained to be between 0.0 and 1.0
        inclusive.
        """

        self.value = max(0.0, min(1.0, float(value)))

    def set_readout_formatter(self, fn):
        # type: (Callable[[float], str]) -> None
        """
        Set the readout formatter.
        """

        self.readout_formatter = fn

    def set_readout_position(self, pos):
        # type: (Optional[str]) -> None
        """
        Set the readout position.

        Valid arguments are `'beginning'`, `'end'`, and `None`.
        """

        if pos in ['beginning', 'end']:
            self.readout_position = pos
        else:
            self.readout_position = None

    def set_readout_size(self, size):
        # type: (int) -> None
        """
        Set the size of the readout.
        """

        self.readout_size = max(1, int(size))

    def draw(self):
        # type: () -> List[List[Tixel]]

        readout = ''  # type: str
        if self.readout_formatter is None:
            readout = '{:.0%}'.format(self.value)
        else:
            readout = str(self.readout_formatter(self.value))
            readout = readout[:self.readout_size]

        total_bar_size = 0  # type: int
        bar_lines_size = 0  # type: int
        should_show_readout = True  # type: bool
        filled_size = 0  # type: int
        unfilled_size = 0  # type: int
        lines = []  # type: List[List[Tixel]]
        if self.is_vertical:
            if self.readout_position is None:
                total_bar_size = self.size.height
                bar_lines_size = total_bar_size - 2
                should_show_readout = False
            else:
                total_bar_size = self.size.height - 2
                if total_bar_size >= 2:
                    should_show_readout = True
                else:
                    total_bar_size = self.size.height
                    should_show_readout = False
                bar_lines_size = total_bar_size - 2
                filled_size = int(self.value * bar_lines_size)
                unfilled_size = bar_lines_size - filled_size

            main_lines = []  # type: List[List[Tixel]]
            main_lines.append(
                [Tixel('=', White, Black), Tixel('=', White, Black)])
            main_lines += [[Tixel(' ', White, Black), Tixel(' ', White, Black)]
                           for i in range(unfilled_size)]
            main_lines += [[Tixel('-', White, Black), Tixel('-', White, Black)]
                           for i in range(filled_size)]
            main_lines.append(
                [Tixel('=', White, Black), Tixel('=', White, Black)])

            lines_with_readout = []  # type: List[List[Tixel]]
            if should_show_readout:
                ro = [Tixel(c, White, Black)
                      for c in readout]  # type: List[Tixel]
                if self.readout_position == 'beginning':
                    lines_with_readout = [ro, []] + main_lines
                else:
                    lines_with_readout = main_lines + [[], ro]

            else:
                lines_with_readout = main_lines

            lines = []
            for line in lines_with_readout:
                left_fill = int((self.size.width - len(line)) / 2)
                right_fill = self.size.width - len(line) - left_fill
                lines.append(left_fill * [Tixel(' ', White, Black)] +
                             line + right_fill * [Tixel(' ', White, Black)])

        else:
            if self.readout_position is None:
                total_bar_size = self.size.width
                bar_lines_size = total_bar_size - 2
                should_show_readout = False
            else:
                total_bar_size = self.size.width - self.readout_size - 1
                if total_bar_size >= 2:
                    should_show_readout = True
                else:
                    total_bar_size = self.size.width
                    should_show_readout = False
                bar_lines_size = total_bar_size - 2
                filled_size = int(self.value * bar_lines_size)
                unfilled_size = bar_lines_size - filled_size

                main_line = []
                main_line.append(Tixel('[', White, Black))
                main_line += filled_size * \
                    [Tixel('|', White, Black)]
                main_line += unfilled_size * \
                    [Tixel(' ', White, Black)]
                main_line.append(Tixel(']', White, Black))

                if should_show_readout:
                    if self.readout_position == 'beginning':
                        readout = readout[:self.readout_size].ljust(
                            self.readout_size, ' ')
                        line = [Tixel(c, White, Black) for c in readout] + \
                            [Tixel(' ', White, Black)] + main_line
                    else:
                        readout = readout[:self.readout_size].rjust(
                            self.readout_size, ' ')
                        line = main_line + \
                            [Tixel(' ', White, Black)] + \
                            [Tixel(c, White, Black)
                             for c in readout]
                else:
                    line = main_line

                lines = [line]

        return lines
