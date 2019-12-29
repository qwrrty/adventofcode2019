#! /usr/bin/env python3

import curses
import io
import time

from intcode import Intcode

class Arcade(object):
    
    def __init__(self, filename="adv13_input.txt"):
        self.intcode = Intcode.from_file(filename)
        self.score = None
        self.ball_coords = None
        self.paddle_coords = None

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

    def play(self):
        return curses.wrapper(self._play)

    def _play(self, stdscr):
        Arcade.init_curses()
        stdscr.clear()
        # Set memory address 0 to 2 to pay for free.
        self.intcode.poke(0, 2)
        # Run the game until it terminates for some reason
        while True:
            self._play_until_blocked(stdscr)
            if self.intcode.is_halted():
                break
            # Move the paddle in the direction of the ball
            joystick = 0
            if self.paddle_coords[0] < self.ball_coords[0]:
                joystick = 1
            elif self.paddle_coords[0] > self.ball_coords[0]:
                joystick = -1

            self.intcode.add_input(joystick)

    def _play_until_blocked(self, stdscr):
        while True:
            output = self.intcode.run(break_on_output=3)
            if output is None:
                break
            x, y, tile_id = output
            if x == -1 and y == 0:
                self.score = tile_id
                continue
            if tile_id == 3:
                self.paddle_coords = (x, y)
            elif tile_id == 4:
                self.ball_coords = (x, y)
            stdscr.addch(y, x, Arcade.TILES[tile_id])
            stdscr.refresh()


def part1():
    game = Arcade()
    game.run()
    print(game.blockcount)


def part2():
    game = Arcade()
    game.play()
    print(game.intcode.state)
    print(game.ball_coords)
    print(game.paddle_coords)
    print(game.score)


if __name__ == "__main__":
    part2()
