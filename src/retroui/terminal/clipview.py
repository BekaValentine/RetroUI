from retroui.terminal.view import *
from retroui.terminal.emptyview import *


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
        super().__init__()

        self.document_view = EmptyView()

    def set_document_view(self, view):
        """
        Set the document view of this view.
        """

        self.document_view = view
        view.set_superview(self)

    def subviews(self):
        return [self.document_view]

    def constrain_origin(self, new_origin):
        """
        Constrains the origin of the `ClipView`.

        The origin can be set to anything, since the purpose of a `ClipView` is
        precisely to render its document view at the origin, and then clip the
        rendering to the `ClipView`'s visible region.
        """

        return new_origin

    def draw(self):
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
