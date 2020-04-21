from retroui.terminal.view import *


class AccordionView(View):
    """
    An `AccordionView` is a way of displaying multiple views with collapsible
    title bars that are used to hide the views as necessary.

    Slots:
        `_accordion_info`
            Internal information about what the subviews are and what their
            titles are.

        `_selected_index`
            The index of the currently selected subview.

        `allows_multiple_expansions`
            Whether or not multiple subviews can be expanded simultaneously.
    """

    __slots__ = ['_accordion_info', '_selected_index',
                 'allows_multiple_expansions']

    def __init__(self):
        super().__init__()

        self._accordion_info = []
        self._selected_index = 0
        self.allows_multiple_expansions = False

    def set_views(self, new_views):
        """
        Sets the views in the `AccordionView` to the given views.

        Argument should be a list of pairs of the title and the view, in that
        order.
        """

        self._accordion_info = []
        for title, view in new_views:
            self._accordion_info.append({
                'title': title,
                'view': view,
                'is_expanded': False
            })

        self._selected_index = 0
        if len(self._accordion_info) != 0:
            self._accordion_info[0]['is_expanded'] = True

        self.recalculate_size()

    def set_allows_multiple_expansions(self, yn):
        """
        Set whether or not multiple views can be expanded at the same time.
        """

        self.allows_multiple_expansions = bool(yn)

        if not yn:
            already_found_first = False
            for entry in self._accordion_info:
                if entry['is_expanded']:
                    if already_found_first:
                        entry['is_expanded'] = False
                    else:
                        already_found_first = True

        self.recalculate_size()

    def set_selection(self, ix):
        """
        Set the selected view.
        """

        self._selected_index = max(0, min(len(self._accordion_info) - 1, ix))
        self.recalculate_size()

    def set_is_expanded(self, ix, yn):
        """
        Set whether or not the view at the specified index is expanded.
        """

        self._accordion_info[ix]['is_expanded'] = bool(yn)

        if yn and not self.allows_multiple_expansions:
            for i, entry in enumerate(self._accordion_info):
                if i != ix:
                    entry['is_expanded'] = False

        self.recalculate_size()

    def constrain_size(self, new_size):
        """
        Constrain the height to be the amount needed for the accordion bars as
        well as the expanded views.
        """

        new_width = new_size.width
        new_height = len(self._accordion_info) + sum(
            [entry['view'].size.height for entry in self._accordion_info if entry['is_expanded']])

        return Size(new_width, new_height)

    def recalculate_size(self):
        """
        Force a recalculation of the size by setting the size to the current
        size, and letting size constraint kick in.
        """

        self.set_size(self.size)

    def size_did_change(self):
        """
        Alert subviews that their width should change.
        """

        for entry in self._accordion_info:
            entry['view'].set_size(
                Size(self.size.width, entry['view'].size.height))

    def key_press(self, ev):
        if ev.key_code == 'Down':
            self.set_selection(self._selected_index + 1)
        elif ev.key_code == 'Up':
            self.set_selection(self._selected_index - 1)
        elif ev.key_code == 'Left':
            self.set_is_expanded(self._selected_index, False)
        elif ev.key_code == 'Right':
            self.set_is_expanded(self._selected_index, True)
        else:
            super().key_press(ev)

    def draw(self):

        lines = []

        for i, entry in enumerate(self._accordion_info):
            if len(entry['title']) < self.size.width - 6:
                title = entry['title']
            else:
                title = entry['title'][:self.size.width - 9] + '...'

            if entry['is_expanded']:
                title_line = ' v ' + title + \
                    (self.size.width - 3 - len(title)) * ' '
            else:
                title_line = ' > ' + title + \
                    (self.size.width - 3 - len(title)) * ' '

            if i == self._selected_index:
                lines.append(Tixel.tixels(
                    title_line, Color.Black, Color.White))
            else:
                lines.append(Tixel.tixels(title_line, Color.Black, Color.Grey))

            if entry['is_expanded']:
                lines += [line[:self.size.width]
                          for line in entry['view'].draw()]

        return lines
