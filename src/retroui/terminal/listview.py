from retroui.terminal.view import *


class ListView(View):
    """
    A `ListView` displays a list of items, which can potentially have sublists.

    Sublists can be expanded or not, allowing part of the list to be hidden when
    not needed.

    Slots:

        `_list_info`
            The internal representation of the list to display.

        `_selected`
            The item in the list that is currently selected.
    """

    __slots__ = ['_list_info']

    def __init__(self):
        self._list_info = {
            'parent': None,
            'sublist': []
        }
        self._selected = None

    @staticmethod
    def make_list_info(parent, new_list):
        """
        Build up the sublist for a list info item.
        """

        new_list_info = []

        for name, sublist in new_list:
            item = {
                'parent': parent,
                'label': name,
                'is_expanded': False
            }
            item['sublist'] = ListView.make_list_info(item, sublist)

            new_list_info.append(item)

        return new_list_info

    def set_list(self, new_list):
        """
        Set the list to display.
        """

        self._list_info['sublist'] = ListView.make_list_info(
            self._list_info, new_list)
        if len(self._list_info['sublist']) > 0:
            self._selected = self._list_info['sublist'][0]

        self.recalculate_size()

    @staticmethod
    def set_is_expanded_for_all(list_info, yn):
        """
        Sets all of the items in the list info to have the given expansion
        value.
        """

        for item in list_info:
            item['is_expanded'] = yn
            ListView.set_is_expanded_for_all(item['sublist'], yn)

    def expand_all(self):
        """
        Expands all of the items in the `ListView`.
        """

        ListView.set_is_expanded_for_all(self._list_info['sublist'], True)

    def collapse_all(self):
        """
        Collapses all of the items in the `ListView`.
        """

        ListView.set_is_expanded_for_all(self._list_info['sublist'], False)

    @staticmethod
    def size_for_list_item(indent, list_item):
        """
        Computes the size of the list item, given an indentation level.
        """

        if len(list_item['sublist']) == 0:
            return Size(indent + len(list_item['label']), 1)
        elif list_item['is_expanded']:
            rec_size = ListView.size_for_list_info(
                indent + 2, list_item['sublist'])
            label_width = indent + 2 + len(list_item['label'])
            return Size(max(label_width, rec_size.width), 1 + rec_size.height)
        else:
            return Size(indent + 2 + len(list_item['label']), 1)

    @staticmethod
    def size_for_list_info(indent, list_info):
        """
        Computes the size of the list info, given an indentation level.
        """

        leave_space_for_expanders = any(
            [len(item['sublist']) != 0 for item in list_info])

        item_sizes = [ListView.size_for_list_item(
            indent + (2 if leave_space_for_expanders else 0), item) for item in list_info]

        width = max([s.width for s in item_sizes], default=0) + \
            (2 if leave_space_for_expanders else 0)

        height = sum([s.height for s in item_sizes])

        return Size(width, height)

    def constrain_size(self, new_size):
        """
        Constrains the size to exactly fit the list content.
        """

        return ListView.size_for_list_info(0, self._list_info['sublist'])

    def recalculate_size(self):
        """
        Sets the current size to fit the list content by setting the size to
        zero, which will be replaced by the `constrain_size` method with the
        correct size.
        """

        self.set_size(Size(0, 0))

    @staticmethod
    def next_item(item):
        """
        Gets the item after the given item, accounting for the tree structure,
        and expansion of sublists
        """

        if len(item['sublist']) != 0 and item['is_expanded']:
            return item['sublist'][0]
        else:
            return ListView.exit_till_next(item)

    @staticmethod
    def exit_till_next(item):
        """
        Traverse out of the right spine of a tree until a next sibling node can
        be reached.
        """

        if item['parent'] is None:
            return None
        else:
            ix = item['parent']['sublist'].index(item)
            if ix + 1 < len(item['parent']['sublist']):
                return item['parent']['sublist'][ix + 1]
            else:
                return ListView.exit_till_next(item['parent'])

    @staticmethod
    def last_item(list_info):
        """
        Get the last item in some list items, accounting for the expansion of
        the proximal last item, and return the recursive last item if it is in
        fact expanded.
        """

        if len(list_info) == 0:
            return None
        elif len(list_info[-1]['sublist']) != 0 and list_info[-1]['is_expanded']:
            return ListView.last_item(list_info[-1]['sublist'])
        else:
            return list_info[-1]

    @staticmethod
    def previous_item(item):
        """
        Gets the item before the given item, accounting for the tree structure,
        and expansion of sublists
        """

        if item['parent'] is None:
            return None
        else:
            ix = item['parent']['sublist'].index(item)
            if ix == 0:
                return item['parent']
            else:
                sibling = item['parent']['sublist'][ix - 1]
                if len(sibling['sublist']) != 0 and sibling['is_expanded']:
                    return ListView.last_item(sibling['sublist'])
                else:
                    return sibling

    def key_press(self, ev):
        if ev.key_code == 'Up':
            prev = ListView.previous_item(self._selected)
            if prev != self._list_info:
                self._selected = prev

        elif ev.key_code == 'Down':
            next = ListView.next_item(self._selected)
            if next is not None:
                self._selected = next

        elif ev.key_code == 'Left':
            self._selected['is_expanded'] = False

        elif ev.key_code == 'Right':
            self._selected['is_expanded'] = True

        else:
            super().key_press(ev)

    @staticmethod
    def list_info_to_lines(indent, list_info):
        """
        Converts the list into lines for rendering.
        """

        lines = []

        leave_space_for_expanders = any(
            [len(item['sublist']) != 0 for item in list_info])

        for item in list_info:
            if len(item['sublist']) == 0:
                lines.append(
                    (item, indent * ' ' + ('  ' if leave_space_for_expanders else '') + item['label']))
            elif item['is_expanded']:
                lines.append((item, indent *
                              ' ' + 'v ' + item['label']))
                lines += ListView.list_info_to_lines(
                    indent + 2 + (2 if leave_space_for_expanders else 0), item['sublist'])
            else:
                lines.append((item, indent *
                              ' ' + '> ' + item['label']))

        return lines

    def draw(self):
        lines = ListView.list_info_to_lines(0, self._list_info['sublist'])

        tixel_lines = []
        for item, line in lines:
            line = line.ljust(self.size.width, ' ')
            if item == self._selected:
                tixel_lines.append(
                    [Tixel(c, Color.Black, Color.White) for c in line])
            else:
                tixel_lines.append(
                    [Tixel(c, Color.White, Color.Black) for c in line])

        return tixel_lines
