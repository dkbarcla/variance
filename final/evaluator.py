from constants import *
from cs50 import SQL
from helpers import enumerator
# TODO: Make database calls its own function in helpers
# TODO: Make joining a string its own function in helpers

# Configure CS50 Library to use SQLite database
# database built using table found at: http://suffe.cool/poker/7462.html
db = SQL("sqlite:///poker.db")

def evaluate(holecard1, holecard2, board):

# set all possible hands to false
    is_highcard = False
    is_pair = False
    is_set = False
    is_twopair = False
    is_fullhouse = False
    is_quads = False
    is_straight = False
    is_flush = False
    is_straightflush = False
    highcard_str = 0

# create the full board (board + hole cards)
    full_board = []
    for card in range(len(board)):
        full_board.append(board[card])
    full_board.append(holecard1)
    full_board.append(holecard2)

    # create a set of the cards to find the unique card values (HIGHEST CARDS FIRST)
    all_values = []
    for card in range(len(full_board)):
        all_values.append(full_board[card].value)
    all_values.sort()
    all_values.reverse()
    unique_values = set(all_values)
    unique_values = list(unique_values)
    unique_values.sort()
    unique_values.reverse()

    # create a list of combo'd cards (combo_values) (HIGHEST CARDS FIRST)
    combo_values = list(all_values) # do this list() to assign a new list at new location
    for i in range(len(unique_values)):
        if unique_values[i] in combo_values:
            combo_values.remove(unique_values[i])

    # create a list of non-combo'd cards (kicker_values) (HIGHEST CARDS FIRST)
    kicker_values = list(unique_values) # do this list() to assign a new list at new location
    for i in range(len(combo_values)):
        if combo_values[i] in kicker_values:
            kicker_values.remove(combo_values[i])

    # check length of the board
    if len(full_board) == 7: #river
        board_len = 7
    if len(full_board) == 6: # turn
        board_len = 6
    elif len(full_board) == 5: # flop
        board_len = 5

    # store inverted values for later
    board_invert = board_len - 5

# checks if a flush
    h_counter = 0
    s_counter = 0
    c_counter = 0
    d_counter = 0
    c_cards = []
    h_cards = []
    d_cards = []
    s_cards = []

    # checks for flush using a counter
    for card in range(len(unique_values)):
        if full_board[card].suit == 's':
            s_cards.append(unique_values[card])
            s_counter += 1
        elif full_board[card].suit == 'c':
            c_cards.append(unique_values[card])
            c_counter += 1
        elif full_board[card].suit == 'd':
            d_cards.append(unique_values[card])
            d_counter += 1
        elif full_board[card].suit == 'h':
            h_cards.append(unique_values[card])
            h_counter += 1

    # if any counter is higher or equal to five, assign its cards to a flush variable, set is_flush to true
    if s_counter >= 5:
        flush_cards = list(s_cards)
        is_flush = True
    elif c_counter >= 5:
        flush_cards = list(c_cards)
        is_flush = True
    elif d_counter >= 5:
        flush_cards = list(d_cards)
        is_flush = True
    elif h_counter >= 5:
        flush_cards = list(h_cards)
        is_flush = True

