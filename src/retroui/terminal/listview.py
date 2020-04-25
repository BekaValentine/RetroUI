from typing import List, NewType, Optional, Tuple

from retroui.terminal.color import Color, Black, White
from retroui.terminal.event import Event
from retroui.terminal.size import Size
from retroui.terminal.tixel import Tixel
from retroui.terminal.view import View


class ListInfoNode(object):
    """
    A `ListInfoNode` is an internal representation of the list as a tree, with
    information about its structure intended for traversal

    Slots:

        `parent`
            The node above this one.

        `label`
            The label of this node.

        `sublist`
            The nodes of the sublist beneath this entry.

        `is_expanded`
            Whether or not the list entry for this node is expanded.
    """

    __slots__ = ['parent', 'label', 'sublist', 'is_expanded']

    def __init__(self, parent, label, sublist, is_expanded):
        # type: (Optional[ListInfoNode], str, List[ListInfoNode], bool) -> None
        self.parent = parent  # type: Optional[ListInfoNode]
        self.label = label  # type: str
        self.sublist = sublist  # type: List[ListInfoNode]
        self.is_expanded = is_expanded  # type: bool


class Tree(object):
    """
    A `Tree` is an n-ary branching tree labeled by strings.

    Slots:

        `label`
            The label of the root node.

        `children`
            The child nodes.
    """

    def __init__(self, label, children):
        # type: (str, List[Tree]) -> None
        self.label = label  # type: str
        self.children = children  # type: List[Tree]


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
        # type: () -> None
        self._list_info = ListInfoNode(
            parent=None,
            label='root',
            sublist=[],
            is_expanded=True)  # type: ListInfoNode
        self._selected = None  # type: Optional[ListInfoNode]

    @staticmethod
    def make_list_info(parent, new_list):
        # type: (Optional[ListInfoNode], Tree) -> ListInfoNode
        """
        Build up the sublist for a list info item.
        """

        # new_list_info = []  # type: List[ListInfoNode]
        #
        # for node in new_list.children:
        #     item = ListInfoNode(
        #         parent=parent,
        #         label=node.label,
        #         sublist=[],
        #         is_expanded=False)
        #     item.sublist = [ListView.make_list_info(
        #         item, c) for c in node.children]
        #
        #     new_list_info.append(item)
        #
        # return ListInfoNode(parent=None, label='root', sublist=new_list_info, is_expanded=True)

        item = ListInfoNode(parent=parent, label=new_list.label,
                            sublist=[], is_expanded=False)
        item.sublist = [ListView.make_list_info(
            item, n) for n in new_list.children]
        return item

    def set_list(self, new_list):
        # type: (List[Tree]) -> None
        """
        Set the list to display.
        """

        self._list_info = ListView.make_list_info(None, Tree('root', new_list))
        if len(self._list_info.sublist) > 0:
            self._selected = self._list_info.sublist[0]

        self.recalculate_size()

    @staticmethod
    def set_is_expanded_for_all(list_info, yn):
        # type: (List[ListInfoNode], bool) -> None
        """
        Sets all of the items in the list info to have the given expansion
        value.
        """

        for item in list_info:
            item.is_expanded = yn
            ListView.set_is_expanded_for_all(item.sublist, yn)

    def expand_all(self):
        # type: () -> None
        """
        Expands all of the items in the `ListView`.
        """

        ListView.set_is_expanded_for_all(self._list_info.sublist, True)

    def collapse_all(self):
        # type: () -> None
        """
        Collapses all of the items in the `ListView`.
        """

        ListView.set_is_expanded_for_all(self._list_info.sublist, False)

    @staticmethod
    def size_for_list_item(indent, list_item):
        # type: (int, ListInfoNode) -> Size
        """
        Computes the size of the list item, given an indentation level.
        """

        if len(list_item.sublist) == 0:
            return Size(indent + len(list_item.label), 1)
        elif list_item.is_expanded:
            rec_size = ListView.size_for_list_info(
                indent + 2, list_item.sublist)
            label_width = indent + 2 + len(list_item.label)
            return Size(max(label_width, rec_size.width), 1 + rec_size.height)
        else:
            return Size(indent + 2 + len(list_item.label), 1)

    @staticmethod
    def size_for_list_info(indent, list_info):
        # type: (int, List[ListInfoNode]) -> Size
        """
        Computes the size of the list info, given an indentation level.
        """

        leave_space_for_expanders = any(
            [len(item.sublist) != 0 for item in list_info])

        item_sizes = [ListView.size_for_list_item(
            indent + (2 if leave_space_for_expanders else 0), item) for item in list_info]

        width = max([s.width for s in item_sizes], default=0) + \
            (2 if leave_space_for_expanders else 0)

        height = sum([s.height for s in item_sizes])

        return Size(width, height)

    def constrain_size(self, new_size):
        # type: (Size) -> Size
        """
        Constrains the size to exactly fit the list content.
        """

        return ListView.size_for_list_info(0, self._list_info.sublist)

    def recalculate_size(self):
        # type: () -> None
        """
        Sets the current size to fit the list content by setting the size to
        zero, which will be replaced by the `constrain_size` method with the
        correct size.
        """

        self.set_size(Size(0, 0))

    @staticmethod
    def next_item(item):
        # type: (ListInfoNode) -> Optional[ListInfoNode]
        """
        Gets the item after the given item, accounting for the tree structure,
        and expansion of sublists
        """

        if len(item.sublist) != 0 and item.is_expanded:
            return item.sublist[0]
        else:
            return ListView.exit_till_next(item)

    @staticmethod
    def exit_till_next(item):
        # type: (ListInfoNode) -> Optional[ListInfoNode]
        """
        Traverse out of the right spine of a tree until a next sibling node can
        be reached.
        """

        if item.parent is None:
            return None
        else:
            ix = item.parent.sublist.index(item)
            if ix + 1 < len(item.parent.sublist):
                return item.parent.sublist[ix + 1]
            else:
                return ListView.exit_till_next(item.parent)

    @staticmethod
    def last_item(list_info):
        # type: (List[ListInfoNode]) -> Optional[ListInfoNode]
        """
        Get the last item in some list items, accounting for the expansion of
        the proximal last item, and return the recursive last item if it is in
        fact expanded.
        """

        if len(list_info) == 0:
            return None
        elif len(list_info[-1].sublist) != 0 and list_info[-1].is_expanded:
            return ListView.last_item(list_info[-1].sublist)
        else:
            return list_info[-1]

    @staticmethod
    def previous_item(item):
        # type: (ListInfoNode) -> Optional[ListInfoNode]
        """
        Gets the item before the given item, accounting for the tree structure,
        and expansion of sublists
        """

        if item.parent is None:
            return None
        else:
            ix = item.parent.sublist.index(item)
            if ix == 0:
                return item.parent
            else:
                sibling = item.parent.sublist[ix - 1]
                if len(sibling.sublist) != 0 and sibling.is_expanded:
                    return ListView.last_item(sibling.sublist)
                else:
                    return sibling

    def key_press(self, ev):
        # type: (Event) -> None
        if ev.key_code == 'Up':
            if self._selected:
                prev = ListView.previous_item(self._selected)
                if prev is not None:
                    self._selected = prev

        elif ev.key_code == 'Down':
            if self._selected:
                next = ListView.next_item(self._selected)
                if next is not None:
                    self._selected = next

        elif ev.key_code == 'Left':
            if self._selected is not None:
                self._selected.is_expanded = False

        elif ev.key_code == 'Right':
            if self._selected is not None:
                self._selected.is_expanded = True

        else:
            super().key_press(ev)

    @staticmethod
    def list_info_to_lines(indent, list_info):
        # type: (int,List[ListInfoNode]) -> List[Tuple[ListInfoNode, str]]
        """
        Converts the list into lines for rendering.
        """

        lines = []  # type: List[Tuple[ListInfoNode, str]]

        leave_space_for_expanders = any(
            [len(item.sublist) != 0 for item in list_info])

        for item in list_info:
            if len(item.sublist) == 0:
                lines.append(
                    (item, indent * ' ' + ('  ' if leave_space_for_expanders else '') + item.label))
            elif item.is_expanded:
                lines.append((item, indent *
                              ' ' + 'v ' + item.label))
                lines += ListView.list_info_to_lines(
                    indent + 2 + (2 if leave_space_for_expanders else 0), item.sublist)
            else:
                lines.append((item, indent *
                              ' ' + '> ' + item.label))

        return lines

    def draw(self):
        # type: () -> List[List[Tixel]]
        lines = ListView.list_info_to_lines(0, self._list_info.sublist)

        tixel_lines = []
        for item, line in lines:
            line = line.ljust(self.size.width, ' ')
            if item == self._selected:
                tixel_lines.append(
                    [Tixel(c, Black, White) for c in line])
            else:
                tixel_lines.append(
                    [Tixel(c, White, Black) for c in line])

        return tixel_lines
