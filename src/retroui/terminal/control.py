from retroui.terminal.view import *


class Control(View):

    def __init__(self):
        # type: () -> None
        super().__init__()

        self.is_enabled = True  # type: bool
