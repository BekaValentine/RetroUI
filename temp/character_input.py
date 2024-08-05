import curses


def main(scr):
    while True:
        key = scr.getkey()
        try:
            scr.addstr(str(key) + ' ')
        except:
            pass


curses.wrapper(main)
