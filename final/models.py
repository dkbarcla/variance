import random as rd
from constants import *

class Card:
    def __init__ (self, rank, suit):
        '''Implement a card with a rank and suit.'''
        self.rank = rank
        self.suit = suit
        self.ranking = list(RANKS.keys())[list(RANKS.values()).index(self.rank)]

        # checks if card is a valid card, raises error if not
        if not self.is_valid():
            raise ValueError('Error: card object could not be instantiated; invalid rank or suit')

        self.value = self.ranking

    def __repr__(self):
        '''Returns the cards value.'''
        card_name = self.rank + self.suit
        return(card_name)

    def is_valid(self):
        '''Checks if rank and suit are valid.'''
        if self.rank in RANKS.values():
            if self.suit in SUITS.values():
                return(True)
        return(False)


class HoleCards:
    def __init__(self, rank1, rank2, suit1, suit2):
        ''' Implements two hole cards.'''
        self.cards = []

        # setting ranks and suits
        self.rank1 = rank1
        self.rank2 = rank2
        self.suit1 = suit1
        self.suit2 = suit2

        # creating cards from ranks and suits
        self.card1 = Card(rank1, suit1)
        self.card2 = Card(rank2, suit2)

        self.cards.append(self.card1)
        self.cards.append(self.card2)

        # creating rankings of each card from key values
        self.ranking1 = list(RANKS.keys())[list(RANKS.values()).index(self.rank1)]
        self.ranking2 = list(RANKS.keys())[list(RANKS.values()).index(self.rank2)]

        # checking if valid hole card
        if not self.is_valid():
            raise ValueError('Error: hand object could not be instantiated, invalid rank or combo')

        self.value = self.value()

    def __repr__(self):
        '''Returns the value of the hand.'''
        hole_list = self.cards
        cards_string = ' '.join(str(card) for card in hole_list)
        return(cards_string)

    def is_valid(self):
        '''Checks if both ranks and combo are valid.'''
        if self.rank1 in RANKS.values():
            if self.suit1 in SUITS.values():
                if self.rank2 in RANKS.values():
                    if self.suit2 in SUITS.values():
                        return(True)
        return(False)

    def value(self):
        '''Evaluates both cards and determines a value for the hole cards'''
        if self.ranking1 > self.ranking2:
            if self.suit1 == self.suit2:
            # Adding the combo ranking here as suited cards are higher value than unsuited (check COMBOS list)
                return(self.ranking1 + 1)
            else:
                return(self.ranking1)

        if self.ranking2 > self.ranking1:
            # If the second card is larger than second card, switch their positions (poker convention)
            temp1 = self.rank2
            self.rank2 = self.rank1
            self.rank1 = temp1
            temp2 = self.suit2
            self.suit2 = self.suit1
            self.suit1 = temp2
            if self.suit1 == self.suit2:
                return(self.ranking2 + 1)
            else:
                return(self.ranking2)

        if self.ranking1 == self.ranking2:
            # Add 13 here if a pair so that the value will always be larger than any non-paired hand
            return(self.ranking1 + 41)


# this is unused at the moment, but will be good for downstream use
class Hand:
    def __init__(self, rank1, rank2, combo):
        ''' Implement a hand of two cards.'''
        self.rank1 = rank1
        self.rank2 = rank2
        self.combo = combo
        self.ranking1 = list(RANKS.keys())[list(RANKS.values()).index(self.rank1)]
        self.ranking2 = list(RANKS.keys())[list(RANKS.values()).index(self.rank2)]
        self.rankingC = list(COMBOS.keys())[list(COMBOS.values()).index(self.combo)]

        if not self.is_valid():
            raise ValueError('Error: hand object could not be instantiated, invalid rank or combo')

        self.value = self.value()
        self.is_pair()

    def __repr__(self):
        '''Returns the value of the hand.'''
        hand_name = self.rank1 + self.rank2 + self.combo
        return(hand_name)

    def is_valid(self):
        '''Checks if both ranks and combo are valid.'''
        if self.rank1 in RANKS.values():
            if self.rank2 in RANKS.values():
                if self.combo in COMBOS.values():
                    return(True)
        return(False)

    def is_pair(self):
        '''Checks if cards are a pair.'''
        if self.rank1 == self.rank2:
            self.combo = ''

    def value(self):
        '''Checks each card's value and returns the higher value.'''
        if self.ranking1 > self.ranking2:
            # Adding the combo ranking here as suited cards are higher value than unsuited (check COMBOS list)
            return(self.ranking1 + self.rankingC)
        if self.ranking2 > self.ranking1:
            # If the second card is larger than second card, switch their positions (poker convention)
            temp = self.rank2
            self.rank2 = self.rank1
            self.rank1 = temp
            return(self.ranking2 + self.rankingC)
        if self.ranking1 == self.ranking2:
            # Add 13 here if a pair so that the value will always be larger than any non-paired hand
            return(self.ranking1 + 42)
        # this comparison is shit, hands are equal if suited cards have +1 added


class Deck:
    def __init__(self):
        '''Implement a deck of cards'''
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                ranks = RANKS[rank]
                suits = SUITS[suit]
                new_card = Card(ranks, suits)
                self.deck.append(new_card)

    def __repr__(self):
        '''Returns the cards in the deck'''
        deck_list = self.deck
        deck_string = ''.join(str(card) for card in deck_list)
        return(deck_string)

    def forDisplay(self):
        '''Inverted implementation of a deck of cards'''
        self.deck = []
        for rank in RANKS:
            for suit in SUITS:
                ranks = RANKS[rank]
                suits = SUITS[suit]
                new_card = Card(ranks, suits)
                self.deck.append(new_card)


class Board:
    def __init__(self, passed_board, *args):
        '''Implement a new board'''
        # reads in cards from user into board object
        self.board = []
        for card in range(len(passed_board)):
            self.board.append(passed_board[card])

    def __repr__(self):
        '''Returns the string of the board.'''
        board_list = self.board
        board_string = ' '.join(str(card) for card in board_list)
        return(board_string)


class random:
    def randomCard(self, deck):
        '''Define a random card'''
        new_card = deck[rd.randint(0, len(deck)-1)]
        # required that you remove the card from the deck so as to not get repeats
        deck.remove(new_card)
        return(new_card)

    def randomHoleCards(self, deck):
        '''Define two random holecards'''
        first_card = self.randomCard(deck)
        second_card = self.randomCard(deck)
        rank1 = first_card.rank
        rank2 = second_card.rank
        suit1 = first_card.suit
        suit2 = second_card.suit
        hole_cards = HoleCards(rank1, rank2, suit1, suit2)
        return(hole_cards)

    def randomHand(self, deck):
        '''Define a random hand'''
        # Pick a card from the deck and remove it
        first_card = self.randomCard(deck)

        # Pick a second card from the deck ands remove it
        second_card = self.randomCard(deck)

        # Call ranks for each card
        first_rank = first_card.rank
        second_rank = second_card.rank

        # Check if cards are suited or unsuited
        if first_card.suit == second_card.suit:
            combo = COMBOS[1]
        else:
            combo = COMBOS[0]

        # Return the hand
        return(Hand(first_rank, second_rank, combo))

