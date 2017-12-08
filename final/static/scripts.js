// Using Vue.js framework for fast, reactive UI

// creating vue instances for each card (this is repetitive and could be designed better, ran out of time. Will markup one, all
// other are the same, with different cards

// changing Vue.js delimiters to work with Jinja
Vue.options.delimiters = ['[[', ']]'];

// Execute when the DOM is fully loaded
$(document).ready(function() {
    var herocard1 = new Vue({
        // bind to html element
        el: '#herocard1',
        // bind data associated with element
        data: {
            // using two data, message and backend. Backend is used in getJSON later for evaluator. Message is used for user feedback.
            message: '__',
            backend: '__'
        },
        methods: {
            // allows reset of the selected card on click and updates the getJSON request
            reset: function(card) {
                herocard1.message = card;
                herocard1.backend = card;
                update();
            }
        }
    });

    var herocard2 = new Vue({
        el: '#herocard2',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                herocard2.message = card;
                herocard2.backend = card;
                update();
            }
        }
    });

    var vilcard1 = new Vue({
        el: '#vilcard1',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                vilcard1.message = card;
                vilcard1.backend = card;
                update();
            }
        }
    });

    var vilcard2 = new Vue({
        el: '#vilcard2',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                vilcard2.message = card;
                vilcard2.backend = card;
                update();
            }
        }
    });

    var flop1 = new Vue({
        el: '#flop1',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                flop1.message = card;
                flop1.backend = card;
                update();
            }
        }
    });

    var flop2 = new Vue({
        el: '#flop2',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                flop2.message = card;
                flop2.backend = card;
                update();
            }
        }
    });

    var flop3 = new Vue({
        el: '#flop3',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                flop3.message = card;
                flop3.backend = card;
                update();
            }
        }
    });

    var turn = new Vue({
        el: '#turn',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                turn.message = card;
                turn.backend = card;
                update();
            }
        }
    });

    var river = new Vue({
        el: '#river',
        data: {
            message: '__',
            backend: '__'
        },
        methods: {
            reset: function(card) {
                river.message = card;
                river.backend = card;
                update();
            }
        }
    });

    // Creating Vue instance for the deck, used to pass info from user button click to vue elements above
    var deck = new Vue({
        // binding to deck element in html
        el: "#deck",
        methods: {
            // function to assign data based on button clicked
            say: function (card) {
                let display = 0;
                // changing the html button value to unicode
                if (card.charAt(1) == 's')
                    display = card.charAt(0) + ' \u2660';
                else if(card.charAt(1) == 'c')
                    display = card.charAt(0) + ' \u2663';
                else if(card.charAt(1) == 'd')
                    display = card.charAt(0) + ' \u2666';
                else if(card.charAt(1) == 'h')
                    display = card.charAt(0) + ' \u2665';

                // changing next available card to button value, both for backend and UI display
                if(herocard1.message == '__')
                    herocard1.message = display,
                    herocard1.backend = card;
                else if(herocard2.message == '__')
                    herocard2.message = display,
                    herocard2.backend = card;
                else if(vilcard1.message == '__')
                    vilcard1.message = display,
                    vilcard1.backend = card;
                else if(vilcard2.message == '__')
                    vilcard2.message = display,
                    vilcard2.backend = card;
                else if(flop1.message == '__')
                    flop1.message = display,
                    flop1.backend = card;
                else if(flop2.message == '__')
                    flop2.message = display,
                    flop2.backend = card;
                else if(flop3.message == '__')
                    flop3.message = display,
                    flop3.backend = card;
                else if(turn.message == '__')
                    turn.message = display,
                    turn.backend = card;
                else if(river.message == '__')
                    river.message = display,
                    river.backend = card;

                // call update, this is the getJSON call
                update();
            }
        }
    });

    // Vue element used to send results to html jumbotron
    var print = new Vue({
        el: '#print',
        data: {
            hero: '',
            villian: '',
            printing: ''
        }
    });

    function update() {
        // set parameters for update
        let results = {
            hero1: herocard1.backend,
            hero2: herocard2.backend,
            vil1: vilcard1.backend,
            vil2: vilcard2.backend,
            flop1: flop1.backend,
            flop2: flop2.backend,
            flop3: flop3.backend,
            turn: turn.backend,
            river: river.backend
        };

        // getJSON to app.py with parameters
        $.getJSON("/results", results, function(data, textStatus, jqXHR) {
            if (!$.isEmptyObject(data)) {
                // send data to "print" vue element
                print.hero = data[0],
                print.villian = data[1],
                print.printing = data[2];
            }
            else {
                alert('Results could not be calculated!');
            }
        });
    }
});
