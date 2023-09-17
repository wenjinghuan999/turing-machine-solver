
NUMBERS = [1, 2, 3, 4, 5]
QUERIES_PER_ROUND = 3

VALIDATORS = {
    1: [
        lambda t, s, c: t == 1,
        lambda t, s, c: t > 1,
    ],
    2: [
        lambda t, s, c: t < 3,
        lambda t, s, c: t == 3,
        lambda t, s, c: t > 3,
    ],
    3: [
        lambda t, s, c: s < 3,
        lambda t, s, c: s == 3,
        lambda t, s, c: s > 3,
    ],
    4: [
        lambda t, s, c: s < 4,
        lambda t, s, c: s == 4,
        lambda t, s, c: s > 4,
    ],
    5: [
        lambda t, s, c: t % 2 == 0,
        lambda t, s, c: t % 2 != 0,
    ],
    6: [
        lambda t, s, c: s % 2 == 0,
        lambda t, s, c: s % 2 != 0,
    ],
    7: [
        lambda t, s, c: c % 2 == 0,
        lambda t, s, c: c % 2 != 0,
    ],
    8: [
        lambda t, s, c: (t == 1) + (s == 1) + (c == 1) == 0,
        lambda t, s, c: (t == 1) + (s == 1) + (c == 1) == 1,
        lambda t, s, c: (t == 1) + (s == 1) + (c == 1) == 2,
        lambda t, s, c: (t == 1) + (s == 1) + (c == 1) == 3,
    ],
    9: [
        lambda t, s, c: (t == 3) + (s == 3) + (c == 3) == 0,
        lambda t, s, c: (t == 3) + (s == 3) + (c == 3) == 1,
        lambda t, s, c: (t == 3) + (s == 3) + (c == 3) == 2,
        lambda t, s, c: (t == 3) + (s == 3) + (c == 3) == 3,
    ],
    10: [
        lambda t, s, c: (t == 4) + (s == 4) + (c == 4) == 0,
        lambda t, s, c: (t == 4) + (s == 4) + (c == 4) == 1,
        lambda t, s, c: (t == 4) + (s == 4) + (c == 4) == 2,
        lambda t, s, c: (t == 4) + (s == 4) + (c == 4) == 3,
    ],
    11: [
        lambda t, s, c: t < s,
        lambda t, s, c: t == s,
        lambda t, s, c: t > s,
    ],
    12: [
        lambda t, s, c: t < c,
        lambda t, s, c: t == c,
        lambda t, s, c: t > c,
    ],
    13: [
        lambda t, s, c: s < c,
        lambda t, s, c: s == c,
        lambda t, s, c: s > c,
    ],
    14: [
        lambda t, s, c: t < s and t < c,
        lambda t, s, c: s < t and s < c,
        lambda t, s, c: c < t and c < s,
    ],
    15: [
        lambda t, s, c: t > s and t > c,
        lambda t, s, c: s > t and s > c,
        lambda t, s, c: c > t and c > s,
    ],
    16: [
        lambda t, s, c: (t % 2 == 0) + (s % 2 == 0) + (c % 2 == 0) >= 2,
        lambda t, s, c: (t % 2 == 0) + (s % 2 == 0) + (c % 2 == 0) < 2,
    ],
    17: [
        lambda t, s, c: (t % 2 == 0) + (s % 2 == 0) + (c % 2 == 0) == 0,
        lambda t, s, c: (t % 2 == 0) + (s % 2 == 0) + (c % 2 == 0) == 1,
        lambda t, s, c: (t % 2 == 0) + (s % 2 == 0) + (c % 2 == 0) == 2,
        lambda t, s, c: (t % 2 == 0) + (s % 2 == 0) + (c % 2 == 0) == 3,
    ],
    18: [
        lambda t, s, c: (t + s + c) % 2 == 0,
        lambda t, s, c: (t + s + c) % 2 != 0,
    ],
    19: [
        lambda t, s, c: t + s < 6,
        lambda t, s, c: t + s == 6,
        lambda t, s, c: t + s > 6,
    ],
    20: [
        lambda t, s, c: t == s == c,
        lambda t, s, c: t == s != c or t == c != s or s == c != t,
        lambda t, s, c: t != s and t != c and s != c,
    ],
    21: [
        lambda t, s, c: t != s and t != c and s != c,
        lambda t, s, c: t == s or t == c or s == c,
    ],
    22: [
        lambda t, s, c: t < s < c,
        lambda t, s, c: t > s > c,
        lambda t, s, c: not (t < s < c) and not (t > s > c),
    ],
    23: [
        lambda t, s, c: t + s + c < 6,
        lambda t, s, c: t + s + c == 6,
        lambda t, s, c: t + s + c > 6,
    ],
    24: [
        lambda t, s, c: t + 1 == s == c - 1,
        lambda t, s, c: t + 1 == s != c - 1 or t + 1 != s == c - 1,
        lambda t, s, c: t + 1 != s != c - 1,
    ],
    25: [
        lambda t, s, c: t + 1 != s != t - 1 and s + 1 != c != s - 1,
        lambda t, s, c: t + 1 == s != c - 1 or t - 1 == s != c + 1 or t + 1 != s == c - 1 or t - 1 != s == c + 1,
        lambda t, s, c: t + 1 == s == c - 1 or t - 1 == s == c + 1,
    ],
    26: [
        lambda t, s, c: t < 3,
        lambda t, s, c: s < 3,
        lambda t, s, c: c < 3,
    ],
    27: [
        lambda t, s, c: t < 4,
        lambda t, s, c: s < 4,
        lambda t, s, c: c < 4,
    ],
    28: [
        lambda t, s, c: t == 1,
        lambda t, s, c: s == 1,
        lambda t, s, c: c == 1,
    ],
    29: [
        lambda t, s, c: t == 3,
        lambda t, s, c: s == 3,
        lambda t, s, c: c == 3,
    ],
    30: [
        lambda t, s, c: t == 4,
        lambda t, s, c: s == 4,
        lambda t, s, c: c == 4,
    ],
    31: [
        lambda t, s, c: t > 1,
        lambda t, s, c: s > 1,
        lambda t, s, c: c > 1,
    ],
    32: [
        lambda t, s, c: t > 3,
        lambda t, s, c: s > 3,
        lambda t, s, c: c > 3,
    ],
    33: [
        lambda t, s, c: t % 2 == 0,
        lambda t, s, c: s % 2 == 0,
        lambda t, s, c: c % 2 == 0,
        lambda t, s, c: t % 2 != 0,
        lambda t, s, c: s % 2 != 0,
        lambda t, s, c: c % 2 != 0,
    ],
    34: [
        lambda t, s, c: s >= t <= c,
        lambda t, s, c: t >= s <= c,
        lambda t, s, c: t >= c <= s,
    ],
    35: [
        lambda t, s, c: s <= t >= c,
        lambda t, s, c: t <= s >= c,
        lambda t, s, c: t <= c >= s,
    ],
    36: [
        lambda t, s, c: (t + s + c) % 3 == 0,
        lambda t, s, c: (t + s + c) % 4 == 0,
        lambda t, s, c: (t + s + c) % 5 == 0,
    ],
    37: [
        lambda t, s, c: t + s == 4,
        lambda t, s, c: t + c == 4,
        lambda t, s, c: s + c == 4,
    ],
    38: [
        lambda t, s, c: t + s == 6,
        lambda t, s, c: t + c == 6,
        lambda t, s, c: s + c == 6,
    ],
    39: [
        lambda t, s, c: t == 1,
        lambda t, s, c: s == 1,
        lambda t, s, c: c == 1,
        lambda t, s, c: t > 1,
        lambda t, s, c: s > 1,
        lambda t, s, c: c > 1,
    ],
    40: [
        lambda t, s, c: t < 3,
        lambda t, s, c: s < 3,
        lambda t, s, c: c < 3,
        lambda t, s, c: t == 3,
        lambda t, s, c: s == 3,
        lambda t, s, c: c == 3,
        lambda t, s, c: t > 3,
        lambda t, s, c: s > 3,
        lambda t, s, c: c > 3,
    ],
    41: [
        lambda t, s, c: t < 4,
        lambda t, s, c: s < 4,
        lambda t, s, c: c < 4,
        lambda t, s, c: t == 4,
        lambda t, s, c: s == 4,
        lambda t, s, c: c == 4,
        lambda t, s, c: t > 4,
        lambda t, s, c: s > 4,
        lambda t, s, c: c > 4,
    ],
    42: [
        lambda t, s, c: s > t < c,
        lambda t, s, c: t > s < c,
        lambda t, s, c: t > c < s,
        lambda t, s, c: s < t > c,
        lambda t, s, c: t < s > c,
        lambda t, s, c: t < c > s,
    ],
    43: [
        lambda t, s, c: t < s,
        lambda t, s, c: t == s,
        lambda t, s, c: t > s,
        lambda t, s, c: t < c,
        lambda t, s, c: t == c,
        lambda t, s, c: t > c,
    ],
    44: [
        lambda t, s, c: s < t,
        lambda t, s, c: s == t,
        lambda t, s, c: s > t,
        lambda t, s, c: s < c,
        lambda t, s, c: s == c,
        lambda t, s, c: s > c,
    ],
    45: [
        lambda t, s, c: [t, s, c].count(1) == 0,
        lambda t, s, c: [t, s, c].count(1) == 1,
        lambda t, s, c: [t, s, c].count(1) == 2,
        lambda t, s, c: [t, s, c].count(3) == 0,
        lambda t, s, c: [t, s, c].count(3) == 1,
        lambda t, s, c: [t, s, c].count(3) == 2,
    ],
    46: [
        lambda t, s, c: [t, s, c].count(3) == 0,
        lambda t, s, c: [t, s, c].count(3) == 1,
        lambda t, s, c: [t, s, c].count(3) == 2,
        lambda t, s, c: [t, s, c].count(4) == 0,
        lambda t, s, c: [t, s, c].count(4) == 1,
        lambda t, s, c: [t, s, c].count(4) == 2,
    ],
    47: [
        lambda t, s, c: [t, s, c].count(1) == 0,
        lambda t, s, c: [t, s, c].count(1) == 1,
        lambda t, s, c: [t, s, c].count(1) == 2,
        lambda t, s, c: [t, s, c].count(4) == 0,
        lambda t, s, c: [t, s, c].count(4) == 1,
        lambda t, s, c: [t, s, c].count(4) == 2,
    ],
    48: [
        lambda t, s, c: t < s,
        lambda t, s, c: t < c,
        lambda t, s, c: s < c,
        lambda t, s, c: t == s,
        lambda t, s, c: t == c,
        lambda t, s, c: s == c,
        lambda t, s, c: t > s,
        lambda t, s, c: t > c,
        lambda t, s, c: s > c,
    ],
}

from typing import Callable, Container
import itertools
def is_mutually_exclusive(standards: Container[Callable[[int, int, int], bool]]):
    for option in itertools.product(NUMBERS, NUMBERS, NUMBERS):
        rs = [standard(*option) for standard in standards]
        if rs.count(True) > 1:
            return False
    return True

MUTUALLY_EXCLUSIVE_VALIDATORS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
]
assert(all([is_mutually_exclusive(VALIDATORS[validator_id]) for validator_id in MUTUALLY_EXCLUSIVE_VALIDATORS]))