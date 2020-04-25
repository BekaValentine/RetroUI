import re
import os
import signal
import sys
import termios
import multiprocessing
import tty
import traceback
from typing import Any, Callable, Generator, List, NewType, Optional, Tuple, Union


ESCAPE_SEQUENCES = {
    '\x1b[1~': 'Home',
    '\x1b[2~': 'Insert',
    '\x1b[3~': 'Delete',
    '\x1b[4~': 'End',
    '\x1b[5~': 'PageUp',
    '\x1b[6~': 'PageDown',
    '\x1b[7~': 'Home',
    '\x1b[8~': 'End',
    '\x1b[10~': 'F0',
    '\x1b[11~': 'F1',
    '\x1b[12~': 'F2',
    '\x1b[13~': 'F3',
    '\x1b[14~': 'F4',
    '\x1b[15~': 'F5',
    '\x1b[17~': 'F6',
    '\x1b[18~': 'F7',
    '\x1b[19~': 'F8',
    '\x1b[20~': 'F9',
    '\x1b[21~': 'F10',
    '\x1b[23~': 'F11',
    '\x1b[24~': 'F12',
    '\x1b[25~': 'F13',
    '\x1b[26~': 'F14',
    '\x1b[28~': 'F15',
    '\x1b[29~': 'F16',
    '\x1b[31~': 'F17',
    '\x1b[32~': 'F18',
    '\x1b[33~': 'F19',
    '\x1b[34~': 'F20',
    '\x1b[A': 'Up',
    '\x1b[B': 'Down',
    '\x1b[C': 'Right',
    '\x1b[D': 'Left',
    '\x1b[F': 'End',
    '\x1b[H': 'Home',
    '\x1b[1P': 'F1',
    '\x1b[1Q': 'F2',
    '\x1b[1R': 'F3',
    '\x1b[1S': 'F4',
}

MODIFIERS = {
    '\x1b[1;2': ['Shift'],
    '\x1b[1;3': ['Alt'],
    '\x1b[1;4': ['Shift', 'Alt'],
    '\x1b[1;5': ['Ctrl'],
    '\x1b[1;7': ['Ctrl', 'Alt'],
}


class ScreenColor(object):
    """
    A `ScreenColor` is how the screen represents color.
    """

    def __init__(self, r, g, b):
        # type: (int,int,int) -> None
        self.r: int = r
        self.g: int = g
        self.b: int = b

    def __repr__(self):
        # type: () -> str
        return 'ScreenColor(%s,%s,%s)' % (self.r, self.g, self.b)


class ScreenTixel(object):
    """
    A `ScreenTixel` is how the screen represents tixels.
    """

    def __init__(self, ch, fg, bg):
        # type: (str,Optional[ScreenColor],Optional[ScreenColor]) -> None
        self.character = ch  # type: str
        self.foreground = fg  # type: Optional[ScreenColor]
        self.background = bg  # type: Optional[ScreenColor]

    def __repr__(self):
        # type: () -> str

        return 'ScreenTixel(%s,%s,%s)' % (repr(self.character), self.foreground, self.background)


ScreenLine = List[ScreenTixel]
ScreenContent = List[ScreenLine]


class Screen(object):
    """
    A `Screen` is an abstract representation of the screen that hosted
    applications can interface with.

    Slots:

        '_manager'
            The `ScreenManager` that is actually managing the screen.
    """

    __slots__ = ['_manager']

    def __init__(self, manager):
        # type: (ScreenManager) -> None
        self._manager = manager  # type: ScreenManager

    def draw(self, lines):
        # type: (ScreenContent) -> None
        """
        Replaces the entire contents of the screen with the specified lines,
        clipping them to fit the screen size.

        If the lines do not cover the screen, the remaining space is left blank.
        """

        self._manager.application_draw(lines)

    def get_size(self):
        # type: () -> Tuple[int, int]
        """
        Gets the screen size.
        """

        return (self._manager.width, self._manager.height)

    def get_cursor_position(self):
        # type: () -> Optional[Tuple[int, int]]
        """
        Gets the cursor position.
        """

        return self._manager._application_cursor_position

    def set_cursor_position(self, x, y):
        # type: (int,int) -> None
        """
        Sets the cursor position.
        """

        # self._manager._main_queue.put(SetCursorPosition(x, y))
        # self.cursor_position = (int(x), int(y))
        self._manager.application_set_cursor_position(x, y)

    def show_cursor(self):
        # type: () -> None
        """
        Shows the cursor.
        """

        # self._manager._main_queue.put(ShowCursor())
        self._manager.application_show_cursor()

    def hide_cursor(self):
        # type: () -> None
        """
        Hides the cursor.
        """

        # self._manager._main_queue.put(HideCursor())
        self._manager.application_hide_cursor()


