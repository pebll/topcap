# Benchmarking

This file's purpose is to track benchmark measurements and list improvements. The base benchmark case will always be running a BFS from the start state with depth 3 and 4.

## First Run (25/11)

### Results

- Total time = 3 min
- states/s = 5.7 /s

This is very bad!! Adding a profiler gives us more information:

```
Total time: 179.05s
States processed: 1,027
Throughput: 5.7 states/sec

__eq__ (board comparison)           ██████████████████████████████████████████████ 163.2s (91%)
move operations                     █ 6.3s (3.5%)
bfs loop overhead                   █ 5.9s (3.3%)
...
```

This is very bad, 90% is taken up by Board comparison. Makes sense.
Solution: implement the `__hash__` function that will convert the board to a int representation.

## Hash function implementation (25/11)

### Solution

Encode the position of each piece into 6 bit (36 possible squares, fits in 2^6 = 64)
Pack into a single 64 bit integer (8 * 6 = 48 fits in 64)

Implement `to_hash()` and `from_hash()` to more efficiently store board states

### Results

 ---- DEPTH = 3 ----

- States per second: 531.4 /s
- Time to complete : 1.594 s
- Number of states : 847

-> 100 times BETTER!

   cum(s)    self(s)   calls        %  name
    1.7 s      0.0 s       1     100%  bfs:10
    0.8 s      0.0 s    1162      45%    move:31
    0.6 s      0.1 s    1162      33%      _update_piece_positions:144
    0.5 s      0.1 s   57855      28%        get_tile_content:121
    0.5 s      0.1 s   57855      28%      get_tile_content:121
    0.5 s      0.3 s    3488      29%    to_hash:205

-> now it seems that the `get_tile_content` is very slow..

 ---- DEPTH = 4 ----

- States per second: 367.7 /s
- Time to complete : 11.690 s
- Number of states : 4298

 ---- 100 GAMES - Randi VS Rando ----

- Games per second: 6.8 /s
- States per second: 208.1 /s
- Number of states: 3078
- Time to complete : 14.788 s

   cum(s)    self(s)   calls        %  name
   14.8 s      0.0 s     100     100%  _run_single_game:26
   14.8 s      0.0 s     100     100%    run_game:42
    7.6 s      0.0 s    3178      51%      _game_step:67
    6.7 s      0.8 s  135124      45%        move_is_valid:43
    3.3 s      0.0 s    3178      22%        get_win_reason:96
    3.8 s      0.0 s    3178      26%      _print_game_state:105
    9.7 s      0.1 s    9517      66%        get_all_valid_moves:88
    3.3 s      0.0 s    3178      22%      get_move:11
    9.7 s      0.1 s    9517      66%        get_all_valid_moves:88

-> loosing 150 games/s when running actual games (with randoms) compared to raw DFS

### Conclusion

->  `get_tile_content` is very slow..
->  `get_all_valid_moves` is very slow..
-> Running games speed is 208 states/s
-> DFS speed is 350 states/s

## Let Cursor optimize the hell out of my code (25/11)

### Solution

Ask Cursor.

### Results

FIRST PASS:

Beginning benchmarking RUN 50 GAMES performance
 ---- 50 GAMES - Randi VS Rando ----

- Games per second: 13.5 /s
- States per second: 378.1 /s
- Number of states: 1397
- Time to complete : 3.695 s

SECOND PASS:

 ---- 50 GAMES - Randi VS Rando ----

- Games per second: 22.8 /s
- States per second: 705.7 /s
- Number of states: 1546
- Time to complete : 2.191 s

 ---- DEPTH = 4 ----

- States per second: 975.4 /s
- Time to complete : 7.676 s
- Number of states : 7487

### Conclusion

FIRST PASS:

Great improvement!
-> 210/s to 380/s (almost 2X boost)

SECOND PASS:

Wow amazing!!
-> 380/s to 700/s (almost 2x boost!)

TOTAL:
-> Running games speed is 700 states/s (3.5x boost)
-> DFS speed is 1000 states/s (2.5x boost)
