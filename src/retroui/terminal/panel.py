from typing import List, Optional

from retroui.terminal.color import *
from retroui.terminal.event import Event
from retroui.terminal.point import Point
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel, tixels

from retroui.terminal.responder import Responder, NoResponderException
from retroui.terminal.application import *
from retroui.terminal.view import View
from retroui.terminal.emptyview import EmptyView


class Panel(Responder):
    """
    A `Panel` is a responder that owns some screen region, analogous to a
    window in a GUI. Panels can overlap one another and be positioned absolutely
    relative to the screen.

    Slots:

        `application`
            The parent application of the panel.

        `is_key_panel`
            Whether or not the panel is the key panel for the application, i.e.
            whether or not it's receiving key press events.

        `is_main_panel`
            Whether or not the panel is the main panel for the application, i.e.
            whether or not it is behind all other panels as the application's
            primary output or backdrop.

        `is_visible`
            Whether or not the panel is visible.

        `location`
            The location of the panel on in screen.

        `size`
            The size of the panel.

        `title`
            The title of the panel. Default: None.

        `has_border`
            Whether or not the panel has a border.

        `background_color`
            The background color of the panel.

        `content_view`
            The view to display inside the panel.

        `first_responder`
            The responder to send input events to.
    """

    __slots__ = ['application', 'is_key_panel', 'is_main_panel', 'location', 'size', 'title',
                 'has_border', 'background_color', 'content_view', 'first_responder']

    def __init__(self):
        # type: () -> None
        super().__init__()

        self.application = None  # type: Optional[Application]
        self.is_key_panel = False  # type: bool
        self.is_main_panel = False  # type: bool
        self.is_visible = True  # type: bool
        self.location = Point(0, 0)  # type: Point
        self.size = Size(0, 0)  # type: Size
        self.title = None  # type: Optional[str]
        self.has_border = True  # type: bool
        self.background_color = Black  # type: Color
        self.content_view = None  # type: Optional[View]
        self.first_responder = None  # type: Optional[Responder]

    def set_application(self, app):
        # type: (Application) -> None
        """
        Set the application that hosts the panel.
        """

        self.application = app

    def can_become_key(self):
        # type: () -> bool
        """
        Whether or not the panel can become the key panel in an application.

        By default, any panel can become the key panel. Subclasses can override
        this to change whether a panel can become key or not.
        """

        return True

    def make_key(self):
        # type: () -> None
        """
        A convenience method for telling the application to make this panel the
        key panel.
        """

        if self.application:
            self.application.set_key_panel(self)

    def become_key(self):
        # type: () -> None
        """
        Tells the panel that it has become the key panel.

        Subclasses can override this to customize behavior, but should always
        call this method from inside the override.
        """

        self.is_key_panel = True

    def resign_key(self):
        # type: () -> None
        """
        Tells the panel it's losing key panel status.

        Subclasses can override this to add new teardown functionality.
        """

        pass

    def can_become_main(self):
        # type: () -> bool
        """
        Whether or not the panel can become the main panel in an application.

        By default, any panel can become the main panel. Subclasses can override
        this to change whether a panel can become main or not.
        """

        return True

    def make_main(self):
        # type: () -> None
        """
        A convenience method for telling the application to make this panel the
        main panel.
        """

        if self.application:
            self.application.set_main_panel(self)

    def become_main(self):
        # type: () -> None
        """
        Tells the panel that it has become the main panel.

        Subclasses can override this to customize behavior, but should always
        call this method from inside the override.
        """

        self.is_main_panel = True

    def resign_main(self):
        # type: () -> None
        """
        Tells the panel it's losing main panel status.

        Subclasses can override this to add new teardown functionality.
        """

        pass

    def set_location(self, loc):
        # type: (Point) -> None
        """
        Sets the panels location.
        """

        self.location = loc

    def set_size(self, size):
        # type: (Size) -> None
        """
        Set the size of the panel.
        """

        self.size = size
        self.resize_content_view()

    def set_title(self, title):
        # type: (Optional[str]) -> None
        """
        Set the title of the panel.
        """

        self.title = title

    def set_background_color(self, color):
        # type: (Color) -> None
        """
        Set the content view of the panel.
        """

        self.background_color = color

    def resize_content_view(self):
        # type: () -> None
        """
        Resize the content view to fit the panel's content view area,
        accounting for borders and titles.
        """

        if self.content_view is not None:
            width = self.size.width
            height = self.size.height

            if self.title is not None:
                height -= 1

            if self.has_border:
                width -= 2
                if self.title is not None:
                    height -= 1
                else:
                    height -= 2

            self.content_view.set_size(Size(width, height))

    def set_content_view(self, view):
        # type: (View) -> None
        """
        Set the content view of the panel.
        """

        self.content_view = view
        self.resize_content_view()

    def set_first_responder(self, responder):
        # type: (Responder) -> None
        """
        Sets the first responder of the panel.
        """

        if (self.first_responder is None or self.first_responder.resign_first_responder()) and\
                responder.accepts_first_responder() and\
                responder.become_first_responder():

            self.first_responder = responder

    def send_event(self, ev):
        # type: (Event) -> None
        """
        Send an event to the panel for handling by its first responder.
        """

        if self.first_responder is not None:
            try:
                self.first_responder.key_press(ev)
            except NoResponderException:
                self.no_responder(ev)
        else:
            self.no_responder(ev)

    def draw(self):
        # type: () -> List[List[Tixel]]

        lines = []  # type: List[List[Tixel]]

        if self.title is not None:
            if self.size.width <= 2:
                lines.append(tixels(self.size.width * ' ', White, Grey))
            else:
                if self.size.width >= 2 + len(self.title):
                    title_content = self.title
                else:
                    title_content = self.title[:self.size.width - 5] + '...'

                    if self.size.width < 2 + len(title_content):
                        title_content = ''

                rpad = self.size.width - 1 - len(title_content)
                lines.append(
                    tixels(' ' + title_content + rpad * ' ', White, Grey))

        if self.content_view is None:
            lines += self.size.height * \
                [self.size.width *
                    [Tixel(' ', self.background_color, self.background_color)]]
        else:
            # TODO: actually composite over the background color
            lines += self.content_view.draw()

        return lines
