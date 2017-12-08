# <center>Variance: Documentation</center>

Welcome to the design breakdown of my single page application: Variance. First, there are a few important things to note about the flow
of the application:

## Object Oriented Programming
I have written the python backend in as much of an object-oriented way as possible. Thus, `models.py` is full of classes that can
be used to define poker objects such as a card, board, deck and hole cards. `constants.py` is used to develop each class by use of a
dictionary called `ranks` and another called `suits`. A poker card is made up of one of each of these. There are 13 ranks and 4 suits,
making 52 cards in the standard deck. As such, I have the ability to pull any rank and/or suit of a card in a deck, board or hole cards
as each of those classes is made up of this standard object `Card`. Each class validates itself before instantiating itself, making
checks fairly simple.

## Javascript through Vue.js
In addition, I have decided to try to make a single page application with the help of vue.js and ajax. Vue is a javascript framework
that is very useful for reactively moving data around a page, as can be shown with this application. Ajax is used as a bridge between
the javascript front-end and the server-side python/flask backend.

These design decisions made the heavy lifting algorithm in `evaluator.py` much easier to write. Knowing this basic flow of the application,
we can dive into the backend.

## Algorithm: Background Theory
There are 52 cards in a standard deck. A hand in texas hold 'em poker is made from 5 cards. `nCr` dictates that there are 2,598,960
possible variations of poker hands. So evaluating each hand individually is somewhat difficult algorithmically.

However, upon doing some research and reading into the subject, I came upon a very interesting [application](http://suffe.cool/poker/evaluator.html)
of the same idea that I had. The most interesting part of this analysis to me (aside from the riveting use of C to evaluate hands through
mathematical calculation), was the "discovery" that there are only 7462 distinct hands in poker. This distinction can be made because,
in poker, suits will only matter for flushes. Even moreso, a QJT98 of spades will be evaluated the same as QJT98 of diamonds. So, if you
are able to collapse all of these variations of hands into distinct categorie that evaluate the same way, you can cut down on the
range of hands you must look at in the first place.

## Algorithm: Implementation
### Data Structure
Armed with this knowledge, I set out to find a way to do these evaluations by setting these 7462 hands into a data structure and
searching through it for each hand I am given. I was thinking of using a list or library to store these values into a sorted order,
then use a good search time complexity algorithm to do the search. However, I found a table of these 7462 hands in a text format that
made me think that I could do something a bit more intricate. After some data manipulation, I was able to pull out the file `hands.csv`
that I then imported into `poker.db` as a "hands" table. This allowed me to store a unique id (or score) for each hand as well as the
text "ranks" of each hand and their descriptions. I theorized that I would be able to do a search in the database using `db.execute`
and a few select parameters.

### Function
I then decided to write my evaluator function, found in `evaluator.py`. This function (although very cryptic and could be of better
design admittedly), was my first pass at trying to write an algorithm that would take a list of cards as input and output the score
and description of the best hand that could be made with that list of cards. I decided that the easiest way to do this as a first pass
would be to sort the full values (full_board) as well as find the unique values by typecasting the list into a set. These unique values
are important as the allow me to find *combos* of cards, i.e. cards that have the same rank. After completing these tasks, I first decided
that I would try to find all the flushes and straights in a list of cards that were given. Flushes were fairly easy to write as you
just had to look at the suits of each card that was input and see if you had 5 of them (giving you a flush). Straights were less
"straight-forward". I had to use the sorted full board list of cards and choose 5 sequential cards as many times as possible, then check
each list for a straight. I was going to use the `enumerate` function that python gives us, but it is used to increment per step, rather
than the decrement I needed. Instead of reversing the list, I decided to quickly rewrite the function in `helpers.py` as `enumerator` to
allow for the decrement. The rest of the evaluation uses the unique values to find how many cards in each hand are distinct and draw
conclusions about the hand before doing any deeper analysis.

### Example
For the sake of brevity, I will give an example (however, each component in the `evaluator` function is well commented). If the
function was given a full_board of `[As, Ad, Qh, 9c, Kh, 3c, Kd]`, it would first run turn the ranks of the cards into
values based on the key:value pair in `constants.py`. This allows for us to sort the board easily as well as typecast it as a set to
get distinct values, then typecast it back to a list to sort. As such, as sorted list would look like `[26, 26, 24, 24, 22, 16, 4]`
and the "sorted set" would like `[26, 24, 22, 16, 4]`. This might look confusing, but it is simply a transition from the rank "value"
to the rank "key". Suits are not used too much in the evaluator (except to find a flush, which we don't have). Using this unique
and full value lists, we can see if we have a straight, but we cannot find a pattern of sequential numbers (best is 26, 24, 22; but we
don't have 20, 18 to complete the pattern). As such, we move into the lower part of the evaluator that looks at combos. Using the unique
values list, we see that we have 5 unique cards. As such, it must be a set or two pair. We can figure this out by creating a list
of combo values, which is essentially subtracting the unqiue values list from the full values list. In our case, since we have a pair
of `26's` and a pair of `24's`, subtracting the two lists gives us an output list of `[26, 24]`. If the subtraction gave us two equal
values, we must have a set. This is because given the constraint of 5 unique cards and subtracting out non-combo'd cards, we would be
left with two cards that have equal values. Since the values in our list are not equal, it must be two pair. We then are able to grab
these values and put together a string that can be passed to the database call.

### Database Calling
This is very straightforward once we have a string that is a representation of the ranks of the 5 cards that make the best hand.
From the example, this would be `'A A K K Q'`. We would then search through the database with the constraints of the string and knowing
that the hand is two pair or `'2P'`. This method is very effective and will give you one output every time, since there is only one
unique hand that will match the parameters. This database call will give us the score and hand description that will be returned later on.

### Evaluation
The evaluation comes at the end, where the function checks each boolean for each possible hand type. All of the booleans are set
to false at the beginning and are set as true for each time they encounter a hand type that the input hand can make. The evaluator chooses
the best hand (this is hardcoded, humans know arbitrarily what hands are better) and returns the score and description to the application.

### Scoring
The scoring function is then used to evaluate two scores given to it and output which player wins. If both hero and villian hands go
through the evaluation, we can score them based on who has the lowest score. Lower score, better score.

### Percentage
Percentage is used to define how good of a hand each player has. It is done as a percentage of all possible distinct hands.

## JSON and Javascript
Vue.js and Ajax were very useful to create a reactive environment where I could make buttons that would send data on click to other
vue instances and let them display that data (i.e. clicking on one card and it appearing on the board to the right). The getJSON call
was used to constantly update the UI based on the current state of the board. We can quickly run it through the evaluator and return a
useful string.

## Conclusion
Hopefully, this algorithm isn't too cryptic for deciphering. I tried to make the flow of the app between the front-end and the back-end
as easy to read as possible. I hope you enjoyed some of the design choices I made along the way. I'm looking forward to continuously
developing this app into something much quicker and much more powerful. Thanks for reading!

-dkb