# checks if a straight
    full_val_strt = list(unique_values)
    for i in range(len(full_val_strt)):
        full_val_strt[i] = full_val_strt[i] / 2
        full_val_strt[i] = int(full_val_strt[i])

    # long, arduous and complex evaluation algorithm parsing the strings based on length and a rewritten inverted enumerate function
    if len(full_val_strt) < 5:
        is_straight = False
    elif len(full_val_strt) == 5:
        if (all(a == b for a, b in enumerator(full_val_strt, full_val_strt[0]))) == True:
            is_straight = True
    elif len(full_val_strt) == 6:
        # prep first string
        first_five = list(full_val_strt)
        del first_five[5]
        if (all(a == b for a, b in enumerator(first_five, first_five[0]))) == True:
            is_straight = True
        # prep second string
        last_five = list(full_val_strt)
        del last_five[0]
        if (all(a == b for a, b in enumerator(last_five, last_five[0]))) == True:
            is_straight = True
    elif len(full_val_strt) == 7:
        # prep first string
        first_five = list(full_val_strt)
        del first_five[5:7]
        if (all(a == b for a, b in enumerator(first_five, first_five[0]))) == True:
            is_straight = True
        # prep middle string
        middle_five = list(full_val_strt)
        del middle_five[6]
        del middle_five[0]
        if (all(a == b for a, b in enumerator(middle_five, middle_five[0]))) == True:
            is_straight = True
        # prep last string
        last_five = list(full_val_strt)
        del last_five[0:2]
        if (all(a == b for a, b in enumerator(last_five, last_five[0]))) == True:
            is_straight = True

    # check if wheel straight (5,4,3,2,A)
    if full_val_strt[0] == 13 and full_val_strt[len(full_val_strt)-1] == 1:
        wheel = []
        full_val_strt.reverse()
        for i in range(4):
            wheel.append(full_val_strt[(3-i)] * 2)
        wheel.append(full_val_strt[-1] * 2)

        if wheel == [8, 6, 4, 2, 26]:
            is_straight = True
            unique_values = wheel

    # if either a straight or flush, make database calls and store
    if is_straight == True or is_flush == True:
        # assign flush cards to highest valued cards
        if is_flush == True:
            card_ranks = []
            for card in range(5):
                card_ranks.append(RANKS[flush_cards[card]])
            cards_string = ' '.join(str(card) for card in card_ranks)
        # else assign highest valued cards
        else:
            card_ranks = []
            for card in range(5):
                card_ranks.append(RANKS[unique_values[card]])
            cards_string = ' '.join(str(card) for card in card_ranks)

        # databased calls depending on flush, straight or straight flush
        if is_straight == False and is_flush == True:
            hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="F")
        elif is_straight == True and is_flush == False:
            hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="S")
        elif is_straight == True and is_flush == True:
            is_straightflush = True
            hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="SF")

        # set hand score and type for later evaluation
        sorf_hand_score = hand_data[0]["hand_score"]
        sorf_type = hand_data[0]["hand_description"]

