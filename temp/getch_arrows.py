import getch
import sys

try:
    while True:
        ch = getch.getch()
        sys.stdout.write('\033[6;3H')
        sys.stdout.write(ch)
        sys.stdout.flush()
except KeyboardInterrupt:
    pass
