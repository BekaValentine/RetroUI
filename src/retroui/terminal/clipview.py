from typing import List

from retroui.terminal.point import Point
from retroui.terminal.tixel import Tixel
from retroui.terminal.view import View
from retroui.terminal.emptyview import EmptyView


class ClipView(View):
    """
    A `ClipView` is a simple container for another view, used to show only a
    portion of the contained view.

    Slots:

        `document_view`
            The view contained within the `ClipView`.
    """

    __slots__ = ['document_view']

    def __init__(self):
        # type: () -> None
        super().__init__()

        self.document_view = EmptyView()  # type: View

    def set_document_view(self, view):
        # type: (View) -> None
        """
        Set the document view of this view.
        """

        self.document_view = view
        view.set_superview(self)

    def subviews(self):
        # type: () -> List[View]
        return [self.document_view]

    def constrain_origin(self, new_origin):
        # type: (Point) -> Point
        """
        Constrains the origin of the `ClipView`.

        The origin can be set to anything, since the purpose of a `ClipView` is
        precisely to render its document view at the origin, and then clip the
        rendering to the `ClipView`'s visible region.
        """

        return new_origin

    def draw(self):
        # type: () -> List[List[Tixel]]
        if self.document_view is None:
            lines = []
        else:
            lines = self.document_view.draw()

        # true_lines = []
        # for line in lines[:self.size.height]:
        #     true_lines.append(
        #         line[:self.size.width].ljust(self.size.width, ' '))
        # true_lines += (self.size.height - len(true_lines)) * \
        #     [self.size.width * ' ']

        return self.bound_lines(lines)
