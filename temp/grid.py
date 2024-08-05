import curses
import time


def origin(x, y):
    if x == 0 and y == 0:
        return '╬'
    elif x == 0:
        return '║'
    elif y == 0:
        return '═'
    else:
        return ' '


def grid(x, y):
    if x % 20 == 0 and y % 10 == 0:
        return '·'
    elif x % 20 == 0:
        return '·'
    elif y % 10 == 0:
        return '·' if x % 2 == 0 else ' '
    else:
        return ' '


def composite(f, g):
    def img(x, y):
        c = f(x, y)
        if c == ' ':
            return g(x, y)
        else:
            return c

    return img


def scale(f, s):
    def img(x, y):
        x0 = int(s * x)
        y0 = int(s * y)
        return f(x0, y0)

    return img


def circle(r):
    def img(x, y):
        if (0.5 * x)**2 + (1.0 * y)**2 <= (1.0 * r)**2:
            return 'o'
        else:
            return ' '
    return img


def sample(img, loc_x, loc_y, width, height):
    lines = []
    for y in range(loc_y, loc_y + height):
        line = ''
        for x in range(loc_x, loc_x + width):
            line += img(x, y)
        lines += [line]
    return lines


def main(scr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    old_x = None
    old_y = None
    x = 0
    y = 0
    zoom = 100
    redraw = False
    image = composite(origin, grid)
    while True:
        if old_x != x or old_y != y or redraw:
            height, width = scr.getmaxyx()
            rendering = sample(scale(image, 0.01 * zoom), x, y, width, height)
            for locy in range(height):
                try:
                    scr.addstr(
                        locy, 0, rendering[locy], curses.color_pair(3))
                except curses.error as e:
                    pass
            old_x = x
            old_y = y
            redraw = False
            scr.refresh()

        cmd = scr.getch()
        print(cmd)
        if cmd == 'KEY_UP':
            y += -1
        elif cmd == 'KEY_DOWN':
            y += 1
        elif cmd == 'KEY_LEFT':
            x += -2
        elif cmd == 'KEY_RIGHT':
            x += 2
        elif cmd == 'KEY_RESIZE':
            redraw = True
        elif cmd == 'q':
            zoom -= 1
            redraw = True
        elif cmd == 'e':
            zoom += 1
            redraw = True
    urses.curs_set(0)


curses.wrapper(main)
