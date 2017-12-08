# define components of cards and hands
SUITS = {
    0: 'h',
    1: 'd',
    2: 'c',
    3: 's'
}

RANKS = {
    2: '2',
    4: '3',
    6: '4',
    8: '5',
    10: '6',
    12: '7',
    14: '8',
    16: '9',
    18: 'T',
    20: 'J',
    22: 'Q',
    24: 'K',
    26: 'A'
}

# unused card component, but will be useful down the road
COMBOS = {
    0: 'o',
    1: 's'
}

# define list of fields from index
board_fields = [
    "hero1",
    "hero2",
    "vil1",
    "vil2",
    "flop1",
    "flop2",
    "flop3",
    "turn",
    "river"
    ]

# define errors
CardError_1 = ["Duplicate Card"]
CardError_2 = ["Not Enough Cards"]