class ScreenManager(object):
    """
    A `Screen` is a convenient wrapper around the functionality for interfacing
    with the terminal.

    It permits the programmer to draw contents to the terminal in a way that
    doesn't disturb scrollback and other terminal content, while also
    abstracting over some details of terminal interfacing.

    Slots:

        `width`
            The width of the screen.

        `height`
            The height of the screen.

        `_cursor_is_visible`
            Whether or not the cursor is actually visible.

        `_cursor_position`
            The actual position of the cursor in the terminal.

        `_original_terminal_settings`
            The terminal settings before grabbing the screen.

        `_main_queue`
            The queue used to pass errors and events out of child threads to the
            main thread so they can be further handled.

        `_application_cursor_is_visible`
            Whether or not the cursor is visible, according to a hosted
            application.

        `_application_cursor_position`
            The position of the cursor as managed by a hosted application.

        `_screen_contents`
            The contents of the screen as managed by a hosted application.

        `_debug`
            Whether or not the `ScreenManager` is being debugged.

        `_log`
            The debug log.
    """

    __slots__ = ['width', 'height', '_cursor_is_visible', '_cursor_position', '_original_terminal_settings',
                 '_main_queue', '_application_cursor_is_visible', '_application_cursor_position', '_screen_contents', '_debug', '_log']

    def __init__(self):
        # type: () -> None
        self._cursor_is_visible = True  # type: bool
        self._cursor_position = (0, 0)  # type: Tuple[int,int]
        self._original_terminal_settings = []  # type: List[Union[int, List[bytes]]]
        self._main_queue = multiprocessing.Queue() \
            # type:  multiprocessing.Queue[Event]
        self._application_cursor_is_visible = False  # type: bool
        self._application_cursor_position = (0, 0)  # type: Tuple[int, int]
        self._screen_contents = []  # type: ScreenContent
        self._debug = False  # type: bool
        self._log = []  # type: List[str]

    # ##### Managing Applications ##############################################

    def setup(self):
        # type: () -> None
        """
        Gets the terminal ready for the main callback to use it.

        Stores terminal properties from before it was grabbed, manages the
        cleaning of the screen, the input events, and resize events.
        """

        size = os.get_terminal_size()
        self.width = size.columns
        self.height = size.lines

        self._original_terminal_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)

        self.hide_cursor()

        self._cursor_position = (0, 0)

        self.start_alternate_screen()
        self.blank_screen()
        sys.stdout.flush()

    def teardown(self):
        # type: () -> None
        """
        Returns the screen to the previous state before it was grabbed.
        """

        self.set_cursor_position(0, 0)
        self.blank_screen()
        self.close_alternate_screen()

        self.show_cursor()

        self.flush_stdio()

        termios.tcsetattr(sys.stdin,
                          termios.TCSADRAIN,
                          self._original_terminal_settings)

    def run_app(self, make_application_coroutine):
        # type: (Callable[[Screen], Generator[None, Optional['Event'], None]]) -> None
        """
        Sets up the screen, spins off threads for the keyboard monitor callback,
        and the resize event listener, and then waits for events to handle. When
        exiting, cleans up the screen as well, and then rethrows any exception
        that the hosted application may have thrown.
        """

        self.setup()

        self._main_queue = multiprocessing.Queue()

        def keypress_handler():
            # type: () -> None
            sys.stdin = open(0)
            while True:
                ch = self.getch()
                self._main_queue.put(KeyPressEvent(*ch))

        kb_monitor = multiprocessing.Process(target=keypress_handler)
        kb_monitor.daemon = True
        kb_monitor.start()

        def resize_handler(signum, frame):
            # type: (Any,Any) -> None
            size = os.get_terminal_size()
            self._main_queue.put(ResizeEvent(size.columns, size.lines))

        old_sigwinch = signal.signal(signal.SIGWINCH, resize_handler)

        should_exit = False

        application_coroutine = make_application_coroutine(Screen(self))

        try:
            application_coroutine.send(None)
            while True:
                msg = self._main_queue.get()
                if isinstance(msg, KeyPressEvent) and msg.key_code == '\x18':
                    should_exit = True
                    break

                if isinstance(msg, KeyPressEvent):
                    application_coroutine.send(msg)
                elif isinstance(msg, ResizeEvent):
                    self.set_size(msg.new_width, msg.new_height)
                    application_coroutine.send(msg)
        except StopIteration:
            err = None
        except BaseException as e:
            err = e

        self.teardown()
        kb_monitor.terminate()
        signal.signal(signal.SIGWINCH, old_sigwinch)

        if self._debug:
            print('--- BEGIN LOG ---')
            print('\n'.join(self._log))
            print('--- END LOG ---')

        if should_exit:
            raise SystemExit

        if err is not None:
            raise err

    def set_size(self, width, height):
        # type: (int,int) -> None
        """
        Resizes the screen and cleans up the resized screen.
        """
        self.width = width
        self.height = height
        self.blank_screen()

    # ##### Interacting With The Terminal ######################################

    def flush_stdio(self):
        # type: () -> None
        """
        Flush the standard input.
        """

        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)

    def start_alternate_screen(self):
        # type: () -> None
        """
        Starts the alternate terminal screen.
        """

        sys.stdout.write('\x1b[?1049h')

    def close_alternate_screen(self):
        # type: () -> None
        """
        Closes the alternate terminal screen.
        """

        sys.stdout.write('\x1b[?1049l')

    @staticmethod
    def enforce_screen_width(tixels, width):
        # type: (ScreenLine,int) -> ScreenLine
        """
        Enforce that a line of tixels is exactly as wide as the screen.
        """

        if len(tixels) < width:
            return tixels + (width - len(tixels)) * [ScreenTixel(' ', ScreenColor(0, 0, 0), ScreenColor(0, 0, 0))]
        else:
            return tixels[:width]

    @staticmethod
    def enforce_screen_height(lines, height):
        # type: (ScreenContent,int) -> ScreenContent
        """
        Enforce that a screenful of tixel lines is exactly as tall as the
        screen.
        """

        if len(lines) < height:
            return lines + (height - len(lines)) * [[]]
        else:
            return lines[:height]

    @staticmethod
    def enforce_screen_size(lines, width, height):
        # type: (ScreenContent, int, int) -> ScreenContent
        """
        Enforce that a screenful of tixel lines is exactly as wide and as tall
        as the screen.
        """

        correct_height = ScreenManager.enforce_screen_height(lines, height)
        correct_width_and_height = [ScreenManager.enforce_screen_width(
            line, width) for line in correct_height]
        return correct_width_and_height

    @staticmethod
    def line_to_terminal_line(line):
        # type: (ScreenLine) -> str
        """
        Convert a line of tixels to a line of terminal text, with the smallest
        amount of color information as possible.
        """

        terminal_line = ''

        fg_color = ScreenColor(0, 0, 0)  # type: ScreenColor
        bg_color = ScreenColor(0, 0, 0)  # type: ScreenColor

        for i, tx in enumerate(line):
            ch = tx.character
            fg = tx.foreground
            bg = tx.background
            if i == 0:
                if fg is None:
                    fg_color = ScreenColor(255, 255, 255)
                else:
                    fg_color = fg

                if bg is None:
                    bg_color = ScreenColor(0, 0, 0)
                else:
                    bg_color = bg

                # add the initial fg color
                terminal_line += '\x1b[38;2;{};{};{}m'.format(
                    fg_color.r, fg_color.g, fg_color.b)

                # add the initial bg color
                terminal_line += '\x1b[48;2;{};{};{}m'.format(
                    bg_color.r, bg_color.g, bg_color.b)
            else:
                if fg is not None and fg != fg_color:
                    # set the new fg color
                    fg_color = fg
                    terminal_line += '\x1b[38;2;{};{};{}m'.format(
                        fg_color.r, fg_color.g, fg_color.b)

                if bg is not None and bg != bg_color:
                    # set the new bg color
                    bg_color = bg
                    terminal_line += '\x1b[48;2;{};{};{}m'.format(
                        bg_color.r, bg_color.g, bg_color.b)

            terminal_line += ch

        # add the color reset
        terminal_line += '\x1b[0m'

        return terminal_line

    @staticmethod
    def lines_to_terminal_lines(lines):
        # type: (ScreenContent) -> List[str]
        """
        Converts a screenful of tixel lines to a screenful of terminal lines.
        """

        return [ScreenManager.line_to_terminal_line(line) for line in lines]

    def draw(self, new_contents):
        # type: (ScreenContent) -> None
        """
        Replaces the content of the screen with the given lines.
        """

        # trim and pad the new contents to fill the screen in both directions
        new_contents = ScreenManager.enforce_screen_size(
            new_contents, self.width, self.height)

        # compute terminal string representations
        new_terminal_lines = \
            ScreenManager.lines_to_terminal_lines(
                new_contents)  # type: List[str]
        # diff the new and old contents
        # CAUTION: Diffing does NOT currently work with color
        #
        # old_terminal_lines = ScreenManager.lines_to_terminal_lines(
        #    self._screen_contents)
        #
        # contents_diff = multiline_diff(old_terminal_lines, new_terminal_lines)
        #
        # write_cmd = ''
        # for y, line_diff in contents_diff:
        #     for x, new_substr in line_diff:
        #         write_cmd += '\x1b[{y};{x}H{s}'.format(
        #             x=x + 1, y=y + 1, s=new_substr)

        write_cmd = ''  # type: str
        for y, line in enumerate(new_terminal_lines):
            write_cmd += '\x1b[{y};0H{s}'.format(y=y + 1, s=line)

        if write_cmd != '':
            self.hide_cursor()
            self.set_cursor_position(0, 0)
            sys.stdout.write(write_cmd)
            sys.stdout.flush()
            self._screen_contents = new_contents

        self.set_cursor_position(0, 0)

    def blank_screen(self):
        # type: () -> None
        """
        Fills the screen with blank space.
        """

        self.draw(self.height *
                  [self.width * [ScreenTixel(' ', None, None)]])

    def terminal_cursor_position(self):
        # type: () -> Optional[Tuple[int, int]]
        """
        Determines the current cursor position in the terminal.
        """

        terminal_settings = termios.tcgetattr(sys.stdin)

        try:
            self.flush_stdio()
            tty.setcbreak(sys.stdin, termios.TCSANOW)
            sys.stdout.write('\x1b[6n')
            sys.stdout.flush()

            position = str(os.read(sys.stdin.fileno(), 10), encoding='ascii')
        finally:
            tty.setraw(sys.stdin)
            termios.tcsetattr(sys.stdin,
                              termios.TCSANOW, terminal_settings)

        m = re.match('^\x1b\[(\d*);(\d*)R', position)

        if m:
            return (int(m.group(2)) - 1, int(m.group(1)) - 1)

        return None

    def show_cursor(self):
        # type: () -> None
        """
        Show the cursor.
        """

        # '\x1b[?25h' is VT escape seq for show cursor
        sys.stdout.write('\x1b[?25h')
        sys.stdout.flush()
        self._cursor_is_visible = True

    def hide_cursor(self):
        # type: () -> None
        """
        Hide the cursor.
        """

        # '\x1b[?25l' is VT escape seq for hide cursor
        sys.stdout.write('\x1b[?25l')
        sys.stdout.flush()
        self._cursor_is_visible = False

    def set_cursor_position(self, x, y):
        # type: (int,int) -> None
        """
        Sets the position of the cursor.
        """

        self._cursor_position = (x, y)
        sys.stdout.write('\x1b[{y};{x}H'.format(x=x + 1, y=y + 1))
        sys.stdout.flush()

    def getch(self):
        # type: () -> Tuple[str, bool, bool, bool]
        """
        Reads a character from standard input.

        This will return a multi-character string for any keypress events that
        write multiple characters to standard input. The contents are replaced
        with cleaned up representations where possible, using the substitutions
        defined by `ESCAPE_SEQUENCES` and `MODIFIERS`.
        """

        char_with_mods = str(
            os.read(sys.stdin.fileno(), 128), encoding='ascii')
        ctrl = False
        alt = False
        shift = False
        if len(char_with_mods) == 1:
            ch = char_with_mods
        if len(char_with_mods) != 1:
            if char_with_mods in ESCAPE_SEQUENCES:
                ch = ESCAPE_SEQUENCES[char_with_mods]
            elif char_with_mods[: 5] in MODIFIERS and ('\x1b[' + char_with_mods[5:]) in ESCAPE_SEQUENCES:
                ch = ESCAPE_SEQUENCES['\x1b[' + char_with_mods[5:]]
                mods = MODIFIERS[char_with_mods[: 5]]
                ctrl = 'Ctrl' in mods
                alt = 'Alt' in mods
                shift = 'Shift' in mods
            else:
                ch = char_with_mods
        return (ch, ctrl, alt, shift)

    # ###### Handling Application Messages #####################################

    def application_set_cursor_position(self, x, y):
        # type: (int,int) -> None
        """
        Sets the hosted-program-managed cursor position.
        """

        self.set_cursor_position(int(x), int(y))
        self._application_cursor_position = (int(x), int(y))

    def application_hide_cursor(self):
        # type: () -> None
        """
        Hides the cursor.
        """

        self.hide_cursor()
        self._application_cursor_is_visible = False

    def application_show_cursor(self):
        # type: () -> None
        """
        Shows the cursor.
        """

        self.show_cursor()
        self._application_cursor_is_visible = True

    def application_draw(self, lines):
        # type: (ScreenContent) -> None
        """
        Replaces the entire contents of the screen with the specified lines,
        clipping them to fit the screen size.

        If the lines do not cover the screen, the remaining space is left blank.
        """

        # Write the line contents
        self.draw(lines)

        # Put the cursor back where the hosted program has it
        self.set_cursor_position(*self._application_cursor_position)

        # Show the cursor if it's supposed to be visible
        if self._application_cursor_is_visible:
            self.show_cursor()

        sys.stdout.flush()


