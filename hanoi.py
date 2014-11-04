import curses
import sys
from os import path


class TowerOfHanoi:
    def __init__(self, stdscr):
        self.disks = 0
        self.pegs = []

        # For the curses-based UI.
        self.stdscr = stdscr
        self.x_base = 5
        self.y_base = 2

    def init_curses_colors(self):
        curses.init_color(1,  894,  102,  110)
        curses.init_color(2,  216,  494,  722)
        curses.init_color(3,  302,  686,  290)
        curses.init_color(4,  596,  306,  639)
        curses.init_color(5, 1000,  498,    0)
        curses.init_color(6, 1000, 1000,  200)
        curses.init_color(7,  651,  337,  157)

        curses.init_pair(1, 1, 0)
        curses.init_pair(2, 2, 0)
        curses.init_pair(3, 3, 0)
        curses.init_pair(4, 4, 0)
        curses.init_pair(5, 5, 0)
        curses.init_pair(6, 6, 0)
        curses.init_pair(7, 7, 0)
        curses.init_pair(8, 8, 0)

    def peg_color(self, disk):
        return curses.color_pair(1 + disk % 8)

    def display_peg(self, letter, peg, y, x):
        s = self.stdscr

        # Draw the peg itself.
        for i in range(self.disks + 1):
            s.addstr(y + i, x + self.disks, "|")

        # Draw the disks on the peg.
        for i in range(len(peg)):
            y_offset = self.disks + y - i
            x_offset = x + 1 + (self.disks - peg[i])

            disk = "#" * (1 + 2 * (peg[i] - 1))
            color = self.peg_color(peg[i])
            s.addstr(y_offset, x_offset, disk, color)

        # Draw the plate.
        s.addstr(y + 1 + self.disks, x, "-" * (1 + self.disks * 2))

        # Draw the letter beneath the peg.
        s.addstr(y + 3 + self.disks, x + self.disks, letter)

    def display_tower(self):
        self.display_peg("A", self.pegs[0], self.y_base, self.x_base)
        self.display_peg("B", self.pegs[1], self.y_base, self.x_base + self.disks * 2 + 3)
        self.display_peg("C", self.pegs[2], self.y_base, self.x_base + 2 * (self.disks * 2 + 3))

    def show_state_and_next_move(self, peg_a, peg_c):
        self.stdscr.clear()
        self.display_tower()

        self.stdscr.addstr(self.y_base + self.disks + 5, self.x_base,
                           "Moving disk %d (= n) from peg %s to peg %s." % (peg_a[1][-1], peg_a[0], peg_c[0]))

        self.stdscr.addstr(self.y_base + self.disks + 7, self.x_base,
                           "Press any key to show the next step...")
        self.stdscr.getch()

    def solve_tower(self, disks):
        # Set up the display colors and hide the cursor.
        self.init_curses_colors()
        curses.curs_set(False)

        # Generate the pegs. Disks are represented by numbers, where the largest number represents the biggest disk.
        # The top of the stack is the end of the peg list.
        self.disks = disks
        self.pegs = []
        self.pegs.append(list(range(disks, 0, -1)))
        self.pegs.append([])
        self.pegs.append([])

        # Start solving the tower.
        self.solve_step(disks, ("A", self.pegs[0]), ("B", self.pegs[1]), ("C", self.pegs[2]))

        # Display the end result, wait for input, and restore the cursor.
        self.stdscr.clear()
        self.display_tower()
        self.stdscr.addstr(self.y_base + self.disks + 5, self.x_base, "Done!")
        self.stdscr.addstr(self.y_base + self.disks + 7, self.x_base, "Press Space to exit.")

        while self.stdscr.getch() != ord(" "):
            pass

        curses.curs_set(True)

    def solve_step(self, n, start, buffer, target):
        if n > 0:
            self.solve_step(n - 1, start, target, buffer)
            self.show_state_and_next_move(start, target)
            target[1].append(start[1].pop())
            self.solve_step(n - 1, buffer, start, target)


def run(stdscr, disks):
    tower = TowerOfHanoi(stdscr)
    tower.solve_tower(disks)


def show_usage_and_exit():
    basepath = path.basename(path.realpath(__file__))
    print("Usage: %s number-of-disks" % basepath)
    sys.exit(1)


def main():
    disks = 0

    if len(sys.argv) != 2:
        show_usage_and_exit()

    try:
        disks = int(sys.argv[1])
    except ValueError:
        show_usage_and_exit()

    if disks < 1:
        show_usage_and_exit()

    curses.wrapper(run, disks)


if __name__ == "__main__":
    main()
