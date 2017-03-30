# Othello AI
An AI I developed for the board game [Othello](en.wikipedia.org/wiki/Reversi)

I used a multi-processed [alpha-beta pruning](en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) routine with a scoring matrix heuristic. This routine is conatined within the `sarkistrat` class in `sarkistrat.py`

*NOTE:* This AI was developed using `Python 3.4`. It is incompatible with `Python 2.7` or older. 

---
###Playing Games

To play a game, simply run `parallel_client.py`. This plays two depth 15 alpha-beta routines for two rounds with a 10 second time limit. 
However, you can play different depth AIs against each other for a different amount of rounds with a different time limit. 
For example, `python parallel_client.py -a 9 -b 1 -g 1 -t 5` would play a depth 9 alpha-beta routine with a depth 3 alpha-beta routine for one round with a 5 second time limit. 

######The full usage:

```
Usage: python parallel_client.py [ARGS...]
-a -AI1 [integer]	: depth of AI1's alpha-beta search (default/max: 15, negative: random AI)
-b -AI2 [integer]	: depth of AI2's alpha-beta search (default/max: 15, negative: random AI)
-t -timelimit [integer]	: time limit per move (default: 10, min: 2)
-g -games [integer]	: number of games to play (default: 2, min: 1)
-h -help		: display this help dialog
```

You can see this help dialog at any time by running `python parallel_client.py -h` or `python parallel_client.py -help`.