class Event(object):
    """
    `Event` is an abstract class representing the various kinds of events that
    the terminal can produce.
    """

    pass


class KeyPressEvent(Event):
    """
    A `KeyPressEvent` is an event that corresponds to a key press by the user.

    Slots:

        `key_code`
            The code for the key that was pressed.

        `has_ctrl_modifier`
            Whether or not the Ctrl modifier key was pressed.

        `has_alt_modifier`
            Whether or not the Alt modifier key was pressed.

        `has_shift_modifier`
            Whether or not the Shift modifier key was pressed.
    """

    __slots__ = ['key_code', 'has_ctrl_modifier',
                 'has_alt_modifier', 'has_shift_modifier']

    def __init__(self, kc, ctrl_mod, alt_mod, shift_mod):
        # type: (str,bool,bool,bool) -> None
        self.key_code = kc  # type: str
        self.has_ctrl_modifier = ctrl_mod  # type: bool
        self.has_alt_modifier = alt_mod  # type: bool
        self.has_shift_modifier = shift_mod  # type: bool

    def __repr__(self):
        # type: () -> str
        return '<KeyPressEvent key_code=%s ctrl=%s alt=%s shift=%s>' % (repr(self.key_code), self.has_ctrl_modifier, self.has_alt_modifier, self.has_shift_modifier)