# checking what hands are possible based on unique cards
    if is_straight == False and is_flush == False:

        # check if all unique cards, has to be a highcard (check works for all board types)
        if len(unique_values) == board_len:
            ranking = 0
            # iterate through all cards to find highcard
            for card in range(len(full_board)):
                if ranking < full_board[card].value:
                    highcard = full_board[card].rank + full_board[card].suit
                    ranking = full_board[card].value

            # iterate through cards again to get kickers for high cards
            card_ranks = []
            for card in range(len(kicker_values)-board_invert):
                card_ranks.append(RANKS[kicker_values[card]])
            cards_string = ' '.join(str(card) for card in card_ranks)

            # database calls for a highcard
            hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="HC")

            # set highcard to true, set hand score and type for later evaluation
            is_highcard = True
            highcard_type = hand_data[0]["hand_description"]
            hand_score = hand_data[0]["hand_score"]

        # checks if all - 1 unique cards, has to be a pair (check works for all board types)
        elif len(unique_values) == (board_len - 1):
            # find dthe pair
            card_ranks = []
            for pair in range(2):
                card_ranks.append(RANKS[combo_values[0]])

            # find the kickers
            for card in range(3):
                card_ranks.append(RANKS[kicker_values[card]])

            # join pair and kickers to a string
            cards_string = ' '.join(str(card) for card in card_ranks)

            # database calls for pairs
            hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="1P")

            # set is pair to true, set hand score and type for late evaluation
            is_pair = True
            pair_type = hand_data[0]["hand_description"]
            hand_score = hand_data[0]["hand_score"]

        # checks if all - 2 unique cards, either a set or two pair (check works for all board types)
        elif len(unique_values) == (board_len - 2):
            card_ranks = []

            # algorithm to find whether a set or two pair based on "unique" cards... found through a set
            if combo_values[0] == combo_values[1]:
                # if a set of the unique cards still returns a paired value, it is a set
                # finding set cards and kickers
                for sets in range(3):
                    card_ranks.append(RANKS[combo_values[0]])
                for card in range(2):
                    card_ranks.append(RANKS[kicker_values[card]])

                # joining into a string
                cards_string = ' '.join(str(card) for card in card_ranks)

                # database calls for a set
                hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="3K")

                # setting values for later evaluation
                is_set = True
                set_type = hand_data[0]["hand_description"]
                hand_score = hand_data[0]["hand_score"]
            else:
                # else it has to be two pair, find the pair and its kickers
                for pair in range(2):
                    card_ranks.append(RANKS[combo_values[0]])
                for pair in range(2):
                    card_ranks.append(RANKS[combo_values[1]])
                card_ranks.append(RANKS[kicker_values[0]])

                # joining into a string
                cards_string = ' '.join(str(card) for card in card_ranks)

                # database calls for two pair
                hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="2P")

                # setting values for later evaluation
                is_twopair = True
                twopair_type = hand_data[0]["hand_description"]
                hand_score = hand_data[0]["hand_score"]


        # checks if all - 3 unique cards, either a full house, quads or two pair (technically 3 pair)
        elif len(unique_values) == (board_len - 3):
            card_ranks = []

            # if the set of combo values is 1, it must be quads
            if len(set(combo_values)) == 1:
                # find the quads and kickers
                for quad in range(4):
                    card_ranks.append(RANKS[combo_values[0]])
                card_ranks.append(RANKS[kicker_values[0]])

                # join into string
                cards_string = ' '.join(str(card) for card in card_ranks)

                # database calls for quads
                hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="4K")

                # setting values for later evaluation
                is_quads = True
                quads_type = hand_data[0]["hand_description"]
                hand_score = hand_data[0]["hand_score"]

            # if the set of combo values is 2, must be a full house
            elif len(set(combo_values)) == 2:
                # find the full house values
                for fullhouse in range(3):
                    card_ranks.append(RANKS[combo_values[1]])
                if combo_values[0] == combo_values[1]:
                    for fullhouse in range(2):
                        card_ranks.append(RANKS[combo_values[2]])
                else:
                    for fullhouse in range(2):
                        card_ranks.append(RANKS[combo_values[0]])

                # join into a string
                cards_string = ' '.join(str(card) for card in card_ranks)

                # database calls for a full house
                hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="FH")

                # setting values for later evaluation
                is_fullhouse = True
                fullhouse_type = hand_data[0]["hand_description"]
                hand_score = hand_data[0]["hand_score"]

            # else if the set of combo values is 3, must be two pair
            elif len(set(combo_values)) == 3:
                # finding two pair values and kickers
                for pair in range(2):
                    card_ranks.append(RANKS[combo_values[0]])
                for pair in range(2):
                    card_ranks.append(RANKS[combo_values[1]])
                if combo_values[2] > kicker_values[0]:
                    card_ranks.append(RANKS[combo_values[2]])
                else:
                    card_ranks.append(RANKS[kicker_values[0]])

                # join into a string
                cards_string = ' '.join(str(card) for card in card_ranks)

                # database calls for a full house
                hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="2P")

                # setting values for later evaluation
                is_twopair = True
                twopair_type = hand_data[0]["hand_description"]
                hand_score = hand_data[0]["hand_score"]


        # checks if all - 4 unique cards, either a full house or quads
        elif len(unique_values) == (board_len - 4):
            card_ranks = []

            # if length of kickers is 1, must be quads
            if len(kicker_values) == 1:
                # find quads and kicker values
                for quads in range(4):
                    card_ranks.append(RANKS[combo_values[1]])
                if combo_values[1] == combo_values[0]:
                    if combo_values[3] > kicker_values[0]:
                        card_ranks.append(RANKS[combo_values[3]])
                    else:
                        card_ranks.append(RANKS[kicker_values[0]])
                elif combo_values[1] == combo_values[3]:
                    if combo_values[0] > kicker_values[0]:
                        card_ranks.append(RANKS[combo_values[0]])
                    else:
                        card_ranks.append(RANKS[kicker_values[0]])

                # join into a string
                cards_string = ' '.join(str(card) for card in card_ranks)

                # database calls for quads
                hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="4K")

                # setting values for later evaluation
                is_quads = True
                quads_type = hand_data[0]["hand_description"]
                hand_score = hand_data[0]["hand_score"]

            # else it has to be a full house
            else:
                # finding values for full house
                if combo_values[0] == combo_values[1]:
                    for s in range(3):
                        card_ranks.append(RANKS[combo_values[0]])
                    if combo_values[2] > combo_values[3]:
                        for p in range(2):
                            card_ranks.append(RANKS[combo_values[2]])
                    else:
                        for p in range(2):
                            card_ranks.append(RANKS[combo_values[3]])

                if combo_values[1] == combo_values[2]:
                    for s in range(3):
                        card_ranks.append(RANKS[combo_values[1]])
                    if combo_values[0] > combo_values[3]:
                        for p in range(2):
                            card_ranks.append(RANKS[combo_values[0]])
                    else:
                        for p in range(2):
                            card_ranks.append(RANKS[combo_values[3]])

                if combo_values[2] == combo_values[3]:
                    for s in range(3):
                        card_ranks.append(RANKS[combo_values[2]])
                    if combo_values[0] > combo_values[1]:
                        for p in range(2):
                            card_ranks.append(RANKS[combo_values[0]])
                    else:
                        for p in range(2):
                            card_ranks.append(RANKS[combo_values[1]])

                # join into a string
                cards_string = ' '.join(str(card) for card in card_ranks)

                # database calls for full house
                hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="FH")

                # setting values for later evaluation
                is_fullhouse = True
                fullhouse_type = hand_data[0]["hand_description"]
                hand_score = hand_data[0]["hand_score"]


        # checks if all - 5 unique cards, has to be quads (with a set)
        elif len(unique_values) == (board_len - 5):
            card_ranks = []

            # find quads values
            for i in range(len(unique_values)):
                for n in range(len(unique_values)):
                    if unique_values[n] in combo_values:
                        combo_values.remove(unique_values[n])
            for i in range(len(combo_values)):
                if combo_values[i] in unique_values:
                    unique_values.remove(combo_values[i])

            for quads in range(4):
                card_ranks.append(RANKS[combo_values[0]])
            card_ranks.append(RANKS[unique_values[0]])

            # join into string
            cards_string = ' '.join(str(card) for card in card_ranks)

            # database calls for full house
            hand_data = db.execute("SELECT * FROM hands WHERE hand = :hand AND hand_type = :hand_type", hand=cards_string, hand_type="4K")

            # setting values for later evaluation
            is_quads = True
            quads_type = hand_data[0]["hand_description"]
            hand_score = hand_data[0]["hand_score"]


