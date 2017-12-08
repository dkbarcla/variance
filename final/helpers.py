from constants import *

# this function used to be useful, keeping around for later logic
def compareCards(card1, card2):
    # compare each cards value, return higher value
    if card1.value > card2.value:
        return(card1)
    if card1.value < card2.value:
        return(card2)
    if card1.value == card2.value:
        return('equal')


# this function used to be useful, keeping around for later logic
def compareHands(hand1, hand2):
    # compare each hands value, return higher value
    if hand1.value > hand2.value:
        return(hand1)
    if hand1.value < hand2.value:
        return(hand2)
    if hand1.value == hand2.value:
        return('equal')


# this function used to be useful, keeping around for later logic
def HandtoHole(hand):
    if hand.combo == "s":
        # its suited
        holecards = []
        for suit in SUITS:
            holecards.append(HoleCards(hand.rank1, hand.rank2, suit, suit))
        print(holecards)

    elif hand.combo == "o":
        #its offsuit
        pass
    else:
        #its a pair
        pass


# function used by evaluator, it inverts the normal "enumerate" function
def enumerator(sequence, start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n -= 1