class ResizeEvent(Event):
    """
    A `ResizeEvent` corresponds to a change in the size of the terminal.

    Slots:

        `new_width`
            The new width of the screen after resizing.

        `new_height`
            The new height of the screen after resizing.
    """

    __slots__ = ['new_width', 'new_height']

    def __init__(self, nw, nh):
        # type: (int,int) -> None
        self.new_width = nw  # type: int
        self.new_height = nh  # type: int

    def __repr__(self):
        # type: () -> str
        return '<ResizeEvent new_width=%i new_height=%i>' % (self.new_width, self.new_height)


LineDiff = NewType('LineDiff', List[Tuple[int, str]])


def line_diff(old, new):
    # type: (str,str) -> LineDiff
    """
    Compute the difference between two equal-length lines of text.

    Returns a list of pairs consisting of the starting index of a difference,
    and the new substring that starts at that index.
    """

    d = ''

    for i in range(min(len(old), len(new))):
        if old[i] == new[i]:
            d += '_'
        else:
            d += 'x'

    j = 0
    blocks = []
    while len(d) > j:
        if d[j] == '_':
            j += 1
        elif d[j] == 'x':
            start = j
            while len(d) > j and d[j] == 'x':
                j += 1
            end = j
            blocks.append((start, end))

    ds = [(start, new[start: end]) for (start, end) in blocks]

    if len(old) < len(new):
        if len(ds) == 0:
            ds.append((len(old), new[len(old):]))
        else:
            x, chg = ds[-1]
            endx = x + len(chg)
            if endx == len(old):
                ds[-1] = (x, chg + new[len(old):])
            else:
                ds.append((len(old), new[len(old):]))

    return LineDiff(ds)


