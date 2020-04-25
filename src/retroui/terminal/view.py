from typing import cast, List, Optional


from retroui.terminal.application import *
from retroui.terminal.color import Color, Black, White
from retroui.terminal.point import Point
from retroui.terminal.responder import Responder
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel


class View(Responder):
    """
    A `View` is a responder which draws to the screen.

    Slots:

        `application`
            The application that the view resides within.

        `superview`
            The view that immediately contains this one.

        `size`
            The size of the view.

        `origin`
            The location in view's internal coordinate system that the view
            draws. Note that this is not the location on the screen that the
            view draws to, but rather the location in the view's coordinate
            system of the content that the view will draw to the screen.
    """

    @staticmethod
    def offset_to_origin(lines, point):
        # type: (List[List[Tixel]], Point) -> List[List[Tixel]]
        """
        Moves content so that the origin of the lines is at the point. Flips
        and pads the top and left edges as necessary.
        """

        hoffset_lines = []  # type: List[List[Tixel]]
        if point.x <= 0:
            hoffset_lines = [-point.x *
                             [Tixel(' ', White, Black)] + line for line in lines]
        else:
            hoffset_lines = [line[point.x:] for line in lines]

        bothoffset_lines = []  # type: List[List[Tixel]]
        if point.y <= 0:
            bothoffset_lines = -point.y * cast(List[List[Tixel]], [[]]) + \
                hoffset_lines
        else:
            bothoffset_lines = hoffset_lines[point.y:]

        return bothoffset_lines

    @staticmethod
    def fit_to_width(line, width):
        # type: (List[Tixel], int) -> List[Tixel]

        if len(line) < width:
            return line + (width - len(line)) * [Tixel(' ', White, Black)]
        else:
            return line[:width]

    @staticmethod
    def fit_to_height(lines, height):
        # type: (List[List[Tixel]], int) -> List[List[Tixel]]

        if len(lines) < height:
            return lines + (height - len(lines)) * cast(List[List[Tixel]], [[]])
        else:
            return lines[:height]

    @staticmethod
    def fit_to_size(lines, size):
        # type: (List[List[Tixel]], Size) -> List[List[Tixel]]
        """
        Fits lines to completely fill the given size by padding with spaces on
        the right, and space-filled lines at the bottom. Clips overflow as
        needed.
        """

        vfit_lines = View.fit_to_height(lines, size.height)

        bothfit_lines = [View.fit_to_width(
            line, size.width) for line in vfit_lines]

        return bothfit_lines

    @staticmethod
    def put_in_bounds(lines, origin, size):
        # type: (List[List[Tixel]], Point, Size) -> List[List[Tixel]]
        return View.fit_to_size(View.offset_to_origin(lines, origin), size)

    __slots__ = ['application', 'superview', 'size', 'origin']

    def __init__(self):
        # type: () -> None
        super().__init__()
        self.application = None  # type: Optional[Application]
        self.superview = None  # type: Optional[View]
        self.size = Size(0, 0)  # type: Size
        self.origin = Point(0, 0)  # type: Point

    def accepts_first_responder(self):
        # type: () -> bool
        """
        Whether or not the view can become the first responder in an
        application.

        By default, views can become first responder because they have a
        visual presence on the screen. This method can be overridden by
        subclasses to change this as needed.
        """

        return True

    def next_responder(self):
        # type: () -> Optional[Responder]
        """
        The next responder in the responder chain after this view.

        By default, a this is the view's superview, unless there is none.
        """
        if self.superview:
            return self.superview
        else:
            return self.application

    def set_application(self, application):
        # type: (Application) -> None
        """
        Set the application that this view is part of.
        """

        self.application = application

        for subview in self.subviews():
            subview.set_application(application)

    def set_superview(self, superview):
        # type: (View) -> None
        """
        Set the superview of this view.
        """

        self.will_move_to_superview(superview)
        self.superview = superview
        if superview.application is not None:
            self.set_application(superview.application)
        self.did_move_to_superview()

    def will_move_to_superview(self, view):
        # type: (View) -> None
        """
        Actions to perform before the view moves to a superview.

        By default, this does nothing, but subclasses can override it as
        needed.
        """

        pass

    def did_move_to_superview(self):
        # type: () -> None
        """
        Actions to perform after the view moves to a superview.

        By default, this does nothing, but subclasses can override it as
        needed.
        """

        pass

    def subviews(self):
        # type: () -> List[View]
        """
        The subviews of this view.

        By default, there are none, so this returns an empty list. Subclasses
        should override this to return the subviews they contain.
        """

        return []

    def set_origin(self, new_origin):
        # type: (Point) -> None
        """
        Sets the origin of the view in its internal coordinate system.
        """

        self.origin = self.constrain_origin(new_origin)
        self.origin_did_change()

    def constrain_origin(self, new_origin):
        # type: (Point) -> Point
        """
        Constrains the new origin of the view.

        By default, the origin is constrained to be at (0,0), but subclasses
        can override this as needed.
        """
        return Point(0, 0)

    def origin_did_change(self):
        # type: () -> None
        """
        Actions to perform after the view's origin changes.

        By default, this does nothing, but subclasses can override it as
        needed.
        """

        pass

    def set_size(self, new_size):
        # type: (Size) -> None
        """
        Set the size of the view.
        """

        new_size = self.constrain_size(new_size)
        self.size = Size(max(new_size.width, 0), max(new_size.height, 0))
        self.size_did_change()

    def constrain_size(self, new_size):
        # type: (Size) -> Size
        """
        Constrains the new size of the view.

        By default, no constraints are applied, but subclasses can override
        this as needed.
        """

        return new_size

    def size_did_change(self):
        # type: () -> None
        """
        Actions to perform after the view's origin changes.

        By default, this does nothing, but subclasses can override it as
        needed.
        """

        pass

    def bound_lines(self, lines):
        # type: (List[List[Tixel]]) -> List[List[Tixel]]
        """
        Put the given lines into the bounds of the receiving view.
        """

        return View.put_in_bounds(lines, self.origin, self.size)

    def draw(self):
        # type: () -> List[List[Tixel]]
        """
        Draw the visible portion of the view's coordinate space, as determined
        by the view's size and origin.

        By default, this returns all spaces.
        """

        return View.fit_to_size([], self.size)