# Returning checks based on innate valuation i.e. SF is better than quads, straight is better than highcard, etc.
# returns an integer "hand_score" and a description of the hand
    if is_straightflush == True:
        return(sorf_hand_score, sorf_type)
    elif is_quads == True:
        return(hand_score, quads_type)
    elif is_fullhouse == True:
        return(hand_score, fullhouse_type)
    elif is_flush == True:
        return(sorf_hand_score, sorf_type)
    elif is_straight == True:
        return(sorf_hand_score, sorf_type)
    elif is_set == True:
        return(hand_score, set_type)
    elif is_twopair == True:
        return(hand_score, twopair_type)
    elif is_pair == True:
        return(hand_score, pair_type)
    elif is_highcard == True:
        return(hand_score, highcard_type)
    else:
        return("This hand doesn't evaluate")

# scoring function to evaluate one players hand over another based on the score. A lower score is better
def scoring(player1, score1, hand_desc1, player2, score2, hand_desc2):
    if score1 < score2:
        # score1 is higher
        return(player1, hand_desc1)
    if score2 < score1:
        # score2 is higher
        return(player2, hand_desc2)
    if score1 == score2:
        # they tie
        return(0)

# turning players scores into percentages as a function of the number of viable poker hands.
def percentage(score):
    percent = (score/7462) * 100
    return("%.2f"% percent)
