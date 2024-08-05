import curses


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    while True:
        try:
            for i in range(0, curses.COLORS):
                curses.init_pair(i + 1, i, -1)
            try:
                for i in range(0, 255):
                    stdscr.addstr('x ', curses.A_REVERSE |
                                  curses.color_pair(i))
                    if i == 16:
                        stdscr.addstr('\n')
                    elif i > 16:
                        if (i - 17) % 6 == 5:
                            stdscr.addstr('\n')
            except curses.error:
                # End of screen reached
                pass
            stdscr.getch()
        except KeyboardInterrupt:
            break


curses.wrapper(main)
