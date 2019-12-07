#! /usr/bin/env python3


class Password(object):

    def __init__(self, pw, lo=158126, hi=624574, strict=False):
        self.pw = pw
        self.lo = lo
        self.hi = hi
        self.strict = strict
        
    # Conditions for a valid password:
    #   - It is a six-digit number.
    #   - The value is within the range given in your puzzle input.
    #   - Two adjacent digits are the same (like 22 in 122345).
    #   - Going from left to right, the digits never decrease; they
    #     only ever increase or stay the same (like 111123 or 135679).
    #
    # With the "strict" criterion enabled (for Part 2):
    #   - the two adjacent matching digits are not part of a larger
    #     group of matching digits.

    def valid(self):

        pwstr = str(self.pw)
        
        # Is it a six-digit number?
        if len(pwstr) != 6:
            return False

        # Is it within the valid range?
        if not (self.lo <= self.pw <= self.hi):
            return False

        # Are two adjacent digits the same?
        for i in range(0, 5):
            if pwstr[i] == pwstr[i+1]:
                if not self.strict:
                    break
                # When strict mode is on, then the duplicated digits
                # must not be in part of a longer set in order to qualify
                if (i == 0 or pwstr[i-1] != pwstr[i]) and (i == 4 or pwstr[i+2] != pwstr[i]):
                    break
        else:
            return False

        # Do the digits increase monotonically?
        for i in range(0, 5):
            if pwstr[i+1] < pwstr[i]:
                return False

        return True


def part1(lo=158126, hi=624574):
    return sum(1 for p in range(lo, hi) if Password(p, lo, hi).valid())


def part2(lo=158126, hi=624574):
    return sum(1 for p in range(lo, hi)
               if Password(p, lo, hi, strict=True).valid())


if __name__ == "__main__":
    print(part2())
    
