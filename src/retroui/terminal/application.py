from typing import cast, Generator, List, Optional

# import curses
import retroui.terminal.screen as screen

from retroui.terminal.color import Color, Black, White, Orange
from retroui.terminal.event import Event
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

        `_main_view`
            The view that will be used to fill the screen.

        `main_panel`
            The panel that will be used to fill the screen.

        `_first_responder`
            The responder that will handle user input.

        `_screen`
            The screen object that the application draws to.

        `_debug`
            Whether or not the application is in debugging mode.

        `_debug_log`
            The log of debugging messages to display when in debugging mode.
    """

    __slots__ = ['name', '_main_view', '_first_responder',
                 '_screen', '_debug', '_debug_log']

    def __init__(self):
        # type: () -> None
        super().__init__()
        self.name = 'Application'  # type: str
        self._main_view = None  # type: Optional[View]
        self.main_panel = None  # type: Optional[Panel]
        self._first_responder = None  # type: Optional[Responder]
        self._screen = None  # type: Optional[screen.Screen]
        self._debug = False  # type: bool
        self._debug_log = []  # type: List[str]

    def set_first_responder(self, responder):
        # type: (Responder) -> None
        """
        Sets the first responder of the application.
        """

        if (self._first_responder is None or self._first_responder.resign_first_responder()) and\
                responder.accepts_first_responder() and\
                responder.become_first_responder():

            self._first_responder = responder

    def no_responder(self, event):
        # type: (Event) -> None
        """
        Allow the event to fall off the responder chain silently.

        Applications are typically the last responder to try to handle an
        event, and if they don't handle it, that's generally fine, so we don't
        care if it falls off the end of the chain.
        """
        pass

    def set_main_view(self, view):
        # type: (View) -> None
        """
        Set the main view of the application.
        """

        self._main_view = view
        view.set_application(self)
        s = self.main_view_size()
        if s is not None:
            view.set_size(s)

    def main_view_size(self):
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
            if self._main_view:

                rendered_lines = self._main_view.draw()
                rendered_lines_for_screen = []
                line = []  # type: List[Tixel]
                for line in rendered_lines:
                    rendered_line = []
                    for tixel in line:
                        scrtx = tixel.render_to_screen_tixel()
                        rendered_line.append(screen.ScreenTixel(
                            scrtx[0],
                            None if scrtx[1] is None else screen.ScreenColor(
                                scrtx[1][0], scrtx[1][1], scrtx[1][2]),
                            None if scrtx[2] is None else screen.ScreenColor(scrtx[2][0], scrtx[2][1], scrtx[2][2])))
                    rendered_lines_for_screen.append(rendered_line)

                max_width, max_height = scr.get_size()
                non_debug_height = max_height

                if not self._debug:
                    scr.draw(rendered_lines_for_screen)
                else:
                    non_debug_height -= 10
                    debug_lines = ['DEBUG: ' +
                                   line for line in self._debug_log[-10:]]
                    debug_lines_for_screen = []
                    debug_line = ''  # type: str
                    for debug_line in debug_lines:
                        debug_line = debug_line[:max_width]
                        rendered_line = []
                        for tixel in tixels(debug_line, Black, Orange):
                            scrtx = tixel.render_to_screen_tixel()
                            rendered_line.append(screen.ScreenTixel(
                                scrtx[0],
                                None if scrtx[1] is None else screen.ScreenColor(
                                    scrtx[1][0], scrtx[1][1], scrtx[1][2]),
                                None if scrtx[2] is None else screen.ScreenColor(scrtx[2][0], scrtx[2][1], scrtx[2][2])))
                        debug_lines_for_screen.append(rendered_line)

                    all_lines_for_screen = rendered_lines_for_screen[:non_debug_height] +\
                        cast(screen.ScreenContent, (non_debug_height - len(rendered_lines_for_screen)) * [[]]) + \
                        debug_lines_for_screen
                    scr.draw(all_lines_for_screen)

            screen_event = yield
            if isinstance(screen_event, screen.ResizeEvent):
                s = self.main_view_size()
                if self._main_view is not None and s is not None:
                    self._main_view.set_size(s)
            elif isinstance(screen_event, screen.KeyPressEvent):
                ev = Event(screen_event.key_code, screen_event.has_ctrl_modifier,
                           screen_event.has_alt_modifier, screen_event.has_shift_modifier)
                if self._first_responder:
                    try:
                        self._first_responder.key_press(ev)
                    except NoResponderException:
                        self.key_press(ev)
                else:
                    self.key_press(ev)

        self.on_terminate()
