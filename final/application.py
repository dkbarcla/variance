from flask import Flask, render_template, request, jsonify
from evaluator import *
from constants import *
from models import *

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    # pass deck information to index page and render it
    myDeck = Deck()
    length = len(myDeck.deck)
    return render_template("index.html", decks=myDeck.deck, suits = SUITS, ranks = RANKS, length = length)

@app.route("/results")
def results():

    # handle blank GET request fields appropriately
    for check in board_fields:
            if not request.args.get(check):
                return(jsonify(CardError_2))

    # obtain a list of 52 card objects (deck) and 2 players
    myDeck = Deck()
    player1 = "Hero"
    player2 = "Villian"

    # get form data
    form_data = []
    for card in range(len(board_fields)):
        form_data.append(request.args.get(board_fields[card]))

    # delete any card field that has not yet been chosen, gets passed to backend as '__'
    form_data[:] = [card for card in form_data if card != '__']

    # check if card has already been selected from deck. If so, throw error. If not, select card from deck and remove.
    cards = []
    for hand in form_data:
        for card in myDeck.deck:
            if card.rank == hand[0] and card.suit == hand[1]:
                cards.append(card)
                myDeck.deck.remove(card)
                break
            elif card.rank == 'A' and card.suit == 's':
                return(jsonify(CardError_1))

    # check if enough cards to evaluate
    if len(cards) < 7:
        return(jsonify(CardError_2))

    # create hero and villian hole cards
    hero = (cards.pop(0), cards.pop(0))
    villian = (cards.pop(0), cards.pop(0))
    hero = HoleCards(hero[0].rank, hero[1].rank, hero[0].suit, hero[1].suit)
    villian = HoleCards(villian[0].rank, villian[1].rank, villian[0].suit, villian[1].suit)

    # create board of cards
    myBoard = Board(cards)

    # pass board and holecards to evaluator
    hero_eval = evaluate(hero.card1, hero.card2, myBoard.board)
    villian_eval = evaluate(villian.card1, villian.card2, myBoard.board)
    score = scoring(player1, hero_eval[0], hero_eval[1], player2, villian_eval[0], villian_eval[1])
    hero_percent = percentage(hero_eval[0])
    villian_percent = percentage(villian_eval[0])

    # formulate hero and villian score outputs
    hero_score = f"Hero has {hero_eval[1]}, in the top {hero_percent}% of all hands"
    villian_score = f"Villian has {villian_eval[1]}, in the top {villian_percent}% of all hands"

    # check if hands are tied
    if score == 0:
        toprint = "Players tie!"
    else:
        toprint = f"{score[0]} wins with {score[1]}"

    # ready data for passing to front-end
    result = [hero_score, villian_score, toprint]

    # return to front-end
    return(jsonify(result))
