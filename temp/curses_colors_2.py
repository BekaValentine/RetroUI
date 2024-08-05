import curses


def main(screen):
    curses.echo()
    while True:
        screen.erase()
        for i in range(0, 16):
            for j in range(0, 16):
                code = str(i * 16 + j)
                screen.addstr(code)
                screen.addstr(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        screen.waddstr(u"\u001b[0m")
        screen.getch()


curses.wrapper(main)
