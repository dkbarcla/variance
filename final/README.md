# <center>Welcome to Variance: A Poker Hand Evaluator</center>

## Introduction
This is a single page application for poker hand evaluation. This evaluator focuses on [Texas Hold 'Em](https://en.wikipedia.org/wiki/Texas_hold_%27em).
It is a game in which each player is given face down two cards as their "hole cards". 5 community cards are drawn in three phases:
the **flop**, the **turn** and the **river**. The flop is 3 cards at once, while the turn and river are one card each. All community cards
are drawn face up. A player wins by having the [best hand](https://www.cardplayer.com/rules-of-poker/hand-rankings) of 5 cards. This
evaluator takes a 'heads up' hand as input from the user and outputs the winner of the hand as well as a few statistics.

This application uses the terminology *hero* and *villian* to denote the two players. This is common jargon in poker used to denote
the player who's perspective we are taking (hero) and the player they are against (villian). There can be multiple players in one hand,
but this evaluator currently can only handle two players at once (one of the many things to develop in the future).

## Running the Application
In order to run the application `flask run` can be used to startup the application once inside the the main directory for the app.
All other modules such as `evaluator.py` and `helpers.py` are piped into the application automatically. Once you have opened up the
flask page, all of the functionality is available by clicking on the provided url in the terminal. Ajax, JQuery and Vue.js are all
imported in `index.html` from respective sources.


## Using the Application
All "cards" are buttons on the left side of the page. Click any button to fill a spot on the board to the right. The application
automatically fills each spot based on the spots on the board available. It will first fill the hero's hole cards, then the villian's
hole cards. After that, it will fill in each flop card individually, then the turn and river cards. This functionality cannot be
manipulated (you cannot select a card for the turn before any of the flop cards). However, you can go back and change your choice
by simply clicking on the selection for any of the board or hand cards. For example, if you would like to switch hero's first card
after filling the board, you can click on the hero's card. This will switch it back to a blank card and you can reselect that card again
from the deck to the left.

As you draw cards, the results tab will respond with either the results of the hand, a warning that there are not enough cards, or
that there are duplicate cards. The evaluator requires 5 cards for each player to start evaluation, results will warn that there are
not enough cards to do the evaluation. In addition, if two of the same card is selected, results will display a warning as well.
The results of the hand will show the hand the **hero** has, the hand the **villian** has and the winner of the hand at the point selected.
It will also output the *percentage* of the hand out of the total number of unique and distinct hands possible (7462, if you were interested).

The page can be reset by reloading or clicking on the nav-brand. This will allow an easier use to run through the application. You
can also (arduously) reset the page by clicking on each board card to the right and resetting everything. You will see that clicking
on any button will reset the results tab to whatever the current state of the board will be.

#### Notes
This evaluator can handle any set of cards as long as there are enough to make a poker hand (5 cards). Thus, you have to input the hero
and villian hole cards as well as the flop to see any evaluation. This is because hero cannot access the villian cards and vice versa.

## Final Thoughts
This project is currently in development, there are many more features that I would like to add given the time. However, I hope that
I haveprovided a tight, user-friendly and interactive application.

So, as of now, this is Variance!

-dkb