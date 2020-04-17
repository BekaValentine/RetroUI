from retroui.terminal.event import *
from retroui.terminal.point import *
from retroui.terminal.view import *
from retroui.terminal.clipview import *
from retroui.terminal.emptyview import *
from retroui.terminal.scroller import *

from retroui.terminal.textview import *


class ScrollView(View):
    """
    A `ScrollView` is a composite view that manages the position of content
    within a clip view and displays that position using `Scroller`s.

    """

    __slots__ = ['_scroll_x', '_scroll_y', 'autohides_scrollers', 'content_view',
                 'document_view', 'vertical_scroller', 'horizontal_scroller']

    def __init__(self):
        super().__init__()

        self._scroll_x = 0
        self._scroll_y = 0

        self.autohides_scrollers = False

        self.content_view = ClipView()
        self.content_view.set_superview(self)
        self.content_view.set_size(
            Size(self.size.width - 1, self.size.height - 1))

        self.document_view = self.content_view.document_view

        self.vertical_scroller = Scroller()
        self.vertical_scroller.set_superview(self)
        self.vertical_scroller.set_size(Size(1, self.size.height - 1))

        self.horizontal_scroller = Scroller()
        self.horizontal_scroller.set_superview(self)
        self.horizontal_scroller.set_is_vertical(False)
        self.horizontal_scroller.set_size(Size(self.size.width - 1, 1))

    def set_document_view(self, view):
        """
        Set the document view.
        """

        self.document_view = view
        self.content_view.set_document_view(view)

    def subviews(self):
        return [self.content_view, self.vertical_scroller, self.horizontal_scroller]

    def set_autohides_scrollers(self, yn):
        """
        Set whether or not the `ScrollView` automatically hides its scrollers
        when they're not necessary.
        """

        self.autohides_scrollers = bool(yn)

    def update_content_view_size(self):
        """
        Updates the size of the content view based on this view's size, as
        well as the size of the document view, and whether or not the
        scrollers are hidden.
        """

        if self.autohides_scrollers:
            hide_vertical, hide_horizontal = self.can_hide_scrollers()

            if hide_vertical:
                width = self.size.width
            else:
                width = self.size.width - 1

            if hide_horizontal:
                height = self.size.height
            else:
                height = self.size.height - 1
        else:
            width = self.size.width - 1
            height = self.size.height - 1

        self.content_view.set_size(Size(width, height))

    def can_hide_scrollers(self):
        """
        Determine for each scroller whether it can be hidden.

        Returns a pair consisting of booleans for the vertical scroller and
        horizontal scroller, respectively.
        """

        dv = self.document_view

        if dv is None:
            return (True, True)

        elif dv.size.width <= self.size.width and dv.size.height <= self.size.height:
            # Content is no larger than scrollview in both dimensions, can hide both
            return (True, True)

        elif dv.size.width > self.size.width and dv.size.height > self.size.height:
            # Content is larger than scrollview in both dimensions, cannot hide anything
            return (False, False)

        elif dv.size.width < self.size.width and dv.size.height > self.size.height:
            # Content is taller than scrollview, so must show vertical scroller
            # but content is strictly narrower than scrollview, so there's space for
            # vertical scroller without clipping any of the content and we can
            # hide the horizontal scroller
            return (False, True)

        elif dv.size.width == self.size.width and dv.size.height > self.size.height:
            # Content is taller than scrollview, so must show vertical scroller
            # and content is exactly as wide as scrollview, so the vertical scroller
            # will clip some content and we must show horizontal scroller
            return (False, False)

        elif dv.size.width > self.size.width and dv.size.height < self.size.height:
            # Content is wider than scrollview, so must show horizontal scroller
            # but content is strictly shorter than scrollview, so there's space for
            # horizontal scroller without clipping any of the content and we can
            # hide the vertical scroller
            return (True, False)

        elif dv.size.width > self.size.width and dv.size.height == self.size.height:
            # Content is wider than scrollview, so must show horizontal scroller
            # and content is exactly as tall as scrollview, so the horizontal scroller
            # will clip some content and we must show vertical scroller
            return (False, False)

    def ensure_content_is_not_overscrolled(self):
        """
        Constrains the position of the document view so that it's never
        scrolled too far.

        This can happen during resizing of the `ScrollView`, when enlarging it
        leads to the right/bottom edge of the content view moving further
        right/down than the right/bottom edge of the document view, leaving an
        unnecessary gap. The content view should never be scrolled so far that
        this gap occurs, so we force the scroll to change to prevent this.
        """

        if self.document_view is not None:
            if self.document_view.size.width > self.content_view.size.width and self.document_view.size.width - self._scroll_x < self.content_view.size.width:
                self.scroll_to_column(
                    self.document_view.size.width - self.content_view.size.width)
            elif self.document_view.size.width <= self.content_view.size.width:
                self.scroll_to_column(0)

            if self.document_view.size.height > self.content_view.size.height and self.document_view.size.height - self._scroll_y < self.content_view.size.height:
                self.scroll_to_line(
                    self.document_view.size.height - self.content_view.size.height)
            elif self.document_view.size.height <= self.content_view.size.height:
                self.scroll_to_line(0)

    def update_scroller_sizes(self):
        """
        Updates the size of the scrollers based on the `ScrollView`'s size,
        and whether or not the scrollers can be hidden.
        """

        if self.autohides_scrollers:
            hide_vertical, hide_horizontal = self.can_hide_scrollers()

            if hide_vertical:
                width = self.size.width
            else:
                width = self.size.width - 1

            if hide_horizontal:
                height = self.size.height
            else:
                height = self.size.height - 1

        else:
            height = self.size.height - 1
            width = self.size.width - 1

        self.vertical_scroller.set_size(Size(1, height))
        self.horizontal_scroller.set_size(Size(width, 1))

    def update_scroller_fractions(self):
        """
        Update the visible fractions of the scrollers based on the document
        view's size in relation to the content view's size.
        """

        if self.document_view is None:
            hfrac = 1.0
            vfrac = 1.0
        else:
            if self.content_view.size.width >= self.document_view.size.width:
                hfrac = 1.0
            else:
                hfrac = float(self.content_view.size.width) / \
                    float(self.document_view.size.width)

            if self.content_view.size.height >= self.document_view.size.height:
                vfrac = 1.0
            else:
                vfrac = float(self.content_view.size.height) / \
                    float(self.document_view.size.height)

        self.vertical_scroller.set_visible_fraction(vfrac)
        self.horizontal_scroller.set_visible_fraction(hfrac)

    def update_scroller_positions(self):
        """
        Update the scrollers' scroll positions to reflect the current scroll
        position of the `ScrollView`.
        """

        if self.document_view is None:
            self.vertical_scroller.set_scroll_position(0.0)
            self.horizontal_scroller.set_scroll_position(0.0)
        else:
            ydiff = self.document_view.size.height - self.content_view.size.height
            if ydiff > 0:
                self.vertical_scroller.set_scroll_position(
                    self._scroll_y / ydiff)
            else:
                self.vertical_scroller.set_scroll_position(0.0)

            xdiff = self.document_view.size.width - self.content_view.size.width
            if xdiff > 0:
                self.horizontal_scroller.set_scroll_position(
                    self._scroll_x / xdiff)
            else:
                self.horizontal_scroller.set_scroll_position(0.0)

    def vertical_scroll(self, amt):
        """
        Scroll vertically by the given number of lines.
        """

        self.scroll_to_line(self._scroll_y + amt)

    def scroll_to_line(self, line):
        """
        Scroll vertically to a specific line.
        """

        if self.document_view.size.height > self.content_view.size.height:
            self._scroll_y = max(0, min(
                self.document_view.size.height - self.content_view.size.height, line))
        else:
            self._scroll_y = 0

        self.content_view.set_origin(
            Point(self.content_view.origin.x, self._scroll_y))

    def horizontal_scroll(self, amt):
        """
        Scroll horizontally by the given number of columns.
        """

        self.scroll_to_column(self._scroll_x + amt)

    def scroll_to_column(self, col):
        """
        Scroll horizontally to a specific column.
        """

        if self.document_view.size.width > self.content_view.size.height:
            self._scroll_x = max(
                0, min(self.document_view.size.width - self.content_view.size.width, col))
        else:
            self._scroll_x = 0

        self.content_view.set_origin(
            Point(self._scroll_x, self.content_view.origin.y))

    def key_press(self, ev):
        """
        Handle a key press.

        When the character codes correspond to arrow keys, the view is
        scrolled by one line or two columns. When the character codes are page
        up or down, the view is scrolled by a full page height minus two
        lines. When the character codes are home or end, the view is scrolled
        to the beginning or end of the document.
        """

        if ev.key_code == 'Down':
            self.vertical_scroll(1)
        elif ev.key_code == 'Up':
            self.vertical_scroll(-1)
        elif ev.key_code == 'Left':
            self.horizontal_scroll(-2)
        elif ev.key_code == 'Right':
            self.horizontal_scroll(2)
        elif ev.key_code == 'PageUp':
            self.vertical_scroll(-self.content_view.size.height + 2)
        elif ev.key_code == 'PageDown':
            self.vertical_scroll(self.content_view.size.height - 2)
        elif ev.key_code == 'Home':
            self.scroll_to_line(0)
        elif ev.key_code == 'End':
            self.scroll_to_line(self.document_view.size.height - 1)
        else:
            super().key_press(ev)

    def draw(self):
        self.update_content_view_size()
        self.ensure_content_is_not_overscrolled()
        self.update_scroller_sizes()
        self.update_scroller_fractions()
        self.update_scroller_positions()

        hide_vertical, hide_horizontal = self.can_hide_scrollers()

        clip_lines = self.content_view.draw()
        vscroll_lines = self.vertical_scroller.draw()

        lines = []
        for i in range(len(clip_lines)):
            if self.autohides_scrollers and hide_vertical:
                lines.append(clip_lines[i])
            else:
                lines.append(clip_lines[i] + vscroll_lines[i])

        hscroll_lines = self.horizontal_scroller.draw()
        if self.autohides_scrollers and hide_horizontal:
            pass
        else:
            if self.autohides_scrollers and hide_vertical:
                lines.append(hscroll_lines[0])
            else:
                lines.append(
                    hscroll_lines[0] + [Tixel(' ', Color.White, Color.Black)])

        return self.bound_lines(lines)
