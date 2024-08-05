from typing import cast, List, Optional

from retroui.terminal.color import Black
from retroui.terminal.point import Point
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel


class Render(object):
    """
    A `Render` is a representation of the result of rendering something for
    presentation on the screen. It consists of some lines of tixels, together
    with a location and size that bounds the lines.

    Slots:

        `location`
            The location on the screen that the render starts.

        `size`
            The size of greatest extent of the render.

        `tixel_lines`
            The tixel lines that make up the render.
    """

    __slots__ = ['location', 'size', 'tixel_lines']

    def __init__(self, loc, size, lines):
        # type: (Point, Size, List[List[Optional[Tixel]]]) -> None
        self.location = loc  # type: Point
        self.size = size  # type: Size

        # clip to size
        lines = [line[:size.width] for line in lines[:size.height]] \
            # pad to length
        lines = lines + \
            (size.height - len(lines)) * \
            cast(List[List[Optional[Tixel]]], [[]])
        lines = [line + (size.width - len(line)) *
                 [cast(Optional[Tixel], None)] for line in lines]

        self.lines = lines  # type: List[List[Optional[Tixel]]]

    def new_render_in_bounds(self, loc, size):
        if loc.y == self.location.y:
            vfixed_new_lines = self.lines
        elif loc.y < self.location.y:
            vfixed_new_lines = (self.location.y - loc.y) * [[]] + self.lines
        elif loc.y > self.location.y:
            vfixed_new_lines = self.lines[loc.y - self.location.y:]

        bothfixed_new_lines = []
        if loc.x == self.location.x:
            bothfixed_new_lines = vfixed_new_lines
        elif loc.x < self.location.x:
            pad = (self.location.x - loc.x) * [None]
            bothfixed_new_lines = [pad + line for line in vfixed_new_lines]
        elif loc.x > self.location.x:
            clip = loc.x - self.location.x
            bothfixed_new_lines = [line[clip:] for line in vfixed_new_lines]

        return Render(loc, size, bothfixed_new_lines)
