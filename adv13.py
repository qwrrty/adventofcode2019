#! /usr/bin/env python3

import curses
import io
import time

from intcode import Intcode

class Arcade(object):
    
    def __init__(self, filename="adv13_input.txt"):
        self.intcode = Intcode.from_file(filename)

    # The curses ACS_* constants are not available until after curses.initscr()
    # has been called so this has to be delayed
    
    def init_curses():
        Arcade.TILES = [
            ' ',                  # tile_id 0 = empty
            curses.ACS_BLOCK,     # tile_id 1 = wall
            curses.ACS_CKBOARD,   # tile_id 2 = block
            curses.ACS_HLINE  ,   # tile_id 3 = paddle
            curses.ACS_DIAMOND,   # tile_id 4 = ball
        ]
    
    def run(self):
        return curses.wrapper(self._run)
        
    def _run(self, stdscr):
        Arcade.init_curses()
        stdscr.clear()
        while True:
            status = self.intcode.run(break_on_output=3)
            if status is None:
                break
            x, y, tile_id = status
            stdscr.addch(y, x, Arcade.TILES[tile_id])
            stdscr.refresh()
        self.blockcount = 0
        for y in range(0, stdscr.getmaxyx()[0]):
            for x in range(0, stdscr.getmaxyx()[1]):
                if stdscr.inch(y,x) == Arcade.TILES[2]:
                    self.blockcount += 1


def part1():
    game = Arcade()
    game.run()
    print(game.blockcount)
    print(curses.ACS_CKBOARD)


if __name__ == "__main__":
    part1()
