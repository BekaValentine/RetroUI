import curses


def main(scr):
    line = 0
    while True:
        ch = scr.getch()
        scr.addstr(line, 0, str(ch))
        line += 1


curses.wrapper(main)
