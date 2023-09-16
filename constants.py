
NUMBERS = [1, 2, 3, 4, 5]

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
}