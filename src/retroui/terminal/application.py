from typing import cast, Generator, List, Optional

# import curses
import retroui.terminal.screen as screen

from retroui.terminal.color import Color, Black, White, Orange
from retroui.terminal.event import Event
from retroui.terminal.point import Point
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel, tixels

from retroui.terminal.responder import Responder, NoResponderException
from retroui.terminal.panel import Panel
from retroui.terminal.view import View


class Application(Responder):
    """
    An application that captures the screen and keyboard input.

    Slots:

        `name`
            The name of the application.

        `main_panel`
            The panel that will be used to fill the screen.

        `non_main_panels`
            The panels that will be drawn above the main panel.

        `key_panel`
            The panel that will receive all of the input events.

        `_screen`
            The screen object that the application draws to.

        `_debug`
            Whether or not the application is in debugging mode.

        `_debug_log`
            The log of debugging messages to display when in debugging mode.
    """

    __slots__ = ['name', 'main_panel', 'non_main_panels', 'key_panel',
                 '_screen', '_debug', '_debug_log']

    def __init__(self):
        # type: () -> None
        super().__init__()
        self.name = 'Application'  # type: str
        self.main_panel = None  # type: Optional[Panel]
        self.non_main_panels = []  # type: List[Panel]
        self.key_panel = None  # type: Optional[Panel]
        self._screen = None  # type: Optional[screen.Screen]
        self._debug = False  # type: bool
        self._debug_log = []  # type: List[str]

    def no_responder(self, event):
        # type: (Event) -> None
        """
        Allow the event to fall off the responder chain silently.

        Applications are typically the last responder to try to handle an
        event, and if they don't handle it, that's generally fine, so we don't
        care if it falls off the end of the chain.
        """
        pass

    def set_main_panel(self, panel):
        # type: (Panel) -> None
        """
        Set the main panel of the application.

        Will resize the panel to fit the screen.
        """

        if panel.can_become_main():
            if self.main_panel is not None:
                self.main_panel.resign_main()

            panel.become_main()
            self.main_panel = panel
            panel.set_application(self)
            s = self.main_panel_size()
            if s is not None:
                panel.set_size(s)

    def add_panel(self, panel):
        # type: (Panel) -> None
        panel.set_application(self)
        self.non_main_panels.append(panel)

    def set_key_panel(self, panel):
        # type: (Panel) -> None
        """
        Set the key panel of the application.
        """

        if panel.can_become_key():
            if self.key_panel is not None:
                self.key_panel.resign_key()

            panel.become_key()
            self.key_panel = panel
            panel.set_application(self)

    def main_panel_size(self):
        # type: () -> Optional[Size]
        """
        Calculate the size for the main view of the application.
        """

        if self._screen is None:
            return None
        else:
            width, height = self._screen.get_size()
            return Size(width, height)

    def set_debug(self, yn):
        # type: (bool) -> None
        """
        Set whether or not the application is in debug mode.
        """

        self._debug = yn

    def debug_log(self, msg):
        # type: (str) -> None
        """
        Write a message to the debug log.
        """

        self._debug_log.append(msg)

    def on_run(self):
        # type: () -> None
        """
        Setup the application to run.

        By default, this method does nothing, but subclasses can override this
        method to define their own setup process as needed.
        """

        pass

    def on_terminate(self):
        # type: () -> None
        """
        Tear down the application after running.

        By default, this method does nothing, but subclasses can override this
        method to define their own tear down process as needed.
        """

        pass

    def run(self):
        # type: () -> None
        """
        Run the application.

        The primary functionality of the application is in the `main` function
        which is then passed to the curses `wrapper` function where it is
        supplied with the screen. This function manages the main event loop
        as well as  the setup and teardown of the application.
        """

        screen.ScreenManager().run_app(self.run_with_screen)
        # curses.wrapper(main)

    def run_with_screen(self, scr):
        # type: (screen.Screen) -> Generator[None, Optional[screen.Event], None]
        self._screen = scr
        self.on_run()

        # The main event loop
        while True:
            size = self.main_panel_size()
            if size is None:
                continue

            composited_lines = size.height * \
                [size.width * [Tixel(' ', Black, Black)]]

            if self.main_panel is not None:
                main_panel_lines = self.main_panel.draw()

                composited_lines = composite_over(
                    composited_lines, Point(0, 0), main_panel_lines)

            for non_main_panel in self.non_main_panels:
                composited_lines = composite_over(
                    composited_lines, non_main_panel.location, non_main_panel.draw())

            scr.draw(convert_lines_to_screen_lines(composited_lines))

            screen_event = yield
            if isinstance(screen_event, screen.ResizeEvent):
                s = self.main_panel_size()
                if self.main_panel is not None and s is not None:
                    self.main_panel.set_size(s)
            elif isinstance(screen_event, screen.KeyPressEvent):
                ev = Event(screen_event.key_code, screen_event.has_ctrl_modifier,
                           screen_event.has_alt_modifier, screen_event.has_shift_modifier)
                if self.key_panel:
                    try:
                        self.key_panel.send_event(ev)
                    except NoResponderException:
                        self.key_press
                else:
                    self.key_press(ev)

        self.on_terminate()


def composite_over(lines, loc, lines2):
    # type: (List[List[Tixel]], Point, List[List[Tixel]]) -> List[List[Tixel]]

    # clip lines2 to within the screen

    composited = lines.copy()
    for dy, line in enumerate(lines2):
        composited[loc.y + dy] = composited[loc.y + dy][:loc.x] + line + \
            composited[loc.y + dy][loc.x + len(line):]

    return composited


def convert_lines_to_screen_lines(lines):
    # type: (List[List[Tixel]]) -> screen.ScreenContent

    lines_for_screen = []
    line = []  # type: List[Tixel]
    for line in lines:
        line_for_screen = []
        for tixel in line:

            scrtx = tixel.render_to_screen_tixel()

            if scrtx[1] is None:
                fg = None
            else:
                fg = screen.ScreenColor(scrtx[1][0], scrtx[1][1], scrtx[1][2])

            if scrtx[2] is None:
                bg = None
            else:
                bg = screen.ScreenColor(scrtx[2][0], scrtx[2][1], scrtx[2][2])

            line_for_screen.append(screen.ScreenTixel(scrtx[0], fg, bg))

        lines_for_screen.append(line_for_screen)

    return lines_for_screen
