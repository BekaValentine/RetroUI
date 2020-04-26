from typing import Callable, List, Optional
from typing_extensions import Literal

from retroui.terminal.color import White, Black
from retroui.terminal.event import Event
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel, tixels
from retroui.terminal.view import View


ButtonStyle = Literal['rectangular', 'radio', 'checkbox', 'on_off']
ButtonInteractionType = Literal['momentary', 'toggle', 'latch']
ButtonLabelLocation = Literal['left', 'right']


class Button(View):
    """
    A `Button` is an input method for invoking some code. Buttons have an
    internal on/off state which changes when pressed. Code is invoked via a
    callback on button press.

    Buttons can be one of three styles:

        `'rectangular'`
            A button that displays its label inside a rectanglular region,
            indicating state by the whole button's look. Default.

        `'radio'`
            A button that displays an indicator circle next to its label,
            indicating its state via a dot inside the indicator circle.

        `'checkbox'`
            A button that displays a checkbox next to its label, indicating its
            state via a check inside the checkbox.

        `'on_off'`
            A button that displays a switch with on/off labels, indicating its
            state via which of the two labels is selected.

    Button labels can be either on the left or the right of the button, when the
    button's style is `'radio'`, `'checkbox'`, or `'on_off'`.

    Buttons can be one of three interaction types, as well:

        `'momentary'`
            Does not stay on indefinitely. Invokes the callback for each press.
            Default.

        `'toggle'`
            Switches states when pressed. Invokes the callback for each press.

        `'latch'`
            Stays in its on state once changed to on. Invokes the callback when
            pressed for the first time.

    Slots:

        `style`
            The style of the button.

        `interaction_type`
            The interaction type of the button.

        `state`
            Whether the button is on or off.

        `label`
            The label to display with the button.

        `label_location`
            Where to display the label, if possible. Either `'left'` or
            `'right'`. Default is `'right'`.

        `callback`
            The callback to call when the state is changed.

    """

    __slots__ = ['style', 'interaction_type', 'state',
                 'label', 'label_location', 'callback']

    def __init__(self):
        # type: () -> None
        super().__init__()

        self.style = 'rectangular'  # type: ButtonStyle
        self.interaction_type = 'momentary'  # type: ButtonInteractionType
        self.state = False  # type: bool
        self.label = 'button'  # type: str
        self.label_location = 'right'  # type: ButtonLabelLocation
        self.callback = None  # type: Optional[Callable[[],None]]

    def constrain_size(self, new_size):
        # type: (Size) -> Size
        """
        Constrain the size to exactly fit the style of button, and its label.
        """

        if self.style == 'rectangular':
            return Size(4 + len(self.label), 1)
        elif self.style == 'on_off':
            return Size(10 + len(self.label), 1)
        else:
            return Size(4 + len(self.label), 1)

    def set_style(self, style):
        # type: (ButtonStyle) -> None
        """
        Set the button's style.
        """

        self.style = style
        self.set_size(self.size)

    def set_interaction_type(self, t):
        # type: (ButtonInteractionType) -> None
        """
        Set the button's interaction type.
        """

        self.interaction_type = t

    def set_label(self, l):
        # type: (str) -> None
        """
        Set the button's label.
        """

        self.label = l
        self.set_size(self.size)

    def set_label_location(self, loc):
        # type: (ButtonLabelLocation) -> None
        """
        Set the button's label location.
        """

        self.label_location = loc

    def set_state(self, new_state):
        # type: (bool) -> None
        """
        Set the button's state, subject to the interaction type's constraints.
        """

        if self.interaction_type == 'latch':
            if not self.state and new_state:
                self.state = True
                if self.callback is not None:
                    self.callback()
        else:
            self.state = new_state
            if self.callback is not None:
                self.callback()

    def set_callback(self, callback):
        # type: (Optional[Callable[[], None]]) -> None
        """
        Set the button's callback.
        """

        self.callback = callback

    def key_press(self, ev):
        # type: (Event) -> None
        """
        Handle a key press. On `'Enter'`, flip the state of the button.
        """

        if ev.key_code == 'Enter':
            self.set_state(not self.state)
        else:
            super().key_press(ev)

    def draw(self):
        # type: () -> List[List[Tixel]]

        lines = []  # type: List[List[Tixel]]
        if self.style == 'rectangular':
            lines.append(tixels('[ ' + self.label + ' ]', White, Black))

        else:
            label = []  # type: List[Tixel]
            if self.label_location == 'right':
                label = tixels(' ' + self.label, White, Black)
            else:
                label = tixels(self.label + ' ', White, Black)

            indicator = []  # type: List[Tixel]
            if self.style == 'radio':
                if self.state:
                    indicator = tixels('(*)', White, Black)
                else:
                    indicator = tixels('( )', White, Black)
            elif self.style == 'checkbox':
                if self.state:
                    indicator = tixels('[x]', White, Black)
                else:
                    indicator = tixels('[ ]', White, Black)
            elif self.style == 'on_off':
                if self.state:
                    indicator = tixels(' off [ON]', White, Black)
                else:
                    indicator = tixels('[OFF] on ', White, Black)

            if self.label_location == 'right':
                lines.append(indicator + label)
            else:
                lines.append(label + indicator)

        return lines
