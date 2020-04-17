# import curses
import retroui.terminal.screen as screen

from retroui.terminal.event import *
from retroui.terminal.responder import *
from retroui.terminal.size import *
from retroui.terminal.emptyview import *


class Application(Responder):
    """
    An application that captures the screen and keyboard input.

    Slots:

        `name`
            The name of the application.

        `_main_view`
            The view that will be used to fill the screen.

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
        super().__init__()
        self.name = 'Application'
        self._main_view = None
        self._first_responder = None
        self._screen = None
        self._debug = False
        self._debug_log = []

    def set_first_responder(self, view):
        """
        Sets the first responder of the application.
        """

        if (self._first_responder is None or self._first_responder.resign_first_responder()) and\
                view.accepts_first_responder() and\
                view.become_first_responder():

            self._first_responder = view

    def no_responder(self, event):
        """
        Allow the event to fall off the responder chain silently.

        Applications are typically the last responder to try to handle an
        event, and if they don't handle it, that's generally fine, so we don't
        care if it falls off the end of the chain.
        """
        pass

    def set_main_view(self, view):
        """
        Set the main view of the application.
        """

        self._main_view = view
        view.set_application(self)
        view.set_size(self.main_view_size())

    def main_view_size(self):
        """
        Calculate the size for the main view of the application.
        """

        width, height = self._screen.get_size()
        return Size(width, height)

    def set_debug(self, yn):
        """
        Set whether or not the application is in debug mode.
        """

        self._debug = yn

    def debug_log(self, msg):
        """
        Write a message to the debug log.
        """

        self._debug_log.append(msg)

    def on_run(self):
        """
        Setup the application to run.

        By default, this method does nothing, but subclasses can override this
        method to define their own setup process as needed.
        """

        pass

    def on_terminate(self):
        """
        Tear down the application after running.

        By default, this method does nothing, but subclasses can override this
        method to define their own tear down process as needed.
        """

        pass

    def run(self):
        """
        Run the application.

        The primary functionality of the application is in the `main` function
        which is then passed to the curses `wrapper` function where it is
        supplied with the screen. This function manages the main event loop
        as well as  the setup and teardown of the application.
        """

        screen.ScreenManager().run_app(self)
        # curses.wrapper(main)

    def run_with_screen(self, scr):
        self._screen = scr
        # curses.curs_set(0)
        self.on_run()

        # The main event loop
        while True:
            # screen.erase()
            if self._main_view:
                rendered_lines = self._main_view.draw()
                rendered_lines = [[tixel.render_to_screen_tixel()
                                   for tixel in line] for line in rendered_lines]

                max_height, max_width = scr.get_size()
                if self._debug:
                    max_height -= 10
                # try:
                #     for y, line in enumerate(rendered_lines[:max_height]):
                #         self._screen.addstr(y, 0, line[:max_width])
                # except curses.error:
                #     pass
                scr.draw(rendered_lines)

                if not self._debug:
                    scr.draw(rendered_lines)
                else:
                    debug_lines = ['DEBUG ' +
                                   line for line in self._debug_log[-10:]]
                    debug_lines = [[Tixel(c, Color.White, Color.Black).render_to_screen_tixel()
                                    for c in line] for line in debug_lines]
                    scr.draw(rendered_lines[:-10] + debug_lines)
                    # try:
                    #     for y, line in enumerate(self._debug_log[-10:]):
                    #         self._screen.addstr(
                    #             max_height + y, 0, ('DEBUG: ' + line)[:max_width], curses.A_REVERSE)
                    # except curses.error:
                    #     pass

            # ch = screen.getch()
            screen_event = yield
            # ch == KEY_RESIZE:
            if isinstance(screen_event, screen.ResizeEvent):
                self._main_view.set_size(self.main_view_size())
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
        # curses.curs_set(1)
