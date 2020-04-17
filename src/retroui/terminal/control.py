from retroui.terminal.view import *


class Control(View):

    def __init__(self):
        super().__init__()

        self.is_enabled = True
        self.value = None
