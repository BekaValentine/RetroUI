import math
from typing import List, Optional, Union

from retroui.terminal.color import White, Black
from retroui.terminal.event import Event
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel, tixels
from retroui.terminal.view import View


class Stepper(View):
    """
    A `Stepper` is a means of controlling an input value that is not fractional,
    but rather is defined by increments, possibly infinite in range.

    Slots:

        `is_float`
            Whether or not the stepper uses float values. Default: False.

        `_steps`
            How many increments, in whole numbers, produce the current value.

        `value`
            The current value of the stepper.

        `step_size`
            The amount to increment and decrement by.

        `maximum_value`
            The maximum value.

        `minimum_value`
    """

    __slots__ = ['is_float', 'value', 'increment_amount',
                 'maximum_value', 'minimum_value']

    def __init__(self):
        # type: () -> None
        super().__init__()
        self.is_float = False  # type: bool
        self._steps = 0  # type: int
        self.value = 0  # type: Union[int,float]
        self.step_size = 1  # type: Union[int,float]
        self.maximum_value = None  # type: Optional[Union[int,float]]
        self.minimum_value = None  # type: Optional[Union[int,float]]

    def constrain_size(self, new_size):
        # type: (Size) -> Size
        """
        Constrain the size to have enough room for ellipsis and arrows.
        """

        return Size(max(7, new_size.width), 1)

    def set_is_float(self, yn):
        # type: (bool) -> None
        """
        Set whether or not the `Stepper` uses float values.
        """

        self.is_float = yn
        self._set_steps(self._steps)

    def _set_steps(self, new_steps):
        # type: (int) -> None
        """
        Sets the number of steps.
        """

        if self.maximum_value is not None:
            max_steps = math.floor(self.maximum_value / self.step_size)
            new_steps = min(new_steps, max_steps)

        if self.minimum_value is not None:
            min_steps = math.ceil(self.minimum_value / self.step_size)
            new_steps = max(min_steps, new_steps)

        self._steps = new_steps
        self.value = self._steps * self.step_size

    def set_value(self, val):
        # type: (Union[int,float]) -> None
        """
        Sets the value, rounding to the nearest whole multiple of the step size.
        """

        if self.is_float:
            val = float(val)
        else:
            val = int(val)

        self._set_steps(round(val / self.step_size))

    def increment(self):
        # type: () -> None
        """
        Increments the value by the step size.
        """

        self._set_steps(self._steps + 1)

    def decrement(self):
        # type: () -> None
        """
        Decrements the value by the step size.
        """

        self._set_steps(self._steps - 1)

    def set_step_size(self, step):
        # type: (Union[int,float]) -> None
        """
        Sets the step size.

        Will adjust the value to be a whole multiple of the new step size.
        """

        if self.is_float:
            step = float(step)
        else:
            step = int(step)

        self.step_size = step
        self._set_steps(round(self.value / self.step_size))

    def set_maximum_value(self, maxval):
        # type: (Optional[Union[int,float]]) -> None
        """
        Sets the maximum value.
        """

        if maxval is not None:
            if self.minimum_value is not None and maxval < self.minimum_value:
                return

            if self.is_float:
                maxval = float(maxval)
            else:
                maxval = int(maxval)

            self.value = min(self.value, maxval)

        self.maximum_value = maxval
        self._set_steps(self._steps)

    def set_minimum_value(self, minval):
        # type: (Optional[Union[int,float]]) -> None
        """
        Sets the minimum value.
        """

        if minval is not None:
            if self.maximum_value is not None and minval > self.maximum_value:
                return

            if self.is_float:
                minval = float(minval)
            else:
                minval = int(minval)

            self.value = max(self.value, minval)

        self.minimum_value = minval
        self._set_steps(self._steps)

    def key_press(self, ev):
        # type: (Event) -> None

        if ev.key_code == 'Left':
            self.decrement()
        elif ev.key_code == 'Right':
            self.increment()
        else:
            super().key_press(ev)

    def draw(self):
        # type: () -> List[List[Tixel]]
        left_arrow = Tixel('<', White, Black)
        right_arrow = Tixel('>', White, Black)

        readout_width = self.size.width - 2
        readout_text = str(self.value)  # type: str
        if self.is_float:
            if readout_text.index('.') < readout_width:
                readout_text = readout_text[:readout_width]
            else:
                readout_text = '...'
        else:
            if len(readout_text) > readout_width:
                readout_text = '...'

        lpad = math.floor(0.5 * (readout_width - len(readout_text)))
        rpad = readout_width - len(readout_text) - lpad
        readout_text = lpad * ' ' + readout_text + rpad * ' '
        readout = tixels(readout_text, White, Black)

        return [[left_arrow, *readout, right_arrow]]
