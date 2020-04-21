import math

from retroui.terminal.view import *


class TabView(View):
    """
    A `TabView` is a way of displaying multiple views in different tabs, and
    navigating between them.

    Slots:
        `_tab_info`
            Internal information about what the subviews are and what their
            titles are.

        `_selected_index`
            The index of the currently selected subview.

        `tab_style`
            How the tabs are shown in the tab bar. Possible values are:

            `'left'`
                The tabs are only as wide as need to be and are aligned on the
                left of the tab bar. Default.

            `'center'`
                The tabs are only as wide as need to be and are aligned on the
                center of the tab bar.

            `'right'`
                The tabs are only as wide as need to be and are aligned on the
                right of the tab bar.

            `'fill_align_left'`
                The tabs are expanded to fill the tab bar, with titles aligned
                on the left of the tab.

            `'fill_align_center'`
                The tabs are expanded to fill the tab bar, with titles aligned
                on the center of the tab.

            `'fill_align_right'`
                The tabs are expanded to fill the tab bar, with titles aligned
                on the right of the tab.
    """

    __slots__ = ['_tab_info', '_selected_index', 'tab_style']

    def __init__(self):
        super().__init__()

        self._tab_info = []
        self._selected_index = 0
        self.tab_style = 'left'

    def set_views(self, new_views):
        """
        Sets the views in the `TabView` to the given views.

        Argument should be a list of pairs of the title and the view, in that
        order.
        """

        self._tab_info = []
        for title, view in new_views:
            self._tab_info.append({
                'title': title,
                'view': view
            })

        self._selected_index = 0

    def set_tab_style(self, style):
        """
        Sets the style of the tabs.
        """

        if style in ['left', 'center', 'right', 'fill_align_left', 'fill_align_center', 'fill_align_right']:
            self.tab_style = style
        else:
            self.tab_style = 'left'

    def set_selection(self, ix):
        """
        Set the selected view.
        """

        self._selected_index = max(0, min(len(self._tab_info) - 1, ix))

    def constrain_size(self, new_size):
        """
        Constrain the height to be at least 1 high for the tabs, and wide enough
        to show at least ellipses in each tab.
        """

        return Size(max(6 * len(self._tab_info) - 1, new_size.width), max(1, new_size.height))

    def size_did_change(self):
        """
        Alert subviews that their width should change.
        """

        for entry in self._tab_info:
            entry['view'].set_size(
                Size(self.size.width, self.size.height - 1))

    def key_press(self, ev):
        if ev.key_code == 'Left':
            self.set_selection(self._selected_index - 1)
        elif ev.key_code == 'Right':
            self.set_selection(self._selected_index + 1)
        else:
            super().key_press(ev)

    @staticmethod
    def fit_titles_into_tabs_width(titles, width):
        """
        Makes the titles small enough so that their tabs fit within the given
        width, possibly truncating with ellipsis.

        Decreases the size of longer titles first.
        """

        while True:
            aggregate_tabs_width = sum(
                [len(title) + 2 for title in titles]) + len(titles) - 1

            if aggregate_tabs_width <= width:
                break

            new_max = max([len(title) for title in titles]) - 1
            titles = [title if len(title) <= new_max else title[:new_max - 3] + '...'
                      for title in titles]

        return titles

    @staticmethod
    def fill_titles_into_tabs_width(titles, width, style):
        """
        Pads the size of the titles until their tabs would fill the given width,
        and aligns the text to the given style's alignment.
        """

        next_to_increment = 0
        while True:
            aggregate_tabs_width = sum(
                [len(title) + 2 for title in titles]) + len(titles) - 1

            if aggregate_tabs_width >= width:
                break

            if style == 'fill_align_left':
                titles[next_to_increment] += ' '
            elif style == 'fill_align_right':
                titles[next_to_increment] = ' ' + titles[next_to_increment]
            elif style == 'fill_align_center':
                new_len = len(titles[next_to_increment]) + 1
                bare = titles[next_to_increment].strip()
                pre = math.floor(0.5 * (new_len - len(bare)))
                post = new_len - len(bare) - pre
                titles[next_to_increment] = pre * ' ' + bare + post * ' '
            next_to_increment = (next_to_increment + 1) % len(titles)

        return titles

    def draw(self):

        lines = []

        if self.tab_style in ['left', 'center', 'right']:
            fitted_titles = TabView.fit_titles_into_tabs_width(
                [entry['title'] for entry in self._tab_info], self.size.width)

            title_line = []
            for i, title in enumerate(fitted_titles):
                if i > 0:
                    title_line.append(Tixel(' ', Color.White, Color.Black))
                if i == self._selected_index:
                    title_line += Tixel.tixels(' ' + title + ' ',
                                               Color.Black, Color.White)
                else:
                    title_line += Tixel.tixels(' ' + title + ' ',
                                               Color.Black, Color.Grey)

            if self.tab_style == 'right':
                pad_size = self.size.width - len(title_line)
                title_line = Tixel.tixels(
                    pad_size * ' ', Color.White, Color.Black) + title_line
            elif self.tab_style == 'center':
                pad_size_left = math.floor(
                    0.5 * (self.size.width - len(title_line)))
                pad_size_right = self.size.width - \
                    len(title_line) - pad_size_left
                title_line = Tixel.tixels(pad_size_left * ' ', Color.White, Color.Black) + \
                    title_line + \
                    Tixel.tixels(pad_size_right * ' ',
                                 Color.White, Color.Black)

        else:

            fitted_titles = TabView.fit_titles_into_tabs_width(
                [entry['title'] for entry in self._tab_info], self.size.width)

            filled_titles = TabView.fill_titles_into_tabs_width(
                fitted_titles, self.size.width, self.tab_style)

            title_line = []
            for i, title in enumerate(filled_titles):
                if i > 0:
                    title_line.append(Tixel(' ', Color.White, Color.Black))
                if i == self._selected_index:
                    title_line += Tixel.tixels(' ' + title + ' ',
                                               Color.Black, Color.White)
                else:
                    title_line += Tixel.tixels(' ' + title + ' ',
                                               Color.Black, Color.Grey)

        lines.append(title_line)

        lines += [line[:self.size.width]
                  for line in self._tab_info[self._selected_index]['view'].draw()]

        return lines