MultiLineDiff = NewType('MultiLineDiff', List[Tuple[int, LineDiff]])


def multiline_diff(olds, news):
    # type: (List[str], List[str]) -> MultiLineDiff
    """
    Computes the difference betweent two equal length lists of equal length
    lines.

    Returns a list of pairs consisting of the line index of each differing line,
    and the line difference of the two lines.
    """

    ds = []  # type: List[Tuple[int, LineDiff]]

    for i, (old, new) in enumerate(zip(olds, news)):
        d = line_diff(old, new)
        if len(d) != 0:
            ds.append((i, d))

    if len(olds) < len(news):
        for y, new in enumerate(news[len(olds):]):
            ds.append((len(olds) + y, LineDiff([(0, new)])))

    return MultiLineDiff(ds)

#
# Demo
#


def string_to_screen_line(s):
    # type: (str) -> ScreenLine
    return [ScreenTixel(ch, None, None) for ch in s]


class App(object):
    def __init__(self):
        # type: () -> None
        self.count = 0  # type: int

    def run(self):
        # type: () -> None
        ScreenManager().run_app(self.run_with_screen)

    def run_with_screen(self, screen):
        # type: (Screen) -> Generator[None, Optional[Event], None]
        events = []  # type: List[Event]
        i: int
        for i in range(15):
            screen.draw([string_to_screen_line(repr(self.count))] +
                        [string_to_screen_line(repr(e)) for e in events])
            if i == 5:

                # Throw a NameError from the internal thread
                # print(foo)

                # Throw a SystemExit error
                # raise SystemExit
                screen.draw(
                    [string_to_screen_line('Showing cursor at 5,10')])
                screen.show_cursor()
                screen.set_cursor_position(5, 10)
                time.sleep(2)
                screen.draw([string_to_screen_line(
                    repr(screen.get_cursor_position()))])
                time.sleep(2)
                screen.hide_cursor()
                screen.draw([string_to_screen_line(repr(self.count))] +
                            [string_to_screen_line(repr(e)) for e in events])
                pass

            if i == 10:
                screen.draw([string_to_screen_line('The current screen size is '),
                             string_to_screen_line(repr(screen.get_size()))])
                time.sleep(4)
                screen.draw([string_to_screen_line(repr(self.count))] +
                            [string_to_screen_line(repr(e)) for e in events])
            ev = yield
            if ev is not None:
                events.append(ev)
            self.count += 1


if __name__ == '__main__':
    import time

    app = App()

    app.run()


if __name__ == '__main2__':
    print(line_diff('__aa', ' _bb'))
    print(multiline_diff(['__aa___',
                          'c________',
                          '______xxx'],
                         ['_____bb__',
                          'c________']))
    print(multiline_diff([], ['abc']))


if __name__ == '__main3__':
    def bouncer():
        # type: () -> Generator[int, Optional[str], None]
        print('hello')
        x: Optional[str]
        x = yield 1
        print('x = ' + repr(x))
        y: Optional[str]
        y = yield 2
        print('y = ' + repr(y))
        z: Optional[str]
        z = yield 3
        print('z = ' + repr(z))

    bounce = bouncer()  # type: Generator[int, Optional[str], None]
    print('--')
    try:
        print(bounce.send(None))
        print(bounce.send('a'))
        print(bounce.send('b'))
        print(bounce.send('c'))
    except StopIteration:
        pass
